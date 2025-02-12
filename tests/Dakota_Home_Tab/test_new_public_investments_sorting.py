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
@allure.feature("Dakota Home Tab - New Public Investments")
@allure.story("Validate data consistency and sorting in New Public Investments")
def test_new_investment_sorting(driver, config):
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
    scroll_element = wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[@class='slds-tabs_default__link'])[3]")))
    driver.execute_script("arguments[0].scrollIntoView();", scroll_element)
    time.sleep(1)


    """Extracts and converts date strings to datetime objects"""
    xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/marketplace-dakota-home-page-main[1]/div[1]/div[5]/div[1]/c-investments-home-page-tabs[1]/lightning-tabset[1]/div[1]/slot[1]/lightning-tab[1]/slot[1]/c-new-object-home-page-list[1]/div[1]/c-custom-datatable[1]/div[2]/div[1]/div[1]/table[1]/tbody[1]/tr/td[8]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-formatted-date-time[1]'''
    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

    # Check if elements are found
    assert elements, "❌ No date elements found!"

    date_list = []
    for element in elements:
        text = element.text.strip()
        try:
            # Convert date and time (including AM/PM)
            date_obj = datetime.strptime(text, "%m/%d/%Y, %I:%M %p")
            date_list.append(date_obj)
        except ValueError:
            allure.attach(f"Invalid date format: {text}", "❌ Date Parsing Error", allure.attachment_type.TEXT)

    # Ensure the list is sorted by date and time (AM/PM included)
    assert date_list, "❌ No date elements found!"
    assert is_sorted(date_list), "❌ New Public Investments section is not sorted by date and time!"
