class InventoryPage:
    def __init__(self, driver):
        self.driver = driver

    def get_url(self):
        return self.driver.current_url