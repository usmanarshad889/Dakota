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

def test_notification_field_change_create_task(driver, config):
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

    # Navigate to installed pakages setup
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Dakota_Setup")
    time.sleep(15)

    try:
        element = wait.until(
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


    # Click on Notify when any field changes
    inactive_button = driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_off'][normalize-space()='Inactive'])[3]")
    if inactive_button.text == "Inactive":
        driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_faux'])[3]").click()
        time.sleep(1)
    else:
        pass

    try:
        # Select Notification Setting for Notify when any field changes
        select_element = driver.find_element(By.XPATH,
                                             "(//select[@name='a7F7z000000ewN4EAI'])[1]")
        select = Select(select_element)
        select.select_by_visible_text("Send Email")
        time.sleep(1)
    except:
        print("Create Task Fields not selected")

    try:
        # Select Notification Recipient for Notify when any field changes
        select_element = driver.find_element(By.XPATH,
                                             "(//select[@name='a7F7z000000ewN4EAI'])[2]")
        select = Select(select_element)
        select.select_by_visible_text("User")
        time.sleep(1)
    except:
        print("Notification Recipient Fields not selected")

    try:
        # Select Notification Assignee User/Group for Notify when any field changes
        select_element = driver.find_element(By.XPATH,
                                             "(//select[@name='a7F7z000000ewN4EAI'])[3]")
        select = Select(select_element)
        select.select_by_visible_text("Aiman Shakil")
        time.sleep(1)
    except:
        print("Notification Assignee User/Group Fields not selected")


    # Select Save Option
    driver.find_element(By.XPATH, "//button[normalize-space()='Save']").click()
    time.sleep(10)
    driver.quit()

