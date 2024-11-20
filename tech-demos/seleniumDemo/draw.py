from cmu_graphics import *
from seleniumDemo import *


def onAppStart(app):
    print(app.width,app.height)
    app.stepsPerSecond = 30
    app.sel = webClass(app.width,app.height)
    
    #nice home page i found
    app.webPage = "https://giphy.com/"

    #Waits until the page is done loading
    app.sel.initPage(app.webPage)


def redrawAll(app):
    drawImage(app.sel.getScreenshot(),0,0)


def onStep(app):
    app.sel.updatePage()

def onMousePress(app,x,y):
    pass

runApp(width=1400,height=800)