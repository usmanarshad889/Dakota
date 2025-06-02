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
    """Fixture for setting up WebDriver"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.mark.release_three
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Metro Areas")
@allure.story('Validate the "Create Account and Related Contact" button in the preview popup for Metro Areas tabs and proper creation.')
def test_create_account_preview_popup_metro_area(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    driver.delete_all_cookies()
    wait = WebDriverWait(driver, 60, poll_frequency=0.5)

    try:
        # Perform login
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.send_keys(config["username"])
        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.send_keys(config["password"])
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        time.sleep(2)
        login_button.click()
        time.sleep(3)

        # Wait for URL change
        wait.until(EC.url_contains("lightning.force.com"))

        # Verify Login
        try:
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[2]"))).click()
        except Exception as e:
            pytest.skip(f"Skipping test due to unexpected login error: {type(e).__name__}")
            driver.quit()

    except Exception as e:
        pytest.skip(f"Skipping test due to unexpected login error: {type(e).__name__}")
        driver.quit()


    with allure.step("Waiting for Document Ready State to be Complete"):
        WebDriverWait(driver, 90).until(
            lambda d: print("Current Ready State:", d.execute_script('return document.readyState')) or
                      d.execute_script('return document.readyState') == 'complete'
        )
    print("Document Ready State is COMPLETE!")
    time.sleep(1)

    # Navigate to the contact search page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Metro_Areas")

    # Wait for elements to present
    try:
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//tbody/tr[1]/td[1])[4]")))
        print(btn.text)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")

    time.sleep(2)


    # Wait for all links under "Metro Area Name"
    all_names = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//th[@data-label='Metro Area Name']//a")))

    # Loop through metro area and find "Boston"
    for name in all_names:
        if name.text.strip() == "Boston":
            ActionChains(driver).move_to_element(name).click().perform()
            print("Clicked on Boston link")
            time.sleep(5)  # Allow time for page to load
            break
    else:
        print("Boston link not found")


    # Get all open tab handles
    tabs = driver.window_handles
    print(f"Total open tabs: {len(tabs)}")

    # Switch to the second tab (index 1)
    if len(tabs) > 1:
        driver.switch_to.window(tabs[1])
        print(f"Switched to second tab: {driver.title}")
    else:
        print("Only one tab is open, cannot switch.")

    # Wait for elements to present
    try:
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='videoMsgStyling']")))
        print(btn.text)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")

    time.sleep(2)

    # Scroll down 3000 pixels
    driver.execute_script("window.scrollBy(0, 3000);")
    time.sleep(2)

    # Scroll to All account button and click on it
    element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='All Accounts']")))
    # Scroll to the element
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(1)
    element.click()

    # Wait for elements to present
    try:
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//tbody/tr[1]/td[1]")))
        print(btn.text)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")

    time.sleep(2)


    # Get all accounts
    accounts = wait.until(EC.presence_of_all_elements_located((By.XPATH, "(//button[@name='accountClicked'])")))

    for index in range(1, len(accounts) + 1):
        # Check if the icon exists for this row
        icon_xpath = f"//tbody/tr[{index}]/th[1]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-icon[1]"
        icon = driver.find_elements(By.XPATH, icon_xpath)

        if not icon:  # If no icon is found
            account_name = accounts[index - 1].text  # Get the account name
            print(f"Account without link icon: {account_name} (Row {index})")

            # Get the account button element
            account_xpath = f"(//button[@name='accountClicked'])[{index}]"
            account_button = wait.until(EC.element_to_be_clickable((By.XPATH, account_xpath)))

            # Scroll to the account button
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", account_button)
            time.sleep(3)  # Wait for smooth scrolling

            # Click on the account
            account_button.click()
            print(f"Scrolled to and clicked on account at row {index}")
            break  # Stop after clicking on the first found account


    # Verify the "Create Account" button on preview popup
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Create Account &')]")))

    assert button.text.strip() == "Create Account & Related Contacts" , f"Expected button was 'Create Account & Related Contacts' but got {button.text}"
    time.sleep(1)

    # Verify the correct creation
    button.click()
    time.sleep(8)

    # Check if "Create Account" button exists
    create_account_buttons = driver.find_elements(By.XPATH, "//button[normalize-space()='Create Account']")

    if create_account_buttons:
        create_account = wait.until(EC.element_to_be_clickable(create_account_buttons[0]))
        create_account.click()

        # Wait for toast message
        toast_message = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
        print(f"Toast message: {toast_message.text}")

        # Verify the Toast message
        assert "successfully" in toast_message.text.lower(), f"Test failed: {toast_message.text}"
        time.sleep(2)

        # Attach a screenshot of the final state
        allure.attach(driver.get_screenshot_as_png(), name="Final_State_Screenshot", attachment_type=AttachmentType.PNG)

    else:
        time.sleep(1)
        # Add Account with Related Contact(s)
        try:
            check_box = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")))
            check_box.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: {type(e).__name__}")

        # click on save/create button
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save and Create']")))
        save_btn.click()

        # Wait for toast message
        toast_message = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
        print(f"Toast message: {toast_message.text}")

        # Take Screenshot & Attach to Allure
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name=f"Verification Screenshot", attachment_type=allure.attachment_type.PNG)

        # Verify the Toast message
        assert "successfully" in toast_message.text.lower(), f"Test failed: {toast_message.text}"
        time.sleep(2)
