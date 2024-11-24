import os
import time
from selenium import webdriver
from PIL import Image
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class webClass:

    def __init__(self,width,height):
        self.width = width
        self.height = height
        
        # When selenium runs chrome in headless mode, 
        #   139 pixels of window size are the top bar 
        self.chromeTopBarHeight = 139

        self.seleniumOptionsInit()
        
        self.screenshotDirectory = "./backend/screenshots/"
        self.screenshotName = "webPage.png"

        self.previousScreenshotName = "previousWebPage.png"
        self.screenshotPath = os.path.join(self.screenshotDirectory, self.screenshotName)
        self.previousScreenshotPath = os.path.join(self.screenshotDirectory, self.previousScreenshotName)


    def seleniumOptionsInit(self):
        

        # Various options set up for the emulation of a browser
        chromeOptions = Options()
        # chromeOptions.add_argument("--headless")
        chromeOptions.add_argument("--no-sandbox")
        chromeOptions.add_argument("--disable-dev-shm-usage")
        chromeOptions.add_argument("--force-device-scale-factor=1")
        chromeOptions.add_argument(f"window-size={self.width
                                            },{
                                                self.height+\
                                                self.chromeTopBarHeight}")
        self.driver = webdriver.Chrome(options=chromeOptions)
        self.actions = ActionChains(self.driver)


    def updateWindowSize(self, width, height):
        print(height)
        self.driver.set_window_size(width,height+self.chromeTopBarHeight)
        print(self.driver.get_window_size())
    
    def getScreenshot(self):
        return self.screenshotPath

    def initPage(self,url):
        self.driver.get(url)
        time.sleep(2)  # Let the page load fully
        
    # Function to check if the image is valid
    def is_valid_image(self, file_path):
        try:
            with Image.open(file_path) as img:
                img.verify()  # Check if the image is valid
            return True
        except (IOError, SyntaxError) as e:
            print(f"Invalid image: {file_path}")
            return False

    # Update the page and put the screenshot path into the queue
    def updatePage(self, screenshotQueue):
        while True:
            # Save the screenshot
            self.driver.save_screenshot(self.screenshotPath)
            

            # Swap the current screenshot with the previous screenshot
            
            os.rename(self.screenshotPath, self.previousScreenshotPath)
            
            screenshotQueue.put(self.previousScreenshotPath)  # Put the previous screenshot path into the queue
            
            
            time.sleep(1 / 480)

    def click(self,x,y):
        print("clicked at", x,y)
        self.actions.move_by_offset(x,y).click().perform()
        self.actions.move_by_offset(-x,-y).perform()
    
    
    def typeInSearchField(self, text):
        
        # Find the search input field (e.g., Google's search bar)
        search_field = self.driver.find_element(By.NAME, "q")  # Google's search input field

        match text:
            case "space":
                search_field.send_keys(Keys.SPACE)
            case "enter":
                search_field.send_keys(Keys.ENTER)
            case "tab":
                search_field.send_keys(Keys.TAB)
            case "backspace":
                search_field.send_keys(Keys.BACK_SPACE)
            case _:
                search_field.send_keys(text)
        
        # Optionally, submit by pressing Enter

