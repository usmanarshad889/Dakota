import time
import pytest
import allure
from allure_commons.types import AttachmentType
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

@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Package uninstallation")
@allure.story("Verify the uninstallation of managed package")
def test_package_uninstallation(driver, config):
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



    # Navigate to installed package
    driver.get(f"{config['base_url']}lightning/setup/ImportedPackage/home")

    # Switch to iframe
    iframe_element = wait.until(EC.element_to_be_clickable((By.XPATH,"//iframe[@title='Installed Packages ~ Salesforce - Enterprise Edition']")))
    driver.switch_to.frame(iframe_element)
    time.sleep(1)

    rows = driver.find_elements(By.XPATH, "/html/body/div[3]/div/div/div[2]/table/tbody/tr")

    target_name = "Dakota Marketplace for Salesforce"  # Replace with the actual name you're searching for

    for index, row in enumerate(rows, start=1):  # Loop through each row
        try:
            # Construct dynamic XPath for the name in the current row
            name_xpath = f"/html/body/div[3]/div/div/div[2]/table/tbody/tr[{index}]/th[1]/a[1]"
            name_element = driver.find_element(By.XPATH, name_xpath)
            print(f"{index}, {name_element.text}")

            if name_element.text.strip() == target_name:
                # Click the found name element
                print(f"Package is present with following name '{name_element.text}'.")

                # Construct dynamic XPath for another element in the same row
                element_xpath = f"/html/body/div[3]/div/div/div[2]/table/tbody/tr[{index}]/td[1]/a[1]"
                another_element = driver.find_element(By.XPATH, element_xpath)

                # Click on the found element in the same row
                print(another_element.text)
                another_element.click()
                break  # Exit loop once found
        except:
            pass
    driver.switch_to.default_content()
    time.sleep(1)


    # Switch to iframe
    iframe_element = wait.until(EC.element_to_be_clickable((By.XPATH,"//iframe[@title='Uninstalling a Package ~ Salesforce - Enterprise Edition']")))
    driver.switch_to.frame(iframe_element)
    time.sleep(1)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='p5']")))
    btn.click()
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='save']")))
    btn.click()
    time.sleep(10)

    driver.switch_to.default_content()
    time.sleep(1)

    # Switch to iframe
    iframe_element = wait.until(EC.element_to_be_clickable((By.XPATH,"//iframe[contains(@title,'Installed Packages ~ Salesforce - Enterprise Edition')]")))
    driver.switch_to.frame(iframe_element)
    time.sleep(1)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    uninstalled_status = wait.until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr[2]/td[5]")))
    print(uninstalled_status.text)
    driver.switch_to.default_content()
    time.sleep(100)

    driver.refresh()
    time.sleep(5)

    # Switch to iframe
    iframe_element = wait.until(EC.element_to_be_clickable((By.XPATH,"//iframe[contains(@title,'Installed Packages ~ Salesforce - Enterprise Edition')]")))
    driver.switch_to.frame(iframe_element)
    time.sleep(1)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    uninstalled_status = wait.until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr[2]/td[5]")))
    print(uninstalled_status.text)

    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Del']")))
    btn.click()
    time.sleep(2)

    alert_app = driver.switch_to.alert
    alert_app.accept()
    time.sleep(3)