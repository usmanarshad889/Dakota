import time
from datetime import datetime
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def is_sorted(data):
    """Check if a list is sorted in either ascending or descending order"""
    return data == sorted(data) or data == sorted(data, reverse=True)

@pytest.fixture(scope="module")
def driver():
    """Fixture for setting up WebDriver"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Dakota Home Tab - Ask Dakota")
@allure.story("Validate data consistency and sorting in Ask Dakota")
def test_ask_dakota_sorting(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 20)

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["username"])
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["password"])
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()

    # Navigate to Dakota Home Page
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Home")

    # Scroll down the element
    scroll_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='title-div'][normalize-space()='Ask Dakota']")))
    driver.execute_script("arguments[0].scrollIntoView();", scroll_element)
    time.sleep(1)

    # Click on View all button
    view_all = wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'View All')])[2]")))
    view_all.click()

    """Extracts and converts date strings to datetime objects"""
    xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/marketplace-comments-relatedto-acc-con-homepage-view-all[1]/article[1]/div[2]/div[1]/div/div[1]/div[2]/div[1]/p[1]'''
    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

    # Check if elements are found
    assert elements, "❌ No date elements found!"

    date_list = []
    for element in elements:
        text = element.text.strip()
        try:
            # Convert full timestamp including AM/PM
            date_obj = datetime.strptime(text, "by Anonymous On %Y/%m/%d %I:%M %p")
            date_list.append(date_obj)
        except ValueError:
            allure.attach(f"Invalid date format: {text}", "❌ Date Parsing Error", allure.attachment_type.TEXT)

    # Ensure the list is sorted by date and time (AM/PM included)
    assert date_list, "❌ No date elements found!"
    assert is_sorted(date_list), "❌ Ask Dakota section is not sorted by date and time!"