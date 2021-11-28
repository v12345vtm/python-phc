from datetime import datetime, timedelta
import pytz
import time




tomorrow = datetime.now() + timedelta(days=1)
tomorrow_formatted = tomorrow.strftime('%d/%m/%Y')

ndatumenuur = datetime.now()
numeteenuurwerk = datetime.now().strftime("%H:%M:%S")
datumentijdobjekt = datetime.now()
dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


lokalertc = pytz.utc.localize(datetime.now())
datenow = (time.strftime("%Y, %m, %d"))
rtctijd = (time.strftime("%H:%M:%S"))
dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
winteruur = time.daylight

# from astral import LocationInfo  # in raspi terminal doe :sudo apt install python3-astral -y of pip3
import astral

loc = astral.LocationInfo(name='Dp-projects', region='Ingelmunster', timezone='Europe/Brussels', latitude=50.938527,longitude=3.779109)

nutijdastral = astral.now().strftime("%H:%M:%S")
astralismis = astral.now()

from astral.sun import sun

s = sun(loc.observer, tzinfo=loc.timezone)  #vandaag
morgen = sun(loc.observer, date=tomorrow, tzinfo=loc.timezone) #morgen komt klaar om

#sunrisetijd = s['sunrise'].strftime("%H:%M:%S")
#dawntijd = s['dawn'].strftime("%H:%M:%S")
#sunsettijd = s['sunset'].strftime("%H:%M:%S")
#dusktijd = s['dusk'].strftime("%H:%M:%S")

dawntijd = s['dawn']  # .strftime("%H:%M:%S")
sunrisetijd = s['sunrise']  # .strftime("%H:%M:%S")
sunsettijd = s['sunset']  # .strftime("%H:%M:%S")
dusktijd = s['dusk']  # .strftime("%H:%M:%S")
dawntijdmorgen = morgen['dawn']  # .strftime("%H:%M:%S")

dehoeveelstezijnwevandaag = s['sunrise'].day

print("dp-zonopneer.py")

print(f"dawntijd {dawntijd}")
print(f"sunrisetijd {sunrisetijd}")
print(f"sunsettijd {sunsettijd}")
print(f"dusktijd {dusktijd}")
print(f"\nlokalertc {lokalertc}")
print(f"winteruur {winteruur}")

print(f"dawntijdmorgen {dawntijdmorgen}\n")

if (lokalertc > dawntijd) and (lokalertc < sunrisetijd):
    print("begint te klaren")

if (lokalertc > sunrisetijd) and (lokalertc < sunsettijd):
    print("tis klaar")

if (lokalertc > sunsettijd) and (lokalertc < dusktijd):
    print("begint te donkeren")

if (lokalertc > dusktijd)and (lokalertc < dawntijdmorgen)  :
    print("nacht ")







debugterfhj = 17
