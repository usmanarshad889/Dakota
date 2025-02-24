import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver(config):
    driver = webdriver.Chrome()
    # Perform login steps here
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
    yield driver
    driver.quit()

def test_case_1(driver, config):
    wait = WebDriverWait(driver, 20)

    # Navigate to installed pakages setup
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Dakota_Setup")

    # Click on Authentication svg button
    try:
        # Wait for full page load
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        element = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='slds-button__icon'])[3]"))
        )
        element.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
        pass
    time.sleep(1)

    # Verify the Authentication with correct Credentials
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Username']"))).clear()
    driver.find_element(By.XPATH, "//input[@name='Username']").send_keys("Fuse Upgrade")
    driver.find_element(By.XPATH, "//input[@name='Password']").clear()
    driver.find_element(By.XPATH, "//input[@name='Password']").send_keys("rolus009")
    driver.find_element(By.XPATH, "//input[@name='AuthorizationURL']").clear()
    driver.find_element(By.XPATH, "//input[@name='AuthorizationURL']").send_keys("https://marketplace-dakota-uat.herokuapp.com")

    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@value='Connect']"))).click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
        print("Connect button is not clicked in the first attempt")
        pass

    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[normalize-space()='Connect'])[1]"))).click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
        print("Connect button clicked successfully in first attempt")
        pass

    time.sleep(2)

    toast = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='toastMessage forceActionsText']")))
    print(f"Toast message : {toast.text}")

    # Verify the Toast message
    assert toast.text.lower() == "dakota marketplace account connected successfully.", f"Test failed: {toast.text}"

    # Attach a screenshot of the final state
    allure.attach(driver.get_screenshot_as_png(), name="Final_State_Screenshot", attachment_type=AttachmentType.PNG)


def test_case_2(driver, config):
    # Navigate to login page
    wait = WebDriverWait(driver, 20)

    # Navigate to installed pakages setup
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Dakota_Setup")

    # Click on Authentication svg button
    try:
        # Wait for full page load
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        element = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='slds-button__icon'])[3]"))
        )
        element.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
        pass
    time.sleep(1)

    # Verify the Authentication with correct Credentials
    driver.find_element(By.XPATH, "//input[@name='Username']").clear()
    driver.find_element(By.XPATH, "//input[@name='Username']").send_keys("Fuse Upgrade")
    driver.find_element(By.XPATH, "//input[@name='Password']").clear()
    driver.find_element(By.XPATH, "//input[@name='Password']").send_keys("4444") # correct --> rolus009
    driver.find_element(By.XPATH, "//input[@name='AuthorizationURL']").clear()
    driver.find_element(By.XPATH, "//input[@name='AuthorizationURL']").send_keys("https://marketplace-dakota-uat.herokuapp.com")

    # Try to click on connect button
    try:
        driver.find_element(By.XPATH, "//button[@value='Connect']").click()
        time.sleep(1)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
        print("Connect button is not clicked in the first attempt")
        pass

    try:
        driver.find_element(By.XPATH, "(//button[normalize-space()='Connect'])[1]").click()
        time.sleep(1)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
        print("Connect button clicked successfully in first attempt")
        pass

    time.sleep(2)

    toast = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='toastMessage forceActionsText']")))
    toast_message = toast.text.strip().lower()
    print(f"Toast message: {toast_message}")

    # Verify the Toast message
    assert toast_message != "dakota marketplace account connected successfully.", f"Actual Toast : {toast.text}"

    # Attach a screenshot of the final state
    allure.attach(driver.get_screenshot_as_png(), name="Final_State_Screenshot", attachment_type=AttachmentType.PNG)