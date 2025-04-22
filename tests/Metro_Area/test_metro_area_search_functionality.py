import time
import random
import pytest
import allure

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Metro Area")
@allure.story("Verify the correct search functionality of Metro Area records.")
def test_metro_area_search_functionality(driver, config):
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

    # 1. Collect all Metro Area Names
    all_names_elements = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//th[@data-label='Metro Area Name']//a"))
    )

    all_names = [elem.text.strip() for elem in all_names_elements if elem.text.strip()]
    assert len(all_names) >= 3, "Not enough Metro Area Names to perform test!"

    # 2. Randomly select 3 unique names
    random_names = random.sample(all_names, 3)  # Ensures no duplicates

    for name in random_names:
        print(f"Testing search for Metro Area: {name}")

        # 3. Enter name in search box
        search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='searchValue']")))
        search_box.clear()
        search_box.send_keys(name)
        search_box.send_keys(Keys.ENTER)  # Or click search button if needed
        time.sleep(2)

        # 4. Verify result format
        result_xpath = f"//a[normalize-space()='{name}']"
        result = wait.until(EC.presence_of_element_located((By.XPATH, result_xpath)))

        assert result.is_displayed(), f"Search result for '{name}' not displayed!"
        print(f"Search result for '{name}' displayed successfully.")

        # 5. Take Screenshot & Attach to Allure
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name=f"Search Result - {name}", attachment_type=allure.attachment_type.PNG)
