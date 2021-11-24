
from datetime import datetime

# datetime object containing current date and time
ndatumenuur = datetime.now()
numeteenuurwerk = datetime.now().strftime("%H:%M:%S")



# dd/mm/YY H:M:S
datumentijdobjekt =  datetime.now()
dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
#print("date and time =", dt_string)

import time
datenow = (time.strftime("%Y, %m, %d"))
rtctijd  = (time.strftime("%H:%M:%S"))
dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
winteruur = time.daylight
#print (datenow)



#from astral import LocationInfo  # in raspi terminal doe :sudo apt install python3-astral -y of pip3
import astral
loc = astral.LocationInfo(name='Dp-projects', region='Ingelmunster', timezone='Europe/Brussels', latitude=50.938527,longitude=3.779109)


nutijdastral = astral.now().strftime("%H:%M:%S")

astralismis = astral.now()
#print(astralismis)
#print(astral.today())

#print(loc)
# LocationInfo(name='SJC', region='CA, USA', timezone='America/Los_Angeles',
#   latitude=37.3713439, longitude=-121.944675)
#print(loc.observer)
# Observer(latitude=37.3713439, longitude=-121.944675, elevation=0.0) datetime.datetime.utcnow().replace(tzinfo=utc)


from astral.sun import sun

s = sun(loc.observer, tzinfo=loc.timezone)




#print(f'\nsunrise:  {s["sunrise"]} en ook '  )
#print(f'Sunset:  {s["sunset"]}  '  )


#print(s.keys() )
#xa = s['sunrise']
#xb = s['sunrise'].strftime("%d/%m/%Y")

sunrisetijd = s['sunrise'].strftime("%H:%M:%S")
dawntijd = s['dawn'].strftime("%H:%M:%S")
sunsettijd = s['sunset'].strftime("%H:%M:%S")
dusktijd = s['dusk'].strftime("%H:%M:%S")


sunrisetijd = s['sunrise']#.strftime("%H:%M:%S")
dawntijd = s['dawn']#.strftime("%H:%M:%S")
sunsettijd = s['sunset']#.strftime("%H:%M:%S")
dusktijd = s['dusk']#.strftime("%H:%M:%S")


xx = s['sunrise'].day
#print(s['sunrise'])

print("dp-zonopneer.py")
print(f"sunrisetijd {sunrisetijd}")
print(f"dawntijd {dawntijd}")
print(f"sunsettijd {sunsettijd}")
print(f"dusktijd {dusktijd}")
print(f"nutijd {datumentijdobjekt}")
print(f"winteruur {winteruur}")




debugterfhj=17