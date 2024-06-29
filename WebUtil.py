from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebUtil:
    def __init__(self, driver):
        self.driver = driver

    def get_text_using_xpath(self, xpath):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element.text

    def click_button_using_xpath(self, xpath):
        button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        button.click()

    def send_keys_using_xpath(self, xpath, keys):
        input_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        input_field.send_keys(keys)

    def clear_input_field_using_xpath(self, xpath):
        input_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        input_field.clear()


