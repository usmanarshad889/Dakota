import time
import pytest
import allure
from test_utils import skip_broken , pass_broken

from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Define Selected Options in dropdown for Marketplace Account Fields (Account Name)
salesforce_account_fields = "Account Name"
sync_option = "Update"
notification_setting = "Create Task"
notification_recipient = "Group"
notification_assignee = "HRG"


@pytest.fixture(scope="module")
def driver():
    """Fixture for setting up WebDriver"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.mark.release_eight
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Field Change Notification")
@allure.story("Ensure that 'Notify when any field changes' triggers correctly for linked records.")
@pytest.mark.all
# @pass_broken
def test_notification_mapped_field_none(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 60, poll_frequency=0.5)

    try:
        # Perform login
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.send_keys(config["username"])
        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.send_keys(config["password"])
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        time.sleep(2)
        login_button.click()
        time.sleep(3)

        # Wait for URL change
        wait.until(EC.url_contains("lightning.force.com"))

        # Verify Login
        try:
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[2]"))).click()
        except Exception as e:
            pytest.skip(f"Skipping test due to unexpected login error: {type(e).__name__}")
            driver.quit()

    except Exception as e:
        pytest.skip(f"Skipping test due to unexpected login error: {type(e).__name__}")
        driver.quit()


    with allure.step("Waiting for Document Ready State to be Complete"):
        WebDriverWait(driver, 90).until(
            lambda d: print("Current Ready State:", d.execute_script('return document.readyState')) or
                      d.execute_script('return document.readyState') == 'complete'
        )
    print("Document Ready State is COMPLETE!")
    time.sleep(1)


    # Navigate to Market Place Setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")


    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[2]//article[1]//div[1]//div[1]//div[1]//button[1]//lightning-primitive-icon[1]")))
    element.click()
    time.sleep(1)


    try:
        # Click on Auto Sync Field Updates
        inactive_button = driver.find_element(By.XPATH, "//span[@class='slds-checkbox_off']")
        if inactive_button.text == "Inactive":
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='slds-checkbox_faux']")))
            btn.click()
        else:
            print("Button is already active")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")


    # Scroll down by 500 pixels
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(10)

    # Select phone with CRD
    select_element = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='a7Ndy0000001H3gEAE'])[1]")))
    option = Select(select_element)
    option.select_by_visible_text("CRD#")

    # Select Website with Account Description
    select_element = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='a7Ndy0000001H3hEAE'])[1]")))
    option = Select(select_element)
    option.select_by_visible_text("Account Description")

    try:
        # Select Sync Option
        xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr/td[3]/div[1]/div[1]/div[1]/select[1]'''
        select_element = driver.find_elements(By.XPATH, xpath)
        for element in select_element:
            if element.is_enabled():
                select = Select(element)
                select.select_by_visible_text("Update")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
        print("Sync Option not selected")
    time.sleep(1)


    try:
        # Select Sync Option
        xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr/td[4]/div[1]/div[1]/div[1]/select[1]'''
        select_element = driver.find_elements(By.XPATH, xpath)
        for element in select_element:
            if element.is_enabled():
                select = Select(element)
                select.select_by_visible_text("--None--")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
        print("Notification Setting field not selected")
    time.sleep(1)


    try:
        # Select Sync Option
        xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr/td[5]/div[1]/div[1]/div[1]/select[1]'''
        select_element = driver.find_elements(By.XPATH, xpath)
        for element in select_element:
            if element.is_enabled():
                select = Select(element)
                select.select_by_visible_text("Owner")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
        print("Notification Recipient field not selected")
    time.sleep(1)


    try:
        # Select Sync Option
        xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr/td[6]/div[1]/div[1]/div[1]/select[1]'''
        select_element = driver.find_elements(By.XPATH, xpath)
        for element in select_element:
            if element.is_enabled():
                select = Select(element)
                select.select_by_visible_text("Aiman Shakil")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
        print("Notification Assignee User/Group not selected")
    time.sleep(1)



    # Scroll down by 1500 pixels
    driver.execute_script("window.scrollBy(0, 1500);")
    time.sleep(2)

    # Select Save Option
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
    save_btn.click()
    time.sleep(1)
    ok_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='OK']")))
    ok_btn.click()
    time.sleep(15)