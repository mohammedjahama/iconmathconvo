from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import csv
import time

# Setup Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless if you don't want a visible browser
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service('/opt/homebrew/bin/chromedriver')  # Use the correct path to your ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the CSV file to write the extracted data
with open('single_lesson_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Lesson Title', 'Lesson URL', 'YouTube Link', 'Worksheet PDF', 'Google Form']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    lesson_url = 'https://iconmath.com/lesson/1031/'
    driver.get(lesson_url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'lesson_all'))
    )

    # Simulate clicking on the lesson items to load the content dynamically
    lesson_title = driver.title.strip()
    lesson_items = driver.find_elements(By.CSS_SELECTOR, 'ul#derivations li a')
    for item in lesson_items:
        item.click()  # Click to load content dynamically
        time.sleep(3)  # Wait a moment for AJAX to load content

        # Re-fetch content area to ensure AJAX-loaded content is captured
        try:
            content_area = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'lesson_all'))
            )
        except Exception as e:
            print(f"Failed to load content for {lesson_title}: {str(e)}")
            continue

        # Extract YouTube video links
        try:
            youtube_link = content_area.find_element(By.XPATH, '//iframe[contains(@src, "youtube.com")]').get_attribute('src')
        except NoSuchElementException:
            youtube_link = None

        # Extract PDF links
        try:
            pdf_link = content_area.find_element(By.XPATH, '//a[contains(@href, ".pdf")]').get_attribute('href')
        except NoSuchElementException:
            pdf_link = None

        # Extract Google Form links
        try:
            google_form_link = content_area.find_element(By.XPATH, '//a[contains(@href, "docs.google.com/forms")]').get_attribute('href')
        except NoSuchElementException:
            google_form_link = None

        # Write to CSV
        writer.writerow({
           ​⬤