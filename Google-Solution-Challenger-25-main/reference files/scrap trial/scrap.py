from bs4 import BeautifulSoup

# Path to the local PHP file
php_file_path = "C:/Users/drivi/OneDrive/Desktop/carnatic/list_albums.php"  # Use forward slashes

# Open and read the PHP file content
with open(php_file_path, 'r', encoding='utf-8') as file:
    php_content = file.read()

# Parse the PHP content as if it's HTML
soup = BeautifulSoup(php_content, 'html.parser')

# Find all 'a' tags with 'href' attributes
links = soup.find_all('a', href=True)

# Extract the href values
extracted_links = [link['href'] for link in links]

# Print the extracted links
for link in extracted_links:
    print(link)
