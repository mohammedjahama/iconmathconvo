from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

# Setup Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless if you don't want a visible browser
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")

service = Service('/opt/homebrew/bin/chromedriver')  # Update with your ChromeDriver path
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL to scrape
url = 'https://iconmath.com/lesson/1029/'
driver.get(url)

# Wait for the lesson title to be present
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'lesson_title')))
    lesson_title = driver.find_element(By.CLASS_NAME, 'lesson_title').text.strip()
    print(f"Lesson Title: {lesson_title}")
except NoSuchElementException:
    print("Lesson title not found.")
    driver.quit()
    exit()

# Click on the worksheet link to load the content
try:
    # Increase wait time or change wait condition
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Worksheet")]')))
    worksheet_link = driver.find_element(By.XPATH, '//a[contains(text(), "Worksheet")]')
    worksheet_link.click()  # This will trigger the loading of the worksheet content
except TimeoutException:
    print("Element not found within the wait time.")
except NoSuchElementException:
    print("Worksheet link not found.")
    print(driver.page_source)  # Debugging: Print page source

# Wait for the content to load
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'lesson_all')))

    # Print the page source for debugging
    print(driver.page_source)  # Debugging: Check if content is loaded

    # Extract the PDF link from the loaded content
    try:
        pdf_link = driver.find_element(By.XPATH, '//a[contains(@href, ".pdf")]').get_attribute('href')
        print(f"Worksheet PDF link found: {pdf_link}")
    except NoSuchElementException:
        print("No PDF link found.")

    # Extract Google Form links
    try:
        google_form_link = driver.find_element(By.XPATH, '//a[contains(@href, "docs.google.com/forms")]').get_attribute('href')
        print(f"Google Form link found: {google_form_link}")
    except NoSuchElementException:
        print("No Google Form link found.")

    # Extract YouTube link
    try:
        youtube_link = driver.find_element(By.XPATH, '//iframe[contains(@src, "youtube.com")]').get_attribute('src')
        print(f"YouTube link found: {youtube_link}")
    except NoSuchElementException:
        print("No YouTube link found.")

except NoSuchElementException:
    print("Worksheet link not found.")

# Clean up
driver.quit()