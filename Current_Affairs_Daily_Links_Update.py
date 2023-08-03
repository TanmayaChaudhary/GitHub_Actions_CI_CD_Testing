############################################# With Logging ################################################

import pandas as pd
import requests
import logging
from datetime import datetime
from bs4 import BeautifulSoup

print("!! Script Run Started !!")

# Configure logging
logging.basicConfig(filename='web_scraping.log', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# URL of the webpage to scrape
url = "https://www.drishtiias.com/current-affairs-news-analysis-editorials"

# Send a GET request to the webpage
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all daily updates list items
s = soup.find('div', class_='box-hide')
all_daily_updates_list = s.find_all('li')

# Create a list to hold the new data
data = []

# Load the existing Excel file (if any) into a DataFrame
try:
    # existing_data = pd.read_excel('daily_current_affairs_links.xlsx')
    existing_data = pd.read_csv('daily_current_affairs_links.csv')
except FileNotFoundError:
    existing_data = pd.DataFrame(columns=["Date", "Link", "PDF Download Link"])

# Iterate over the list and extract the date and link
for li_element in all_daily_updates_list:
    href_url = li_element.find('a')['href']
    date = datetime.strptime(href_url.split('/')[-1], "%d-%m-%Y").strftime("%d %B %Y")

    # Log the date
    logging.info(f"Date: {date}")

    # Find PDF download link
    response = requests.get(href_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_links = soup.find_all('a', class_='btn pdf')
    pdf_download_link = pdf_links[1].get('href')

    # Log the PDF download link
    logging.info(f"PDF Download Link: {pdf_download_link}")

    print(f"PDF Download Link: {pdf_download_link}")

    # Check if the date already exists in the existing data
    if date not in existing_data['Date'].values:
        data.append({"Date": date, "Link": href_url, "PDF Download Link": pdf_download_link})

# Concatenate the data to the DataFrame
combined_data = pd.concat([pd.DataFrame(data), existing_data])

# Save the combined data to the Excel file
#combined_data.to_excel('daily_current_affairs_links.xlsx', index=False)
combined_data.to_csv('daily_current_affairs_links.csv', index=False)

logging.info("Daily Current Affairs List Successfully Updated!")
