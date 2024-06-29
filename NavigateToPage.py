import time

from WebUtil import WebUtil



class NavigateToPage(WebUtil):

    def __init__(self, driver):
        # Initialize with the provided driver
        self.driver = driver

    def go_to_desired_page(self, EMAIL, PASS, DATE):
        # Define constants for email, password and date

        # Fill in email and password fields
        self.send_keys_using_xpath('//*[@id="Login"]', EMAIL)
        self.send_keys_using_xpath('//*[@id="Password"]', PASS)

        # Click the login button
        self.click_button_using_xpath('//*[@id="login_form"]/section/button')
        # Navigate through several pages using the given links and buttons to go working place
        self.click_button_using_xpath("//a[@href='/Main/?tag=TABLE_DOC_VENDOR']")
        self.click_button_using_xpath("//span[text()='საქონლის შესყიდვა']")
        self.click_button_using_xpath("//div[@ng-if=\"operation.tag == 'DOC_PRODUCTIN' && operation.show_rs \"]/a")
        self.click_button_using_xpath("//a[contains(text(), 'ზედნადებების ჯგუფური ჩამოტვირთვა')]")

        # Changing date of searching documents
        self.click_button_using_xpath('/html/body/div[1]/div/div/div[2]/div/div/div[1]/ng-include/div/input[1]')
        self.click_button_using_xpath("//button[text()='გასუფთავება']")
        self.send_keys_using_xpath(
            "//input[contains(@class, 'form-control') and contains(@uib-datepicker-popup, 'dd/MM/yyyy')]", DATE)
        self.click_button_using_xpath("//button[@ng-click='refresh()']")

        try:
            self.click_button_using_xpath("//button[@class='ngdialog-button ngdialog-button-primary ng-binding']")
        except:
            pass
        finally:
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


        print("Navigated To Desired Page With Desired Date..")
        # Wait for 3 seconds to ensure all operations are completed
        time.sleep(3)
