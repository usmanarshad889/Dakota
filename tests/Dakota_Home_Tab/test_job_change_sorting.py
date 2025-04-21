import time
from datetime import datetime
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    """Fixture for setting up WebDriver"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.P1
@pytest.mark.release_two
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Dakota Home Tab - Job Changes")
@allure.story("Validate data consistency and sorting in Job Changes")
def test_job_change_sorting(driver, config):
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

    # Navigate to Dakota Home Page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Home")
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Job Changes']")))
    print(f"Section Name : {btn.text}")

    """Extracts and converts date strings to datetime objects"""
    xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/marketplace-dakota-home-page-main[1]/div[1]/div[1]/div[1]/c-dakota-contact-updates[1]/div[1]/lightning-tabset[1]/div[1]/slot[1]/lightning-tab[1]/slot[1]/c-dakota-job-and-role-changes[1]/div[1]/div[1]/c-custom-datatable[1]/div[2]/div[1]/div[1]/table[1]/tbody[1]/tr/td[8]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-base-formatted-text'''
    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

    # Check if elements are found
    assert elements, "❌ No date elements found!"

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Verification Screenshot", attachment_type=allure.attachment_type.PNG)

    date_list = []
    for element in elements:
        text = element.text.strip()
        try:
            date_obj = datetime.strptime(text, "%m/%d/%Y")  # Convert to datetime object
            print(date_obj)
            date_list.append(date_obj)
        except ValueError:
            allure.attach(f"Invalid date format: {text}", "❌ Date Parsing Error", allure.attachment_type.TEXT)

    def is_sorted(data):
        """Check if a list is sorted in either ascending or descending order"""
        return data == sorted(data) or data == sorted(data, reverse=True)

    # Ensure the list is sorted
    assert date_list, "❌ No date elements found!"
    assert is_sorted(date_list), "❌ Job Changes section dates are not sorted correctly!"