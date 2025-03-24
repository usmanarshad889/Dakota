import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
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
def test_load_contacts_unlinked(driver, config):
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
        btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[@data-target-selection-name='sfdc:TabDefinition.Marketplace__Dakota_Search']")))
        btn.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
    time.sleep(1)

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
    dropdown_option.select_by_visible_text("Unlinked Contacts")
    time.sleep(1)

    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    button.click()

    # Parameters
    max_records = 200
    retry_limit = 3  # How many times to retry if no new records load

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
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", last_element)
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

    # Verify the linked icon
    xpath = '''//tbody/tr/th[1]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-icon[1]'''
    all_linked_icons = driver.find_elements(By.XPATH, xpath)

    print(f"Actual Displayed Contacts: {len(names)}")
    print(f"Actual Displayed Icons: {len(all_linked_icons)}")

    assert len(all_linked_icons) <= 0 , f"Found Linked icons : {len(all_linked_icons)}"