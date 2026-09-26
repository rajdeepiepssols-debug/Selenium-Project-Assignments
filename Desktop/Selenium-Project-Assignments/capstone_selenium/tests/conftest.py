import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.driver_factory import get_driver, load_config


@pytest.fixture(scope="function")
def driver():
    """Launches a fresh browser per test (capstone requirement #1) and quits it afterwards."""
    config = load_config()
    drv = get_driver(config)
    yield drv
    drv.quit()
