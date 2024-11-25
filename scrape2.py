{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import requests\
from bs4 import BeautifulSoup\
import re\
from urllib.parse import urljoin, urlparse\
import time\
import os\
import random\
\
# Set of visited URLs to avoid crawling the same page multiple times\
visited_urls = set()\
\
# List to store found Google Form URLs\
google_form_urls = []\
\
# Create a directory to save HTML files\
if not os.path.exists("scraped_html"):\
    os.makedirs("scraped_html")\
\
# Function to find Google Form URLs on a page and save the HTML structure\
def find_google_form_urls(url):\
    global visited_urls, google_form_urls\
    \
    # Send a GET request to the website with a User-Agent header\
    headers = \{\
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"\
    \}\
    try:\
        response = requests.get(url, headers=headers, timeout=10)\
        response.raise_for_status()  # Check for request errors\
    except requests.RequestException as e:\
        print(f"Request failed: \{e\}")\
        return\
\
    # Parse the content with BeautifulSoup\
    soup = BeautifulSoup(response.content, 'html.parser')\
    \
    # Scrape and print all the text on the page\
    page_text = soup.get_text(separator=' ', strip=True)\
    print(f"Text from \{url\}:\\n\{page_text\}\\n")\
    \
    # Save the HTML content to a file\
    save_html(url, response.content)\
\
    # Find all hyperlinks in the page\
    links = soup.find_all('a', href=True)\
    \
    # Filter and collect Google Form URLs\
    for link in links:\
        href = link['href']\
        if re.search(r'https://docs.google.com/forms/', href):\
            if href not in google_form_urls:\
                google_form_urls.append(href)\
    \
    # Find and crawl all internal links\
    for link in links:\
        href = link['href']\
        full_url = urljoin(url, href)\
        \
        # Check if the link is within the same domain and hasn't been visited\
        if is_internal_link(full_url, url) and full_url not in visited_urls:\
            visited_urls.add(full_url)\
            time.sleep(random.uniform(1, 3))  # Randomized delay between requests\
            find_google_form_urls(full_url)\
\
# Function to check if a URL is internal to the domain\
def is_internal_link(link, base_url):\
    # Parse the base URL and the link\
    base_domain = urlparse(base_url).netloc\
    link_domain = urlparse(link).netloc\
    \
    # Check if the link domain is the same as the base domain\
    return base_domain == link_domain or link_domain == ''\
\
# Function to save HTML content to a file\
def save_html(url, content):\
    # Create a valid filename from the URL\
    parsed_url = urlparse(url)\
    filename = parsed_url.path.strip("/").replace("/", "_") + ".html"\
    if not filename:\
        filename = "index.html"\
    \
    # Save the HTML file to the scraped_html directory\
    filepath = os.path.join("scraped_html", filename)\
    with open(filepath, "wb") as f:\
        f.write(content)\
\
# Define the starting point for crawling\
start_url = 'https://example.com'  # Replace with your target site\
\
# Start crawling from the start URL\
visited_urls.add(start_url)\
find_google_form_urls(start_url)\
\
# Print the found Google Form URLs\
for url in google_form_urls:\
    print(url)}