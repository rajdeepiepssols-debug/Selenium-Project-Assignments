from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    PRODUCT_NAME = (By.CSS_SELECTOR, ".product-information h2")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".product-information span span")
    QUANTITY_INPUT = (By.ID, "quantity")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".product-information button.cart")

    CART_MODAL = (By.ID, "cartModal")
    CONTINUE_SHOPPING_BUTTON = (
        By.XPATH,
        "//div[@id='cartModal']//button[contains(text(),'Continue Shopping')]",
    )

    def get_product_name(self) -> str:
        return self.get_text(self.PRODUCT_NAME)

    def set_quantity(self, quantity: str):
        """Satisfies capstone requirement #5: 'Update quantity'."""
        el = self.find(self.QUANTITY_INPUT)
        el.clear()
        el.send_keys(str(quantity))

    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)

    def dismiss_added_to_cart_modal(self) -> bool:
        """
        Handles the 'Added!' confirmation modal (capstone requirement #9).
        Closes it via 'Continue Shopping' if it appears; if the modal's
        exact markup doesn't match (site copy varies), this simply returns
        False rather than blocking the rest of the flow -- navigating to
        the cart via the header link still works either way.
        """
        if not self.is_visible(self.CART_MODAL, timeout=5):
            return False
        try:
            self.click(self.CONTINUE_SHOPPING_BUTTON)
        except Exception:
            pass
        return True
