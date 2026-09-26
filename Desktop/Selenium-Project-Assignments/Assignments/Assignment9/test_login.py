from selenium.webdriver.common.by import By

def test_valid_login(driver):
    driver.get("https://www.saucedemo.com/")

    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.NAME, "password").send_keys("secret_sauce")
    driver.find_element(By.XPATH, "//input[@type='submit']").click()

    assert "/inventory.html" in driver.current_url


def test_invalid_login(driver):
    driver.get("https://www.saucedemo.com/")

    driver.find_element(By.ID, "user-name").send_keys("wrong_user")
    driver.find_element(By.NAME, "password").send_keys("wrong_password")
    driver.find_element(By.XPATH, "//input[@type='submit']").click()

    error = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
    assert error.is_displayed()