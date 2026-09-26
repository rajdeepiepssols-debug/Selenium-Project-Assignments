from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/javascript_alerts")

driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']").click()
alert = driver.switch_to.alert
alert.accept()

driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']").click()
alert = driver.switch_to.alert
alert.dismiss()

driver.find_element(By.XPATH, "//button[text()='Click for JS Prompt']").click()
alert = driver.switch_to.alert
alert.send_keys("Hello Selenium")
alert.accept()

print(driver.find_element(By.ID, "result").text)

driver.quit()