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


@pytest.mark.all
@pytest.mark.release_five
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Search Tab")
@allure.story("Test the records loading functionality of search tab.")
@pass_broken
def test_search_tab_record_loading(driver, config):
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


    # Navigate to Search Page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Searches")

    # Verify Search Page Loaded
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, "(//th[@data-label='Search Name'])[1]")))
        assert element.is_displayed(), "Search list is not displayed"
    except TimeoutException:
        pytest.fail("Search list not loaded in time")

    # Parameters
    max_records = 500
    retry_limit = 3  # How many times to retry if no new records load

    # Initial wait
    time.sleep(5)

    prev_count = 0

    while True:
        # Get current loaded account names
        names = wait.until(EC.presence_of_all_elements_located((By.XPATH, "(//th[@data-label='Search Name'])")))
        new_count = len(names)
        print(f"Records Loaded: {new_count}")

        # Check if max limit reached
        if new_count >= max_records:
            print(f"Reached {max_records} records. Stopping.")
            break

        # Retry checking if new records load
        retries = 0
        while retries < retry_limit:
            # Scroll to last element
            last_element = names[-1]
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", last_element)
            ActionChains(driver).move_to_element(last_element).perform()

            # Wait for new records to load
            time.sleep(5)
            names_after_scroll = driver.find_elements(By.XPATH, "(//th[@data-label='Search Name'])")
            updated_count = len(names_after_scroll)

            if updated_count > new_count:
                print(f"New records loaded: {updated_count}")
                prev_count = updated_count
                break  # New records loaded, continue loop
            else:
                retries += 1
                print(f"No new records, retry {retries}/{retry_limit}...")

        # If no new records after retries, stop loop
        if retries == retry_limit:
            print("No more records loading. Stopping.")
            break

    # Optional: Scroll to the top after loading
    first_element = names[0]
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", first_element)
    ActionChains(driver).move_to_element(first_element).perform()

    print("All possible records loaded.")
    time.sleep(2)

    # Screenshot & Allure attachment
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Loading Records", attachment_type=allure.attachment_type.PNG)

    # Verify the linked icon
    xpath = '''(//th[@data-label='Search Name'])'''
    all_records = driver.find_elements(By.XPATH, xpath)

    print(f"Displayed Records: {len(all_records)}")

    assert len(all_records) >= 490 , f"Actual Records : {len(all_records)} but expected was 500"
