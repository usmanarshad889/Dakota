import time
from asyncio import wait_for

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

    # Navigate to the contact search page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    # Select the Contacts tab and print its text
    tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Contacts']")))
    print(f"Current Tab : {tab.text}")
    tab.click()

    # Wait for the results to load
    time.sleep(8)

    # Select Display Criteria (Linked Account)
    criteria_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='DisplayCriteria'])[2]")))
    dropdown_option = Select(criteria_dropdown)
    dropdown_option.select_by_visible_text("Linked Contacts")

    # Click the Search button and print its text
    search_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")
    ))
    print(f"Button Text : {search_button.text}")
    search_button.click()


    # Extract all contacts names text using a simpler XPath
    account_names = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//lightning-datatable//tbody/tr/td[2]")
    ))

    # Extract all link icons
    link_icons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/th[1]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-icon[1]")))

    # Assert that the number of account names matches the number of link icons
    assert len(account_names) == len(link_icons), "Error occurred: Number of account names does not match number of link icons"
    time.sleep(2)


    # Click on reset button
    reset_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='buttonDiv']//button[@title='Reset'][normalize-space()='Reset']")))
    reset_button.click()
    time.sleep(1)


    # Select Display Criteria (Unlinked Account)
    criteria_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='DisplayCriteria'])[2]")))
    dropdown_option = Select(criteria_dropdown)
    dropdown_option.select_by_visible_text("Unlinked Contacts")

    # Click the Search button and print its text
    search_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")
    ))
    print(f"Button Text : {search_button.text}")
    search_button.click()


    # Extract all contacts names text using a simpler XPath
    account_names = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//lightning-datatable//tbody/tr/td[2]")
    ))

    for name in account_names:
        print(name.text)

    # Extract all link icons
    link_icons = driver.find_elements(By.XPATH, "//tbody/tr/th[1]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-icon[1]")

    # Assert that the no link icon found
    assert len(link_icons) <= 0, f"Error occurred: Link icon found : {len(link_icons)}"
    time.sleep(2)
