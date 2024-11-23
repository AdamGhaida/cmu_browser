
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

    app.webPageXStart = (300/1710)*app.width
    app.webPageYStart = 10

    app.screenshotQueue = queue.Queue()
    
    app.isScreenshotReady = False
    app.previousScreenshotPath = "./backend/screenshots/previousWebPage.png"
    
    # Start the background thread for capturing screenshots
    startScreenshotThread(app)

    app.inputWord = ""



def redrawAll(app):
    if app.isScreenshotReady:
        
        if not app.screenshotQueue.empty():
            screenshot_path = app.screenshotQueue.get()
            
            
            if os.path.exists(screenshot_path):
                drawImage(screenshot_path, app.webPageXStart, app.webPageYStart)
        
        
        app.isScreenshotReady = False
    else:
        if os.path.exists(app.previousScreenshotPath):
            drawImage(app.previousScreenshotPath, app.webPageXStart, app.webPageYStart)


def startScreenshotThread(app):
    if not hasattr(app, 'screenshotThread'):
        app.screenshotThread = threading.Thread(target=app.sel.updatePage, args=(app.screenshotQueue,))
        app.screenshotThread.daemon = True  # Allow the thread to exit when the program exits
        app.screenshotThread.start()


def onStep(app):
    startScreenshotThread(app)

    if app.width != app.previousWidth or app.height != app.previousHeight:
        print(f"Window size changed to: {app.width}x{app.height}")

        app.sel.updateWindowSize(app.width-app.webPageXStart-10,app.height-20)
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
        app.sel.click(x-app.webPageXStart,y-10)

runApp(width=1710,height=920)