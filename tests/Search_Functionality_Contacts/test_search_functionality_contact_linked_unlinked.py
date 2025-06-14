import time
import pytest
import allure
from test_utils import skip_broken , pass_broken

from selenium import webdriver
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


@pytest.mark.smoke
@pytest.mark.release_three
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Contacts")
@allure.story("Ensure correct results for linked and unlinked contacts.")
@pytest.mark.all
@pass_broken
def test_search_linked_unlinked(driver, config):
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
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    # Select the Contacts tab and print its text
    tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Contacts']")))
    print(f"Current Tab : {tab.text}")
    tab.click()

    # Wait for the results to load
    time.sleep(15)

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

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Verification Screenshot", attachment_type=allure.attachment_type.PNG)

    for name in account_names:
        print(name.text)

    # Extract all link icons
    link_icons = driver.find_elements(By.XPATH, "//tbody/tr/th[1]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-icon[1]")

    # Assert that the no link icon found
    assert len(link_icons) <= 0, f"Error occurred: Link icon found : {len(link_icons)}"
    time.sleep(2)
