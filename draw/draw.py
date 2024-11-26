from backend import *
from cmu_graphics import *
import threading
import queue
import os 

# main thread obv loads image on screen

# thread B loads the next image to make it ready for frame N+1


def onAppStart(app):
    print(app.width,app.height)
    app.stepsPerSecond = 60
    app.webPageXStart = (300/1710)*app.width
    app.webPageYStart = 10
    app.sel = webClass(app.width-app.webPageXStart-10,app.height-20)
    app.sel.updateWindowSize(app.width-app.webPageXStart-10,app.height-20)
    app.tabDaemon = tabsClass()

    #nice home page i found
    app.webPage = "https://google.com"
    

    
    app.loadedTabs = app.tabDaemon.parseTabs()
    print(app.loadedTabs)

    #Waits until the page is done loading
    app.sel.initPage(app.webPage)

    app.currentImage = CMUImage(app.sel.updatePage())

    app.previousWidth = app.width
    app.previousHeight = app.height

    

    app.screenshotQueue = queue.Queue()
    
    app.isScreenshotReady = False
    app.previousScreenshotPath = "./backend/screenshots/previousWebPage.png"
    
    # Start the background thread for capturing screenshots
    # startScreenshotThread(app)

    app.inputWord = ""



def redrawAll(app):
    drawRect(0,0,app.width,app.height,fill="red")
    drawLabel("ScottyBrowser",app.webPageXStart/2,20,size=14)
    
    drawImage(app.currentImage, app.webPageXStart, app.webPageYStart)
    # if app.isScreenshotReady:
    #     if not app.screenshotQueue.empty():
    #         screenshot_path = app.screenshotQueue.get()
            
    #         if os.path.exists(screenshot_path):
    #             drawImage(screenshot_path, app.webPageXStart, app.webPageYStart)
        
        
    #     app.isScreenshotReady = False
    # else:
    #     if os.path.exists(app.previousScreenshotPath):
    #         drawImage(app.previousScreenshotPath, app.webPageXStart, app.webPageYStart)
    
    drawRect(10,40,app.webPageXStart-20,30, fill='gray')
    drawLabel("New Tab +", (10+app.webPageXStart-20)/2,10+40)


    count = 0
    for tabGroup in app.loadedTabs['tabs']:
        drawRect(10,count*50+90,app.webPageXStart-20,30, fill='gray')
        drawLabel(tabGroup['name'],(10+(10+app.webPageXStart-20)/2),count*50+105)
        count+=1
        

def startScreenshotThread(app):
    if not hasattr(app, 'screenshotThread'):
        app.screenshotThread = threading.Thread(target=app.sel.updatePage, args=(app.screenshotQueue,))
        app.screenshotThread.daemon = True  # Allow the thread to exit when the program exits
        app.screenshotThread.start()


def onStep(app):
    # startScreenshotThread(app)

    if app.width != app.previousWidth or app.height != app.previousHeight:
        print(f"Window size changed to: {app.width}x{app.height}")

        app.sel.updateWindowSize(app.width-app.webPageXStart-10,app.height-20)
        # Update previous dimensions
        app.previousWidth = app.width
        app.previousHeight = app.height
    
    app.currentImage = CMUImage(app.sel.updatePage())
        
def onKeyPress(app, key):
    print(f"Key pressed: {key}")
    app.sel.typeInSearchField(key)
        
def onMousePress(app,x,y):
    if app.webPageXStart<x<app.width-10 and 0<y<app.height-10:
        print("clicked!!!", x,y)
        app.sel.click(x-app.webPageXStart,y-10)
        return
    
    count = 0
    for tabGroup in app.loadedTabs['tabs']:

        boxX = 10
        boxY = count * 50 + 105
        width = app.webPageXStart - 20
        height = 30
        
        # Check if the mouse click is within the bounds of the current rectangle
        if boxX <= x <= boxX + width and boxY <= y <= boxY + height:
            print(f"Tab '{tabGroup['name']}' clicked!")
            app.sel.initPage(tabGroup['url'])
            app.webPage = tabGroup['url']
        
        count += 1
    
    if 10 <= x <= app.webPageXStart-20 and 35 <= y <= 90:
        # new tab 
        print("new tab!")

runApp(width=900,height=485)