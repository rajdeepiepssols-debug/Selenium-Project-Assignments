"""
test_ecommerce_flow.py
-----------------------
Capstone Assignment 1: Automate an E-Commerce Web Application using
Selenium WebDriver with Python.

Business scenario: a customer wants to purchase a product.
This suite implements all 10 required steps end to end, driven by
test data read from JSON (or Excel -- see utils/data_reader.py):

  1. Launch browser                 -> driver fixture (conftest.py)
  2. Login to application           -> LoginPage.ensure_logged_in()
  3. Search product                 -> ProductsPage.search_product()
  4. Add product to cart            -> ProductDetailPage.add_to_cart()
  5. Update quantity                -> ProductDetailPage.set_quantity()
  6. Verify cart details            -> CartPage.get_cart_line_items()
  7. Capture screenshots            -> utils/screenshot_helper.py
  8. Read test data from Excel/JSON -> utils/data_reader.py
  9. Handle popup/alerts            -> BasePage alert/modal helpers
  10. Generate execution report     -> utils/report_generator.py
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_detail_page import ProductDetailPage
from pages.products_page import ProductsPage
from utils.data_reader import get_test_cases, get_user_data
from utils.driver_factory import load_config
from utils.report_generator import ExecutionReport
from utils.screenshot_helper import capture_screenshot

CONFIG = load_config()
SCREENSHOT_DIR = os.path.join(
    os.path.dirname(__file__), "..", CONFIG.get("screenshot_dir", "screenshots")
)

# Data-driven: one full purchase flow per row in test_data.json / test_data.xlsx
TEST_CASES = get_test_cases(source="json")
USER = get_user_data()


@pytest.mark.parametrize(
    "case",
    TEST_CASES,
    ids=[c["case_id"] for c in TEST_CASES],
)
def test_ecommerce_purchase_flow(driver, case):
    report = ExecutionReport(case_id=case["case_id"])

    def step(name, action, status="PASS"):
        """Runs one automation step, screenshots it, and logs it to the report."""
        action()
        # Guard against ad popups stealing window focus mid-flow (requirement #9)
        BasePage(driver).close_extra_windows()
        shot = capture_screenshot(driver, f"{case['case_id']}_{name}", SCREENSHOT_DIR)
        report.log_step(name, status, shot)

    try:
        home = HomePage(driver)
        login_page = LoginPage(driver)
        products_page = ProductsPage(driver)
        product_detail = ProductDetailPage(driver)
        cart_page = CartPage(driver)

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
            product_detail.set_quantity(case["quantity"])
            product_detail.add_to_cart()
            driver.switch_to.default_content()

        step("04_add_product_to_cart", do_add_with_quantity)

        # 9. Handle popup/alerts: dismiss the 'Added!' modal, then use the
        # header's Cart link (already proven reliable during login) to view it
        def do_go_to_cart():
            product_detail.dismiss_added_to_cart_modal()
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

    except Exception:
        capture_screenshot(driver, f"{case['case_id']}_UNEXPECTED_FAILURE", SCREENSHOT_DIR)
        report.log_step("unexpected_failure", "FAIL")
        raise
    finally:
        # 10. Generate execution report
        report_path = report.render()
        print(f"\nExecution report for {case['case_id']}: {report_path}")
