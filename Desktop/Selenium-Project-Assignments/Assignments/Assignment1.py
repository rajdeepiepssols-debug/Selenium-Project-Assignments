from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.saucedemo.com/")

username = driver.find_element(By.ID, "user-name")
username.send_keys("standard_user")

password = driver.find_element(By.NAME, "password")
password.send_keys("secret_sauce")

login_button = driver.find_element(By.XPATH, "//input[@type='submit']")
login_button.click()
assert "/inventory.html" in driver.current_url

print("Login successful!")
print("Current URL:", driver.current_url)
driver.quit()