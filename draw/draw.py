
from backend import webClass
from cmu_graphics import *

def onAppStart(app):
    print(app.width,app.height)
    app.stepsPerSecond = 30
    app.sel = webClass(1400,900)
    
    #nice home page i found
    app.webPage = "https://web2.qatar.cmu.edu/~shajizad/"

    #Waits until the page is done loading
    app.sel.initPage(app.webPage)


def redrawAll(app):
    drawImage(app.sel.getScreenshot(),300,10)



def onStep(app):
    app.sel.updatePage()

def onMousePress(app,x,y):
    pass

runApp(width=1710,height=920)