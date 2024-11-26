import os
import time
from selenium import webdriver
from PIL import Image
import io 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .tabs import tabsClass
from webdriver_manager.chrome import ChromeDriverManager


class webClass:

    def __init__(self,width,height):
        self.width = width
        self.height = height
        
        # When selenium runs chrome in headless mode, 
        #   139 pixels of window size are the top bar 
        self.chromeTopBarHeight = 139

        self.tabDaemon = tabsClass()


        self.seleniumOptionsInit()
        
        self.screenshotDirectory = "./backend/screenshots/"
        self.screenshotName = "webPage.png"

        self.previousScreenshotName = "previousWebPage.png"
        self.screenshotPath = os.path.join(self.screenshotDirectory, self.screenshotName)
        self.previousScreenshotPath = os.path.join(self.screenshotDirectory, self.previousScreenshotName)


    def seleniumOptionsInit(self):
        

        # Various options set up for the emulation of a browser
        chromeOptions = Options()
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument("--no-sandbox")
        chromeOptions.add_argument("--disable-dev-shm-usage")
        chromeOptions.add_argument("--force-device-scale-factor=1")
        
        #trying to fix the 
        effectiveWidth = self.width
        effectiveHeight = self.height+self.chromeTopBarHeight

        chromeOptions.add_argument(f"window-size={effectiveWidth},{
            effectiveHeight}")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                                       options=chromeOptions)
        self.actions = ActionChains(self.driver)


    def updateWindowSize(self, width, height):
        print(height)
        self.driver.set_window_size(width,height+self.chromeTopBarHeight)
        print(self.driver.get_window_size())
    
    def getScreenshot(self):
        return self.screenshotPath

    def initPage(self,url):

        self.driver.get(url)

        
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
    def updatePage(self):
        # while True:
        #     # Save the screenshot
        #     # self.driver.save_screenshot(self.screenshotPath)
            
            temp = io.BytesIO(self.driver.get_screenshot_as_png())

            currentImage = Image.open(temp)

            return currentImage
            # Swap the current screenshot with the previous screenshot
            
            os.rename(self.screenshotPath, self.previousScreenshotPath)
            
            screenshotQueue.put(self.previousScreenshotPath)  # Put the previous screenshot path into the queue
            
            
            time.sleep(1 / 60)

    def click(self,x,y):
        print("clicked at", x,y)
        self.actions.move_by_offset(x,y).click().perform()
        self.actions.move_by_offset(-x,-y).perform()
    
    
    def findInputField(self,name=None, id=None, class_name=None, placeholder=None):
        if name:
            try:
                return self.driver.find_element(By.NAME, name)
            except:
                pass
        
        if id:
            try:
                return self.driver.find_element(By.ID, id)
            except:
                pass
        
        if class_name:
            try:
                return self.driver.find_element(By.CLASS_NAME, class_name)
            except:
                pass
        
        if placeholder:
            try:
                return self.driver.find_element(By.XPATH, f"//input[@placeholder='{placeholder}']")
            except:
                pass

        return None  # If no search field is found

    def typeInSearchField(self, text):
        
        # Find the search input field (e.g., Google's search bar)
        field = self.findInputField(name="q", id="search-box", class_name="search-input")  # Google's search input field
        
        if field == None:
            print("no field found")
            return 
        
        match text:
            case "space":
                field.send_keys(Keys.SPACE)
            case "enter":
                field.send_keys(Keys.ENTER)
            case "tab":
                field.send_keys(Keys.TAB)
            case "backspace":
                field.send_keys(Keys.BACK_SPACE)
            case _:
                field.send_keys(text)
        
        # Optionally, submit by pressing Enter

