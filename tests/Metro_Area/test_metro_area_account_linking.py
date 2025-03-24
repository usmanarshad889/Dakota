import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
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

@pytest.mark.P1
def test_metro_area_account_linking(driver, config):
    # Navigate to login page of fuse app
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


    # Navigate to the contact search page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Metro_Areas")

    # Wait for elements to present
    try:
        btn = wait.until(EC.presence_of_element_located((By.XPATH, "//tbody/tr[1]/th[1]/lightning-primitive-cell-factory[1]/span[1]")))
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

    # Sroll to All account button and click on it
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


    # Verify the "Link Account" button on preview popup
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Link Account']")))

    assert button.text.strip() == "Link Account" , f"Expected button was 'Link Account' but got {button.text}"
    time.sleep(1)

    # Verify the correct linking
    button.click()

    # Locate all 'Link' buttons
    all_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "(//button[@title='Link'][normalize-space()='Link'])")))

    # Check if any button is enabled
    enabled_buttons = [button for button in all_buttons if button.is_enabled()]

    if not enabled_buttons:  # If all buttons are disabled
        print(f"All {len(all_buttons)} 'Link' buttons are disabled. Performing alternative action.")

        # search the element
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='SearchBar']")))
        btn.clear()
        btn.send_keys("test")
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='slds-button slds-button_brand'][normalize-space()='Search']")))
        btn.click()
        time.sleep(2)


        # Locate all 'Link' buttons
        all_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "(//button[@title='Link'][normalize-space()='Link'])")))

        # Check if any button is enabled
        enabled_buttons = [button for button in all_buttons if button.is_enabled()]

        if not enabled_buttons:
            print("All accounts are already linked and we found no account to link")
            pytest.skip(f"Skipping the Testcase ...")

    else:
        print(f"Found {len(enabled_buttons)} enabled 'Link' buttons.")


    # Click on first enabled button
    for button in enabled_buttons:
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
        time.sleep(2)
        button.click()
        time.sleep(2)

        toast_message = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
        print(f"Actual Toast Text : {toast_message.text}")

        assert toast_message.text.strip() == "Account successfully linked", f"Contact not clicked: {toast_message.text}"
        break  # Stop after clicking the first enabled button
    time.sleep(2)
