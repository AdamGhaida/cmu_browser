

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class webClass:

    def __init__(self,width,height):
        self.width = width
        self.height = height
        
        self.seleniumOptionsInit()
        
        self.screenshotDirectory = "/backend/screenshots/"
        self.screenshotName = "webPage.png"

        self.screenshotPath = self.screenshotDirectory+self.screenshotName

    def seleniumOptionsInit(self):
        # When selenium runs chrome in headless mode, 
        #   139 pixels of window size are the top bar 
        chromeTopBarHeight = 139

        # Various options set up for the emulation of a browser
        chromeOptions = Options()
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument("--no-sandbox")
        chromeOptions.add_argument("--disable-dev-shm-usage")
        chromeOptions.add_argument("--force-device-scale-factor=1")
        chromeOptions.add_argument(f"window-size={self.width
                                            },{
                                                self.height+\
                                                chromeTopBarHeight}")
        self.driver = webdriver.Chrome(options=chromeOptions)


    
    
    def getScreenshot(self):
        return self.screenshotPath

    def initPage(self,url):
        self.driver.get(url)
        time.sleep(2)  # Let the page load fully
        self.updatePage()

    def updatePage(self):
        self.driver.save_screenshot(self.screenshotPath)
        print(f"Captured screenshot at {time.time()}")
        print(self.driver.get_window_size())
