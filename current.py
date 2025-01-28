import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)
print("Successfully open the Chrome")

# Open the Salesforce URL
driver.get("https://dakotanetworks--sand2024.sandbox.lightning.force.com/lightning/n/Marketplace__Investments")
print("Successfully open the Salesforce")

# Log in
wait = WebDriverWait(driver, 10)
username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
username.clear()
mailto:username.send_keys("draftsf@draftdata.com.sand2024")

password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
password.clear()
password.send_keys("LOWYqfakgQ8oo")

login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
login_button.click()

# Wait for page to load
time.sleep(5)
print("Successfully login to salesforce")

# Locate and click "Marketplace Search"
marketplace_search = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='slds-truncate' and text()='Marketplace Search']")))
driver.execute_script("arguments[0].click();", marketplace_search)
print("Successfully clicked on Marketplace Search")
time.sleep(15)


# Select Display Criteria (Linked Account)
criteria_dropdown = driver.find_element(By.XPATH, "(//select[@name='DisplayCriteria'])")
dropdown_option = Select(criteria_dropdown)
dropdown_option.select_by_visible_text("Linked Accounts")

# click on search button
button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
button.click()
time.sleep(10)

# Find the element and Verify
sag_element = driver.find_elements(By.XPATH, "//tbody/tr[1]/th[1]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-icon[1]/span[1]/lightning-primitive-icon[1]//*[name()='svg']")

if sag_element:
    assert True, "Element found"
else:
    assert False, "Test case failed: Element not found"
time.sleep(2)

# Select Display Criteria (Unlinked Account)
criteria_dropdown = driver.find_element(By.XPATH, "(//select[@name='DisplayCriteria'])")
dropdown_option = Select(criteria_dropdown)
dropdown_option.select_by_visible_text("Unlinked Accounts")

# click on search button
button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
button.click()
time.sleep(10)

# Find the element and Verify
sag_element = driver.find_elements(By.XPATH, "//tbody/tr[1]/th[1]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-icon[1]/span[1]/lightning-primitive-icon[1]//*[name()='svg']")

if sag_element:
    assert False, "Element not found"
else:
    assert True, "Test case failed: Element found"
time.sleep(2)

driver.quit()
