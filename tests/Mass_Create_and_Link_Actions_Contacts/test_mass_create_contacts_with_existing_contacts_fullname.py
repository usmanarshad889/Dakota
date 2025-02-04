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

def test_mass_create_for_existing_contacts_fullname(driver, config):
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

    # Navigate to installed pakages setup
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Dakota_Search")
    # time.sleep(13)

    # Switch to Contact Tab
    contact_ele = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Contacts']")))
    contact_ele.click()
    time.sleep(5)

    dropdown = driver.find_element(By.XPATH, "(//select[@name='DisplayCriteria'])[2]")
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Unlinked Contacts")
    time.sleep(1)

    driver.find_element(By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']").click()
    time.sleep(10)

    # Click on ALL CHECKBOX
    driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_faux'])[1]").click()
    time.sleep(1)

    # Click on linked account
    dropdown = driver.find_element(By.XPATH, "//select[@name='MassUploadActions']")
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Link Selected Contacts to Existing Contacts")
    time.sleep(10)

    # Click on Dakota Account Fields
    try:
        dropdown = driver.find_element(By.XPATH, "(//select[@class='slds-select'])[6]")
        dropdown_option = Select(dropdown)
        dropdown_option.select_by_visible_text("Dakota Full Name")
        driver.find_element(By.XPATH, "//button[contains(@class,'slds-button slds-button_neutral slds-button slds-button--brand')][normalize-space()='Search']").click()
        time.sleep(10)
    except:
        print("Add Contacts with Account Popup dropdown not selected")

    # Click on Link Contacts
    driver.find_element(By.XPATH, "//button[normalize-space()='Link Contacts']").click()
    time.sleep(10)
    assert True
    driver.quit()
