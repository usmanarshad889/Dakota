import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
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

@pytest.mark.release_one
@pytest.mark.P1
def test_link_unlink_account(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 30)

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["username"])
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["password"])
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()

    # Navigate to installed pakages setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='DisplayCriteria']")))
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Unlinked Accounts")
    time.sleep(1)

    # Click on search button
    try:
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='searchTerm']")))
        btn.clear()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
        pass

    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
    time.sleep(5)
    btn.click()

    # store account name
    account_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//tbody/tr[1]/td[2]")))
    account_name = account_field.text

    # Click on first account name checkbox
    first_box = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[contains(@class,'slds-checkbox_faux')])[2]")))
    first_box.click()

    # Click on linked account
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='MassUploadActions']")))
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Link Account")

    # Click on linked account
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@class='slds-select'])[4]")))
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Dakota Name")

    try:
        dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@class='slds-select'])[5]")))
        dropdown_option = Select(dropdown)
        dropdown_option.select_by_visible_text("Account Name")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
        pass

    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='slds-button slds-button_neutral slds-button slds-button--brand '][normalize-space()='Search']"))).click()
    time.sleep(8)

    # Check if it is already mapped
    cross_icon = driver.find_elements(By.XPATH, "(//lightning-primitive-icon[@variant='bare'])[129]")

    if not cross_icon:
        # Select account name
        search_fld = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search by Name']")))
        search_fld.click()
        # search_fld.send_keys("Test")
        time.sleep(3)

        try:
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//li[@role='presentation' and @class='slds-listbox__item MarketplaceCustomLookupResult'])[3]")))
            btn.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: {type(e).__name__}")
            print("1")
            pass

        try:
            # search_fld.send_keys("Test Contacts")
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='some-class']//span[contains(text(),' ')])[1]")))
            btn.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: {type(e).__name__}")
            print("2")
            pass

        try:
            # search_fld.send_keys("Test Contacts")
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='some-class']//span[contains(text(),' ')]")))
            btn.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: {type(e).__name__}")
            print("3")
            pass



    # Click on linked account
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Link Accounts']")))
    btn.click()

    time.sleep(2)

    toast_message = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
    print(f"Actual Toast Text : {toast_message.text}")

    valid_messages = [
        "Account(s) linking is in progress",
        "No account to link."
    ]

    toast_text = toast_message.text.strip()
    assert toast_text in valid_messages, f"Unexpected Toast Message: {toast_text}"
    time.sleep(2)