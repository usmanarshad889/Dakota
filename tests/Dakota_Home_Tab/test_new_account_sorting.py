import time
from datetime import datetime
import pytest
import allure
from test_utils import skip_broken , pass_broken

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
    yield driver
    driver.quit()

@pytest.mark.release_two
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Dakota Home Tab - New Accounts")
@allure.story("Validate data consistency and sorting in New Accounts")
@pytest.mark.all
@pass_broken
def test_new_accounts_sorting(driver, config):
    driver.get(config["base_url"])
    driver.delete_all_cookies()
    wait = WebDriverWait(driver, 30, poll_frequency=0.5)

    # Login block
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(config["username"])
        wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(config["password"])
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.ID, "Login"))).click()
    except Exception as e:
        driver.quit()
        pytest.skip(f"Skipping test due to login failure: {type(e).__name__}")

    # Confirm login success
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='App Launcher']")))
        print("App Launcher is found")
    except Exception as e:
        driver.quit()
        pytest.skip(f"Skipping test due to missing App Launcher: {type(e).__name__}")

    # Navigate to Dakota Home Page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Home")

    wait = WebDriverWait(driver, 60, poll_frequency=0.5)

    # Scroll down the element
    scroll_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='New Accounts']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'nearest'});",scroll_element)
    time.sleep(1)

    # Click on New F13 Filling
    new_filling = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='New Accounts']")))
    new_filling.click()
    time.sleep(1)

    """Extracts and converts date strings to datetime objects"""
    xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/marketplace-dakota-home-page-main[1]/div[1]/div[5]/div[1]/c-investments-home-page-tabs[1]/lightning-tabset[1]/div[1]/slot[1]/lightning-tab[3]/slot[1]/c-new-object-home-page-list[1]/div[1]/c-custom-datatable[1]/div[2]/div[1]/div[1]/table[1]/tbody[1]/tr/td[6]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-formatted-date-time[1]'''
    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

    # Check if elements are found
    assert elements, "❌ No date elements found!"

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Verification Screenshot", attachment_type=allure.attachment_type.PNG)

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
    assert is_sorted(date_list), "❌ New Accounts section is not sorted by date and time!"
