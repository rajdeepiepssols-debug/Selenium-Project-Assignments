from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")
start_button = driver.find_element(By.XPATH, "//button[text()='Start']")
start_button.click()
wait = WebDriverWait(driver, 10)

text_element = wait.until(
    EC.visibility_of_element_located((By.ID, "finish"))
)
text = text_element.text

print("Dynamic text:", text)
driver.quit()