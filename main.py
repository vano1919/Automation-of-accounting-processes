from DocumentHandler import DocumentHandler
from WebDriverSetup import WebDriverSetup
from NavigateToPage import NavigateToPage

browser = WebDriverSetup()
driver = browser.open_page("https://web.fina24.ge/Main/?tag=TABLE_DOC_VENDOR#")
EMAIL = "...."
PASS = "...."
DATE = "....."


navigator = NavigateToPage(driver)
navigator.go_to_desired_page(EMAIL,PASS,DATE)
product_handler = DocumentHandler(driver, 'D:\PythonGeneral\pythonOop\dataFiles\companies.txt')

while True:
    product_handler.click_if_desired()
    # try:
    #
    # except:
    #     product_handler.downloadDocument()
    #     print("Not Found Product To Change Price, Downloading Document..")

driver.quit()
