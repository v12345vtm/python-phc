
import requests
from requests.structures import CaseInsensitiveDict

url = "http://api.tameteo.nl/index.php?api_lang=nl&localidad=181688&affiliate_id=sy7xtza756tc&v=2.0"

headers = CaseInsensitiveDict()
headers["Accept"] = "*/*"


resp = requests.get(url, headers=headers)




#print(resp.status_code)
#print(resp.url)
#print(resp.headers)
#print(resp.content) #raw bytes
print(resp.text)  #string


f = open("meteodump.xml", "wb")
#f.write("Woops! I have deleted the content!")
f.write(resp.content)
f.close()

#open and read the file after the appending:
f = open("meteodump.xml", "r")
print(f.read())
f.close()



import xml.etree.ElementTree as ET
tree = ET.parse('meteodump.xml')
root = tree.getroot()

# one specific item attribute
print('Item #2 attribute:')
print(root[0][1].attrib)

# all item attributes
print('\nAll attributes:')
for elem in root:
    for subelem in elem:
        print(subelem.attrib)

# one specific item's data
print('\nItem #2 data:')
print(root[0][1].text)

# all items data
print('\nAll item data:')
for elem in root:
    for subelem in elem:
        print(subelem.text)