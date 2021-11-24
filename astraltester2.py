from datetime import datetime, timedelta
import pytz
from pytz import timezone
import time
import astral # from astral import LocationInfo  # in raspi terminal doe :sudo apt install python3-astral -y of pip3
#import RPi.GPIO as GPIO
from time import sleep # Importeer de time biblotheek voor tijdfuncties.
from astral.sun import sun

format = "%Y-%m-%d %H:%M:%S %Z%z"

#tomorrow = datetime.now() + timedelta(days=1) #init
lokalertc = pytz.utc.localize(datetime.now())#init

def updatezonnekalender() :
    # update de zonopkalender
    tomorrow = datetime.now() + timedelta(days=1)
    winteruur = time.daylight
    lokalertc = datetime.now().astimezone(timezone('Europe/Brussels'))
    klokje = lokalertc.strftime("%H:%M:%S")
    print(f"\nklokje {klokje} {watishetnubuiten}")
    standvandezonvandaag = sun(loc.observer, tzinfo=loc.timezone)  # vandaag
    standvandezonmorgen = sun(loc.observer, date=tomorrow, tzinfo=loc.timezone)  # standvandezonmorgen komt klaar om
    dawntijd = standvandezonvandaag['dawn']  # .strftime("%H:%M:%S")
    sunrisetijd = standvandezonvandaag['sunrise']  # .strftime("%H:%M:%S")
    sunsettijd = standvandezonvandaag['sunset']  # .strftime("%H:%M:%S")
    dusktijd = standvandezonvandaag['dusk']  # .strftime("%H:%M:%S")
    dawntijdstandvandezonmorgen = standvandezonmorgen['dawn']  # .strftime("%H:%M:%S")
    dehoeveelstezijnwevandaag = standvandezonvandaag['sunrise'].day
    print(f"dawntijd {dawntijd}")
    print(f"sunrisetijd {sunrisetijd}")
    print(f"sunsettijd {sunsettijd}")
    print(f"dusktijd {dusktijd}")
    print(f"lokalertc {lokalertc}")


    print(f"winteruur {winteruur}")
    print(f"dawntijdstandvandezonmorgen {dawntijdstandvandezonmorgen}\n")

loc = astral.LocationInfo(name='Dp-projects', region='Ingelmunster', timezone='Europe/Brussels', latitude=50.938527,longitude=3.779109)

for tz in pytz.all_timezones:
    print (tz) # Europe/Brussels



#GPIO.setmode(GPIO.BCM)# Zet de pinmode op Broadcom SOC.
#GPIO.setwarnings(False)# Zet waarschuwingen uit.
schemer = 4 #gpio relais
dag0nacht1 =14 #gpio relais
watishetnubuiten = "init"
#GPIO.setup(schemer, GPIO.OUT) # Zet de GPIO pin als uitgang.
#GPIO.setup(dag0nacht1, GPIO.OUT) # Zet de GPIO pin als uitgang.


standvandezonvandaag = sun(loc.observer, tzinfo=loc.timezone)  #vandaag
standvandezonmorgen = sun(loc.observer, date=datetime.now() + timedelta(days=1), tzinfo=loc.timezone) #standvandezonmorgen komt klaar om
dawntijd = standvandezonvandaag['dawn']  # .strftime("%H:%M:%S")
sunrisetijd = standvandezonvandaag['sunrise']  # .strftime("%H:%M:%S")
sunsettijd = standvandezonvandaag['sunset']  # .strftime("%H:%M:%S")
dusktijd = standvandezonvandaag['dusk']  # .strftime("%H:%M:%S")
dawntijdstandvandezonmorgen = standvandezonmorgen['dawn']  # .strftime("%H:%M:%S")
dehoeveelstezijnwevandaag = standvandezonvandaag['sunrise'].day


lijstvantijden = [lokalertc , dawntijd ,sunrisetijd , sunsettijd ,  dusktijd , dawntijdstandvandezonmorgen  ]
volgordetijden = sorted(lijstvantijden)


for key in volgordetijden:
    #print(f'{key.strftime("%H:%M:%S")}'  )
    if key ==  lokalertc:
        print(f'{key.strftime("%H:%M:%S")} <---RTC')

    else:
        print(f'{key.strftime("%H:%M:%S")}')


#print(volgordetijden)


print("starting dp-zonopneer4.py and calculate zon van vandaag en morgen")
updatezonnekalender()



try:
    while True:
        if (pytz.utc.localize(datetime.now()) > dawntijd) and (pytz.utc.localize(datetime.now()) < sunrisetijd):
            watishetnubuiten = "begint te klaren"
            print(watishetnubuiten)
            # GPIO.output(dag0nacht1, 1)
            # GPIO.output(schemer, 1)


        if (pytz.utc.localize(datetime.now()) > sunrisetijd) and (pytz.utc.localize(datetime.now()) < sunsettijd):
            watishetnubuiten = "tis klaar buiten"
            print(watishetnubuiten)
            #GPIO.output(dag0nacht1, 0)
            #  GPIO.output(schemer, 0)


        if (  pytz.utc.localize(datetime.now()  ) > sunsettijd)  and (pytz.utc.localize(datetime.now()) < dusktijd):
            watishetnubuiten = "begint te donkeren"
            print(watishetnubuiten)

            print(pytz.utc.localize(datetime.now()))

            print(sunsettijd)
            print(dusktijd)
            # GPIO.output(dag0nacht1, 0)
            # GPIO.output(schemer, 1)

        if (pytz.utc.localize(datetime.now()) > dusktijd) and (pytz.utc.localize(datetime.now()) < dawntijdstandvandezonmorgen):
            watishetnubuiten = "nacht"
            print(f"******  {watishetnubuiten } ****** {pytz.utc.localize(datetime.now())}")
            #GPIO.output(dag0nacht1, 1)
            #GPIO.output(schemer, 0)


        updatezonnekalender()
        sleep(1)





except KeyboardInterrupt:
    # GPIO netjes afsluiten.
    #GPIO.cleanup()
    debgterfhj = 17
