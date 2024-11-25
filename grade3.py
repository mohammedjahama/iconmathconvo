from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
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
with open('lessons_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Grade', 'Unit', 'Lesson Title', 'Lesson URL', 'YouTube Link', 'Worksheet PDF', 'Google Form']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    grade = "Grade 3"  # Hardcoded based on your input, adjust accordingly

    driver.get('https://iconmath.com/math/grade-3/')  # Replace with your target URL

    # Fetch units with retry mechanism
    for attempt in range(3):
        try:
            units = driver.find_elements(By.CLASS_NAME, 'chappter')
            break
        except StaleElementReferenceException:
            if attempt < 2:
                time.sleep(2)
            else:
                print("Failed to fetch unit elements after 3 attempts.")
                driver.quit()
                exit()

    for unit_index in range(len(units)):
        # Refetch units to avoid stale references using index
        units = driver.find_elements(By.CLASS_NAME, 'chappter')
        unit = units[unit_index]

        for attempt in range(3):
            try:
                unit_title = unit.find_element(By.TAG_NAME, 'span').text.strip()
                break
            except StaleElementReferenceException:
                if attempt < 2:
                    time.sleep(2)
                else:
                    print("Failed to fetch unit title after 3 attempts.")
                    continue

        # Refetch lessons to avoid stale references using index
        for attempt in range(3):
            try:
                lessons = unit.find_elements(By.CLASS_NAME, 'lesson')
                break
            except StaleElementReferenceException:
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
                    break
                except StaleElementReferenceException:
                    if attempt < 2:
                        time.sleep(2)
                    else:
                        print(f"Failed to fetch lesson title after {attempt + 1} attempts.")
                        continue

            if not lesson_title or not lesson_url:
                continue

            driver.get(lesson_url)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'lesson_all'))
            )

            youtube_link = None
            pdf_link = None
            google_form_link = None

            # Simulate clicking on the lesson items to load the content dynamically
            lesson_items = driver.find_elements(By.CSS_SELECTOR, 'ul#derivations li a')
            for item in lesson_items:
                item.click()  # Click to load content dynamically
                time.sleep(2)  # Wait a moment for AJAX to load content

                # Extract YouTube video links
                try:
                    youtube_link = driver.find_element(By.XPATH, '//iframe[contains(@src, "youtube.com")]').get_attribute('src')
                except NoSuchElementException:
                    youtube_link = None

                # Extract PDF links
                try:
                    pdf_link = driver.find_element(By.XPATH, '//a[contains(@href, ".pdf")]').get_attribute('href')
                except NoSuchElementException:
                    pdf_link = None

                # Extract Google Form links
                try:
                    google_form_link = driver.find_element(By.XPATH, '//a[contains(@href, "docs.google.com/forms")]').get_attribute('href')
                except NoSuchElementException:
                    google_form_link = None

            # Write to CSV
            writer.writerow({
                'Grade': grade,
                'Unit': unit_title,
                'Lesson Title': lesson_title,
                'Lesson URL': lesson_url,
                'YouTube Link': youtube_link if youtube_link else 'N/A',
                'Worksheet PDF': pdf_link if pdf_link else 'N/A',
                'Google Form': google_form_link if google_form_link else 'N/A'
            })

            # Navigate back to the main grade page
            driver.back()
            time.sleep(2)  # Short pause to ensure the page is fully loaded

            # Refetch units and lessons to avoid stale references
            units = driver.find_elements(By.CLASS_NAME, 'chappter')
            unit = units[unit_index]
            lessons = unit.find_elements(By.CLASS_NAME, 'lesson')

print("Data extraction complete. Check 'lessons_data.csv' for results.")
driver.quit()