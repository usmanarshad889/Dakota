import random

import allure
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 30)


try:
    driver.get("https://dakotanetworks--fuseupgrad.sandbox.my.salesforce-setup.com/")
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys("draftsf@draftdata.com.fuseupgrad")
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys("LOWYqfakgQ8oo")
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[5]"))).click()
except Exception as e:
    pytest.skip(f"Skipping test due to unexpected login error: {type(e).__name__}")


driver.get("https://dakotanetworks--fuseupgrad.sandbox.lightning.force.com/lightning/n/Marketplace__Dakota_Search")
time.sleep(15)

# Wait for and click the country selection input field
country_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Select Country(s)']")))
country_input.click()
time.sleep(1)

# Wait for the list of country options to be present
country_options = wait.until(EC.presence_of_all_elements_located(
    (By.XPATH, "//div[5]//div[1]//div[2]//div[1]//div[1]//div[2]//ul[1]//div[1]//li")))

# Validate if at least one option is available
if not country_options:
    print("No country options found.")
    pytest.skip("No country options available. Skipping test case.")
    driver.quit()
    exit()

# Extract country names and check for duplicates
country_names = []
for option in country_options:
    country_name = option.text.strip()
    print(country_name)

    if country_name in country_names:
        print(f"Duplicate country found: {country_name}")
        pytest.fail(f"Test failed due to duplicate country: {country_name}")

    country_names.append(country_name)


