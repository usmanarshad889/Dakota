import time
import requests
import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
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

def test_search_functionality_account_fields(driver, config):
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

    # Navigate to installed packages setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")


    # Validate API response separately
    url = '''https://dakotanetworks--fuseupgrad.sandbox.lightning.force.com/aura?r=23&Marketplace.AccountSearchTab.fetchCountryValue=1&Marketplace.AccountSearchTab.getInvestmentPrefFilterFields=1&Marketplace.AccountSearchTab.getUserTimeZoneOffSet=1&Marketplace.AccountSearchTab.getValuesForPickList=4&Marketplace.AccountSearchTab.getValuesForPickListFromDakota=1'''
    api_response = requests.get(url)
    print(api_response.status_code == 200)

    # Click on Search button
    if api_response.status_code == 200:
        button = driver.find_element(By.XPATH, "//button[@title='Search']")
        button.click()
    else:
        print(api_response.status_code)