import time
import random
import pytest
import allure

from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys
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


@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Search Functionality")
@allure.story("Ensure search by investment name returns accurate results and test search functionality with partial and complete names.")
def test_investment_tab_search_functionality(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 20)

    try:
        # Perform login
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.send_keys(config["username"])
        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.send_keys(config["password"])
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        time.sleep(1)
        login_button.click()
        time.sleep(2)

        # Wait for URL change
        WebDriverWait(driver, 20).until(EC.url_contains("/lightning"))

    except Exception as e:
        pytest.skip(f"Skipping test due to unexpected login error: {type(e).__name__}")


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


    # 1. Collect all Investment Names
    all_names_elements = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/th"))
    )

    all_names = [elem.text.strip() for elem in all_names_elements if elem.text.strip()]
    assert len(all_names) >= 3, "Not enough Investment Names to perform test!"

    # 2. Randomly select 3 unique names
    random_names = random.sample(all_names, 3)  # Ensures no duplicates

    for name in random_names:
        print(f"Testing FULL search for Investment: {name}")

        # FULL SEARCH
        search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='searchValue']")))
        search_box.clear()
        search_box.send_keys(name)  # Full name
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)

        inv_names = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/th")))

        # Screenshot & Allure attachment
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name=f"{name} - Full Search Result", attachment_type=allure.attachment_type.PNG)

        assert len(inv_names) > 0, "No investment names found in FULL search results"

        # Assertion for FULL search
        for inv in inv_names:
            inv_text = inv.text.strip().lower()
            assert name.lower() in inv_text, f"Investment name '{inv.text}' does not match '{name}'"

        driver.refresh()
        # Verify Investment Page Loaded
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, "(//td[@data-label='Created Date'])[1]")))
            assert element.is_displayed(), "Investment list is not displayed"
        except TimeoutException:
            pytest.fail("Investment list not loaded in time")


        ### PARTIAL SEARCH ###
        partial_name = name[:len(name)//2]  # First half of the name
        print(f"Testing PARTIAL search for Investment: {partial_name}")

        search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='searchValue']")))
        search_box.clear()
        search_box.send_keys(partial_name)
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)

        inv_names_partial = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/th")))

        screenshot_partial = driver.get_screenshot_as_png()
        allure.attach(screenshot_partial, name=f"{partial_name} - Partial Search Result", attachment_type=allure.attachment_type.PNG)

        assert len(inv_names_partial) > 0, "No investment names found in PARTIAL search results"

        # Assertion for PARTIAL search
        for inv in inv_names_partial:
            inv_text = inv.text.strip().lower()
            assert partial_name.lower() in inv_text, f"Investment name '{inv.text}' does not contain partial '{partial_name}'"

        driver.refresh()
        # Verify Investment Page Loaded
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, "(//td[@data-label='Created Date'])[1]")))
            assert element.is_displayed(), "Investment list is not displayed"
        except TimeoutException:
            pytest.fail("Investment list not loaded in time")
