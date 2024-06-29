from selenium import webdriver


class WebDriverSetup:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def open_page(self, url):
        self.driver.get(url)
        return self.driver

    def close_driver(self):
        self.driver.quit()

