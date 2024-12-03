from backend import *
from cmu_graphics import *
import threading
import queue
import os 
from PIL import Image
from . import drawUtils
    
def onAppStart(app):
    app.scottyEasterEggImage = CMUImage(Image.open("draw/asset/scottyEasterEgg.jpg"))

    # colors! 
    app.cmuRed = rgb(196,18,48)
    app.cmuDarkGrey = rgb(109, 110, 113)
    app.cmuSkiboRed = rgb(149, 17, 32)
    app.cmuGreen = rgb(31, 76, 76)

    app.stepCounter=0
    app.stepsPerSecond = 60

    app.webPageXStart = (300/1710)*app.width
    app.webPageYStart = 10

    # Web daemon
    app.webDaemon = webClass(app.width-app.webPageXStart-10,app.height-20)
    app.webDaemon.updateWindowSize(app.width-app.webPageXStart-10,app.height-20)

    app.tabDaemon = tabsClass()

    app.focusedTabIndex = -1

    #nice home page i found
    app.homePage = "https://web.tabliss.io/"
    app.webPage = app.homePage
    app.loadedTabs = app.tabDaemon.parseTabs()
    print(app.loadedTabs)

    #Waits until the page is done loading
    app.webDaemon.initPage(app.webPage)

    app.currentImage = CMUImage(app.webDaemon.updatePage())

    app.previousWidth = app.width
    app.previousHeight = app.height

    app.screenshotQueue = queue.Queue()
    
    app.isScreenshotReady = False
    app.previousScreenshotPath = "./backend/screenshots/previousWebPage.png"

    app.textBoxWord = ""  # Store the text entered in the text box
    app.textBoxInFocus = False 
    app.textBoxX = 100  # X position of the text box
    app.textBoxY = 150  # Y position of the text box
    app.textBoxWidth = 300  # Width of the text box
    app.textBoxHeight = 40  # Height of the text box
    app.cursorPosition = len(app.textBoxWord)  # Keep track of cursor position
    app.cursorBlink = True

    app.hoveredTab = None

    app.drawUtils = drawUtils.drawUtils()

    app.bootSound = Sound('asset/bootSound.mp3')
    app.bootSound.play(restart=True, loop=False)

