import time
from DocumentHandler import DocumentHandler
from WebUtil import WebUtil
from selenium.common.exceptions import NoSuchElementException
from CalculatePriceBasedOnHigherValue import CalculatePriceBasedOnHigherValue
from CalculatePriceBasedOnLowerValue import CalculatePriceBasedOnLowerValue


class ProductHandler(WebUtil):

    def __init__(self, driver):
        """Initialize the ProductHandler.

        :param driver: Selenium WebDriver instance.
        """
        super().__init__(driver)

    def clickDesiredButton(self):
        """Handle interactions based on specific product conditions."""
        global productStatusInDb
        productIndex = 0
        temList = [None]
        temListAll = [None, None]

        while True:
            try:
                # Fetch product details using XPaths
                productName = self.get_text_using_xpath(f'//*[@id="row{productIndex}jqxGrid3"]/div[12]/div')
                productMyUnit = self.get_text_using_xpath(f'//*[@id="row{productIndex}jqxGrid3"]/div[10]/div')
                productCompanyUnit = self.get_text_using_xpath(f'//*[@id="row{productIndex}jqxGrid3"]/div[10]/div')
                productId = self.get_text_using_xpath(f'//*[@id="row{productIndex}jqxGrid3"]/div[13]/div')

                # Check if the current product ID is repeated
                if productId == temListAll[-1] == temListAll[-2]:
                    product_handler = DocumentHandler(self.driver, 'D:\PythonGeneral\pythonOop\dataFiles\companies.txt')
                    product_handler.downloadDocument()
                    print("Not Found Product To Change Price, Downloading Document..")

                # Check price difference condition
                try:
                    productNewValue = float(self.get_text_using_xpath(
                        f'//*[@id="row{productIndex}jqxGrid3"]/div[5]/div'))
                    productOldValue = float(self.get_text_using_xpath(
                        f'//*[@id="row{productIndex}jqxGrid3"]/div[6]/div'))
                    if productOldValue != 0:

                        percentageDifference = abs(
                            (productNewValue - productOldValue) / productOldValue) * 100
                        calc_price = CalculatePriceBasedOnLowerValue()
                        productStatusInDb = calc_price.product_exists(productId)

                    else:
                        percentageDifference = 10  # added value that will be default

                    if percentageDifference > 5 or productStatusInDb:
                        if productMyUnit == productCompanyUnit and productId not in temList:
                            self.click_button_using_xpath(f'//*[@id="row{productIndex}jqxGrid3"]')
                            finalPrice = self.get_calculated_price(productNewValue, productOldValue, productId)
                            print(finalPrice)

                            if finalPrice is not None:
                                pass

                            print(f"Product With Different Value Found: {productName}..")
                            temList.append(productId)



                except ValueError:
                    # Handling potential conversion errors
                    pass

                # Handle scrolling and resetting of productIndex
                if productIndex == 6:
                    temListAll.append(productId)
                    productIndex = 1
                    for _ in range(2):
                        self.click_button_using_xpath(f'//*[@id="jqxScrollBtnDownverticalScrollBarjqxGrid3"]')
                productIndex += 1

            except NoSuchElementException:
                break

    def get_calculated_price(self, productNewValue, productOldValue, productId):
        if productNewValue > productOldValue:
            calculator = CalculatePriceBasedOnHigherValue()
            return calculator.calculate_final_price(productNewValue)
        else:
            with CalculatePriceBasedOnLowerValue() as calculator:
                return calculator.calculate_final_price(productId, productNewValue)

    def handle_dialog(self, productIndex):
        """Handle dialog and interactions after certain conditions."""
        self.click_button_using_xpath(f'//*[@id="row{productIndex}jqxGrid2"]')
        time.sleep(3)
        self.click_button_using_xpath("//button[contains(@class, 'btn-success') and @ng-click='choose()']")
        try:
            self.click_button_using_xpath("//button[text()='დიახ']")
        except NoSuchElementException:
            print("The dialog did not appear within the expected time.")
        product_handler = DocumentHandler(self.driver)
        product_handler.click_if_desired()
