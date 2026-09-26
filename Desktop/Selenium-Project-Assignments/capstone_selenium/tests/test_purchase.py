"""
test_purchase.py
-----------------
Capstone Assignment 1: Automate an E-Commerce Web Application using
Selenium WebDriver with Python.

Business scenario: a customer wants to purchase a product from an
e-commerce site. This suite drives the flow all the way to a confirmed
order (not just an item sitting in the cart), against
https://automationexercise.com, using test data read from JSON (or
Excel -- see utils/data_reader.py):

  1.  Launch browser                 -> driver fixture (conftest.py)
  2.  Login to application           -> LoginPage.ensure_logged_in()
  3.  Search product                 -> ProductsPage.search_product()
  4.  Add product to cart            -> ProductsPage.add_to_cart()
  5.  Update quantity                -> ProductsPage.set_quantity()
  6.  Verify cart details            -> CartPage.get_cart_line_items()
  7.  Capture screenshots            -> utils/screenshot_helper.py
  8.  Read test data from Excel/JSON -> utils/data_reader.py
  9.  Handle popup/alerts            -> BasePage / ProductsPage modal helpers
  10. Generate execution report      -> reports/report.html (pytest-html,
                                         with every screenshot embedded
                                         via the built-in `extras` fixture)

Beyond the 10 required steps, the flow also completes checkout and
payment and asserts the order confirmation screen, so the automation
proves an actual completed purchase rather than stopping at "item added
to cart".
"""

import os
import sys

import pytest
import pytest_html.extras as html_extras
import base64

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.data_reader import get_payment_data, get_test_cases, get_user_data
from utils.driver_factory import load_config
from utils.screenshot_helper import capture_screenshot

CONFIG = load_config()
SCREENSHOT_DIR = os.path.join(
    os.path.dirname(__file__), "..", CONFIG.get("screenshot_dir", "screenshots")
)

# Data-driven: one full purchase flow per row in data/test_data.json (or .xlsx)
TEST_CASES = get_test_cases(source="json")
USER = get_user_data()
PAYMENT = get_payment_data()


@pytest.mark.parametrize(
    "case",
    TEST_CASES,
    ids=[c["case_id"] for c in TEST_CASES],
)
def test_purchase_flow(driver, case, extras):
    """`extras` is provided by pytest-html: appending to it embeds each
    image directly into reports/report.html (saved under reports/assets/)."""
    captured = []  # (label, screenshot_path) for this test run

    def step(name, action):
        action()
        shot = capture_screenshot(driver, f"{case['case_id']}_{name}", SCREENSHOT_DIR)
        captured.append((name.replace("_", " "), shot))

    home = HomePage(driver)
    login_page = LoginPage(driver)
    products_page = ProductsPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    try:
        # 1. Launch browser (done by the `driver` fixture) + open the site
        step("01_launch_browser_and_open_site", home.load)
        assert home.is_loaded(), "Home page did not load"

        # 2. Login to application (auto-signs-up on first run)
        def do_login():
            home.go_to_login()
            login_page.ensure_logged_in(USER)
            home.accept_alert_if_present()  # requirement #9

        step("02_login_to_application", do_login)
        assert home.is_logged_in(), "Login/registration did not succeed"

        # 3. Search product
        def do_search():
            home.go_to_products()
            products_page.search_product(case["search_term"])

        step("03_search_product", do_search)
        assert products_page.is_search_results_shown(), "Search results not shown"

        # 4 & 5. Open the first search result, update quantity, add to cart
        def do_add_with_quantity():
            products_page.open_first_product_detail()
            products_page.set_quantity(case["quantity"])
            products_page.add_to_cart()

        step("04_update_quantity_and_add_to_cart", do_add_with_quantity)

        # 9. Handle popup/alerts: dismiss the 'Added!' modal, then use the
        # header's Cart link to view it
        def do_go_to_cart():
            products_page.dismiss_added_to_cart_modal()
            home.go_to_cart()

        step("05_handle_popup_and_view_cart", do_go_to_cart)

        # 6. Verify cart details
        cart_items = []

        def do_verify_cart():
            nonlocal cart_items
            cart_items = cart_page.get_cart_line_items()

        step("06_verify_cart_details", do_verify_cart)

        assert len(cart_items) > 0, "Cart is empty after adding a product"
        added_item = cart_items[-1]
        assert case["quantity"] in added_item["quantity"], (
            f"Expected quantity {case['quantity']} but cart shows "
            f"{added_item['quantity']}"
        )

        # Beyond the 10 required steps: complete an actual purchase.
        def do_checkout():
            cart_page.proceed_to_checkout()
            checkout_page.add_order_comment(PAYMENT["order_comment"])
            checkout_page.place_order()

        step("07_proceed_to_checkout", do_checkout)

        def do_pay():
            checkout_page.fill_payment_details(PAYMENT)
            checkout_page.pay_and_confirm_order()

        step("08_enter_payment_details", do_pay)

        assert checkout_page.is_order_placed(), "Order confirmation was not shown"

        # A distinctly named screenshot marking the successful purchase
        success_shot = capture_screenshot(driver, "purchase_success", SCREENSHOT_DIR)
        captured.append(("Purchase Success", success_shot))

    except Exception:
        try:
            fail_shot = capture_screenshot(
                driver, f"FAILURE_{case['case_id']}", SCREENSHOT_DIR
            )
            captured.append(("Failure", fail_shot))
        except Exception:
            pass
        raise

    finally:
        # 10. Embed every screenshot from this run into the pytest-html report
        for label, path in captured:
            try:
                with open(path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode("ascii")
                extras.append(html_extras.image(b64, name=label))
            except Exception:
                pass
