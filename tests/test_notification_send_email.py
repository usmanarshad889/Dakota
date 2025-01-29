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

def test_notification_setting_send_email(driver, config):
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
    driver.get("https://dakotanetworks--fuseupgrad.sandbox.lightning.force.com/lightning/n/Marketplace__Dakota_Setup")
    time.sleep(15)

    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='slds-button__icon'])[5]"))
        )
        element.click()
    except:
        pass
    time.sleep(1)

    # Scroll down by 500 pixels
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(10)

    # Click on Sync Account/Contact Type Field
    inactive_button = driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_off'][normalize-space()='Inactive'])[1]")
    if inactive_button.text == "Inactive":
        driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_faux'])[1]").click()
        time.sleep(1)
    else:
        pass


    # Click on Auto Sync new Accounts and related Contacts
    inactive_button = driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_off'][normalize-space()='Inactive'])[2]")
    if inactive_button.text == "Inactive":
        driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]").click()
        time.sleep(1)
    else:
        pass

    try:
        # Select Notification Setting for Auto Sync new Accounts and related Contacts
        select_element = driver.find_element(By.XPATH,
                                             "(//select[@name='a7F7z000000ewN3EAI'])[1]")
        select = Select(select_element)
        select.select_by_visible_text("Send Email")
        time.sleep(1)
    except:
        print("Create Task Fields not selected")

    try:
        # Select Notification Recipient for Auto Sync new Accounts and related Contacts
        select_element = driver.find_element(By.XPATH,
                                             "(//select[@name='a7F7z000000ewN3EAI'])[2]")
        select = Select(select_element)
        select.select_by_visible_text("User")
        time.sleep(1)
    except:
        print("Notification Recipient Fields not selected")

    try:
        # Select Notification Assignee User/Group for Auto Sync new Accounts and related Contacts
        select_element = driver.find_element(By.XPATH,
                                             "(//select[@name='a7F7z000000ewN3EAI'])[3]")
        select = Select(select_element)
        select.select_by_visible_text("Aiman Shakil")
        time.sleep(1)
    except:
        print("Notification Assignee User/Group Fields not selected")


    # Select Save Option
    driver.find_element(By.XPATH, "//button[normalize-space()='Save']").click()
    time.sleep(8)
    driver.quit()

