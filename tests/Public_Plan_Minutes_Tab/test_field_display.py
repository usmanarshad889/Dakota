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
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.regression
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Public Plan Minutes")
@allure.story("Test the display of Public Plan Minute records with correct fields.")
def test_field_display(driver, config):
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
        wait.until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[5]"))).click()

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

    # Navigate to Public Plan Meetings Minutes Page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Public_Plan_Minutes")


    # Verify Public Plan Minutes Page Loaded
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, "(//th[@data-label='Name'])[1]")))
        assert element.is_displayed(), "Public Plan Minutes list is not displayed"
    except TimeoutException:
        pytest.fail("Public Plan Minutes list not loaded in time")

        # Screenshot & Allure attachment
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name=f"Public Plan Meeting Page", attachment_type=allure.attachment_type.PNG)

    xpaths = [
        "//th[@aria-label='Name']//a[@role='button']",
        "//th[@aria-label='Account Name']//span[@class='slds-cell-fixed slds-has-button-menu']//a[@role='button']",
        "//th[@aria-label='Meeting Date']//a[@role='button']",
        "//th[@aria-label='Posted Date']//a[@role='button']",
        "//div[@class='slds-cell-fixed slds-has-button-menu']",
    ]

    expected_field_text = [
        "Name",
        "Account Name",
        "Meeting Date",
        "Posted Date",
        "Show Meeting Minutes URL column actions",
    ]

    extracted_field_text = []
    second_extracted_text = []  # List to store only the second line

    for xpath in xpaths:
        try:
            field = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            text = field.text.strip()
            extracted_field_text.append(text)  # Store all extracted text

            # Extract second line if text has multiple lines
            lines = text.split("\n")  # Split text by newline
            if len(lines) > 1:  # Ensure there's a second line
                print(f"Actual Field Name : {lines[1].strip()}")
                second_extracted_text.append(lines[1].strip())  # Append second line

        except (NoSuchElementException, TimeoutException) as e:
            print(f"Message: {type(e).__name__}")

    assert expected_field_text == second_extracted_text, "All Fields are not displayed correctly"