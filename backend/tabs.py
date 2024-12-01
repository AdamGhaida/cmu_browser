import json 
import os
from .jsonParser import JSONParser

class tabsClass:

    def __init__(self):
        scriptDir = os.path.dirname(os.path.abspath(__file__))
        self.jsonPath = os.path.join(scriptDir, "tabs.json")


        self.JSONInterface = JSONParser()
        
        self.parsedTabs = self.parseTabs()


    def parseTabs(self):
        return self.JSONInterface.parse(self.readData())
    
    def addTab(self, tabName, tabURL, faviconURL=""):        
        # If the "tabs" key doesn't exist, initialize it
        if "tabs" not in self.parsedTabs:
            self.parsedTabs["tabs"] = []
        
        # Create the new tab entry
        newTabDict = {
            "favicon": faviconURL,
            "name": tabName,
            "url": tabURL
        }

        # Append the new tab to the list of tabs
        self.parsedTabs["tabs"].append(newTabDict)

        # Convert the dictionary back to JSON string format
        newJsonStr = self.JSONInterface.dictToJSONString(self.parsedTabs)

        # Write the updated JSON back to the file
        
        self.writeData(newJsonStr)
        print(f"Tab '{tabName}' added successfully.")

    def removeTab(self, index):
        removedTab = self.parsedTabs["tabs"].pop(index)

        # Convert the updated dictionary back to JSON
        newJsonStr = self.JSONInterface.dictToJSONString(self.parsedTabs)
        self.writeData(newJsonStr)
        

    def readData(self):
        with open(self.jsonPath, 'r') as JSONFile:
            return JSONFile.read()

    def writeData(self,data):
        with open(self.jsonPath, 'w') as JSONFile:
            JSONFile.write(data)

    def uploadData(self, newJsonObject):
        newTab = json.dump(newJsonObject)
        self.tabsFile["tabs"].append(newTab)


