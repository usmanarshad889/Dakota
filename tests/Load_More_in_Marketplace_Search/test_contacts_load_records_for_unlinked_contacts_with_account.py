import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
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

@pytest.mark.load
@pytest.mark.release_one
@pytest.mark.P1
def test_load_contacts_for_unlinked_accounts(driver, config):
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

    # Navigate to installed packages setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    # Print Current Tab
    tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Contacts']")))
    print(f"Current Tab : {tab.text}")
    tab.click()

    button = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    print(f"Button Text : {button.text}")
    time.sleep(8)

    # Select linked accounts from filter
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='DisplayCriteria'])[2]")))
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Unlinked Contacts with Linked Accounts")
    time.sleep(1)

    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    button.click()

    # Wait for contacts names to load
    time.sleep(5)
    prev_count = 0
    max_records = 300  # Stop when we reach 500 records

    while True:
        # Get all contact names
        names = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/td[2]")))
        new_count = len(names)

        print(f"Records Loaded: {new_count}")

        # Stop loop if 300 records are loaded
        if new_count >= max_records:
            print(f"Reached {max_records} records, stopping.")
            break

        # Break loop if no new records are loaded
        if new_count == prev_count:
            break

        prev_count = new_count

        # Scroll to the last element
        last_element = names[-1]
        driver.execute_script("arguments[0].scrollIntoView();", last_element)
        ActionChains(driver).move_to_element(last_element).perform()

        # Wait for the loader to appear and disappear
        try:
            loader = wait.until(EC.presence_of_element_located((By.XPATH, "//lightning-spinner[@class='slds-spinner_container']")))
            wait.until(EC.invisibility_of_element(loader))
        except TimeoutException:
            pass  # If no loader appears, continue

        # Wait a bit for new records to load
        time.sleep(7)

    # Print index and name
    for index, name in enumerate(names[:max_records], start=1):
        print(f"{index}: {name.text}")

    time.sleep(5)


    contact_icon_xpath = "//tbody/tr/th[1]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-icon[1]"
    account_icon_xpath = "//tbody/tr/td[3]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-icon[1]"

    # Find all contact and account icons
    contact_icons = driver.find_elements(By.XPATH, contact_icon_xpath)
    account_icons = driver.find_elements(By.XPATH, account_icon_xpath)

    # Assertions
    assert len(contact_icons) == 0, "Some contacts have a linked icon unexpectedly."
    assert len(account_icons) == len(names), f"Expected {len(names)} account icons, but found {len(account_icons)}."
