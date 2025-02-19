import time
import pytest
import allure
from allure_commons.types import AttachmentType
from faker import Faker
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_search_functionality_account_fields(driver, config):
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

    # Navigate to installed pakages setup
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Dakota_Search")

    # Print Current Tab
    tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Accounts']")))
    print(f"Current Tab : {tab.text}")

    button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@title='Search']")))
    print(f"Button Text : {button.text}")
    time.sleep(10)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
    button.click()

    # Save all account names
    names = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/td[2]")))

    # Scroll to the last element
    if names:
        last_element = names[-1]
        driver.execute_script("arguments[0].scrollIntoView();", last_element)
        ActionChains(driver).move_to_element(last_element).perform()

    # Print index and name
    for index, name in enumerate(names, start=1):
        print(f"{index}: {name.text}")

    time.sleep(10)

    # Navigate to Market Place Search
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Dakota_Search")

    # Define the stopping condition element
    stopping_condition_locator = (By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")

    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        # Refresh page and clear cookies
        driver.delete_all_cookies()
        driver.refresh()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-label='Contacts']"))).click()

        # Wait for search input and enter the search term
        name_input = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@name='searchTerm'])[2]")))
        name_input.clear()
        name_input.send_keys(search_name)

        search_element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))

        # Double-click search button multiple times until condition is met
        actions = ActionChains(driver)
        for _ in range(3):
            if driver.find_elements(*stopping_condition_locator):
                print("Stopping condition met. Exiting loop.")
                break

            actions.double_click(search_element).perform()

        # If element is found, exit the while loop
        if driver.find_elements(*stopping_condition_locator):
            break

        attempts += 1  # Increment attempt counter

    # Fail test if maximum attempts reached and condition is not met
    assert attempts < max_attempts, "Test failed: Stopping condition not met after 5 attempts"

    # Verify Contact name filter
    checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")
    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    print("Contact name filter verified")
    time.sleep(1)

    # Verify account name filter
    acc_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='accountName']")))
    acc_name.send_keys("test")
    acc_name.click()
    search_element = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    search_element.click()

    # Verify Account name filter
    checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")
    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    print("Account name filter verified")
    time.sleep(1)

    # Verify Coverage Area
    cov_area = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@placeholder='Select Coverage Area(s)'])")))
    cov_area.click()
    value_field = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@placeholder='Filter values..'])[5]")))
    value_field.send_keys("Commodities")
    com_value = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//li[@data-name='Commodities'])")))
    com_value.click()

    search_element = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    search_element.click()

    # Verify Coverage Area filter
    checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")
    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    print("Coverage Area filter is verified")
    time.sleep(1)

    # Verify Channel Focus
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Select Channel Focus']")))
    btn.click()
    value_field = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@placeholder='Filter values..'])[6]")))
    value_field.send_keys("Banks")
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//li[@data-name='Banks'])")))
    btn.click()

    search_element = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    search_element.click()

    # Verify Channel Focus filter
    checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")
    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    print("Channel Focus filter is verified")
    time.sleep(1)

    # Verify Metro Area Filter
    btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "(//input[contains(@placeholder,'Select Metro Area(s)')])[2]")))
    btn.click()
    value_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, "(//input[contains(@placeholder,'Filter values..')])[7]")))
    value_field.send_keys("Boston")
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//li[@data-name='Boston'])[2]")))
    btn.click()

    search_element = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    search_element.click()

    # Verify Metro Area filter
    checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")
    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    print("Metro Area filter is verified")
    time.sleep(1)

    # Verify State Filter
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@placeholder,'Select State(s)')])[2]")))
    btn.click()
    value_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, "(//input[contains(@placeholder,'Filter values..')])[9]")))
    value_field.send_keys("Florida")
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//li[@data-name='Florida'])[2]")))
    btn.click()

    search_element = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    search_element.click()

    # Verify State filter
    checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")
    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    print("State filter is verified")
    time.sleep(1)

    # Verify Contact Type Filter
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@placeholder,'Select Type(s)')])[2]")))
    btn.click()
    value_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, "(//input[contains(@placeholder,'Filter values..')])[10]")))
    value_field.send_keys("Administrator")
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//li[@data-name='Administrator'])")))
    btn.click()

    search_element = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    search_element.click()

    # Verify Contact Type filter
    checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")
    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    print("Contact Type filter is verified")
    time.sleep(1)
