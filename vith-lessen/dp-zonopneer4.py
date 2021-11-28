from datetime import datetime, timedelta , time
#import datetime
from pytz import timezone
import pytz
import time
import astral # from astral import LocationInfo  # in raspi terminal doe :sudo apt install python3-astral -y of pip3
import RPi.GPIO as GPIO
from time import sleep # Importeer de time biblotheek voor tijdfuncties.
from astral.sun import sun





######
def toontijden() :
    dawntijd = standvandezonvandaag['dawn']  # .strftime("%H:%M:%S")
    sunrisetijd = standvandezonvandaag['sunrise']  # .strftime("%H:%M:%S")
    sunsettijd = standvandezonvandaag['sunset']  # .strftime("%H:%M:%S")
    dusktijd = standvandezonvandaag['dusk']  # .strftime("%H:%M:%S")
    tomorrow = datetime.now().astimezone(timezone('Europe/Brussels')) + timedelta(days=1)
    standvandezonmorgen = sun(loc.observer, date=tomorrow, tzinfo=loc.timezone)  # standvandezonmorgen komt klaar om
    dawntijdstandvandezonmorgen = standvandezonmorgen['dawn']  # .strftime("%H:%M:%S")
    lokalertc =  datetime.now().astimezone(timezone("Europe/Brussels")) ##RTC mogen we wel contnue updaten
    lijstvantijden = [lokalertc, dawntijd, sunrisetijd, sunsettijd, dusktijd, dawntijdstandvandezonmorgen]
    volgordetijden = sorted(lijstvantijden)
    print("-*-*-*-*toontijden")
    for key in volgordetijden:
        if key == lokalertc:
            print(f'{key.strftime("%H:%M:%S")} <---RTC {watishetnubuiten} schemerrelais:{GPIO.input(schemer) }  dag0nacht1:{GPIO.input(dag0nacht1) }  +++--- {datetime.now().astimezone(timezone("Europe/Brussels"))} ')

        if key == dawntijd:
            print(f'{key.strftime("%H:%M:%S")} dawntijd')

        if key == sunrisetijd:
            print(f'{key.strftime("%H:%M:%S")} sunrisetijd')

        if key == sunsettijd:
            print(f'{key.strftime("%H:%M:%S")} sunsettijd')

        if key == dusktijd:
            print(f'{key.strftime("%H:%M:%S")} dusktijd')

        if key == dawntijdstandvandezonmorgen:
            print(f'{key.strftime("%H:%M:%S")} dawntijd morgen')


########


def updatezonnekalender() :
    # update de zonopkalender
    begin_of_day_datetime = datetime.now().astimezone(timezone('Europe/Brussels')).replace(hour=update_tijdstip_uur, minute=update_tijdstip_minuut-5, second=0, microsecond=0)
    end_of_day_datetime = datetime.now().astimezone(timezone('Europe/Brussels')).replace(hour=update_tijdstip_uur, minute=update_tijdstip_minuut, second=0,microsecond=0)
    winteruur = time.daylight
    lokalertc = datetime.now().astimezone(timezone('Europe/Brussels'))
    klokje = lokalertc.strftime("%H:%M:%S")
    #print(f"\nklokje {klokje} {watishetnubuiten}")
    standvandezonvandaag = sun(loc.observer, tzinfo=loc.timezone)  # vandaag
    standvandezonmorgen = sun(loc.observer, date=datetime.now().astimezone(timezone('Europe/Brussels')) + timedelta(days=1), tzinfo=loc.timezone)  # standvandezonmorgen komt klaar om
    dawntijd = standvandezonvandaag['dawn']  # .strftime("%H:%M:%S")
    sunrisetijd = standvandezonvandaag['sunrise']  # .strftime("%H:%M:%S")
    sunsettijd = standvandezonvandaag['sunset']  # .strftime("%H:%M:%S")
    middagtijd = standvandezonvandaag['noon']  # .strftime("%H:%M:%S")  ## smiddags doen we een herberekening
    dusktijd = standvandezonvandaag['dusk']  # .strftime("%H:%M:%S")
    tomorrow = datetime.now().astimezone(timezone('Europe/Brussels')) + timedelta(days=1)
    standvandezonmorgen = sun(loc.observer, date=tomorrow, tzinfo=loc.timezone)  # standvandezonmorgen komt klaar om
    dawntijdstandvandezonmorgen = standvandezonmorgen['dawn']  # .strftime("%H:%M:%S")
    print("-*-*-*-*berekende net niewe getijden upd")



tomorrow = datetime.now().astimezone(timezone('Europe/Brussels'))+ timedelta(days=1) #init
lokalertc = datetime.now().astimezone(timezone('Europe/Brussels')) #init




loc = astral.LocationInfo(name='Dp-projects', region='Ingelmunster', timezone='Europe/Brussels', latitude=50.938527,longitude=3.779109)
GPIO.setmode(GPIO.BCM)# Zet de pinmode op Broadcom SOC.
GPIO.setwarnings(False)# Zet waarschuwingen uit.
schemer = 18 #gpio relais
dag0nacht1 =4 #gpio relais

