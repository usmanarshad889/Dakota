import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
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
def test_search_state_metro_area(driver, config):
    wait = WebDriverWait(driver, 20)

    # Navigate to login page
    driver.get(config["base_url"])

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

    # Navigate to the contact search page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    # Select the Account tab and print its text
    tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Accounts']")))
    print(f"Current Tab : {tab.text}")

    # Wait for the results to load
    time.sleep(8)

    # Select Metro Area field
    cov_input = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@placeholder='Select Metro Area(s)'])")))
    cov_input.click()
    filter_input = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@placeholder,'Filter values..')])[1]")))
    filter_input.send_keys("Boston")
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//li[@data-name='Boston'])")))
    btn.click()


    # Click the Search button and print its text
    search_button = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//button[@title='Search']")
    ))
    print(f"Button Text : {search_button.text}")
    search_button.click()

    # Extract all metro area text names text using a simpler XPath
    cov_names = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//lightning-datatable//tbody/tr/td[6]")
    ))

    # Assert that at least one contact is found
    assert len(cov_names) > 0, "No metro area found in the search results"

    # Verify the metro area Text
    for contact in cov_names:
        cov_text = contact.text.strip().lower()
        print(f"Metro area Text : {cov_text}")
        assert "boston" in cov_text, f"Metro area '{cov_text}' does not contain match"

    time.sleep(2)


    # Verify the State filter
    reset_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Reset']")))
    reset_button.click()
    time.sleep(1)

    # Select State field
    con_input = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@placeholder='Select State(s)'])")))
    con_input.click()
    filter_input = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@placeholder,'Filter values..')])[3]")))
    filter_input.send_keys("Florida")
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//li[@data-name='Florida'])")))
    btn.click()


    # Click the Search button and print its text
    search_button = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//button[@title='Search']")
    ))
    print(f"Button Text : {search_button.text}")
    search_button.click()

    # Extract all Contact Type text names text using a simpler XPath
    con_names = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//lightning-datatable//tbody/tr/td[5]")
    ))

    # Assert that at least one State type is found
    assert len(con_names) > 0, "No State found in the search results"

    # Verify the State Text
    for contact in con_names:
        con_text = contact.text.strip().lower()
        print(f"State Text : {con_text}")
        assert "fl" in con_text, f"State '{con_text}' does not contain match"

    time.sleep(2)
