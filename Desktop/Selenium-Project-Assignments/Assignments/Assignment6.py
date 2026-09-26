from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/iframe")

driver.switch_to.frame("mce_0_ifr")

body = driver.find_element(By.ID, "tinymce")
body.clear()
body.send_keys("Hello Selenium")

driver.switch_to.default_content()

driver.get("https://the-internet.herokuapp.com/windows")

main_window = driver.current_window_handle

driver.find_element(By.LINK_TEXT, "Click Here").click()

windows = driver.window_handles

for window in windows:
    if window != main_window:
        driver.switch_to.window(window)
        print("New Tab Title:", driver.title)
        driver.close()
        break

driver.switch_to.window(main_window)

print("Main Window Title:", driver.title)

driver.quit()