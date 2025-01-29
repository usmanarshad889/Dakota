import time
import pytest
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# Fixture to load the configuration
@pytest.fixture(scope="module")
def config(request):
    import json
    import os
    env = request.config.getoption("--env")
    config_file_path = os.path.join("config", f"config.{env}.json")
    with open(config_file_path) as file:
        return json.load(file)

def test_search_aum(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 10)

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["username"])

    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["password"])

    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()
    time.sleep(3)

    # Navigate to Marketplace Search
    driver.get("https://dakotanetworks--fuseupgrad.sandbox.lightning.force.com/lightning/n/Marketplace__Dakota_Search")
    time.sleep(15)

    # Select Marketplace Created Date Filter
    date = driver.find_element(By.XPATH, "//select[@name='CRMCreatedDate']")
    dropdown = Select(date)
    dropdown.select_by_visible_text("Last 90 Days")
    time.sleep(2)

    # Select Display Criteria (Unlinked Account)
    criteria_dropdown = driver.find_element(By.XPATH, "(//select[@name='DisplayCriteria'])")
    dropdown_option = Select(criteria_dropdown)
    dropdown_option.select_by_visible_text("Unlinked Accounts")

    # click on search button
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
    button.click()
    time.sleep(10)

    # Click on first Result
    driver.find_element(By.XPATH, "/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[2]/p[1]/div[1]/div[1]/div[1]/lightning-datatable[1]/div[2]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[2]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-primitive-cell-button[1]/lightning-button[1]/button[1]").click()
    time.sleep(10)

    # Copy Dakota Created Date
    account_date = driver.find_element(By.XPATH, "/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[9]/section[1]/div[1]/div[1]/form[1]/div[1]/div[1]/div[1]/marketplace-preview-unlinked-account[1]/div[1]/div[1]/lightning-accordion[1]/div[1]/slot[1]/lightning-accordion-section[1]/div[1]/section[1]/div[2]/slot[1]/table[1]/tr[7]/div[1]/div[1]/div[1]/p[1]/lightning-formatted-text[1]")
    account_date_text = account_date.text.strip()

    # Parse the date string into a datetime object
    account_date = datetime.strptime(account_date_text, "%m/%d/%Y, %I:%M %p")

    # Calculate the date range for the last 90 days
    current_date = datetime.now()
    start_date = current_date - timedelta(days=90)

    # Perform the range check
    is_within_range = start_date <= account_date <= current_date

    # Use assert True with the range check result
    assert is_within_range, f"Date {account_date_text} is not within the last 90 days range."

    print(f"Date {account_date_text} is valid and within the last 90 days.")
