import time
import pytest
import allure
import random
import string
from test_utils import skip_broken

from selenium.webdriver import ActionChains
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Generate random phone and mobile numbers
phone = "".join(random.choices(string.digits, k=10))
mobile = "".join(random.choices(string.digits, k=10))

# Generate a random suffix
suffix = random.choice(["Jr.", "Sr.", "I", "II", "III", "IV", "V"])

# Generate a random email
email = "".join(random.choices(string.ascii_lowercase, k=7)) + "@example.com"

# Generate a random CRD number
CRD = "".join(random.choices(string.digits, k=5))

print("Phone:", phone)
print("Mobile:", mobile)
print("Suffix:", suffix)
print("Email:", email)
print("CRD:", CRD)

@pytest.fixture(scope="module")
def driver():
    """Fixture for setting up WebDriver"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.mark.release_six
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Contact Creation")
@allure.story("Verify the correct creation of contact in Metro Area.")
@pytest.mark.all
# @skip_broken
def test_metro_area_account_creation(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
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

    # Sroll to All contact button and click on it
    element = wait.until(EC.presence_of_element_located((By.XPATH, "//c-dakota-contacts-home-office-in-metro-area//slot//a[@class='slds-card__header-link']")))
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


    # Get all contacts
    contacts = wait.until(EC.presence_of_all_elements_located((By.XPATH, "(//button[@name='contactClicked'])")))

    for index in range(1, len(contacts) + 1):
        # Check if the icon exists for this row
        icon_xpath = f"//tbody/tr[{index}]/th[1]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-icon[1]"
        icon = driver.find_elements(By.XPATH, icon_xpath)

        if not icon:  # If no icon is found
            contact_name = contacts[index - 1].text  # Get the contact name
            print(f"Account without link icon: {contact_name} (Row {index})")

            # Get the contact button element
            contact_xpath = f"(//button[@name='contactClicked'])[{index}]"
            contact_button = wait.until(EC.element_to_be_clickable((By.XPATH, contact_xpath)))

            # Scroll to the contact button
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", contact_button)
            time.sleep(3)  # Wait for smooth scrolling

            # Click on the contact
            contact_button.click()
            print(f"Scrolled to and clicked on contact at row {index}")
            break  # Stop after clicking on the first found contact


    # Verify the "Create Account" button on preview popup
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Create Contact']")))

    assert button.text.strip() == "Create Contact" , f"Expected button was 'Create Account' but got {button.text}"
    time.sleep(1)

    # Verify the correct Creation
    button.click()

    # Select Account Name
    try:
        input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search Accounts...']")))
        input_field.clear()
        input_field.send_keys("Test Contacts")
        time.sleep(3)
        dropdown_option = wait.until(EC.visibility_of_element_located((By.XPATH, "(//lightning-base-combobox-item[@role='option'])[2]")))
        dropdown_option.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")


    # Select name - Salutation
    salutation_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@name='salutation']")))
    salutation_field.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//lightning-base-combobox-item[@data-value='Mr.']").click()

    # Enter Phone
    name_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Phone']")))
    name_field.clear()
    name_field.send_keys(phone)

    # Enter Mobile
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='MobilePhone']")))
    field.clear()
    field.send_keys(mobile)

    # Scroll down
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='MobilePhone']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    # Select Suffix
    suffix_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='suffix']")))
    suffix_input.clear()
    suffix_input.send_keys(suffix)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='suffix']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    # Enter Email
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Email']")))
    field.clear()
    field.send_keys(email)

    # click on save button
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
    save_btn.click()

    time.sleep(2)

    # Wait for toast message
    toast_message = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
    print(f"Toast message: {toast_message.text}")

    # Verify the Toast message
    assert "was created" in toast_message.text.lower(), f"Test failed: {toast_message.text}"
    time.sleep(2)

    # Attach a screenshot of the final state
    allure.attach(driver.get_screenshot_as_png(), name="Final_State_Screenshot", attachment_type=AttachmentType.PNG)
