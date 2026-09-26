from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HomePage(BasePage):
    URL = "https://automationexercise.com/"

    SIGNUP_LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/login']")
    LOGGED_IN_AS = (By.XPATH, "//a[contains(text(),'Logged in as')]")
    PRODUCTS_LINK = (By.CSS_SELECTOR, "a[href='/products']")
    CART_LINK = (By.CSS_SELECTOR, "a[href='/view_cart']")

    def load(self):
        self.driver.get(self.URL)
        self.dismiss_cookie_consent_if_present()

    def is_loaded(self) -> bool:
        return "Automation Exercise" in self.driver.title

    def go_to_login(self):
        self.click(self.SIGNUP_LOGIN_LINK)

    def go_to_products(self):
        self.click(self.PRODUCTS_LINK)

    def go_to_cart(self):
        self.click(self.CART_LINK)

    def is_logged_in(self) -> bool:
        return self.is_visible(self.LOGGED_IN_AS, timeout=5)
