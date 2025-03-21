import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def wait_for_page_load(driver, timeout=90):
    """Wait for document ready state AND universal main content element."""
    # Step 1: Wait for document ready
    with allure.step("Waiting for Document Ready State to be Complete"):
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
    print("Document Ready State is COMPLETE!")

    # Step 2: Wait for key content element (common to all pages)
    key_locator = (By.CSS_SELECTOR, "div[role='main']")
    try:
        with allure.step("Waiting for main content element to load"):
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(key_locator)
            )
        print("Main content element loaded successfully!")
    except TimeoutException:
        allure.attach(driver.get_screenshot_as_png(), name="Timeout Error", attachment_type=AttachmentType.PNG)
        pytest.fail("Page content did not load properly.")


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
    wait = WebDriverWait(driver, 20)

    # Navigate to login page
    driver.get(config["base_url"])

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["username"])
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["password"])
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()

    # Define pages with their URLs
    pages = [
        {
            "name": "Home Page",
            "url": f"{config['base_url']}"
        },
        {
            "name": "Metro Area Page",
            "url": f"{config['base_url']}lightning/n/Marketplace__Metro_Areas"
        },
        {
            "name": "Account Page",
            "url": f"{config['base_url']}lightning/o/Account/list?filterName=__Recent"
        },
        {
            "name": "Contact Page",
            "url": f"{config['base_url']}lightning/o/Contact/list?filterName=__Recent"
        },
        {
            "name": "Dakota Marketplace Page",
            "url": f"{config['base_url']}lightning/n/Marketplace__Dakota_Search"
        },
        {
            "name": "Dakota Video Page",
            "url": f"{config['base_url']}lightning/n/Marketplace__Dakota_Video"
        },
        {
            "name": "Dakota Search Page",
            "url": f"{config['base_url']}lightning/n/Marketplace__Searches"
        },
        {
            "name": "Dakota Investment Page",
            "url": f"{config['base_url']}lightning/n/Marketplace__Investments"
        },
        {
            "name": "Dakota Manager Presentation Page",
            "url": f"{config['base_url']}lightning/n/Marketplace__Manager_Presentations"
        },
        {
            "name": "Dakota Public Plan Page",
            "url": f"{config['base_url']}lightning/n/Marketplace__Public_Plan_Minutes"
        },
        {
            "name": "Dakota Conference Page",
            "url": f"{config['base_url']}lightning/n/Marketplace__Conferences"
        },
        {
            "name": "Dakota Marketplace Update Page",
            "url": f"{config['base_url']}lightning/o/Marketplace__Activity_Stream__c/list?filterName=__Recent"
        },
        {
            "name": "Dakota Task Page",
            "url": f"{config['base_url']}lightning/o/Task/home"
        },
        {
            "name": "Dakota Reports Page",
            "url": f"{config['base_url']}lightning/o/Report/home?queryScope=mru"
        },
        {
            "name": "Member Comment Page",
            "url": f"{config['base_url']}lightning/n/Marketplace__Member_Comments"
        },
        {
            "name": "Dakota Setup Page",
            "url": f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup"
        },
    ]

    # Iterate and measure each page
    for page in pages:
        measure_page_load(driver, page["url"], page["name"])

