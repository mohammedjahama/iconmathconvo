import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin, urlparse
import time

class WebCrawler:
    def __init__(self, start_url, max_depth=3):
        self.start_url = start_url
        self.max_depth = max_depth
        self.visited = set()
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def is_dynamic(self, url):
        # Check if the page is likely to be dynamic
        response = requests.get(url)
        static_content = response.text
        self.driver.get(url)
        time.sleep(2)  # Wait for JavaScript to execute
        dynamic_content = self.driver.page_source
        return len(dynamic_content) - len(static_content) > 1000  # Arbitrary threshold

    def crawl_static(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.process_page(url, soup)

    def crawl_dynamic(self, url):
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        self.process_page(url, soup)

    def process_page(self, url, soup):
        print(f"Crawling: {url}")
        # Here you can add code to process the page content as needed
        # For example, you could extract and print all text:
        # print(soup.get_text())

        # Extract links
        links = soup.find_all('a', href=True)
        for link in links:
            full_url = urljoin(url, link['href'])
            if self.should_crawl(full_url):
                yield full_url

    def should_crawl(self, url):
        if url in self.visited:
            return False
        parsed_url = urlparse(url)
        return parsed_url.netloc == urlparse(self.start_url).netloc

    def crawl(self, url, depth=0):
        if depth > self.max_depth or url in self.visited:
            return

        self.visited.add(url)

        if self.is_dynamic(url):
            links = self.crawl_dynamic(url)
        else:
            links = self.crawl_static(url)

        for link in links:
            self.crawl(link, depth + 1)

    def run(self):
        self.crawl(self.start_url)
        self.driver.quit()

if __name__ == "__main__":
    start_url = input("Enter the URL to crawl: ")
    crawler = WebCrawler(start_url)
    crawler.run()