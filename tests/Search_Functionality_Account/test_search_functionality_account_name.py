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

def test_search_account_name(driver, config):
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
    time.sleep(3)

    # Navigate to Marketplace Search
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Dakota_Search")
    time.sleep(15)

    # Click on Search Button
    driver.find_element(By.XPATH,
                        "//div[@class='SearchbuttonDiv']//button[@title='Search'][normalize-space()='Search']").click()
    time.sleep(5)

    # Copy the Account Name text
    account_name = driver.find_element(By.XPATH,
                                       "//lightning-primitive-cell-factory[@data-label='Account Name']//div[@class='slds-truncate']")
    account_name_text = account_name.text

    # Search Account name
    driver.find_element(By.XPATH, "//input[@name='searchTerm']").send_keys(account_name_text)
    time.sleep(1)

    # Click on Search Button
    driver.find_element(By.XPATH,
                        "//div[@class='SearchbuttonDiv']//button[@title='Search'][normalize-space()='Search']").click()
    time.sleep(5)

    # Copy the Search Account Name text
    account_name = driver.find_element(By.XPATH,
                                       "//lightning-primitive-cell-factory[@data-label='Account Name']//div[@class='slds-truncate']")
    search_account_name_text = account_name.text

    if account_name_text == search_account_name_text:
        assert True
    else:
        assert False