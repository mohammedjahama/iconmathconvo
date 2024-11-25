from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
import csv
import time

# Setup Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless if you don't want a visible browser
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--enable-javascript")  # Enable JavaScript
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-background-timer-throttling")
chrome_options.add_argument("--disable-backgrounding-occluded-windows")
chrome_options.add_argument("--disable-renderer-backgrounding")

# Update this path to the actual location of your ChromeDriver
chrome_driver_path = '/opt/homebrew/bin/chromedriver'  # {{ edit_1 }}

service = Service(chrome_driver_path)  # {{ edit_2 }}
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.set_page_load_timeout(120)  # Increase timeout to 120 seconds

print("WebDriver initialized")

# Navigate to the login page
driver.get('https://example.com/login')  # Replace with the actual login URL

# Locate and fill in the username and password fields
username_field = driver.find_element(By.NAME, 'username')  # Adjust selector as needed
password_field = driver.find_element(By.NAME, 'password')  # Adjust selector as needed

username_field.send_keys('your_username')  # Replace with your username
password_field.send_keys('your_password')  # Replace with your password

# Submit the login form
login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')  # Adjust selector as needed
login_button.click()

# Wait for the login to complete and the next page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'element_after_login')))  # Adjust as needed

# Open the CSV file to write the extracted data
with open('lessons_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Grade', 'Unit', 'Lesson Title', 'Lesson URL', 'YouTube Link', 'Worksheet PDF', 'Google Form']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    grade = "Grade 3"  # Hardcoded based on your input, adjust accordingly

    driver.get('https://iconmath.com/math/grade-3/')  # Replace with your target URL
    print("Grade 3 page loaded")

    # Fetch units with retry mechanism
    for attempt in range(3):
        try:
            units = driver.find_elements(By.CLASS_NAME, 'chappter')
            print(f"Found {len(units)} units")
            break
        except StaleElementReferenceException:
            print("Failed to fetch unit elements, retrying...")
            if attempt < 2:
                time.sleep(2)
            else:
                print("Failed to fetch unit elements after 3 attempts.")
                driver.quit()
                exit()

    for unit_index in range(len(units)):
        # Refetch units to avoid stale references using index
        units = driver.find_elements(By.CLASS_NAME, 'chappter')
        # Ensure unit_index is within the bounds of the units list
        if unit_index >= len(units):
            print(f"Error: unit_index {unit_index} is out of range for units list of length {len(units)}.")
            break  # Exit the loop if the index is out of range

        unit = units[unit_index]

        for attempt in range(3):
            try:
                unit_title = unit.find_element(By.TAG_NAME, 'span').text.strip()
                print(f"Processing unit: {unit_title}")
                break
            except StaleElementReferenceException:
                print("Failed to fetch unit title, retrying...")
                if attempt < 2:
                    time.sleep(2)
                else:
                    print("Failed to fetch unit title after 3 attempts.")
                    continue

        # Refetch lessons to avoid stale references using index
        for attempt in range(3):
            try:
                lessons = unit.find_elements(By.CLASS_NAME, 'lesson')
                print(f"Found {len(lessons)} lessons in unit: {unit_title}")
                break
            except StaleElementReferenceException:
                print("Failed to fetch lessons, retrying...")
                if attempt < 2:
                    time.sleep(2)
                else:
                    print("Failed to fetch lessons after 3 attempts.")
                    continue

        for lesson_index in range(len(lessons)):
            lesson_title = None
            lesson_url = None

            # Retry loop for handling StaleElementReferenceException
            for attempt in range(3):
                try:
                    lessons = unit.find_elements(By.CLASS_NAME, 'lesson')  # Refetch lessons each time
                    lesson = lessons[lesson_index]  # Get the current lesson by index
                    lesson_title = lesson.text.strip()
                    lesson_url = lesson.get_attribute('href')
                    print(f"Processing lesson: {lesson_title}")
                    break
                except StaleElementReferenceException:
                    print(f"Failed to fetch lesson title, retrying... (Attempt {attempt + 1}/3)")
                    if attempt < 2:
                        time.sleep(2)
                    else:
                        print(f"Failed to fetch lesson title after {attempt + 1} attempts.")
                        continue

            if not lesson_title or not lesson_url:
                print("Skipping lesson due to missing title or URL.")
                continue

            # Click on the worksheet link to load the content
            try:
                worksheet_link = driver.find_element(By.XPATH, '//a[contains(text(), "Worksheet")]')
                worksheet_link.click()  # This will trigger the loading of the worksheet content

                # Wait for the content to load
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'lesson_all')))

                # Now extract the PDF link from the loaded content
                try:
                    pdf_link = driver.find_element(By.XPATH, '//a[contains(@href, ".pdf")]').get_attribute('href')
                    print(f"Worksheet PDF link found: {pdf_link}")  # {{ edit_1 }}
                except NoSuchElementException:
                    print("No PDF link found.")  # Added debug statement
                    pdf_link = None

                # Extract Google Form links
                try:
                    google_form_link = driver.find_element(By.XPATH, '//a[contains(@href, "docs.google.com/forms")]').get_attribute('href')
                    print(f"Google Form link found: {google_form_link}")  # {{ edit_2 }}
                except NoSuchElementException:
                    print("No Google Form link found.")  # Added debug statement
                    google_form_link = None

                # Extract YouTube link
                try:
                    youtube_link = driver.find_element(By.XPATH, '//iframe[contains(@src, "youtube.com")]').get_attribute('src')
                    print(f"YouTube link found: {youtube_link}")  # {{ edit_3 }}
                except NoSuchElementException:
                    print("No YouTube link found.")  # Added debug statement
                    youtube_link = None

            except NoSuchElementException:
                print("Worksheet link not found.")
                continue

            # Write to CSV
            print(f"Writing data for lesson '{lesson_title}' to CSV...")  # {{ edit_4 }}
            writer.writerow({
                'Grade': grade,
                'Unit': unit_title,
                'Lesson Title': lesson_title,
                'Lesson URL': lesson_url,
                'YouTube Link': youtube_link if youtube_link else 'N/A',
                'Worksheet PDF': ', '.join(pdf_links) if pdf_links else 'N/A',  # Join multiple PDF links
                'Google Form': google_form_link if google_form_link else 'N/A'
            })

            print(f"Data for lesson '{lesson_title}' written to CSV.")

            # Navigate back to the main grade page
            try:
                # Increase the timeout duration
                driver.set_page_load_timeout(30)  # Set to 30 seconds

                # Example of using explicit wait before navigating back
                try:
                    # Wait for a specific element to be present before going back
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'some_element_id')))
                    driver.back()
                except TimeoutException:
                    print("Timeout while waiting for the element.")

                time.sleep(2)  # Short pause to ensure the page is fully loaded
            except TimeoutException:
                print("Timeout while trying to navigate back. Refreshing the page instead.")
                driver.get('https://iconmath.com/math/grade-3/')
                time.sleep(2)  # Short pause to ensure the page is fully loaded

            # Refetch units and lessons to avoid stale references
            units = driver.find_elements(By.CLASS_NAME, 'chappter')
            unit = units[unit_index]
            lessons = unit.find_elements(By.CLASS_NAME, 'lesson')

print("Data extraction complete. Check 'lessons_data.csv' for results.")
driver.quit()