import time
import random
import logging
from pathlib import Path
from typing import Iterator

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pdftotext import PDF
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up constants
BASE_URL = 'www.iconmath.com'
PDF_DIR = Path('output/pdfs')
TXT_DIR = Path('output/texts')
USER_AGENT = UserAgent()
MIN_WAIT_TIME = 2  # Minimum wait time between requests in seconds
MAX_WAIT_TIME = 5

# Set the path to the ChromeDriver
chrome_driver_path = '/opt/homebrew/bin/chromedriver'  # {{ edit_1 }}

def create_directories():
    """Create necessary output directories if they don't exist."""
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    TXT_DIR.mkdir(parents=True, exist_ok=True)
    print("Output directories created/exist.")

def fetch_page(url: str) -> Iterator[str]:
    """Fetch content from a URL using a random user-agent string and wait time."""
    user_agent = USER_AGENT.random
    headers = {
        'User-Agent': user_agent
    }

    print(f"Fetching page with user-agent: {user_agent}")

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for non-2xx status codes

    wait_time = MIN_WAIT_TIME + random.random() * (MAX_WAIT_TIME - MIN_WAIT_TIME)
    print(f"Waiting for {wait_time:.2f} seconds before next request.")
    time.sleep(wait_time)

    return response.iter_lines(decode_unicode=True), extract_links(response.text)

def extract_links(html_content: str) -> Iterator[str]:
    """Extract all links from the HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    return (link.get('href') for link in soup.find_all('a', href=True) if link.get('href').startswith('http'))

def parse_pdf_urls(html_content: Iterator[str]) -> Iterator[str]:
    """Extract PDF URLs from HTML content."""
    # Ensure html_content is a string
    html_content = ''.join(html_content)  # Convert generator to string
    soup = BeautifulSoup(html_content, 'html.parser')
    return (link.get('href') for link in soup.find_all('a') if link.get('href').endswith('.pdf'))

def download_pdf(pdf_url: str, output_dir: Path = PDF_DIR):
    """Download PDF from a URL to the output directory."""
    filename = pdf_url.split('/')[-1]
    filepath = output_dir / filename

    print(f"Downloading PDF: {pdf_url}")

    try:
        response = requests.get(pdf_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {pdf_url}: {e}")
        return

    with open(filepath, 'wb') as file:
        file.write(response.content)

    print(f"PDF saved to: {filepath}")

def transcribe_pdf(pdf_path: Path):
    """Transcribe PDF file at the given path to a text file."""
    if not pdf_path.exists():
        print(f"PDF file {pdf_path} does not exist. Skipping.")
        return

    print(f"Transcribing PDF: {pdf_path}")

    try:
        pdf = PDF(str(pdf_path))
        text = '\n'.join(pdf)

        filename = pdf_path.stem + '.txt'
        filepath = TXT_DIR / filename

        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(text)

        print(f"Text saved to: {filepath}")

    except Exception as e:
        print(f"Error transcribing {pdf_path}: {e}")

def crawl_subpages(url: str, visited: set):
    """Crawl subpages recursively."""
    if url in visited:
        return
    visited.add(url)

    print(f"Crawling subpage: {url}")
    response = requests.get(url)  # Ensure you have the response from the URL
    soup = BeautifulSoup(response.content, 'html.parser')  # Define soup here

    # Fetch page content and links
    page_content, links = fetch_page(url)  # Ensure you have the response from the URL

    # Process PDF URLs from the current page
    pdf_urls = parse_pdf_urls(page_content)  # Use the parse_pdf_urls function
    for pdf_url in pdf_urls:
        download_pdf(pdf_url)

    # Recursively crawl links
    for link in links:
        crawl_subpages(link, visited)

def fetch_page_with_selenium(url: str):
    """Fetch content from a URL using Selenium."""
    options = Options()
    options.headless = True  # Run in headless mode (no GUI)
    service = Service(chrome_driver_path)  # Update with your ChromeDriver path
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(3)  # Wait for JavaScript to load

    html_content = driver.page_source
    driver.quit()

    return html_content

def download_and_transcribe_pdfs():
    """Main function to download and transcribe PDFs from the website."""
    create_directories()

    url = 'https://iconmath.com/lesson/1029/'  # Test with a specific URL
    print(f"Fetching PDFs from {url}")

    # Fetch page content using Selenium
    html_content = fetch_page_with_selenium(url)

    # Process PDF URLs from the current page
    pdf_urls = parse_pdf_urls(html_content)  # Use the parse_pdf_urls function
    for pdf_url in pdf_urls:
        download_pdf(pdf_url)

    # Transcribe PDFs to text files
    for pdf_path in PDF_DIR.glob('*.pdf'):
        transcribe_pdf(pdf_path)

if __name__ == "__main__":
    download_and_transcribe_pdfs()
    print("Script execution complete.")
