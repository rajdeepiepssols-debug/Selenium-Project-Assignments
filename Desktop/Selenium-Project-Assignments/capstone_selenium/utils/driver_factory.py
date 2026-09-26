"""
driver_factory.py
------------------
Centralized WebDriver creation so tests never hard-code browser setup.
Reads browser choice / headless flag / timeouts from config/config.json.
"""

import json
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "config.json")


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_driver(config: dict = None):
    """
    Build and return a configured WebDriver instance based on config.json.
    Supports chrome (default) and firefox, headless or headed.
    """
    config = config or load_config()
    browser = config.get("browser", "chrome").lower()
    headless = config.get("headless", False)

    if browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    else:
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-translate")
        # Interact as soon as the DOM is ready rather than waiting for every
        # ad/tracking script on the page to finish loading.
        options.page_load_strategy = "eager"
        # NOTE: intentionally NOT disabling Chrome's popup blocker -- this
        # site's ad network likes to spawn popup/redirect windows, and the
        # built-in blocker stops most of them before they ever open.
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option(
            "prefs",
            {
                "profile.default_content_setting_values.popups": 2,  # 2 = block
                "profile.default_content_setting_values.notifications": 2,
                "profile.managed_default_content_settings.popups": 2,
            },
        )
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    driver.implicitly_wait(config.get("implicit_wait", 10))
    if not headless:
        driver.maximize_window()

    # Remember the one legitimate window so we can recover if an ad
    # manages to spawn an extra one anyway (see BasePage.close_extra_windows).
    driver.main_window_handle = driver.current_window_handle

    return driver
