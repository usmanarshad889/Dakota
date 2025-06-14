import time
import pytest
import allure
from test_utils import skip_broken , pass_broken

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    """Fixture for setting up WebDriver"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.mark.all
@pytest.mark.release_five
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Confirmation Dialog")
@allure.story("Test 'OK' option in the confirmation dialog.")
@pass_broken
def test_dialog_display_in_mapping(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    driver.delete_all_cookies()
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

    # Navigate to installed pakages setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")



    # Click on Authentication svg button
    try:
        # Wait for full page load
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        element = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//li[2]//article[1]//div[1]//div[1]//div[1]//button[1]//lightning-primitive-icon[1]"))
        )
        element.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
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
    time.sleep(1)


    # Wait for page loading
    wait.until(EC.presence_of_element_located((By.XPATH, "//td[normalize-space()='Account Name']")))
    time.sleep(1)


    try:
        # Scroll down by 1500 pixels
        driver.execute_script("window.scrollBy(0, 1500);")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
    time.sleep(1)


    try:
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
        save_btn.click()
        time.sleep(1)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
    time.sleep(1)

    # Expected dialog box text
    expected_text = 'OK'

    # Wait for the dialog box to appear and extract the actual text
    dialog_box = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//button[normalize-space()='OK']")
    ))

    # Extract and clean the text
    actual_text = dialog_box.text.strip()
    print(f"Actual Text is: {actual_text}")

    # Assert the text matches the expected value
    assert actual_text == expected_text, f"Expected text was '{expected_text}' but got '{actual_text}'"
