"""
checkout_page.py
-----------------
Covers the two screens that come after 'Proceed To Checkout':

  1. /checkout    -- review delivery/billing address and cart, add an
                      optional order comment, click 'Place Order'
  2. /payment     -- enter (dummy/test) card details and confirm payment

This is what actually completes the business scenario ("a customer wants
to purchase a product") end to end, rather than stopping at the cart.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    # --- /checkout ---
    ADDRESS_DELIVERY = (By.ID, "address_delivery")
    ORDER_COMMENT = (By.CSS_SELECTOR, "textarea[name='message']")
    PLACE_ORDER_BUTTON = (By.XPATH, "//a[contains(text(),'Place Order')]")

    # --- /payment ---
    NAME_ON_CARD = (By.CSS_SELECTOR, "input[data-qa='name-on-card']")
    CARD_NUMBER = (By.CSS_SELECTOR, "input[data-qa='card-number']")
    CVC = (By.CSS_SELECTOR, "input[data-qa='cvc']")
    EXPIRY_MONTH = (By.CSS_SELECTOR, "input[data-qa='expiry-month']")
    EXPIRY_YEAR = (By.CSS_SELECTOR, "input[data-qa='expiry-year']")
    PAY_BUTTON = (By.CSS_SELECTOR, "button[data-qa='pay-button']")

    # --- Order confirmation ---
    ORDER_PLACED_HEADER = (By.CSS_SELECTOR, "h2[data-qa='order-placed']")
    DOWNLOAD_INVOICE_LINK = (By.XPATH, "//a[contains(text(),'Download Invoice')]")
    CONTINUE_BUTTON = (By.XPATH, "//a[contains(text(),'Continue')]")

    def get_delivery_address_text(self) -> str:
        return self.get_text(self.ADDRESS_DELIVERY)

    def add_order_comment(self, comment: str):
        self.type_text(self.ORDER_COMMENT, comment)

    def place_order(self):
        self.click(self.PLACE_ORDER_BUTTON)

    def fill_payment_details(self, payment: dict):
        self.type_text(self.NAME_ON_CARD, payment["name_on_card"])
        self.type_text(self.CARD_NUMBER, payment["card_number"])
        self.type_text(self.CVC, payment["cvc"])
        self.type_text(self.EXPIRY_MONTH, payment["expiry_month"])
        self.type_text(self.EXPIRY_YEAR, payment["expiry_year"])

    def pay_and_confirm_order(self):
        self.click(self.PAY_BUTTON)

    def is_order_placed(self) -> bool:
        return self.is_visible(self.ORDER_PLACED_HEADER, timeout=10)

    def is_invoice_downloadable(self) -> bool:
        return self.is_visible(self.DOWNLOAD_INVOICE_LINK, timeout=5)

    def continue_after_order(self):
        self.click(self.CONTINUE_BUTTON)
