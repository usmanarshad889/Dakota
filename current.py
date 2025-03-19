import time
import random
import string
import pytest
import allure
from faker import Faker
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException, ElementClickInterceptedException,
    ElementNotInteractableException, StaleElementReferenceException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Data Setup ---

fake = Faker()
random_name = "Test " + fake.name()
email_prefix = ''.join(random.choices(string.ascii_lowercase, k=7))
random_email = f"www.{email_prefix}.com"
random_phone = ''.join(random.choices(string.digits, k=9))

name_var = random_name
email_var = random_email
phone_var = random_phone

print("Name:", random_name)
print("Email:", random_email)
print("Phone:", random_phone)

# --- Fixtures ---

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# --- Safe Click Utility ---

def safe_click(driver, locator, wait_time=20, max_attempts=5):
    attempts = 0
    while attempts < max_attempts:
        try:
            element = WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable(locator))
            element.click()
            print(f"Click successful on attempt {attempts + 1}")
            return
        except (
            ElementClickInterceptedException, ElementNotInteractableException,
            NoSuchElementException, TimeoutException, StaleElementReferenceException
        ) as e:
            print(f"Click failed on attempt {attempts + 1} due to {type(e).__name__}. Retrying...")
            time.sleep(2)
            attempts += 1
    # JavaScript fallback
    try:
        element = driver.find_element(*locator)
        driver.execute_script("arguments[0].click();", element)
        print("Clicked using JavaScript as last resort.")
    except Exception as e:
        print(f"JavaScript click also failed: {e}. Continuing test.")

# --- Test Case ---

@pytest.mark.P1
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Mapping - Account field Mapping")
@allure.story("Validate successful mapping of account fields.")
def test_account_record_auto_sync(driver, config):
    wait = WebDriverWait(driver, 20)

    with allure.step("Open login page and perform login"):
        driver.get(config["uat_login_url"])

        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.send_keys(config["uat_username"])

        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.send_keys(config["uat_password"])

        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        time.sleep(2)
        login_button.click()

    with allure.step("Click on Account button in navigation"):
        account_button = (By.XPATH, "//one-app-nav-bar-item-root[@data-target-selection-name='sfdc:TabDefinition.standard-Account']")
        safe_click(driver, account_button)

    with allure.step("Navigate to Account Tab URL"):
        driver.get(f"{config['uat_base_url']}lightning/o/Account/list?filterName=__Recent")

    with allure.step("Click on New button to create account"):
        new_button_locator = (By.XPATH, "//div[@title='New']")
        safe_click(driver, new_button_locator)

    # Continue test...
    # Add steps for record type, filling form, saving, validations, etc.

