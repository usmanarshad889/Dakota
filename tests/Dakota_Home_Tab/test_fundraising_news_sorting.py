import time
from datetime import datetime
import pytest
import allure
from test_utils import skip_broken , pass_broken

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def is_sorted(data):
    """Check if a list is sorted in either ascending or descending order"""
    return data == sorted(data) or data == sorted(data, reverse=True)

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.mark.release_two
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Dakota Home Tab - Fundraising News")
@allure.story("Validate data consistency and sorting in Fundraising News")
@pytest.mark.all
@pass_broken
def test_fundraising_news_sorting(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    driver.delete_all_cookies()
    wait = WebDriverWait(driver, 30, poll_frequency=0.5)

    # Login block
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(config["username"])
        wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(config["password"])
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.ID, "Login"))).click()
    except Exception as e:
        driver.quit()
        pytest.skip(f"Skipping test due to login failure: {type(e).__name__}")

    # Confirm login success
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='App Launcher']")))
        print("App Launcher is found")
    except Exception as e:
        driver.quit()
        pytest.skip(f"Skipping test due to missing App Launcher: {type(e).__name__}")

    # Navigate to Dakota Home Page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Home")

    wait = WebDriverWait(driver, 60, poll_frequency=0.5)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/marketplace-dakota-home-page-main[1]/div[1]/div[2]/div[1]/c-dakota-news[1]/article[1]/div[3]/lightning-card[1]/article[1]/div[2]/slot[1]/div[4]/p[1]/span[1]/lightning-formatted-date-time[1]")))
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)

    # Click on View all button
    view_all = wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'View All')])[1]")))
    view_all.click()

    """Extracts and converts date strings to datetime objects"""
    xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]
    /div[1]/div[1]/div[1]/div[1]/div[1]/marketplace-dakota-news-view-all[1]
    /article[1]/div[2]/div[1]/div/p[1]/span[1]/lightning-formatted-date-time[1]'''
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
            date_list.append(date_obj)
        except ValueError:
            allure.attach(f"Invalid date format: {text}", "❌ Date Parsing Error", allure.attachment_type.TEXT)

    # Ensure the list is sorted
    assert date_list, "❌ No date elements found!"
    assert is_sorted(date_list), "❌ Fundraising News section dates are not sorted correctly!"