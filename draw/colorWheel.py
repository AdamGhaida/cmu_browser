from cmu_graphics import *
import math
from PIL import *

# Helper function to calculate RGB from HSV
def hsvToRgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    if s == 0.0:
        r = g = b = v
        return rgb(int(r * 255), int(g * 255), int(b * 255))
    i = int(h * 6.0)  # Sector
    f = (h * 6.0) - i  # Fractional part
    p, q, t = v * (1.0 - s), v * (1.0 - s * f), v * (1.0 - s * (1.0 - f))
    i %= 6
    if i == 0: r, g, b = v, t, p
    elif i == 1: r, g, b = q, v, p
    elif i == 2: r, g, b = p, v, t
    elif i == 3: r, g, b = p, q, v
    elif i == 4: r, g, b = t, p, v
    elif i == 5: r, g, b = v, p, q
    return rgb(int(r * 255), int(g * 255), int(b * 255))

# Initialize color picker state
def onAppStart(app):
    app.colorWheelCenter = (200, 200)
    app.colorWheelRadius = 100
    app.selectedColor = rgb(255,255,255)
    app.setMaxShapeCount(100000000)
    app.colorWheelImage = Image.open("draw/SCR-20241201-lsij.png").resize((200,200))


# Draw the color wheel and selection
def redrawAll(app):
    drawImage(CMUImage(app.colorWheelImage), app.colorWheelCenter[0]-app.colorWheelRadius,app.colorWheelCenter[1]-app.colorWheelRadius)
    drawRect(350, 150, 100, 100, fill=app.selectedColor, border='black', borderWidth=2)
    drawLabel("Selected Color", 400, 270, size=14, align='center')

# Draw a color wheel
def drawColorWheel(cx, cy, radius):
    for angle in range(360):  # Sweep 360 degrees
        for r in range(radius):  # Sweep radius
            hue = angle / 360
            saturation = r / radius
            color = hsvToRgb(hue, saturation, 1.0)
            x = cx + math.cos(math.radians(angle)) * r
            y = cy + math.sin(math.radians(angle)) * r
            drawRect(x, y, 3,3, fill=color)

# Detect user clicks and pick color
def onMousePress(app, mouseX, mouseY):
    cx, cy = app.colorWheelCenter
    dx, dy = mouseX - cx, mouseY - cy
    distance = math.sqrt(dx ** 2 + dy ** 2)
    if distance <= app.colorWheelRadius:
        # Convert to polar coordinates
        hue = (math.degrees(math.atan2(dy, dx)) + 360) % 360 / 360
        saturation = distance / app.colorWheelRadius
        app.selectedColor = hsvToRgb(hue, saturation, 1.0)
        print(app.selectedColor)

runApp()
