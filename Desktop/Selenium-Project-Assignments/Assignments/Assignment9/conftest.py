import pytest
from selenium import webdriver

@pytest.fixture
def driver(request):
    driver = webdriver.Chrome()
    driver.maximize_window()

    yield driver

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshot = f"screenshot_{request.node.name}.png"
        driver.save_screenshot(screenshot)

        if hasattr(request.node, "extra"):
            from pytest_html import extras
            request.node.extra.append(extras.image(screenshot))

    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)