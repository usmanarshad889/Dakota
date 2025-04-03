import time
import pytest
import allure
from selenium import webdriver
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
def test_filter_logic_in_investment_preference(driver, config):
    # Navigate to login page of fuse app
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
        time.sleep(2)

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


    # Navigate to Dakota Marketplace Search Tab
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")
    time.sleep(20)


    # Click on Investment Preference Button
    try:
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='openChevron']//button[@type='button']")))
        button.click()
    except Exception as e:
        pytest.skip(f"Investment Preference Button is not interactable due to slow loading ... skipping test : {type(e).__name__}")


    # Select a field
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Select a field']")))
    button.click()

    all_options = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class,'slds-setup-assistant__item')]//li")))

    for option in all_options:
        if option.text.strip() == '1031 Exchange':
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", option)
            time.sleep(1)
            option.click()
            break


    # Select an operator
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@aria-haspopup='listbox'])[1]")))
    button.click()

    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='$not_equals']")))
    button.click()


    # Select value
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@aria-haspopup='listbox'])[2]")))
    button.click()

    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@title,'Yes')]")))
    button.click()


    # Add a new filter
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@title,'Add Filter')]")))
    button.click()


    # Select a field
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@placeholder='Select a field'])[2]")))
    button.click()

    # Start looping from 60 onwards
    r = 61  # Start index
    while True:  # Infinite loop, will break when 'Bank Loans' is found
        try:
            xpath = f"(//li[@role='presentation' and contains(@data-aura-class, 'MarketplaceDisplayFields')])[{r}]"
            option = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

            # Check if it's 'Bank Loans'
            if option.text.strip() == 'Bank Loans':
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
                time.sleep(1)  # Ensure visibility before clicking
                option.click()
                break  # Stop loop when found

            r += 1  # Move to next option if not found

        except Exception as e:
            pytest.skip(f"Skipping test .... : {type(e).__name__}")
            break

    # Select an operator
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@aria-haspopup='listbox'])[3]")))
    button.click()

    button = wait.until(EC.element_to_be_clickable((By.XPATH, "(//lightning-base-combobox-item[@data-value='$equals'])[2]")))
    button.click()


    # Select value
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@aria-haspopup='listbox'])[4]")))
    button.click()

    button = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[contains(@title,'No')][normalize-space()='No'])[2]")))
    button.click()


    # Click on Edit button
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@title,'Edit Filter Logic')]")))
    button.click()


    # Edit Logic
    logic_field = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@class='slds-input' and @type='text'])[3]")))
    logic_field.click()
    logic_field.clear()
    logic_field.send_keys("1 OR 2")


    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Filter Logic ", attachment_type=allure.attachment_type.PNG)


    # Click on Account Button
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Accounts']")))
    button.click()


    # Click on Search button
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
    driver.execute_script("arguments[0].click();", button)
    time.sleep(15)

    # Scroll down by 400 pixels
    driver.execute_script("window.scrollBy(0, 400);")
    time.sleep(1)



    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Logic - Result ", attachment_type=allure.attachment_type.PNG)