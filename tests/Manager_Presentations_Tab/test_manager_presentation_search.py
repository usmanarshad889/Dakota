import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.regression
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Authentication - Correct Credentials")
@allure.story("Validate successful authentication with correct credentials for the Heroku.")
def test_manager_presentation_search(driver, config):
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

    # Navigate to installed pakages setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Manager_Presentations")
    time.sleep(5)

    # Enter in Search button
    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='searchValue' and @placeholder='Search']")))
    search_button.send_keys("Invoice-3033F255-0002")
    time.sleep(5)

    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Search']")))
    btn.click()
    time.sleep(1)

    # Extract the search name text
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//th[@data-label='Manager Presentation Name']")))
    print(f"Searched Manager Presentation Name : {btn.text.strip()}")

    assert btn.text.strip() == "Invoice-3033F255-0002" , "Search Functionality is not working"
    time.sleep(2)
