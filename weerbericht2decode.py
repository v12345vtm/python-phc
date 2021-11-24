import xml.etree.ElementTree as ET
tree = ET.parse('meteodump.xml')
root = tree.getroot()
import sys
print(sys.path)
"""
# one specific item attribute
print('Item #2 attribute:')
print(root[0][1].attrib)

# all item attributes
print('\nAll attributes:11')
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



# find the first 'item' object
print('\n test item vith:')

print(root.attrib)
print(root[0].tag) #location
print(root[0][0].tag) #interesting
print(root[0][1].tag) #day
print(root[0][1][0].tag) #symbol
print(root[0][1][1].tag) #tempmin
print(root[0][1][10].tag) #sun


x=0

for subelem in root[0][1]:
    print(subelem.tag + " met tagnummer=" +str(x))
    x=x+1

print('\n ******************* zonop-zonneer:')



print(root[0][1][10].attrib)   #{'in': '08:00', 'mid': '12:31', 'out': '17:02'}

print(root[0][1].attrib.get("name"))  #dag dat we vandaag zijn , vb zondag

print(root[0][1][10].attrib.get("in"))  # 8:00 zon op tijd
print(root[0][1][10].attrib.get("out"))  # 8:00 zonneer tijd
print('\n ******************* zonop-zonneer: 14novvith')


"""



zonop = (root[0][1][10].attrib.get("in"))  # 8:00 zon op tijd
zonneer = (root[0][1][10].attrib.get("out"))  # 8:00 zonneer tijd
vandaag = (root[0][1].attrib.get("name"))  #dag dat we vandaag zijn , vb zondag
print(zonop +" zon gaat op om")
print(zonneer+" zon gaat onder om")
print(vandaag)


##################################################


from datetime import datetime

# datetime object containing current date and time
now = datetime.now()

#print("now =", now)

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("rtc=", dt_string)




