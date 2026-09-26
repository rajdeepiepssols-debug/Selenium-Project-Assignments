from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://demoqa.com/automation-practice-form")

checkbox1 = driver.find_element(By.ID, "hobbies-checkbox-1")
checkbox2 = driver.find_element(By.ID, "hobbies-checkbox-2")

if not checkbox1.is_selected():
    checkbox1.click()

if not checkbox2.is_selected():
    checkbox2.click()

assert checkbox1.is_selected()
assert checkbox2.is_selected()

city = driver.find_element(By.ID, "react-select-4-input")
city.send_keys("NCR")

wait = WebDriverWait(driver, 10)
options = wait.until(
    EC.visibility_of_all_elements_located(
        (By.XPATH, "//div[contains(@id,'react-select-4-option')]")
    )
)

for option in options:
    if option.text == "NCR":
        option.click()
        break

driver.quit()