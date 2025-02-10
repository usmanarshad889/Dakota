import time
import pytest
import allure
from allure_commons.types import AttachmentType
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

def test_search_linked_unlinked(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 20)

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

    # Select Display Criteria (Linked Account)
    criteria_dropdown = driver.find_element(By.XPATH, "(//select[@name='DisplayCriteria'])")
    dropdown_option = Select(criteria_dropdown)
    dropdown_option.select_by_visible_text("Linked Accounts")

    # click on search button
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
    button.click()
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
    criteria_dropdown = driver.find_element(By.XPATH, "(//select[@name='DisplayCriteria'])")
    dropdown_option = Select(criteria_dropdown)
    dropdown_option.select_by_visible_text("Unlinked Accounts")

    # click on search button
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
    button.click()
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