def redrawAll(app):
    drawRect(0,0,app.width,app.height,fill=app.cmuRed)
    drawLabel("ScottyBrowser",app.webPageXStart/2,20,size=14)
    
    drawImage(app.currentImage, app.webPageXStart, app.webPageYStart)

    app.drawUtils.drawBrowserNavButtons(color=app.cmuSkiboRed)
    
    app.drawUtils.drawRoundedRect(10,80,app.webPageXStart-20,30,10,app.cmuSkiboRed)
    drawLabel("New Tab +",((app.webPageXStart)/2),95)

    drawLine(10,120,148,120, fill=app.cmuDarkGrey)

    count = 0
    for tabGroup in app.loadedTabs['tabs']:
        tabName = tabGroup['name']
        if len(tabName)>19:
            tabName = tabName[:15]+"..."

        app.drawUtils.drawRoundedRect(10,count*50+130,app.webPageXStart-20,30,10,app.cmuGreen)
        drawLabel(tabName,((app.webPageXStart)/2),count*50+145)
        
        
        if count == app.hoveredTab:
            drawCircle(10+app.webPageXStart-20, count*50+130,5,fill='white')
            drawLabel("x",10+app.webPageXStart-20, count*50+130,size=14)
        
        count+=1

    if app.textBoxInFocus:
        drawRect(0,0,app.width,app.height,fill="black",opacity=50)

        app.drawUtils.drawRoundedRect(app.width/9,app.height/5,7*(app.width)/9,app.height/5,
                        app.height/15,app.cmuRed)

        app.drawUtils.drawRoundedRect(app.width/9+10,app.height/5+10,7*(app.width)/9-20,
                        app.height/5-20,app.height/22,"white")
        
        # Search or Internet Buttons:

        drawCircle(8/9 * app.width, app.height/5,10,fill='white')

        drawLabel("x",8/9 * app.width, app.height/5,size=16)

        
        drawCircle(14/18 * app.width, (3/2)*app.height/5,min(app.height,app.width)/25,fill='silver')

        drawLabel("G",14/18 * app.width, (3/2)*app.height/5,size=16)
        
        drawCircle(15/18 * app.width, (3/2)*app.height/5,min(app.height,app.width)/25,fill='silver')

        drawLabel("WWW",15/18 * app.width, (3/2)*app.height/5,size=12)


        maxVisibleLength = int((13 / 18 * app.width - (app.width / 9 + 20)) // 12) - 3 
        # TextBox Stuff:
        if app.width/9+20 + 12*len(app.textBoxWord) > 13/18 * app.width:
             
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
            if app.width/9+20 + 12*len(app.textBoxWord) < 13/18 * app.width:
                cursorX = app.width/9+20 + 12*len(app.textBoxWord)
            else:
                cursorX = app.width/9+20 + 12*(maxVisibleLength+3)
            cursorY = (2*(app.height/5+10)+app.height/5-20)/2
            drawLine(cursorX, cursorY-10, cursorX, cursorY + 10, lineWidth=2)
        
    
def onMouseMove(app, mouseX, mouseY):
    app.hoveredTab = None  # Reset hovered tab
    count = 0
    for tabIndex in range(len(app.loadedTabs['tabs'])):
        x = 10
        y = count * 50 + 130
        width = app.webPageXStart - 10
        height = 30
        if x <= mouseX <= x + width and y-10 <= mouseY <= y + height:
            app.hoveredTab = tabIndex
            break
        count += 1

def startScreenshotThread(app):
    if not hasattr(app, 'screenshotThread'):
        app.screenshotThread = threading.Thread(target=app.webDaemon.updatePage, args=(app.screenshotQueue,))
        app.screenshotThread.daemon = True  # Allow the thread to exit when the program exits
        app.screenshotThread.start()

def onResize(app):
    print(f"Window size changed to: {app.width}x{app.height}")

    app.webDaemon.updateWindowSize(app.width-app.webPageXStart-10,app.height-20)
    # Update previous dimensions
    app.previousWidth = app.width
    app.previousHeight = app.height

def onStep(app):

    if app.focusedTabIndex != -1 and \
        app.webDaemon.currentPageDifferent(app.loadedTabs['tabs'][app.focusedTabIndex]):
        
        app.tabDaemon.updateTab(app.focusedTabIndex, app.webDaemon.getPageInfo())
        
        app.loadedTabs = app.tabDaemon.parseTabs()
        

    if not app.textBoxInFocus:
        app.currentImage = CMUImage(app.webDaemon.updatePage())
    

    if app.stepCounter % (app.stepsPerSecond // 2) == 0:
        
        app.cursorBlink = not app.cursorBlink
    
    app.stepCounter+=1
        
def onKeyPress(app, key):
    if not app.textBoxInFocus:
        app.webDaemon.typeInSearchField(key)
        return 
    
    
    if key == 'backspace':  # Handle backspace
        app.textBoxWord = app.textBoxWord[:-1]
        app.cursorPosition = len(app.textBoxWord)  
    elif key == "space":
        app.textBoxWord += " "
        app.cursorPosition = len(app.textBoxWord)  
    elif key == 'enter': 
        app.webDaemon.initPage(f"https://www.google.com/search?q={app.textBoxWord.replace(" ","+")}")
        pageInfo = app.webDaemon.getPageInfo()
        app.tabDaemon.addTab(*pageInfo)
        app.loadedTabs = app.tabDaemon.parseTabs()
        app.textBoxInFocus = False
        app.focusedTabIndex = len(app.loadedTabs)-1

    else:
        app.textBoxWord += key  
        app.cursorPosition = len(app.textBoxWord)  

        
def onMousePress(app,x,y):
    if not app.textBoxInFocus and app.webPageXStart<x<app.width-10 and 0<y<app.height-10:
        app.webDaemon.click(x-app.webPageXStart,y-10)
        return
    
    count = 0
    for index, tabGroup in enumerate(app.loadedTabs['tabs']):

        boxX = 10
        boxY = count * 50 + 125
        width = app.webPageXStart - 20
        height = 30
        
        # Check if the mouse click is within the bounds of the current rectangle
        if boxX <= x <= boxX + width and boxY <= y <= boxY + height:
            print(f"Tab '{tabGroup['name']}' clicked!")
            app.webDaemon.initPage(tabGroup['url'])
            
            app.webPage = tabGroup['url']
            app.focusedTabIndex = index
        
        count += 1
    
    if 10 <= x <= app.webPageXStart-20 and 80 <= y <= 110:
        # new tab 
        app.textBoxWord = ""
        app.textBoxInFocus = True
    
    if app.hoveredTab!=None and 5+app.webPageXStart-20<=x<=15+app.webPageXStart-20 and \
          app.hoveredTab*50+125<=y<=app.hoveredTab*50+135:
        print(app.hoveredTab, "REMOVED")
        app.tabDaemon.removeTab(app.hoveredTab)
        app.loadedTabs = app.tabDaemon.parseTabs()
        if app.hoveredTab == app.focusedTabIndex:
            app.focusedTabIndex = -1
            app.webDaemon.initPage(app.homePage)
        elif app.focusedTabIndex > app.hoveredTab:
            app.focusedTabIndex-=1
    
    if app.textBoxInFocus:

        if circularDistance((x,y),(8/9 * app.width,app.height/5)) <= 10:
            app.textBoxInFocus = False 
        
        searchCircleRad = min(app.height,app.width)/25
        if circularDistance((x,y),(14/18 * app.width, (3/2)*app.height/5)) <= searchCircleRad:
            app.webDaemon.initPage(f"https://www.google.com/search?q={app.textBoxWord.replace(" ","+")}")
            pageInfo = app.webDaemon.getPageInfo()
            app.tabDaemon.addTab(*pageInfo)
            app.loadedTabs = app.tabDaemon.parseTabs()
            app.textBoxInFocus = False
            app.focusedTabIndex = len(app.loadedTabs)-1

        if circularDistance((x,y),(15/18 * app.width, (3/2)*app.height/5)) <= searchCircleRad:
            try:
                app.webDaemon.initPage(f"https://{app.textBoxWord}")
                pageInfo = app.webDaemon.getPageInfo()
                app.tabDaemon.addTab(*pageInfo)
                app.loadedTabs = app.tabDaemon.parseTabs()
                app.textBoxInFocus = False
            except:
                errorDict = [
                    "404! here's scotty instead",
                    "https://www.cmu.edu/brand/images/artifact-scotty-900x600-min.jpg",
                    "error"
                ]
                
                app.tabDaemon.addTab(*errorDict)
                app.loadedTabs = app.tabDaemon.parseTabs()
                app.textBoxInFocus = False
            
            app.focusedTabIndex = len(app.loadedTabs)-1

    # Browser Nav

    if 10<=x<=40 and 15<=y<=65:
        app.webDaemon.tabBackward()
    elif 64<=x<=94 and 15<=y<=65:
        app.webDaemon.tabForward()
    elif 118<=x<=148 and 15<=y<=65:
        app.webDaemon.refresh()


def circularDistance(xy1,xy2):
    return ((xy1[0]-xy2[0])**2+(xy1[0]-xy2[0])**2)**0.5


runApp(width=900,height=485)