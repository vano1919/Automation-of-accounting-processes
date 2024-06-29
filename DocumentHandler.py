import re
import time
from selenium.common.exceptions import NoSuchElementException
from WebUtil import WebUtil
from WebDriverSetup import WebDriverSetup
from NavigateToPage import NavigateToPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from WebDriverSetup import WebDriverSetup


class DocumentHandler(WebUtil):

    def __init__(self, driver, filepath=None):
        """
        Initialize the DocumentHandler.

        :param driver: Selenium WebDriver instance.
        :param filepath: Optional. Path to the file containing company data.
        """
        self.driver = driver
        if filepath:
            # Load companies from the provided file
            self.company_list = self._load_companies_from_file(filepath)
        else:
            self.company_list = []
        self.row_num = 0  # Initialize row_num

    def _load_companies_from_file(self, filepath):
        """
        Load company IDs from a given file.

        This function reads company IDs separated by commas from the provided file.

        :param filepath: Path to the file.
        :return: List of company IDs.
        """
        with open(filepath, 'r', encoding="utf-8") as file:
            content = file.read()
        return content.strip().split(",")

    def get_text_using_xpath(self, xpath):
        """
        Get text from a web element using XPath.

        :param xpath: XPath string with placeholder for row number.
        :return: Text content of the web element.
        """
        # Adjust the XPath to include the row id
        xpath = xpath.format(row_num=self.row_num)
        return self.driver.find_element(By.XPATH, xpath).text

    def click_if_desired(self):

        """
        Click on a row if it meets certain conditions.

        This method checks rows for the presence of specific text. If present, it checks the
        company's value of that row. If the company value is not in the company list, the method
        clicks on the row. It will increment row_num and check the next row if conditions are not met.
        """

        max_attempts = 6  # Limit the number of rows to check for safety

        for _ in range(max_attempts):

            # Use a try-except block to catch the exception if the element is not found
            try:
                is_active_present = self.get_text_using_xpath(
                    "//div[@id='row{row_num}jqxGrid2']//div[contains(text(), 'აქტიური') or contains(text(), 'დასრულებული')]"
                ) in ['აქტიური', 'დასრულებული']

            except NoSuchElementException:
                is_active_present = False

            if is_active_present:
                companyDownloadStatus = self.get_text_using_xpath(f'//*[@id="row{self.row_num}jqxGrid2"]/div[14]/div')

                if companyDownloadStatus == 'არ არის ჩამოტვირთული':
                    self.click_button_using_xpath(f'//*[@id="row{self.row_num}jqxGrid2"]')
                    print("Not Downloaded Document Is Found..")

                    company_info = self.get_text_using_xpath(f'//*[@id="row{self.row_num}jqxGrid2"]/div[8]/div')

                    if company_info not in self.company_list:
                        from ProductHandler import ProductHandler  # Lazy import
                        self.row_num = 0
                        handler = ProductHandler(self.driver)
                        handler.clickDesiredButton()
                        break
                    else:
                        self.row_num = 0
                        product_handler = DocumentHandler(self.driver,
                                                          'D:\PythonGeneral\pythonOop\dataFiles\companies.txt')
                        product_handler.downloadDocument()
                        print(f"Do Not Changing Price Of The Company: {company_info}, Downloading Document..")

            # Increment to check the next row if conditions are not met
            self.row_num += 1

    def downloadDocument(self):
        time.sleep(3)

        """
        Download a document based on the current row_num.

        :return: None
        """

        self.click_button_using_xpath("//button[contains(.//i/@class, 'fa-check')]")


        try:
            self.click_button_using_xpath("//button[text()='დიახ']")

        except:
            print("Not Found Product To Change Price, Downloading Document..")

        time.sleep(3)
        self.click_button_using_xpath('//*[@id="columntablejqxGrid2"]/div[14]/div')


        firstDocumentStatus = self.get_text_using_xpath(f'//*[@id="row0jqxGrid2"]/div[14]/div')
        refresherCounter = 0
        while firstDocumentStatus == 'ჩამოტვირთულია':
            self.click_button_using_xpath('//*[@id="columntablejqxGrid2"]/div[14]/div')
            firstDocumentStatus = self.get_text_using_xpath(f'//*[@id="row0jqxGrid2"]/div[14]/div')
            if refresherCounter > 10:
                self.driver.quit()
                import os
                os._exit(0)  # ensure the program terminates

            refresherCounter += 1

        time.sleep(3)
