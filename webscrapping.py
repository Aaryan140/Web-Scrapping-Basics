import requests
from bs4 import BeautifulSoup
import csv
import json
import time

# Function to scrape data from a URL
def scrape_data(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract relevant information
            title = soup.title.string.strip()  # Get the title of the page
            
            # Extract text content
            text_content = soup.get_text(separator='\n')
            
            # Extract image URLs
            img_tags = soup.find_all('img')
            image_urls = [img['src'] for img in img_tags if 'src' in img.attrs]
            
            # Extract links
            link_tags = soup.find_all('a', href=True)
            links = [link['href'] for link in link_tags]
            
            # Return a dictionary containing all extracted data
            return {
                'url': url,
                'title': title,
                'text_content': text_content,
                'image_urls': image_urls,
                'links': links
            }
        else:
            print(f"Failed to fetch URL: {url}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error accessing URL: {url} - {e}")
        return None

# list of URLS from where you need to scrape the data 
urls = [
    "https://products.basf.com/global/en/ci/n-vinyl-2-pyrrolidone.html",
    "https://pubchem.ncbi.nlm.nih.gov/compound/N-Vinyl-2-pyrrolidone",
    "https://www.shokubai.co.jp/en/products/detail/nvp/",
    "https://pubchem.ncbi.nlm.nih.gov/compound/N-Vinyl-2-pyrrolidone",
    "https://www.sciencedirect.com/topics/pharmacology-toxicology-and-pharmaceutical-science/1-vinyl-2-pyrrolidinone",
    "https://adhesives.specialchem.com/product/m-basf-n-vinyl-pyrrolidone-nvp",
    "https://www.welinkschem.com/nvp-n-vinyl-pyrrolidone/",
    "https://pubs.rsc.org/en/content/articlelanding/2019/py/c8py01459k",
    "https://www.science.gov/topicpages/n/n-vinyl+pyrrolidone+nvp",
    "https://shdexiang.en.made-in-china.com/product/tXfQDioPsKVn/China-N-Vinylpyrrolidone-CAS-No-88-12-0-C6h9no.html",
    "https://www.cphi-online.com/nvp-n-vinylpyrrolidone-prod1288298.html",
    "https://www.mdpi.com/2073-4360/11/6/1079"
]

# Container to hold scraped data
scraped_data = []

# Iterate through each URL and scrape data
for url in urls:
    data = scrape_data(url)
    if data:
        scraped_data.append(data)
    time.sleep(1)  # Add a delay of 1 second between requests to avoid being blocked (good practice for more clear error handling)

output_format = input("Enter 'csv' or 'json' to choose the output format: ").strip().lower()

#if user enters CSV as the specified format script stores data in CSV format.
if output_format == 'csv':
    with open('CSVscraped_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['url', 'title', 'text_content', 'image_urls', 'links']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for data in scraped_data:
            writer.writerow(data)
    print("Data has been saved in 'CSVscraped_data.csv'")

#if user enters json as the specified format script stores data in JSON format.
elif output_format == 'json':
    with open('JSONscraped_data.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(scraped_data, jsonfile, indent=4)
    print("Data has been saved in 'JSONscraped_data.json'")
else:
    print("Invalid output format. Please choose either 'csv' or 'json'.")
