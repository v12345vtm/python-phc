
import requests
from requests.structures import CaseInsensitiveDict

url = "http://api.tameteo.nl/index.php?api_lang=nl&localidad=181688&affiliate_id=sy7xtza756tc&v=2.0&h=1"

headers = CaseInsensitiveDict()
headers["Accept"] = "*/*"


resp = requests.get(url, headers=headers)

#print(resp.status_code)
#print(resp.url)
#print(resp.headers)
print(resp.content)



f = open("demofile3.txt", "w")
#f.write("Woops! I have deleted the content!")
f.write(str(resp.content))
f.close()

#open and read the file after the appending:
f = open("demofile3.txt", "r")
print(f.read())