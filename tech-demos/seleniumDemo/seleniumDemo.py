import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

"""
This class covers the basic functionality of Selenium and it's use during the 
MVP stage of ScottySurf.
"""
class webClass:

    def __init__(self,width,height):
        self.width = width
        self.height = height
        
        self.seleniumOptionsInit()
        
        self.screenshotDirectory = "/Users/adam/Developer/cmu_browser/tech-demos/seleniumDemo/screenshots/"
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
        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        chromeOptions.add_argument(f"--user-agent={userAgent}")
        
        # mainly for time, we render precisely the size it appears on screen.
        #   I might change this later depending on if it looks really bad, 
        #   but it works for now
        chromeOptions.add_argument("--force-device-scale-factor=1")
        chromeOptions.add_argument(f"window-size={self.width
                                            },{
                                                self.height+\
                                                chromeTopBarHeight}")
        self.driver = webdriver.Chrome(options=chromeOptions)

    def clicked(self,x,y):
        self.driver.click
    
    def getScreenshot(self):
        return self.screenshotPath

    def initPage(self,url):
        self.driver.get(url)
        time.sleep(2)  # Let the page load fully
        self.updatePage()

    def updatePage(self):
        self.driver.save_screenshot(self.screenshotPath)