update_tijdstip_uur = 0
update_tijdstip_minuut = 6 ##  6-5 = 00:01start en 00:06 stop

watishetnubuiten = "init"
GPIO.setup(schemer, GPIO.OUT) # Zet de GPIO pin als uitgang.
GPIO.setup(dag0nacht1, GPIO.OUT) # Zet de GPIO pin als uitgang.


tgttg = datetime.now().astimezone(timezone('Europe/Brussels')).strftime("%H:%M:%S")


standvandezonvandaag = sun(loc.observer, tzinfo=loc.timezone)  #vandaag
standvandezonmorgen = sun(loc.observer, date=datetime.now() + timedelta(days=1), tzinfo=loc.timezone) #standvandezonmorgen komt klaar om
dawntijd = standvandezonvandaag['dawn']  # .strftime("%H:%M:%S")
sunrisetijd = standvandezonvandaag['sunrise']  # .strftime("%H:%M:%S")
sunsettijd = standvandezonvandaag['sunset']  # .strftime("%H:%M:%S")
dusktijd = standvandezonvandaag['dusk']  # .strftime("%H:%M:%S")
dawntijdstandvandezonmorgen = standvandezonmorgen['dawn']  # .strftime("%H:%M:%S")
begin_of_day_datetime = datetime.now().astimezone(timezone('Europe/Brussels')).replace(hour=update_tijdstip_uur, minute=update_tijdstip_minuut-5, second=0, microsecond=0)
end_of_day_datetime = datetime.now().astimezone(timezone('Europe/Brussels')).replace(hour=update_tijdstip_uur, minute=update_tijdstip_minuut, second=0, microsecond=0)
middagtijd = standvandezonvandaag['noon']
#dawntijdstandvandezonmorgen = datetime.now().astimezone(timezone('Europe/Brussels'))+ timedelta(seconds=10)

#dehoeveelstezijnwevandaag = standvandezonvandaag['sunrise'].day

print("starting dp-zonopneer4.py and calculate zon van vandaag en morgen")
#updatezonnekalender()



try:
    while True:
        print("\n\n-*-*-*-*loop checkt :wat ist nu buiten")

        if (5 >  6 ) and ( 8 <  5 ):
            print("WEL upd nodig vd getijden")
            updatezonnekalender()
        else:
            print("geen upd nodig vd getijden")

        if ( datetime.now().astimezone(timezone('Europe/Brussels')).strftime("%H:%M:%S") > begin_of_day_datetime.strftime("%H:%M:%S")  ) and (datetime.now().astimezone(timezone('Europe/Brussels') ).strftime("%H:%M:%S") < end_of_day_datetime.strftime("%H:%M:%S") ):
            print("oudWEL upd nodig vd getijden")
            #updatezonnekalender()
        else:
            print("oudgeen upd nodig vd getijden")


        if ( datetime.now().astimezone(timezone('Europe/Brussels')) > dawntijd) and (datetime.now().astimezone(timezone('Europe/Brussels'))< sunrisetijd):
            watishetnubuiten = "begint te klaren + upd"
            print(watishetnubuiten)
            GPIO.output(dag0nacht1, 1)
            GPIO.output(schemer, 1)



        elif (datetime.now().astimezone(timezone('Europe/Brussels')) > sunrisetijd) and (datetime.now().astimezone(timezone('Europe/Brussels')) < sunsettijd):
            watishetnubuiten = "tis klaar buiten"
            print(watishetnubuiten)
            GPIO.output(dag0nacht1, 0)
            GPIO.output(schemer, 0)


        elif (datetime.now().astimezone(timezone('Europe/Brussels')) > sunsettijd) and (datetime.now().astimezone(timezone('Europe/Brussels'))< dusktijd):
            watishetnubuiten = "begint te donkeren"
            print(watishetnubuiten)
            #print(datetime.now().astimezone(timezone('Europe/Brussels')))
            #print(sunsettijd)
            #print(dusktijd)
            GPIO.output(dag0nacht1, 0)
            GPIO.output(schemer, 1)

        elif (datetime.now().astimezone(timezone('Europe/Brussels')) > dusktijd) and (datetime.now().astimezone(timezone('Europe/Brussels')) < dawntijdstandvandezonmorgen):
            watishetnubuiten = "nacht"
            print(f"******  {watishetnubuiten } ****** {datetime.now().astimezone(timezone('Europe/Brussels'))}")
            GPIO.output(dag0nacht1, 1)
            GPIO.output(schemer, 0)

        else:
            watishetnubuiten = "geenidee"
            print(f"else dawntijd {dawntijd}")
            print(f"sunrisetijd {sunrisetijd}")
            print(f"sunsettijd {sunsettijd}")
            print(f"dusktijd {dusktijd}")
            print(f"lokalertc {datetime.now().astimezone(timezone('Europe/Brussels'))}")
            print(f"dawntijdstandvandezonmorgen {dawntijdstandvandezonmorgen}\n")
            sleep(1800)



        #updatezonnekalender()
        toontijden()
        sleep(1.5)





except KeyboardInterrupt:
    # GPIO netjes afsluiten.
    GPIO.cleanup()




debugterfhj = 17
