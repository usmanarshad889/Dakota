import time
import pytest
import allure
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
)

# Setup logging for better debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def safe_click(driver, element):
    try:
        element.click()
    except (ElementClickInterceptedException, ElementNotInteractableException) as e:
        logging.warning(f"Standard click failed: {e}. Trying JavaScript click...")
        driver.execute_script("arguments[0].click();", element)


def login(driver, wait, username_id, password_id, login_btn_id, username_val, password_val):
    try:
        username = wait.until(EC.element_to_be_clickable((By.ID, username_id)))
        username.clear()
        username.send_keys(username_val)

        password = wait.until(EC.element_to_be_clickable((By.ID, password_id)))
        password.clear()
        password.send_keys(password_val)

        # Optional: Wait for spinners or overlays to disappear
        try:
            wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "slds-spinner")))
        except TimeoutException:
            logging.info("No spinner or took too long to disappear.")

        login_button = wait.until(EC.element_to_be_clickable((By.ID, login_btn_id)))
        driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
        time.sleep(0.5)
        safe_click(driver, login_button)

    except TimeoutException as e:
        logging.error("Timeout while logging in.")
        raise e


@pytest.mark.parametrize("run", range(1, 6))  # Run this test 5 times
@pytest.mark.P1
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Mapping - Account field Mapping")
@allure.story("Validate successful mapping of account fields.")
def test_account_record_auto_sync(driver, config, run):
    wait = WebDriverWait(driver, 30, poll_frequency=0.5)

    # --- Step 1: Login to Salesforce ---
    driver.get(config["uat_login_url"])
    login(
        driver, wait,
        username_id="username",
        password_id="password",
        login_btn_id="Login",
        username_val=config["uat_username"],
        password_val=config["uat_password"]
    )

    # --- Step 2: Navigate to Account Tab ---
    driver.get(f"{config['uat_base_url']}lightning/o/Account/list?filterName=__Recent")
    time.sleep(2)

    # --- Step 3: Login to Fuse App ---
    driver.get(config["base_url"])
    login(
        driver, wait,
        username_id="username",
        password_id="password",
        login_btn_id="Login",
        username_val=config["username"],
        password_val=config["password"]
    )

    # --- Step 4: Navigate to Setup Page ---
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")
    time.sleep(3)
