import time
from datetime import datetime
import pytest
import allure
from test_utils import skip_broken , pass_broken

from allure_commons.types import AttachmentType
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


@pytest.mark.release_four
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Default List Views")
@allure.story('Verify default list views ("All," "Public Investments," "13F Filings") display records accurately.')
@pytest.mark.all
@pass_broken
def test_list_view_display(driver, config):
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

    # Click on Marketplace Search button
    try:
        btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[5]")))
        btn.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
    time.sleep(1)


    # Navigate to Marketplace Investment Page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Investments")


    # Verify Investment Page Loaded
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, "(//td[@data-label='Created Date'])[1]")))
        assert element.is_displayed(), "Investment list is not displayed"
    except TimeoutException:
        pytest.fail("Investment list not loaded in time")


    # Select and Verify Multiple List Views
    try:
       # Define List Views to check
        list_views = ['All', 'Public Investment', '13F Filings']

        for view in list_views:
            # Click on the List View dropdown button
            view_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@name='Investments']")))
            view_btn.click()

            # Select View Option
            view_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//lightning-base-combobox-item[@data-value='{view}']")))
            view_option.click()

            # Confirm table element appears after selecting the view
            element = wait.until(EC.presence_of_element_located((By.XPATH, "(//td[@data-label='Created Date'])[1]")))

            # Take Screenshot & Attach to Allure
            screenshot = driver.get_screenshot_as_png()
            allure.attach(screenshot, name=f"{view} - Screenshot", attachment_type=allure.attachment_type.PNG)

            assert element.is_displayed(), f"List View '{view}' label not visible"
            time.sleep(1)

    except (NoSuchElementException, TimeoutException) as e:
        pytest.fail(f"List view selection failed: {type(e).__name__}")
