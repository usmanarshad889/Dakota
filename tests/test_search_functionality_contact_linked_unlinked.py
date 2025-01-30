import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# Fixture to load the configuration
@pytest.fixture(scope="module")
def config(request):
    import json
    import os
    env = request.config.getoption("--env")
    config_file_path = os.path.join("config", f"config.{env}.json")
    with open(config_file_path) as file:
        return json.load(file)

def test_search_linked_unlinked(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 10)

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["username"])

    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["password"])

    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()
    time.sleep(3)

    # Navigate to Marketplace Search
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Dakota_Search")
    time.sleep(15)

    # Navigate to Contacts Tab
    driver.find_element(By.XPATH, "//li[@title='Contacts']").click()
    time.sleep(7)

    # Select Display Criteria (Linked Account)
    criteria_dropdown = driver.find_element(By.XPATH, "(//select[@name='DisplayCriteria'])[2]")
    dropdown_option = Select(criteria_dropdown)
    dropdown_option.select_by_visible_text("Linked Contacts")

    # Click on Search Button
    driver.find_element(By.XPATH,
                        "//div[contains(@class,'filterInnerDiv')]//button[contains(@title,'Search')][normalize-space()='Search']").click()
    time.sleep(10)

    # Find the element and Verify
    sag_element = driver.find_elements(By.XPATH,
                                       "//tbody/tr[1]/th[1]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-icon[1]/span[1]/lightning-primitive-icon[1]//*[name()='svg']")

    if sag_element:
        assert True, "Element found"
    else:
        assert False, "Test case failed: Element not found"
    time.sleep(2)

    # Select Display Criteria (Unlinked Account)
    criteria_dropdown = driver.find_element(By.XPATH, "(//select[@name='DisplayCriteria'])[2]")
    dropdown_option = Select(criteria_dropdown)
    dropdown_option.select_by_visible_text("Unlinked Contacts")

    # Click on Search Button
    driver.find_element(By.XPATH,
                        "//div[contains(@class,'filterInnerDiv')]//button[contains(@title,'Search')][normalize-space()='Search']").click()
    time.sleep(10)

    # Find the element and Verify
    sag_element = driver.find_elements(By.XPATH,
                                       "//tbody/tr[1]/th[1]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-icon[1]/span[1]/lightning-primitive-icon[1]//*[name()='svg']")

    if sag_element:
        assert False, "Element not found"
    else:
        assert True, "Test case failed: Element found"
    time.sleep(2)

    driver.quit()