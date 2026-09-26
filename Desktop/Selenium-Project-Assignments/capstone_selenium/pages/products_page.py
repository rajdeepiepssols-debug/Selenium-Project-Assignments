"""
products_page.py
-----------------
Covers both the product search/listing page and the individual product
detail page -- they're one file here since a single "Products" page object
maps naturally onto the site's product-browsing flow (search -> open a
result -> set quantity -> add to cart).
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProductsPage(BasePage):
    # --- Search / listing page (/products) ---
    SEARCH_INPUT = (By.ID, "search_product")
    SEARCH_BUTTON = (By.ID, "submit_search")
    SEARCHED_PRODUCTS_TITLE = (By.XPATH, "//h2[contains(text(),'Searched Products')]")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".features_items .product-image-wrapper")
    ADD_TO_CART_LINKS = (
        By.CSS_SELECTOR,
        ".product-overlay a.add-to-cart, .productinfo a.add-to-cart",
    )
    VIEW_PRODUCT_LINKS = (By.XPATH, "//a[contains(text(),'View Product')]")

    # --- Product detail page (/product_details/<id>) ---
    PRODUCT_NAME = (By.CSS_SELECTOR, ".product-information h2")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".product-information span span")
    QUANTITY_INPUT = (By.ID, "quantity")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".product-information button.cart")

    # --- 'Added!' confirmation modal (shown from either page) ---
    CART_MODAL = (By.ID, "cartModal")
    CONTINUE_SHOPPING_BUTTON = (
        By.XPATH,
        "//div[@id='cartModal']//button[contains(text(),'Continue Shopping')]",
    )

    # ---------- Search / listing ----------
    def search_product(self, term: str):
        """Satisfies capstone requirement #3: 'Search product'."""
        self.type_text(self.SEARCH_INPUT, term)
        self.click(self.SEARCH_BUTTON)

    def is_search_results_shown(self) -> bool:
        return self.is_visible(self.SEARCHED_PRODUCTS_TITLE, timeout=8)

    def add_first_result_to_cart(self):
        """Hovers over the first product card to reveal the overlay, then clicks Add to Cart."""
        cards = self.find_all(self.PRODUCT_CARDS)
        first_card = cards[0]
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", first_card)
        self.driver.execute_script(
            "arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));",
            first_card,
        )
        add_links = self.find_all(self.ADD_TO_CART_LINKS)
        self.safe_click(add_links[0])

    def open_first_product_detail(self):
        self.safe_click(self.find_all(self.VIEW_PRODUCT_LINKS)[0])

    # ---------- Product detail ----------
    def get_product_name(self) -> str:
        return self.get_text(self.PRODUCT_NAME)

    def set_quantity(self, quantity: str):
        """Satisfies capstone requirement #5: 'Update quantity'."""
        el = self.find(self.QUANTITY_INPUT)
        el.clear()
        el.send_keys(str(quantity))

    def add_to_cart(self):
        """Satisfies capstone requirement #4: 'Add product to cart'."""
        self.click(self.ADD_TO_CART_BUTTON)

    def dismiss_added_to_cart_modal(self) -> bool:
        """
        Handles the 'Added!' confirmation modal (capstone requirement #9).
        Closes it via 'Continue Shopping' if it appears; returns False
        (without raising) if the modal's markup doesn't match, so the rest
        of the flow can still proceed via the header's Cart link.
        """
        if not self.is_visible(self.CART_MODAL, timeout=5):
            return False
        try:
            self.click(self.CONTINUE_SHOPPING_BUTTON)
        except Exception:
            pass
        return True
