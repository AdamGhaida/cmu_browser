from backend import *
from cmu_graphics import *
import threading
import queue
import os 

# main thread obv loads image on screen

# thread B loads the next image to make it ready for frame N+1
    
def onAppStart(app):
    # colors! 
    app.cmuRed = rgb(196,18,48)
    app.cmuDarkGrey = rgb(109, 110, 113)
    app.cmuSkiboRed = rgb(149, 17, 32)
    app.cmuGreen = rgb(31, 76, 76)

    app.stepCounter=0
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
    startScreenshotThread(app)

    app.textBoxWord = ""  # Store the text entered in the text box
    app.textBoxInFocus = False 
    app.textBoxX = 100  # X position of the text box
    app.textBoxY = 150  # Y position of the text box
    app.textBoxWidth = 300  # Width of the text box
    app.textBoxHeight = 40  # Height of the text box
    app.cursorPosition = len(app.textBoxWord)  # Keep track of cursor position
    app.cursorBlink = True

    app.hoveredTab = None

# Thank you Mr Shikfa for showing me how to do this!
def drawRoundedRect(x, y, width, height, radius, color):
    # Draw corners as circles
    drawCircle(x + radius, y + radius, radius, fill=color)  
    drawCircle(x + width - radius, y + radius, radius, fill=color)  
    drawCircle(x + radius, y + height - radius, radius, fill=color)  
    drawCircle(x + width - radius, y + height - radius, radius, fill=color)  
    
    # Draw edges as rectangles
    drawRect(x + radius, y, abs(width - 2 * radius), height, fill=color)  
    drawRect(x, y + radius, width, abs(height - 2 * radius), fill=color)  

    # Fill the center
    drawRect(x + radius, y + radius, abs(width - 2 * radius), 
                                     abs(height - 2 * radius), fill=color)


