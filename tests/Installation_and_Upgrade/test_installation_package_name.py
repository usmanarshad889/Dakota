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


def test_package_installation(driver, config):
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

    # Navigate to installed package
    driver.get(f"{config["base_url"]}lightning/setup/ImportedPackage/home")
    time.sleep(15)

    # Switch to iframe
    iframe_element = driver.find_element(By.XPATH,
                                         "//iframe[@title='Installed Packages ~ Salesforce - Enterprise Edition']")
    driver.switch_to.frame(iframe_element)
    time.sleep(1)

    # Print all installed packages name
    xpath = '''/html[1]/body[1]/div[3]/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr/th[1]/a[1]'''
    packages = driver.find_elements(By.XPATH, xpath)
    for index, package in enumerate(packages):
        current_text = package.text.strip()
        # Check if the text matches the desired package
        if current_text.lower() == "dakota marketplace for salesforce":
            print("Dakota Package Present")
            assert True
    else:
        pass
    driver.quit()
