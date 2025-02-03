import time
import pytest
from selenium import webdriver
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

# Fixture to load the configuration
@pytest.fixture(scope="module")
def config(request):
    import json
    import os
    env = request.config.getoption("--env")
    config_file_path = os.path.join("config", f"config.{env}.json")
    with open(config_file_path) as file:
        return json.load(file)

def test_create_account_single_record(driver, config):
    # Navigate to login page of fuse app
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

    # Navigate to Market Place Search
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Dakota_Search")
    time.sleep(13)

    # Search by name
    driver.find_element(By.XPATH, "//input[@name='searchTerm']").send_keys("Funcef")
    driver.find_element(By.XPATH, "//button[@title='Search']").click()
    time.sleep(10)

    driver.find_element(By.XPATH, "(//button[@class='slds-button slds-button_icon-border slds-button_icon-x-small'])[1]").click()
    time.sleep(1)

    driver.find_element(By.XPATH, "//span[normalize-space()='Link Account']").click()
    time.sleep(10)

    # driver.find_element(By.XPATH, "//input[@name='SearchBar']").send_keys("Test")
    # driver.find_element(By.XPATH, "//button[@class='slds-button slds-button_brand'][normalize-space()='Search']").click()
    # time.sleep(5)

    # Link account
    all_buttons = driver.find_elements(By.XPATH, "(//button[@title='Link'][normalize-space()='Link'])")
    for button in all_buttons:
        driver.execute_script("arguments[0].scrollIntoView();", button)
        if button.is_enabled():
            button.click()
            time.sleep(1)
            break

    time.sleep(10)

    try:
        driver.find_element(By.XPATH, "//lightning-primitive-icon[@size='small']//*[name()='svg']").click()
        time.sleep(5)
    except:
        pass