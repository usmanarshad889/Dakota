import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
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

def test_additional_settings_toggle(driver, config):
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
    time.sleep(5)


    # Navigate to Market Place Setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")


    element = wait.until(EC.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='slds-button__icon'])[5]")))
    element.click()
    time.sleep(1)

    # Scroll down by 500 pixels
    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(2)

    try:
        # Click on Auto Sync Field Updates
        inactive_button = driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_off'])[1]")
        if inactive_button.text == "Inactive":
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='slds-checkbox_faux'])[1]")))
            btn.click()
        else:
            print("Button is already active")
    except (NoSuchElementException, TimeoutException) as e:
        print("Sync Account/Contact Type Field is not working")
        print(f"Error: {type(e).__name__}")


    try:
        # Click on Auto Sync Field Updates
        inactive_button = driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_off'])[2]")
        if inactive_button.text == "Inactive":
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")))
            btn.click()
        else:
            print("Button is already active")
    except (NoSuchElementException, TimeoutException) as e:
        print("Auto Sync new Accounts and related Contacts is not working")
        print(f"Error: {type(e).__name__}")


    try:
        # Click on Auto Sync Field Updates
        inactive_button = driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_off'])[3]")
        if inactive_button.text == "Inactive":
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='slds-checkbox_faux'])[3]")))
            btn.click()
        else:
            print("Button is already active")
    except (NoSuchElementException, TimeoutException) as e:
        print("Notify when any field changes is not working")
        print(f"Error: {type(e).__name__}")


    try:
        # Click on Auto Sync Field Updates
        inactive_button = driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_off'])[4]")
        if inactive_button.text == "Inactive":
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='slds-checkbox_faux'])[4]")))
            btn.click()
        else:
            print("Button is already active")
    except (NoSuchElementException, TimeoutException) as e:
        print("Receive Follow Notification is not working")
        print(f"Error: {type(e).__name__}")


    # Scroll down by 1500 pixels
    driver.execute_script("window.scrollBy(0, 1500);")
    time.sleep(5)

    # Select Save Option
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
    save_btn.click()
    time.sleep(2)

    toast_message = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage forceActionsText']")))
    text = toast_message.text
    print(f"Actual Toast message : {text}")

    assert text in ["Mapping saved successfully.", "Status changed successfully!"], f"Unexpected toast message: {text}"
    time.sleep(2)