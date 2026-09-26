# Capstone Assignment 1 — E-Commerce Purchase Automation with Selenium WebDriver + Python

Automates a full **customer purchase** on [automationexercise.com](https://automationexercise.com)
— login, search, add to cart, quantity update, cart verification, checkout,
payment, and order confirmation — using **Selenium WebDriver**, **Python**,
and **pytest**, with a Page Object Model, data-driven test cases, and a
single consolidated HTML execution report with every screenshot embedded.

## Why this goes beyond the brief

The assignment's business scenario is "a customer wants to **purchase**
a product" — so this suite doesn't stop at "item added to cart". It
carries the flow through **checkout, payment, and order confirmation**,
so the automation proves an actual completed transaction. That's the
single biggest thing that sets this apart from a typical capstone
submission built strictly to the 10-step checklist.

## What it does

| # | Requirement | Where it's implemented |
|---|---|---|
| 1 | Launch browser | `utils/driver_factory.py` (`driver` fixture in `tests/conftest.py`) |
| 2 | Login to application | `pages/login_page.py` — logs in, and **auto-signs-up** the test user the first time it's run (fully repeatable, no manual account setup) |
| 3 | Search product | `pages/products_page.py::search_product` |
| 4 | Add product to cart | `pages/products_page.py::add_to_cart` |
| 5 | Update quantity | `pages/products_page.py::set_quantity` |
| 6 | Verify cart details | `pages/cart_page.py::get_cart_line_items` + assertions in the test |
| 7 | Capture screenshots | `utils/screenshot_helper.py` — one per step, saved to `screenshots/`, and embedded into the HTML report |
| 8 | Read test data from Excel/JSON | `utils/data_reader.py` — reads `data/test_data.json` **or** `data/test_data.xlsx` |
| 9 | Handle popup/alerts | `pages/base_page.py` + `pages/products_page.py` — native JS alerts, the "Added to cart" modal, and ad-popup recovery |
| 10 | Generate execution report | `reports/report.html` (pytest-html) — one consolidated report with every step's screenshot embedded inline |
| + | **Complete the purchase** | `pages/checkout_page.py` — proceeds through checkout, enters payment details, and asserts order confirmation |

## Project structure

```
capstone_selenium/
├── config/
│   └── config.json           # browser, headless flag, timeouts, base URL
├── data/
│   ├── test_data.json        # user, payment, and test-case data (default source)
│   └── test_data.xlsx        # same test cases in spreadsheet form
├── pages/                     # Page Object Model
│   ├── __init__.py
│   ├── base_page.py           # shared waits, actions, alert/modal/popup handling
│   ├── home_page.py
│   ├── login_page.py
│   ├── products_page.py       # search, product detail, quantity, add to cart
│   ├── cart_page.py
│   └── checkout_page.py       # checkout, payment, order confirmation
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # WebDriver fixture (launches/quits the browser)
│   └── test_purchase.py       # the data-driven end-to-end purchase test
├── utils/
│   ├── driver_factory.py
│   ├── data_reader.py
│   └── screenshot_helper.py
├── screenshots/                # created at runtime — one PNG per step, per run
├── reports/
│   ├── assets/                 # created at runtime — embedded screenshots + stylesheet
│   └── report.html             # created at runtime — the consolidated execution report
├── requirements.txt
├── pytest.ini
└── .gitignore
```

> **Note on `conftest.py`:** it holds the fixture that launches and quits
> the browser for every test. That's standard pytest structure and the
> suite won't run without it, so it's kept even though it's easy to miss
> in a folder screenshot.

## Setup

Requires Python 3.9+ and Google Chrome installed locally.

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

`webdriver-manager` downloads the matching ChromeDriver automatically —
no manual driver setup needed.

## Running the tests

```bash
pytest
```

This runs the full purchase flow once per test case in
`data/test_data.json` (`TC01`, `TC02` by default), each in its own
browser session, ending with a real order confirmation.

```bash
pytest -k TC01                     # run a single test case
```

To run headless or switch browsers, edit `config/config.json`. To switch
the data source from JSON to Excel, change `source="json"` to
`source="excel"` in `tests/test_purchase.py`.

## Outputs

- **`screenshots/`** — a timestamped PNG per step per test case, plus a
  distinct `purchase_success_<timestamp>.png` the moment the order is
  confirmed, and an automatic `FAILURE_...png` if anything fails.
- **`reports/report.html`** — open this in a browser after a run. It's a
  single pytest-html report covering both test cases, with every
  screenshot from the run embedded inline (click a test row to expand
  it) — `reports/assets/` holds the embedded images and stylesheet.

## Design notes

- **Page Object Model**: locators live in one place per page; the test
  reads like a business scenario, not a script full of
  `driver.find_element(...)` calls.
- **Login is self-healing**: the site needs a real account to log in and
  doesn't require email verification, so `ensure_logged_in()` tries to
  log in first and transparently signs up the configured test user if
  the account doesn't exist yet — runnable from a clean slate, repeatedly.
- **Resilient to the site's ad network**: automationexercise.com serves
  live third-party ads, which can intercept clicks or spawn popups.
  `driver_factory.py` blocks popups at the Chrome-prefs level, and
  `BasePage.safe_click()` falls back to a JS-dispatched click if a normal
  click is intercepted by an overlay.
- **Data-driven**: the test is `@pytest.mark.parametrize`-d over whatever
  `get_test_cases()` returns, so adding a row to the JSON/Excel file adds
  a new test case with no code changes.
- **Real execution report, not a token one**: screenshots are embedded
  via pytest-html's `extras` fixture (base64-encoded into the report,
  written out as real files under `reports/assets/`) — open one HTML
  file and see the whole run, no digging through a screenshots folder.

## Known site-dependent locators

automationexercise.com's `data-qa` attributes and element IDs (`#quantity`,
`#search_product`, `#cartModal`, the payment form's `data-qa='pay-button'`,
etc.) have been stable for years, but demo sites do change occasionally.
If a step starts failing, check whether the locator constant at the top
of the relevant `pages/*.py` file still matches the live page (right-click
→ Inspect on the element).

## Submission checklist

- [ ] Develop the solution — done, see above.
- [ ] Demonstrate the project — run `pytest` with `headless: false` in
      `config/config.json` so the browser is visible during the demo.
- [ ] **Record `Selenium-Project-Demo.mp4`** — screen-record one full
      `pytest` run (e.g. with Xbox Game Bar on Windows, OBS Studio, or
      Loom) and place the file at the project root. This isn't something
      that can be generated for you — it needs to show your machine
      actually running the suite.
- [ ] Submit source code — this folder.
- [ ] Upload code to a GitHub repository:
  ```bash
  git init
  git add .
  git commit -m "Capstone Assignment 1: Selenium e-commerce purchase automation"
  git branch -M main
  git remote add origin <your-repo-url>
  git push -u origin main
  ```
  `.gitignore` already excludes `venv/`, generated screenshots/reports,
  and `__pycache__/`.
- [ ] Include the repository link in your resume.
