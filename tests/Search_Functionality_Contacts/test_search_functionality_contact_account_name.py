import time
import pytest
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

# Fixture to load the configuration
@pytest.fixture(scope="module")
def config(request):
    import json
    import os
    env = request.config.getoption("--env")
    config_file_path = os.path.join("config", f"config.{env}.json")
    with open(config_file_path) as file:
        return json.load(file)

def test_search_contact_account_name(driver, config):
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
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Dakota_Search")
    time.sleep(15)

    # Navigate to Contacts Tab
    driver.find_element(By.XPATH, "//li[@title='Contacts']").click()
    time.sleep(7)

    # Click on Search Button
    driver.find_element(By.XPATH,
                        "//div[contains(@class,'filterInnerDiv')]//button[contains(@title,'Search')][normalize-space()='Search']").click()
    time.sleep(5)

    # Copy the Contact-Account Name text
    contact_name = driver.find_element(By.XPATH,
                                       "//body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/article[1]/div[2]/p[1]/div[1]/div[1]/div[1]/lightning-datatable[1]/div[2]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[4]")
    contact_name_text = contact_name.text

    # Search Account name
    driver.find_element(By.XPATH, "//input[@name='accountName']").send_keys(contact_name_text)
    time.sleep(1)

    # Click on Search Button
    driver.find_element(By.XPATH,
                        "//div[contains(@class,'filterInnerDiv')]//button[contains(@title,'Search')][normalize-space()='Search']").click()
    time.sleep(5)

    # Copy the Search Contact Name text
    contact_name = driver.find_element(By.XPATH,
                                       "//body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/article[1]/div[2]/p[1]/div[1]/div[1]/div[1]/lightning-datatable[1]/div[2]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[4]")
    search_contact_name_text = contact_name.text

    if contact_name_text == search_contact_name_text:
        assert True
    else:
        assert False