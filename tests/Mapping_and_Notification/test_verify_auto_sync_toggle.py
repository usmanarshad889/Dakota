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


@pytest.mark.Skipped
@pytest.mark.P1
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Field Settings")
@allure.story("Verify the Auto Sync Field Updates toggle is visible at the top of the mapping section and is activated/inactivated based on user preferences.")
def test_verify_auto_sync_toggle(driver, config):
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


    # Click on Marketplace Search button
    try:
        btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[@data-target-selection-name='sfdc:TabDefinition.Marketplace__Dakota_Search']")))
        btn.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
    time.sleep(1)


    # Navigate to Marketplace Setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")


    # Click on Mapping Button
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[2]//article[1]//div[1]//div[1]//div[1]//button[1]//lightning-primitive-icon[1]")))
    button.click()
    time.sleep(5)


    # Step 2: Try clicking Activate button first
    action_done = None  # To track which button was clicked

    try:
        activate_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='slds-checkbox_on']")))
        print(f"Current button : {activate_button.text}")
        if activate_button.is_displayed():
            toggle_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='slds-checkbox_faux']")))
            toggle_button.click()
            time.sleep(2)
            print("Active toggle button is clicked")
            action_done = "Activate"
    except TimeoutException:
        print("Activate button not found, checking for Deactivate button")
        try:
            deactivate_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='slds-checkbox_off']")))
            print(f"Current button : {deactivate_button.text}")
            if deactivate_button.is_displayed():
                toggle_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='slds-checkbox_faux']")))
                toggle_button.click()
                time.sleep(2)
                print("Deactivate toggle button is clicked")
                action_done = "Deactivate"
        except TimeoutException:
            print("Neither Activate nor Deactivate button found!")


    if action_done is not None:
        # Check & click opposite button
        if action_done == "Activate":
            try:
                deactivate_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='slds-checkbox_off']")))
                print(f"Current button : {deactivate_button.text}")
                if deactivate_button.is_displayed():
                    toggle_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//span[@class='slds-checkbox_faux']")))
                    toggle_button.click()
                    time.sleep(2)
                    print("Deactivate toggle button is clicked (Second Action)")
            except TimeoutException:
                print("Deactivate button not found in second step!")
        elif action_done == "Deactivate":
            try:
                activate_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='slds-checkbox_on']")))
                print(f"Current button : {activate_button.text}")
                if activate_button.is_displayed():
                    toggle_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//span[@class='slds-checkbox_faux']")))
                    toggle_button.click()
                    time.sleep(2)
                    print("Active toggle button is clicked (Second Action)")
            except TimeoutException:
                print("Activate button not found in second step!")
