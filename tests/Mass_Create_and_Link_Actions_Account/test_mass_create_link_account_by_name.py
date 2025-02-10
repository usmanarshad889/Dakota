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

def test_mass_create_link_account_by_name(driver, config):
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

    # Navigate to installed pakages setup
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Dakota_Search")
    time.sleep(13)

    dropdown = driver.find_element(By.XPATH, "//select[@name='DisplayCriteria']")
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Unlinked Accounts")
    time.sleep(1)

    driver.find_element(By.XPATH, "//button[@title='Search']").click()
    time.sleep(10)

    # Click on ALL CHECKBOX
    driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_faux'])[1]").click()
    time.sleep(1)

    # Click on linked account
    dropdown = driver.find_element(By.XPATH, "//select[@name='MassUploadActions']")
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Link Account")
    time.sleep(10)

    # Click on linked account
    driver.find_element(By.XPATH, "//button[normalize-space()='Link Accounts']").click()
    time.sleep(10)
    driver.quit()
