import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define Selected Options in dropdown for Marketplace Account Fields (Account Name)
salesforce_account_fields = "Account Name"
sync_option = "Update"
notification_setting = "Create Task"
notification_recipient = "Group"
notification_assignee = "HRG"


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def config(request):
    import json
    import os
    env = request.config.getoption("--env")
    config_file_path = os.path.join("config", f"config.{env}.json")
    with open(config_file_path) as file:
        return json.load(file)


def wait_and_click(driver, by, value, timeout=10):
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value))).click()


def wait_and_select(driver, by, value, text, timeout=10):
    select_element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
    Select(select_element).select_by_visible_text(text)


def test_data_sync(driver, config):
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 10)

    # Perform login
    wait.until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(config["username"])
    wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(config["password"])
    wait_and_click(driver, By.ID, "Login")

    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")

    # Click expandable menu (if available)
    try:
        wait_and_click(driver, By.XPATH, "(//*[name()='svg'][@class='slds-button__icon'])[4]", timeout=20)
    except:
        pass

    # Click Auto Sync Field Updates if inactive
    try:
        inactive_button = driver.find_element(By.XPATH, "//span[@class='slds-checkbox_off']")
        if inactive_button.text == "Inactive":
            wait_and_click(driver, By.XPATH, "//span[@class='slds-checkbox_faux']")
    except:
        pass

    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(10)

    # Select dropdowns
    try:
        wait_and_select(driver, By.XPATH, "//select[contains(@name, 'accountFields')]", salesforce_account_fields)
        wait_and_select(driver, By.XPATH, "//select[contains(@name, 'syncOption')]", sync_option)
        wait_and_select(driver, By.XPATH, "//select[contains(@name, 'notificationSetting')]", notification_setting)
        wait_and_select(driver, By.XPATH, "//select[contains(@name, 'notificationRecipient')]", notification_recipient)
        wait_and_select(driver, By.XPATH, "//select[contains(@name, 'notificationAssignee')]", notification_assignee)
    except:
        print("Dropdown selections failed")

    driver.execute_script("window.scrollBy(0, 1500);")

    # Click Save & OK
    wait_and_click(driver, By.XPATH, "//button[normalize-space()='Save']")
    wait_and_click(driver, By.XPATH, "//button[normalize-space()='OK']")

    driver.quit()
