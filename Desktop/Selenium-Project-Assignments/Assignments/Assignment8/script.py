import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

with open("login_data.csv", newline="") as file:
    test_data = list(csv.DictReader(file))

for data in test_data:
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")

    driver.find_element(By.ID, "user-name").send_keys(data["username"])
    driver.find_element(By.NAME, "password").send_keys(data["password"])
    driver.find_element(By.XPATH, "//input[@type='submit']").click()

    if data["expected"] == "success":
        assert "/inventory.html" in driver.current_url
    else:
        error = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
        assert error.is_displayed()

    driver.quit()