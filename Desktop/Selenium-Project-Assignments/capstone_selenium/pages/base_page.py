"""
base_page.py
------------
Common functionality shared by every page object: explicit waits,
element interaction wrappers, and alert/popup handling
(capstone requirement #9: "Handle popup/alerts if available").
"""

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoAlertPresentException,
    NoSuchWindowException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ---------- Waits ----------
    def find(self, locator: tuple):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_clickable(self, locator: tuple):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def find_all(self, locator: tuple):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def is_visible(self, locator: tuple, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    # ---------- Actions ----------
    def safe_click(self, element):
        """
        Clicks a WebElement, falling back to a JS-dispatched click if a
        normal click is intercepted -- this site's ad iframes frequently
        sit on top of real elements and would otherwise block the click.
        """
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", element
            )
            self.driver.execute_script("arguments[0].click();", element)

    def click(self, locator: tuple):
        self.safe_click(self.find_clickable(locator))

    def type_text(self, locator: tuple, text: str):
        el = self.find(locator)
        el.clear()
        el.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        return self.find(locator).text

    def scroll_to(self, locator: tuple):
        el = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        return el

    # ---------- Alerts / popups ----------
    def accept_alert_if_present(self, timeout: int = 3) -> bool:
        """
        Handles native JS alerts (window.alert/confirm). Returns True if an
        alert was found and accepted, False if none appeared.
        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            return True
        except (TimeoutException, NoAlertPresentException):
            return False

    def dismiss_cookie_consent_if_present(self):
        """
        automationexercise.com occasionally shows a GDPR-style consent banner
        injected by an ad/consent script. This is a defensive no-op if it's
        not present, and closes it if it is.
        """
        consent_locators = [
            (By.ID, "accept-btn"),
            (By.CSS_SELECTOR, "button[aria-label='Consent']"),
            (By.CSS_SELECTOR, ".fc-cta-consent"),
        ]
        for locator in consent_locators:
            if self.is_visible(locator, timeout=3):
                try:
                    self.click(locator)
                    return True
                except Exception:
                    continue
        return False

    def close_modal_if_present(self, modal_locator: tuple, close_button_locator: tuple):
        """Generic helper for Bootstrap-style modals (e.g. 'Added!' cart modal)."""
        if self.is_visible(modal_locator, timeout=5):
            self.click(close_button_locator)
            return True
        return False

    def close_extra_windows(self):
        """
        Ad networks on this site occasionally spawn an extra popup/redirect
        window. If one appears, close it and switch focus back to the
        original window so the test doesn't lose track of the real page.
        Safe to call after every step even when nothing popped up.
        """
        main_handle = getattr(self.driver, "main_window_handle", None)
        if not main_handle:
            return
        try:
            handles = self.driver.window_handles
        except NoSuchWindowException:
            return
        if len(handles) <= 1:
            return
        for handle in handles:
            if handle != main_handle:
                try:
                    self.driver.switch_to.window(handle)
                    self.driver.close()
                except NoSuchWindowException:
                    pass
        try:
            self.driver.switch_to.window(main_handle)
        except NoSuchWindowException:
            pass
