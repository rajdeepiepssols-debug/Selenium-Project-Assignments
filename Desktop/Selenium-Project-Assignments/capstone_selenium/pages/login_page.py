from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class LoginPage(BasePage):
    # --- Login form ---
    LOGIN_EMAIL = (By.CSS_SELECTOR, "input[data-qa='login-email']")
    LOGIN_PASSWORD = (By.CSS_SELECTOR, "input[data-qa='login-password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-qa='login-button']")
    LOGIN_ERROR = (By.XPATH, "//p[contains(text(),'incorrect')]")

    # --- Signup form (name/email) ---
    SIGNUP_NAME = (By.CSS_SELECTOR, "input[data-qa='signup-name']")
    SIGNUP_EMAIL = (By.CSS_SELECTOR, "input[data-qa='signup-email']")
    SIGNUP_BUTTON = (By.CSS_SELECTOR, "button[data-qa='signup-button']")
    SIGNUP_ERROR = (By.XPATH, "//p[contains(text(),'Email Address already exist')]")

    # --- Account information form ---
    TITLE_MR = (By.ID, "id_gender1")
    TITLE_MRS = (By.ID, "id_gender2")
    ACCOUNT_PASSWORD = (By.ID, "password")
    DAYS = (By.ID, "days")
    MONTHS = (By.ID, "months")
    YEARS = (By.ID, "years")
    FIRST_NAME = (By.ID, "first_name")
    LAST_NAME = (By.ID, "last_name")
    ADDRESS1 = (By.ID, "address1")
    COUNTRY = (By.ID, "country")
    STATE = (By.ID, "state")
    CITY = (By.ID, "city")
    ZIPCODE = (By.ID, "zipcode")
    MOBILE_NUMBER = (By.ID, "mobile_number")
    CREATE_ACCOUNT_BUTTON = (By.CSS_SELECTOR, "button[data-qa='create-account']")

    ACCOUNT_CREATED = (By.CSS_SELECTOR, "h2[data-qa='account-created']")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "a[data-qa='continue-button']")

    def login(self, email: str, password: str):
        self.type_text(self.LOGIN_EMAIL, email)
        self.type_text(self.LOGIN_PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def login_failed(self) -> bool:
        return self.is_visible(self.LOGIN_ERROR, timeout=4)

    def start_signup(self, name: str, email: str):
        self.type_text(self.SIGNUP_NAME, name)
        self.type_text(self.SIGNUP_EMAIL, email)
        self.click(self.SIGNUP_BUTTON)

    def signup_email_taken(self) -> bool:
        return self.is_visible(self.SIGNUP_ERROR, timeout=4)

    def complete_account_info(self, user: dict):
        """Fills the 'ENTER ACCOUNT INFORMATION' page shown after signup."""
        if user.get("title", "Mr") == "Mr":
            self.click(self.TITLE_MR)
        else:
            self.click(self.TITLE_MRS)

        self.type_text(self.ACCOUNT_PASSWORD, user["password"])
        Select(self.find(self.DAYS)).select_by_visible_text(user["birth_date"])
        Select(self.find(self.MONTHS)).select_by_visible_text(user["birth_month"])
        Select(self.find(self.YEARS)).select_by_visible_text(user["birth_year"])

        self.type_text(self.FIRST_NAME, user["first_name"])
        self.type_text(self.LAST_NAME, user["last_name"])
        self.type_text(self.ADDRESS1, user["address"])
        Select(self.find(self.COUNTRY)).select_by_visible_text(user["country"])
        self.type_text(self.STATE, user["state"])
        self.type_text(self.CITY, user["city"])
        self.type_text(self.ZIPCODE, user["zipcode"])
        self.type_text(self.MOBILE_NUMBER, user["mobile_number"])

        self.click(self.CREATE_ACCOUNT_BUTTON)

    def is_account_created(self) -> bool:
        return self.is_visible(self.ACCOUNT_CREATED, timeout=8)

    def continue_after_account_created(self):
        self.click(self.CONTINUE_BUTTON)

    def ensure_logged_in(self, user: dict):
        """
        Full login-with-signup-fallback flow: tries logging in with the given
        credentials; if the account does not exist yet, signs it up on the fly.
        Satisfies capstone requirement #2 ("Login to application") in a way
        that is repeatable across fresh test runs.
        """
        self.login(user["email"], user["password"])

        if self.login_failed():
            self.type_text(self.SIGNUP_NAME, user["name"])
            self.type_text(self.SIGNUP_EMAIL, user["email"])
            self.click(self.SIGNUP_BUTTON)

            if self.is_visible(self.ACCOUNT_PASSWORD, timeout=8):
                self.complete_account_info(user)
                if self.is_account_created():
                    self.continue_after_account_created()