def redrawAll(app):
    drawRect(0,0,app.width,app.height,fill=app.cmuRed)
    drawLabel("ScottyBrowser",app.webPageXStart/2,20,size=14)

    
    
    drawImage(app.currentImage, app.webPageXStart, app.webPageYStart)
    if app.isScreenshotReady:
        if not app.screenshotQueue.empty():
            screenshot_path = app.screenshotQueue.get()
            
            if os.path.exists(screenshot_path):
                drawImage(screenshot_path, app.webPageXStart, app.webPageYStart)
        
        
        app.isScreenshotReady = False
    else:
        if os.path.exists(app.previousScreenshotPath):
            drawImage(app.previousScreenshotPath, app.webPageXStart, app.webPageYStart)
    
    drawRoundedRect(10,40,app.webPageXStart-20,30,10,app.cmuSkiboRed)
    drawLabel("New Tab +",((app.webPageXStart)/2),55)

    count = 0
    for tabGroup in app.loadedTabs['tabs']:
        tabName = tabGroup['name']
        if len(tabName)>19:
            tabName = tabName[:15]+"..."

        drawRoundedRect(10,count*50+90,app.webPageXStart-20,30,10,app.cmuGreen)
        drawLabel(tabName,((app.webPageXStart)/2),count*50+105)
        
        
        if count == app.hoveredTab:
            drawCircle(10+app.webPageXStart-20, count*50+90,5,fill='white')
            drawLabel("x",10+app.webPageXStart-20, count*50+90,size=14)
        
        count+=1

    if app.textBoxInFocus:
        drawRect(0,0,app.width,app.height,fill="black",opacity=50)

        drawRoundedRect(app.width/9,app.height/5,7*(app.width)/9,app.height/5,
                        app.height/15,app.cmuRed)

        drawRoundedRect(app.width/9+10,app.height/5+10,7*(app.width)/9-20,
                        app.height/5-20,app.height/22,"white")
        
        # Search or Internet Buttons:

        drawCircle(8/9 * app.width, app.height/5,10,fill='white')

        drawLabel("x",8/9 * app.width, app.height/5,size=16)

        
        drawCircle(14/18 * app.width, (3/2)*app.height/5,20,fill='silver')

        drawLabel("G",14/18 * app.width, (3/2)*app.height/5,size=16)
        
        drawCircle(15/18 * app.width, (3/2)*app.height/5,20,fill='silver')

        drawLabel("WWW",15/18 * app.width, (3/2)*app.height/5,size=12)

        # TextBox Stuff:
        if app.width/9+20 + 12*len(app.textBoxWord) > 13/18 * app.width:
            maxVisibleLength = int((13 / 18 * app.width - (app.width / 9 + 20)) // 12) - 3  
            visibleSegment = app.textBoxWord[-maxVisibleLength:]  
            drawLabel("..." + visibleSegment, app.width / 9 + 20,
                    (2 * (app.height / 5 + 10) + app.height / 5 - 20) / 2,
                    size=20, font='monospace', align='left')
        else:
            drawLabel(app.textBoxWord, app.width/9+20, 
                (2*(app.height/5+10)+app.height/5-20)/2, size=20, 
                font='monospace', align='left')

        # Optional: Draw a cursor at the end of the text (simulating a blinking cursor)
        if app.cursorBlink:  # Toggle cursor visibility for blinking effect
            cursorX = app.width/9+20 + 12*len(app.textBoxWord)
            cursorY = (2*(app.height/5+10)+app.height/5-20)/2
            drawLine(cursorX, cursorY-10, cursorX, cursorY + 10, lineWidth=2)
        
    
def onMouseMove(app, mouseX, mouseY):
    app.hoveredTab = None  # Reset hovered tab
    count = 0
    for tabIndex in range(len(app.loadedTabs['tabs'])):
        x = 10
        y = count * 50 + 90
        width = app.webPageXStart - 10
        height = 30
        if x <= mouseX <= x + width and y-10 <= mouseY <= y + height:
            app.hoveredTab = tabIndex
            break
        count += 1

def startScreenshotThread(app):
    if not hasattr(app, 'screenshotThread'):
        app.screenshotThread = threading.Thread(target=app.sel.updatePage, args=(app.screenshotQueue,))
        app.screenshotThread.daemon = True  # Allow the thread to exit when the program exits
        app.screenshotThread.start()

def onResize(app):
    print(f"Window size changed to: {app.width}x{app.height}")

    app.sel.updateWindowSize(app.width-app.webPageXStart-10,app.height-20)
    # Update previous dimensions
    app.previousWidth = app.width
    app.previousHeight = app.height

def onStep(app):

    
    if not app.textBoxInFocus:
        app.currentImage = CMUImage(app.sel.updatePage())
    

    if app.stepCounter % (app.stepsPerSecond // 2) == 0:
        
        app.cursorBlink = not app.cursorBlink
    
    app.stepCounter+=1
        
def onKeyPress(app, key):
    if not app.textBoxInFocus:
        app.sel.typeInSearchField(key)
        return 
    
    
    if key == 'backspace':  # Handle backspace
        app.textBoxWord = app.textBoxWord[:-1]
        app.cursorPosition = len(app.textBoxWord)  
    elif key == "space":
        app.textBoxWord += " "
        app.cursorPosition = len(app.textBoxWord)  
    elif key == 'enter': 
        app.sel.initPage(f"https://www.google.com/search?q={app.textBoxWord.replace(" ","+")}")
        pageInfo = app.sel.getPageInfo()
        app.tabDaemon.addTab(*pageInfo)
        app.loadedTabs = app.tabDaemon.parseTabs()
        app.textBoxInFocus = False

    else:
        app.textBoxWord += key  
        app.cursorPosition = len(app.textBoxWord)  

        
def onMousePress(app,x,y):
    if not app.textBoxInFocus and app.webPageXStart<x<app.width-10 and 0<y<app.height-10:
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
        app.textBoxInFocus = True
                      
    if 5+app.webPageXStart-20<=x<=15+app.webPageXStart-20 and app.hoveredTab*50+85<=y<=count*50+95:
        app.tabDaemon.removeTab(app.hoveredTab)
        app.loadedTabs = app.tabDaemon.parseTabs()
    
    if app.textBoxInFocus:
        if ((x-(8/9 * app.width))**2+(y-(app.height/5))**2)**0.5 <=10:
            app.textBoxInFocus = False 
        


runApp(width=900,height=485)