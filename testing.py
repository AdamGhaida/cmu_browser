from cmu_graphics import *
from bs4 import BeautifulSoup

class HTMLElement:
    def __init__(self, tag, attributes=None, children=None, text=""):
        self.tag = tag
        self.attributes = attributes or {}
        self.children = children or []
        self.text = text
        self.styles = {}

    def __repr__(self):
        return f"HTMLElement(tag={self.tag}, text={self.text}, attributes={self.attributes}, styles={self.styles})"

def parseHTML(html):
    soup = BeautifulSoup(html, "html.parser")
    print(soup)
    elements = []

    def parse_element(bs_element):
        tag = bs_element.name
        if tag is None:
            return None

        attributes = bs_element.attrs
        text = bs_element.get_text(strip=True) if bs_element.string else ""
        children = [parse_element(child) for child in bs_element.find_all(recursive=False)]
        children = [child for child in children if child is not None]

        return HTMLElement(tag=tag, attributes=attributes, children=children, text=text)

    # Parse the main body of the HTML
    root_elements = soup.body if soup.body else soup.contents
    for bs_element in root_elements:
        element = parse_element(bs_element)
        if element:
            elements.append(element)

    return elements

def parseCSS(css_text):
    css = {}

    # Split CSS into individual rules
    rules = css_text.split('}')
    for rule in rules:
        if '{' in rule:
            selector, properties = rule.split('{')
            selector = selector.strip()
            properties = properties.strip()

            # Parse properties
            property_dict = {}
            for prop in properties.split(';'):
                if ':' in prop:
                    name, value = prop.split(':')
                    property_dict[name.strip()] = value.strip()

            # Store rules by selector
            css[selector] = property_dict

    return css

def applyStyles(elements):
    for element in elements:
        if element.tag == "p":
            element.styles = {"color": "black", "font-size": 12}
        elif element.tag == "div":
            element.styles = {"color": "blue", "font-size": 14}
        # Add more styles as needed
        for child in element.children:
            applyStyles([child])



def drawElement(app, element, x, y):
    if element.tag == "p":
        drawLabel(element.text, x, y, 
                           fill=element.styles.get("color", "black"), 
                           font=("Arial"))
    elif element.tag == "div":
        drawRect(0, y, app.width, element.styles.get("height",100), fill=element.styles.get("color", "white"))
        drawLabel(element.text, x+100, y+15,
                           fill=element.styles.get("color", "black"), 
                           font=("Arial"))
    for child in element.children:
        y += 30  # Adjust for nested elements
        drawElement(app, child, x + 50, y)  # Indent nested elements

def applyCSSStyles(elements,css_rules):
    for element in elements:
        # Apply styles based on tag, id, and class
        if element.tag in css_rules:
            element.styles.update(css_rules[element.tag])
        
        # Apply class-based styles (CSS class selectors)
        class_name = element.attributes.get("class")
        if class_name:
            class_selector = f".{class_name}"
            if class_selector in css_rules:
                element.styles.update(css_rules[class_selector])

        # Apply ID-based styles (CSS ID selectors)
        element_id = element.attributes.get("id")
        if element_id:
            id_selector = f"#{element_id}"
            if id_selector in css_rules:
                element.styles.update(css_rules[id_selector])

        # Apply styles recursively to children
        for child in element.children:
            applyCSSStyles([child], css_rules)

def onAppStart(app):
    app.html = """
    <div id="main-container">Hello, World!
        <p class="highlight">This is a simple paragraph.</p>
        <div class="box">Another div with <p>nested paragraph.</p></div>
    </div>
    <div id="second">
        <p class="highlight">ibsdkfjn</p>
        <div class="box">Another div with <p>nested paragraph.</p></div>
    </div>"""
    app.elements = parseHTML(app.html)

    # Load CSS and apply it to elements
    css = """
    #main-container {
        color: green;
        background-color: yellow;
    }

    p {
        color: black;
        font-size: 16;
    }
    #second {
        color: yellow;
        background-color: yellow;

    }
    .box {
        background-color: blue;
        font-size: 14;
    }
    """

    applyCSSStyles(app.elements, parseCSS(css))

def redrawAll(app):
    y = 20
    for element in app.elements:
        drawElement(app, element, x=20, y=y)
        y += 50  # Adjust spacing between elements

runApp(width=400, height=300)
