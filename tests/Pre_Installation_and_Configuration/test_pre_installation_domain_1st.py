import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

domains = []
expected_domains = ["dakotanetworks--fuseupgrad.sandbox.my.salesforce-sites.com", "dakotanetworks--fuseupgrad.sandbox.my.salesforce.com", "dakotanetworks--fuseupgrad.sandbox.my.site.com", "pardot.dakotafunds.com"]

# Fixture to set up the WebDriver
@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# Test function to log in and create a custom object
def test_pre_installation_1(driver, config):
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

    # Navigate to Domain Setup
    driver.get(f"{config["base_url"]}lightning/setup/DomainNames/home")
    time.sleep(15)

    # Switch to iframe
    iframe_element = driver.find_element(By.XPATH, "//iframe[@title='Domains ~ Salesforce - Enterprise Edition']")
    driver.switch_to.frame(iframe_element)
    time.sleep(1)

    # Verify that text for my domain
    all_domains_xpath = '''/html[1]/body[1]/div[5]/div[1]/div[2]/table[1]/tbody[1]/tr/th[1]/a[1]'''
    all_domains_element = driver.find_elements(By.XPATH, all_domains_xpath)
    for domain in all_domains_element:
        all_text = domain.text
        domains.append(all_text)
    time.sleep(2)
    driver.switch_to.default_content()

    n = min(len(domains), len(expected_domains))
    if expected_domains[:n] == domains[:n]:
        assert True
    else:
        print("My custom domain verification has been failed")


    # Navigate to Deliver ability Setup
    driver.get(f"{config["base_url"]}lightning/setup/OrgEmailSettings/home")
    time.sleep(15)

    # Switch to iframe
    iframe_element = driver.find_element(By.XPATH, "//iframe[@title='Deliverability ~ Salesforce - Enterprise Edition']")
    driver.switch_to.frame(iframe_element)
    time.sleep(1)

    select_element = driver.find_element(By.XPATH, "/html[1]/body[1]/form[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[1]/select[1]")
    select = Select(select_element)
    selected_option = select.first_selected_option.text
    print(selected_option)
    driver.switch_to.default_content()

    if selected_option.lower().strip() == "all email":
        assert True
    else:
        print(f"Access Level is {selected_option} but expected was All Email")
        print("Test Case Fail")

    driver.quit()
