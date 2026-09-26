from selenium import webdriver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

driver = webdriver.Chrome()
driver.get("https://www.saucedemo.com/")

login_page = LoginPage(driver)
login_page.login("standard_user", "secret_sauce")

inventory_page = InventoryPage(driver)

assert "/inventory.html" in inventory_page.get_url()

driver.quit()