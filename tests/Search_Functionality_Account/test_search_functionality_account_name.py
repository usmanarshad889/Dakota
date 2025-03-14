import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
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

@pytest.mark.P1
def test_search_account_name(driver, config):
    wait = WebDriverWait(driver, 20)

    # Navigate to login page
    driver.get(config["base_url"])

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["username"])
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["password"])
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()

    # Navigate to the account search page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    # Select the Account tab and print its text
    tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Accounts']")))
    print(f"Current Tab : {tab.text}")

    # Enter the Account name "Test"
    account_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Account Name']")))
    account_input.send_keys("Test")

    # Wait for the results to load
    time.sleep(8)

    # Click the Search button and print its text
    search_button = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//button[@title='Search']")
    ))
    print(f"Button Text : {search_button.text}")
    search_button.click()

    # Extract all Account names text using a simpler XPath
    account_names = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//lightning-datatable//tbody/tr/td[2]")
    ))

    # Assert that at least one Account is found
    assert len(account_names) > 0, "No Account names found in the search results"

    # Check that all returned Account names contain the text "test"
    for account in account_names:
        account_text = account.text.strip().lower()
        print(f"Contact: {account_text}")
        assert "test" in account_text, f"Account name '{account.text}' does not contain 'test'"