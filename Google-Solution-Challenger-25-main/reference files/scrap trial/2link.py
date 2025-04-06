import requests
from bs4 import BeautifulSoup

# Function to fetch download links from a given URL
def fetch_download_links(url):
    # Send an HTTP request to the URL
    response = requests.get(url, verify=False)
    
    # If the request is successful, parse the content
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <a> tags with class="download"
        download_links = soup.find_all('a', class_='download')
        
        # Extract and print the download links
        for link in download_links:
            # Extract the URL from the onmousedown attribute
            try:
                download_url = link['onmousedown'].split('"')[7]  # The download URL is typically the 8th quoted part
                print(download_url)
            except IndexError:
                print("Error: Could not extract download URL.")
    else:
        print(f"Failed to fetch page {url}, Status code: {response.status_code}")

# Path to the local PHP file (already obtained links)
php_file_path = r"C:\Users\drivi\OneDrive\Desktop\carnatic\list_albums.php"

# Open and read the PHP file content
with open(php_file_path, 'r', encoding='utf-8') as file:
    php_content = file.read()

# Parse the PHP content as if it's HTML
soup = BeautifulSoup(php_content, 'html.parser')

# Find all 'a' tags with 'href' attributes (previously extracted links)
links = soup.find_all('a', href=True)

# Iterate over the first two links
for i, link in enumerate(links):
    if i >= 2:  # Stop after the second link
        break

    link_url = link['href']
    
    # Skip non-HTTP(S) URLs like javascript:;
    if not link_url.startswith('http'):
        continue  # Skip this iteration if the URL doesn't start with 'http'

    print(f"Fetching download links from: {link_url}")
    fetch_download_links(link_url)
