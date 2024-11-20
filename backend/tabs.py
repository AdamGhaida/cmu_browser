import json 

with open('tabs.json', 'r') as file:
    data = json.load(file)

# Print the data
print(data)