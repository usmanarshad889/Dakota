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

def test_mass_create_link_account_by_crd(driver, config):
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
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Dakota_Search")
    time.sleep(30)

    try:
        ff = driver.find_element(By.XPATH, "//input[@id='input-22114' and @class='slds-input']")
        ff.clear()
        ff.send_keys("Test")
    except:
        print("1")

    try:
        ff = driver.find_element(By.XPATH, "(//input[@class='slds-input' and @type='text'])[3]")
        ff.clear()
        ff.send_keys("Test")
    except:
        print("2")

    try:
        ff = driver.find_element(By.XPATH, "//input[@id='input-22114' and @aria-describedby='help-message-22114']")
        ff.clear()
        ff.send_keys("Test")
    except:
        print("3")
    time.sleep(10)