import time
import pytest
import allure
from test_utils import skip_broken , pass_broken

from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys, ActionChains
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


@pytest.mark.release_five
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("PDF Generation")
@allure.story("Validate the ability to generate PDFs for 1–100 selected records.")
@pytest.mark.all
@pass_broken
def test_public_plan_minutes_pdf_generation(driver, config):
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

    # Navigate to Public Plan Meetings Minutes Page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Public_Plan_Minutes")


    # Verify Public Plan Minutes Page Loaded
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, "(//th[@data-label='Name'])[1]")))
        assert element.is_displayed(), "Public Plan Minutes list is not displayed"
    except TimeoutException:
        pytest.fail("Public Plan Minutes list not loaded in time")


    # Verify that 100 records are displayed
    records = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='recordShow']")))

    assert "100" in records.text.strip() , "100 records are not displayed"


    # Click on All Checkbox button
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='slds-checkbox_faux'])[1]")))
    button.click()

    # Click on Generate PDF button
    pdf_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Generate PDF']")))
    pdf_button.click()
    time.sleep(2)

    # Wait for the button to disappear
    is_disappeared = wait.until(EC.invisibility_of_element_located((By.XPATH, "//button[normalize-space()='Generate PDF']")))

    # Assertion to confirm the button is no longer visible
    assert is_disappeared, "Error: The 'Generate PDF' button is still visible after clicking."

    print("PDF generation process started successfully.")
    time.sleep(10)

    # Screenshot & Allure attachment
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"PDF Generation", attachment_type=allure.attachment_type.PNG)