import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
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


def wait_for_page_load(driver, timeout=90):
    """Reusable function to wait for document ready state."""
    time.sleep(2)
    with allure.step("Waiting for Document Ready State to be Complete"):
        WebDriverWait(driver, 90).until(
            lambda d: print("Current Ready State:", d.execute_script('return document.readyState')) or
                      d.execute_script('return document.readyState') == 'complete'
        )
    print("Document Ready State is COMPLETE!")


@pytest.mark.release_eight
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Performance Testing")
@allure.story("Test the loading time of the SF Org Tabs.")
def measure_page_load(driver, url, page_name):
    """Reusable function to measure and report page load time."""
    with allure.step(f"Navigating to {page_name}"):
        driver.get(url)

    start_time = time.time()
    wait_for_page_load(driver)
    end_time = time.time()

    time_taken = end_time - start_time
    print(f"Total time taken for {page_name}: {time_taken:.2f} seconds")

    allure.attach(
        body=f"Page Load Time for {page_name}: {time_taken:.2f} seconds",
        name=f"{page_name} Load Time",
        attachment_type=AttachmentType.TEXT
    )


@allure.severity(allure.severity_level.CRITICAL)
def test_performance_optimization(driver, config):
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

    # Measure Home Page load time
    measure_page_load(driver, f"{config['base_url']}", "Home Page")

    # Measure Metro Area Page load time
    measure_page_load(driver, f"{config['base_url']}lightning/n/Marketplace__Metro_Areas", "Metro Area Page")

    # Measure Account Page load time
    measure_page_load(driver, f"{config['base_url']}lightning/o/Account/list?filterName=__Recent", "Account Page")

    # Measure Contact Page load time
    measure_page_load(driver, f"{config['base_url']}lightning/o/Contact/list?filterName=__Recent", "Contact Page")

    # Measure Dakota Marketplace Page load time
    measure_page_load(driver, f"{config['base_url']}lightning/n/Marketplace__Dakota_Search", "Dakota Marketplace Page")

    # Measure Dakota Video Page load time
    measure_page_load(driver, f"{config['base_url']}lightning/n/Marketplace__Dakota_Video", "Dakota Video Page")

    # Measure Dakota Search Page load time
    measure_page_load(driver, f"{config['base_url']}lightning/n/Marketplace__Searches", "Dakota Search Page")

    # Measure Dakota Investment Page load time
    measure_page_load(driver, f"{config['base_url']}lightning/n/Marketplace__Investments", "Dakota Investment Page")

    # Measure Dakota Manager Presentation Page load time
    measure_page_load(driver, f"{config['base_url']}lightning/n/Marketplace__Manager_Presentations", "Dakota Manager Presentation Page")

    # Measure Dakota Public Plan Page load time
    measure_page_load(driver, f"{config['base_url']}lightning/n/Marketplace__Public_Plan_Minutes", "Dakota Public Plan Page")

    # Measure Dakota Conference Page load time
    measure_page_load(driver, f"{config['base_url']}lightning/n/Marketplace__Conferences", "Dakota Conference Page")

    # Measure Dakota Marketplace Update Page load time
    measure_page_load(driver, f"{config['base_url']}lightning/o/Marketplace__Activity_Stream__c/list?filterName=__Recent", "Dakota Marketplace Update Page")

    # Measure Dakota Task Page load time
    measure_page_load(driver, f"{config['base_url']}lightning/o/Task/home", "Dakota Task Page")

    # Measure Dakota Reports Page load time
    measure_page_load(driver, f"{config['base_url']}lightning/o/Report/home?queryScope=mru", "Dakota Reports Page")

    # Measure Member Comment Page load time
    measure_page_load(driver, f"{config['base_url']}lightning/n/Marketplace__Member_Comments", "Member Comment Page")

    # Measure Dakota Setup Page load time
    measure_page_load(driver, f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup", "Dakota Setup Page")
