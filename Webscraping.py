import requests
import re
from bs4 import BeautifulSoup

url = "https://www.example.com"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:

    page_content = response.text
    soup = BeautifulSoup(page_content, 'html.parser')
    souptext = soup.get_text()

    # Remove excessive newlines and spaces
    souptext = re.sub(r'\n+', '\n', souptext)  # Replace multiple newlines with a single newline
    souptext = souptext.strip()  # Remove leading and trailing whitespace

    print(souptext)
else:
    print("Failed to retrieve page")
