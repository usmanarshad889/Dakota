import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
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

@pytest.mark.P1
@pytest.mark.release_two
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
    time.sleep(2)
    login_button.click()

    # Click on Marketplace Search button
    try:
        btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[@data-target-selection-name='sfdc:TabDefinition.Marketplace__Dakota_Search']")))
        btn.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
    time.sleep(1)


    # Navigate to installed packages setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    # Print Current Tab
    tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Accounts']")))
    print(f"Current Tab : {tab.text}")

    button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@title='Search']")))
    print(f"Button Text : {button.text}")
    time.sleep(8)

    # Select linked accounts from filter
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='DisplayCriteria']")))
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("All Accounts")
    time.sleep(1)

    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
    button.click()

    # Parameters
    max_records = 1000
    retry_limit = 3  # How many times to retry if no new records load
    wait = WebDriverWait(driver, 20)

    # Initial wait
    time.sleep(5)

    prev_count = 0

    while True:
        # Get current loaded account names
        names = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/td[2]")))
        new_count = len(names)
        print(f"Records Loaded: {new_count}")

        # Check if max limit reached
        if new_count >= max_records:
            print(f"Reached {max_records} records. Stopping.")
            break

        # Retry checking if new records load
        retries = 0
        while retries < retry_limit:
            # Scroll to last element
            last_element = names[-1]
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'end'});", last_element)
            ActionChains(driver).move_to_element(last_element).perform()

            # Wait for new records to load
            time.sleep(5)
            names_after_scroll = driver.find_elements(By.XPATH, "//tbody/tr/td[2]")
            updated_count = len(names_after_scroll)

            if updated_count > new_count:
                print(f"New records loaded: {updated_count}")
                prev_count = updated_count
                break  # New records loaded, continue loop
            else:
                retries += 1
                print(f"No new records, retry {retries}/{retry_limit}...")

        # If no new records after retries, stop loop
        if retries == retry_limit:
            print("No more records loading. Stopping.")
            break

    # Optional: Scroll to the top after loading
    first_element = names[0]
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", first_element)
    ActionChains(driver).move_to_element(first_element).perform()

    print("All possible records loaded.")
    time.sleep(2)


    # Click on ALL CHECKBOX
    all_box = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='slds-checkbox_faux'])[1]")))
    all_box.click()

    # Click on linked account
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='MassUploadActions']")))
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Create Account")
    time.sleep(5)

    # Click on linked account
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='slds-button slds-button_neutral slds-button slds-button--brand ']")))
    btn.click()

    time.sleep(2)

    toast_message = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
    print(f"Actual Toast Text : {toast_message.text}")

    valid_messages = [
        "Account(s) creation is in progress.",
        "No account to create."
    ]

    toast_text = toast_message.text.strip()
    assert toast_text in valid_messages, f"Unexpected Toast Message: {toast_text}"
    time.sleep(4)
