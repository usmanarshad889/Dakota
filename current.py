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
time.sleep(3)
print("Successfully login to salesforce")

# Navigate to Marketplace Search
driver.get("https://dakotanetworks--sand2024.sandbox.lightning.force.com/lightning/n/Marketplace__Dakota_Search")
time.sleep(15)

# Navigate to Contacts Tab
driver.find_element(By.XPATH, "//li[@title='Contacts']").click()
time.sleep(7)

# Click on Search Button
driver.find_element(By.XPATH,
                    "//div[contains(@class,'filterInnerDiv')]//button[contains(@title,'Search')][normalize-space()='Search']").click()
time.sleep(5)

# Copy the Contact Name text
contact_name = driver.find_element(By.XPATH,
                                   "//body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/article[1]/div[2]/p[1]/div[1]/div[1]/div[1]/lightning-datatable[1]/div[2]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[2]")
contact_name_text = contact_name.text

# Search Account name
driver.find_element(By.XPATH, "(//input[@placeholder='Contact Name'])").send_keys(contact_name_text)
time.sleep(1)

# Click on Search Button
driver.find_element(By.XPATH,
                    "//div[contains(@class,'filterInnerDiv')]//button[contains(@title,'Search')][normalize-space()='Search']").click()
time.sleep(5)

# Copy the Search Contact Name text
contact_name = driver.find_element(By.XPATH,
                                   "//body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/article[1]/div[2]/p[1]/div[1]/div[1]/div[1]/lightning-datatable[1]/div[2]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[2]")
search_contact_name_text = contact_name.text

if contact_name_text == search_contact_name_text:
    assert True
else:
    assert False
