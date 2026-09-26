"""
screenshot_helper.py
---------------------
Satisfies capstone requirement #7: "Capture screenshots".
Saves timestamped PNGs into the configured screenshots directory.
"""

import os
import time


def capture_screenshot(driver, name: str, screenshot_dir: str = None) -> str:
    screenshot_dir = screenshot_dir or os.path.join(
        os.path.dirname(__file__), "..", "screenshots"
    )
    os.makedirs(screenshot_dir, exist_ok=True)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in name)
    filepath = os.path.join(screenshot_dir, f"{safe_name}_{timestamp}.png")

    driver.save_screenshot(filepath)
    return filepath
