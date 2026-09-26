from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    CART_ROWS = (By.CSS_SELECTOR, "#cart_info_table tbody tr")
    ROW_DESCRIPTION = (By.CSS_SELECTOR, ".cart_description h4 a")
    ROW_PRICE = (By.CSS_SELECTOR, ".cart_price p")
    ROW_QUANTITY_INPUT = (By.CSS_SELECTOR, ".cart_quantity_input")
    ROW_TOTAL = (By.CSS_SELECTOR, ".cart_total_price")
    EMPTY_CART_MSG = (By.XPATH, "//b[contains(text(),'Cart is empty')]")
    PROCEED_TO_CHECKOUT_BUTTON = (By.XPATH, "//a[contains(text(),'Proceed To Checkout')]")

    def get_cart_line_items(self) -> list:
        """
        Satisfies capstone requirement #6: 'Verify cart details'.
        Returns a list of dicts: [{name, price, quantity, total}, ...]
        """
        items = []
        rows = self.find_all(self.CART_ROWS)
        for row in rows:
            try:
                name = row.find_element(*self.ROW_DESCRIPTION).text
                price = row.find_element(*self.ROW_PRICE).text
                # .cart_quantity_input is an <input> -- .text is always "" for
                # inputs, the actual displayed number lives in the value attribute
                quantity = row.find_element(*self.ROW_QUANTITY_INPUT).get_attribute("value")
                total = row.find_element(*self.ROW_TOTAL).text
                items.append(
                    {"name": name, "price": price, "quantity": quantity, "total": total}
                )
            except Exception:
                continue
        return items

    def is_cart_empty(self) -> bool:
        return self.is_visible(self.EMPTY_CART_MSG, timeout=3)

    def proceed_to_checkout(self):
        """Moves from the cart into the actual purchase/checkout flow."""
        self.click(self.PROCEED_TO_CHECKOUT_BUTTON)
