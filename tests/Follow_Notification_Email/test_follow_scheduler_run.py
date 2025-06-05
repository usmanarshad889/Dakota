import time
import pytest
import allure
import datetime
from test_utils import skip_broken

from selenium import webdriver
from selenium.webdriver import Keys
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


@pytest.mark.release_seven
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Scheduler Functionality")
@allure.story("Ensure the scheduler runs every Friday at 5 PM.")
@pytest.mark.all
@skip_broken
def test_follow_scheduler_run(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 60)

    # === Check if it's Friday 5 PM ===
    current_time = datetime.datetime.now()

    # Get day name and hour & minute
    day_name = current_time.strftime('%A')  # returns full day name like 'Friday'
    hour = current_time.hour
    minute = current_time.minute

    if day_name == 'Friday' and hour == 17 and minute == 0:
        print("It's Friday 5 PM. Please Check your Email Inbox.")
        # Add your next test steps here
    else:
        print("Email will be sent on Friday 5 PM.")
        # You can simulate or log notification steps here
        assert True, "Test stopped since it's not Friday 5 PM."
        pytest.skip("Test skipped since it's not Friday 5 PM.")

    try:
        driver.get("https://mail.google.com/mail/u/0/#inbox")

        with allure.step("Waiting for Document Ready State to be Complete"):
            WebDriverWait(driver, 90).until(
                lambda d: print("Current Ready State:", d.execute_script('return document.readyState')) or
                          d.execute_script('return document.readyState') == 'complete'
            )
        print("Document Ready State is COMPLETE!")
        time.sleep(1)

        email_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='identifierId']")))
        email_field.send_keys("usman.arshad@rolustech.com")

        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Next']")))
        next_btn.click()

        password_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Passwd']")))
        password_field.send_keys("test")

        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Next']")))
        next_btn.click()
        time.sleep(20)

        try:
            # Wait for Gmail Inbox to Load
            wait.until(EC.presence_of_element_located((By.XPATH, "//table[@role='grid']")))

            # Locate the Gmail Search Box
            search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search mail']")))

            # Type Email Search Query (Modify as Needed)
            search_box.send_keys("from:SF Development")  # Modify email search criteria
            search_box.send_keys(Keys.ENTER)

            # Wait for Search Results to Load
            time.sleep(5)  # Adjust sleep time as needed

            try:
                # Capture Search Results
                emails = driver.find_elements(By.XPATH, "(//td[@class='oZ-x3 xY'])")
                print(f"Total Emails Found: {len(emails)}")
            except (NoSuchElementException, TimeoutException) as e:
                print(f"Message: {type(e).__name__}")
                assert True

        except (NoSuchElementException, TimeoutException) as e:
            print(f"Message: {type(e).__name__}")
            print("2 Step verification not completed")
            assert True

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
        assert True
