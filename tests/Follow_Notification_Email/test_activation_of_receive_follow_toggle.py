import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
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

@pytest.mark.P1
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Notification Settings")
@allure.story("Test the activation of the 'Receive Follow Notification' toggle.")
def test_activation_of_receive_follow_toggle(driver, config):
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

    # Navigate to installed packages setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='slds-button__icon'])[5]")))
    element.click()
    time.sleep(1)

    # Scroll down by 500 pixels
    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(7)

    try:
        # Receive Follow Notification
        inactive_button = driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_off'])[4]")
        if inactive_button.text == "Inactive":
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='slds-checkbox_faux'])[4]")))
            btn.click()
        else:
            print("Button is already active")
    except (NoSuchElementException, TimeoutException) as e:
        print("Sync Account/Contact Type Field is not working")
        print(f"Error: {type(e).__name__}")


    # Select Save Option
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
    save_btn.click()
    time.sleep(2)

    toast_message = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage forceActionsText']")))
    text = toast_message.text
    print(f"Actual Toast message : {text}")

    assert text in ["Mapping saved successfully.", "Status changed successfully!"], f"Unexpected toast message: {text}"
    time.sleep(2)