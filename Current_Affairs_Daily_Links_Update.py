import os
import pandas as pd
import requests
import logging
from datetime import datetime
from bs4 import BeautifulSoup


print("!! Script Run Start !!")

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
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"current directory : {current_dir}")

file_path = os.path.join(current_dir, 'daily_current_affairs_links.csv')
print(f"File Path : {file_path}")

try:
    existing_data = pd.read_csv(file_path)
except FileNotFoundError:
    existing_data = pd.DataFrame(columns=["Date", "Link", "PDF Download Link"])

# Iterate over the list and extract the date and link
for li_element in all_daily_updates_list:
    try:
        href_url = li_element.find('a')['href']
        date = datetime.strptime(href_url.split('/')[-1], "%d-%m-%Y").strftime("%d %B %Y")

        print(f"Date : {date}, Link : {href_url}")
    except:
        logging.error(f"href_url not present !")

    # Log the date
    logging.info(f"Date: {date}")

    # Find PDF download link
    response = requests.get(href_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        pdf_links = soup.find_all('a', class_='btn pdf')
        pdf_download_link = pdf_links[1].get('href')
        print(pdf_download_link)
    except:
        pdf_download_link = "Not available now!"
        logging.error(f"pdf download link not available for {href_url}!")

    # Log the PDF download link
    logging.info(f"PDF Download Link: {pdf_download_link}")

    # Check if the date already exists in the existing data
    if date not in existing_data['Date'].values:
        data.append({"Date": date, "Link": href_url, "PDF Download Link": pdf_download_link})

# Concatenate the data to the DataFrame
combined_data = pd.concat([pd.DataFrame(data), existing_data])

print(f"File Path : {file_path}")
# Save the combined data to the CSV file
combined_data.to_csv(file_path, index=False)

logging.info("Daily Current Affairs List Successfully Updated!")
print("Daily Current Affairs List Successfully Updated!")
