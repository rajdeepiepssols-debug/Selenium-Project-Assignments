from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/tables")

rows = driver.find_elements(By.XPATH, "//table[@id='table1']/tbody/tr")

for row in rows:
    columns = row.find_elements(By.TAG_NAME, "td")
    if columns[1].text == "Frank":
        print("Name:", columns[1].text)
        print("Status:", columns[4].text)
        break

driver.quit()