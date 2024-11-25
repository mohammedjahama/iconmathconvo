from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

try:
    # Open the Google Form URL
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSfNB2P_sZNS5Pmlg8bdqVIDUh68dusNm8Q3WZf0_fSYRNVP8Q/viewform")
    print("Opened Google Form")

    # Wait for the form to load and locate the first input field for the name
    name_input = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@type='text']"))
    )
    print("Located the name input field")

    # Scroll the element into view
    driver.execute_script("arguments[0].scrollIntoView(true);", name_input)
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='text']")))
    print("Scrolled to the name input field")

    # Click the input field to focus on it
    name_input.click()

    # Use the send_keys method to type the name naturally
    name_input.send_keys("Your Name Here")
    print("Entered the name using send_keys")

    # Locate and click the "Next" button
    next_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
    )
    next_button.click()
    print("Clicked the Next button")

    # Wait for the next section of the form to load
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "freebirdFormviewerViewItemsItemItem"))
    )
    print("Form loaded successfully after name submission")

    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("Scrolled to the bottom of the page")

    # Wait for the next "Next" button to be clickable and click it
    next_button_again = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
    )
    next_button_again.click()
    print("Clicked the Next button again")

finally:
    # Close the WebDriver
    driver.quit()
    print("Closed the WebDriver")