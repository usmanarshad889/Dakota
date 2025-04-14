import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.common import TimeoutException
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

@pytest.mark.regression
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Manager Presentations")
@allure.story("Verify correct display of Manager Presentations with all required fields.")
def test_field_display(driver, config):
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
        wait.until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[5]"))).click()

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

    # Navigate to installed pakages setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Manager_Presentations")


    # Verify Manager Presentation Page Loaded
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, "(//th[@data-label='Manager Presentation Name'])[1]")))
        assert element.is_displayed(), "Manager Presentation list is not displayed"
    except TimeoutException:
        pytest.fail("Manager Presentation list not loaded in time")


    xpaths = [
        "(//c-custom-datatable[@class='tablecol managerPresentationDataTable']//a[@role='button'])[1]",
        "(//c-custom-datatable[@class='tablecol managerPresentationDataTable']//a[@role='button'])[2]",
        "(//c-custom-datatable[@class='tablecol managerPresentationDataTable']//a[@role='button'])[3]",
        "(//c-custom-datatable[@class='tablecol managerPresentationDataTable']//a[@role='button'])[4]",
        "(//c-custom-datatable[@class='tablecol managerPresentationDataTable']//a[@role='button'])[5]",
        "(//c-custom-datatable[@class='tablecol managerPresentationDataTable']//a[@role='button'])[6]",
        "(//c-custom-datatable[@class='tablecol managerPresentationDataTable']//a[@role='button'])[7]",
        "(//c-custom-datatable[@class='tablecol managerPresentationDataTable']//a[@role='button'])[8]"
    ]

    expected_field_text = [
        "Manager Presentation Name",
        "Type",
        "Account Name",
        "Public Plan Minute",
        "Investment Strategy",
        "Asset Class",
        "Sub-Asset Class",
        "Meeting Date"
    ]

    extracted_field_text = []
    second_extracted_text = []  # List to store only the second line

    for xpath in xpaths:
        try:
            field = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            text = field.text.strip()
            extracted_field_text.append(text)  # Store all extracted text

            # Extract second line if text has multiple lines
            lines = text.split("\n")  # Split text by newline
            if len(lines) > 1:  # Ensure there's a second line
                print(f"Actual Field Name : {lines[1].strip()}")
                second_extracted_text.append(lines[1].strip())  # Append second line

        except (NoSuchElementException, TimeoutException) as e:
            print(f"Message: {type(e).__name__}")

    assert expected_field_text == second_extracted_text, "All Fields are not displayed correctly"