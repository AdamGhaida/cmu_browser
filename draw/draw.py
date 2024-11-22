
from backend import webClass
from cmu_graphics import *
import threading
import queue
import os 

def onAppStart(app):
    print(app.width,app.height)
    app.stepsPerSecond = 120
    app.sel = webClass(1400,900)
    
    #nice home page i found
    app.webPage = "https://google.com"

    #Waits until the page is done loading
    app.sel.initPage(app.webPage)

    app.previousWidth = app.width
    app.previousHeight = app.height

    app.widthProportion = (1400/1710)
    app.webPageXStart = (300/1710)*app.width
    app.webPageYStart = 10

    app.screenshotQueue = queue.Queue()
    
    app.isScreenshotReady = False
    app.previousScreenshotPath = "./backend/screenshots/previousWebPage.png"
    
    # Start the background thread for capturing screenshots
    start_screenshot_thread(app)

    app.inputWord = ""



def redrawAll(app):
    if app.isScreenshotReady:
        # If the screenshot is ready, draw it
        if not app.screenshotQueue.empty():
            screenshot_path = app.screenshotQueue.get()
            
            # Check if the screenshot file exists before drawing it
            if os.path.exists(screenshot_path):
                drawImage(screenshot_path, app.webPageXStart, app.webPageYStart)
        
        # Set the flag back to False to indicate we are drawing the current image
        app.isScreenshotReady = False
    else:
        # If the screenshot isn't ready, draw the previous one
        if os.path.exists(app.previousScreenshotPath):
            drawImage(app.previousScreenshotPath, app.webPageXStart, app.webPageYStart)


# Function to start the screenshot capture thread (only once)
def start_screenshot_thread(app):
    if not hasattr(app, 'screenshotThread'):
        app.screenshotThread = threading.Thread(target=app.sel.updatePage, args=(app.screenshotQueue,))
        app.screenshotThread.daemon = True  # Allow the thread to exit when the program exits
        app.screenshotThread.start()


# CMU Graphics `onStep()` function (called 30 times per second)
def onStep(app):
    start_screenshot_thread(app)

    if app.width != app.previousWidth or app.height != app.previousHeight:
        print(f"Window size changed to: {app.width}x{app.height}")

        app.sel.updateWindowSize(app.widthProportion*app.width,app.height-20)
        # Update previous dimensions
        app.previousWidth = app.width
        app.previousHeight = app.height
        
def onKeyPress(app, key):
    print(f"Key pressed: {key}")

    # Accumulate the current word based on key input
    if key == "Space":
        # When space is pressed, add the word to the input field and reset for next word
        app.sel.typeInSearchField(app.inputWord)
        app.inputWord = ""  # Clear the accumulated word
    elif key == "Enter":
        # Pressing Enter submits the current word and clears it
        app.sel.typeInSearchField(app.inputWord)
        app.currentWord = ""  # Clear the accumulated word
    else:
        # Append the character to the current word
        app.inputWord += key

def onMousePress(app,x,y):
    if app.webPageXStart<x<app.width-10 and 0<y<app.height-10:
        print("clicked!!!", x,y)
        app.sel.click(x-330,y-10)

runApp(width=1710,height=920)