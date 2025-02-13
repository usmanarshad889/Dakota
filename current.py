import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)

driver.get("https://dakotanetworks--fuseupgrad.sandbox.my.salesforce-setup.com/")

wait = WebDriverWait(driver, 20)
username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
username.send_keys("draftsf@draftdata.com.fuseupgrad")
password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
password.send_keys("LOWYqfakgQ8oo")
login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
login_button.click()

btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[@class='slds-tabs_default__link'])[1]")))
print(btn.text)
print("")

xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/marketplace-dakota-home-page-main[1]/div[1]/div[1]/div[1]/c-dakota-contact-updates[1]/div[1]/lightning-tabset[1]/div[1]/slot[1]/lightning-tab[1]/slot[1]/c-dakota-job-and-role-changes[1]/div[1]/div[1]/c-custom-datatable[1]/div[2]/div[1]/div[1]/table[1]/tbody[1]/tr/td[2]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-primitive-custom-cell[1]/c-custom-link-field[1]/lightning-button[1]/button[1]'''
all_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

for element in all_elements:
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(1)
    element.click()
    break
