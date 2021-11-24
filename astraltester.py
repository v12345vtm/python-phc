import datetime
import astral #from astral import LocationInfo  # in raspi terminal doe :sudo apt install python3-astral -y of pip3
from astral.sun import sun
from pytz import timezone
from time import sleep # Importeer de time biblotheek voor tijdfuncties.
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)  # Zet de pinmode op Broadcom SOC.
    GPIO.setwarnings(False)  # Zet waarschuwingen uit.
    schemer = 18  # gpio relais
    dag0nacht1 = 4  # gpio relais
    GPIO.setup(schemer, GPIO.OUT)  # Zet de GPIO pin als uitgang.
    GPIO.setup(dag0nacht1, GPIO.OUT)  # Zet de GPIO pin als uitgang.
    GPIO.output(schemer, 0) # zet uit
    GPIO.output(dag0nacht1, 0)
    GPIO.cleanup()
    print("gpio ok raspi")
except:
    print("geen  gpio op deze machine raspi")

#constanten
brussel =  timezone('Europe/Brussels')
loc = astral.LocationInfo(name='Dp-projects', region='Ingelmunster', timezone='Europe/Brussels', latitude=50.938527,longitude=3.779109)


#functies
def getzonneklok() :
    global standvandezonvandaag , rtc, dawntijd, sunrisetijd, sunsettijd, dusktijd, dawntijdmorgen , standvandezonmorgen
    standvandezonvandaag = sun(loc.observer,  date=astral.now(brussel)  ,tzinfo=loc.timezone)
    standvandezonmorgen = sun(loc.observer, date=astral.now(brussel)  + datetime.timedelta(days=1), tzinfo=loc.timezone)
    dawntijd = standvandezonvandaag['dawn']  # .strftime("%H:%M:%S")
    sunrisetijd = standvandezonvandaag['sunrise']  # .strftime("%H:%M:%S")
    sunsettijd = standvandezonvandaag['sunset']  # .strftime("%H:%M:%S")
    dusktijd = standvandezonvandaag['dusk']  # .strftime("%H:%M:%S")
    dawntijdmorgen = standvandezonmorgen['dawn']  # .strftime("%H:%M:%S")
    rtc = astral.now(brussel)
    print(f'      dawntijd {dawntijd}')  # 2021-11-23 07:36:12.214774+01:00
    print(f'   sunrisetijd {sunrisetijd}')
    print(f'    sunsettijd {sunsettijd}')
    print(f'      dusktijd {dusktijd}')
    print(f'dawntijdmorgen {dawntijdmorgen}')
    print(f'           RTC {rtc}')

#datenow = (time.strftime("%Y, %m, %d"))
#rtctijd  = (time.strftime("%H:%M:%S"))
#winteruur = time.daylight
#nutijd = astral.now().strftime("%H:%M:%S")
# astral.now(tzinfo: datetime.tzinfo = <UTC>) → datetime.datetime  "Europe/Brussels
#sunrisetijd = s['sunrise'].strftime("%H:%M:%S")
#        dawntijd 2021-11-23 07:36:12.214774+01:00
#     sunrisetijd 2021-11-23 08:14:24.873092+01:00
#      sunsettijd 2021-11-23 16:47:47.790356+01:00
#        dusktijd 2021-11-23 17:25:58.819066+01:00
#  dawntijdmorgen 2021-11-23 07:36:12.214774+01:00


def toontabellen() :
    rtc = astral.now(brussel)
    lijstvantijden = [rtc, dawntijd, sunrisetijd, sunsettijd, dusktijd, dawntijdmorgen]
    volgordetijden = sorted(lijstvantijden)

    for key in volgordetijden:
        if key == rtc:
            print(f'{key.strftime("%H:%M:%S")} <<<<<<rtc {watishetnubuiten}')

        if key == dawntijd:
            print(f'{key.strftime("%H:%M:%S")} dawntijd')

        if key == sunrisetijd:
            print(f'{key.strftime("%H:%M:%S")} sunrisetijd')

        if key == sunsettijd:
            print(f'{key.strftime("%H:%M:%S")} sunsettijd')

        if key == dusktijd:
            print(f'{key.strftime("%H:%M:%S")} dusktijd')

        if key == dawntijdmorgen:
            print(f'{key.strftime("%H:%M:%S")} dawntijd morgen')




##start
try:
    aaa = astral.now()
    print(f' {aaa} astral.now() zo niet gebruiken maar zo: astral.now(brussel)' )
    getzonneklok()

    while True:
        global watishetnubuiten
        startupdtijd = dawntijdmorgen.replace(hour=0 , minute=0 , second= 10)
        stopupdtijd = dawntijdmorgen.replace(hour=0, minute=1, second=10)
        if (rtc > startupdtijd) and (rtc < stopupdtijd):
            watishetnubuiten = "tis net middernacht geweest , upd zonnewijzer"
            getzonneklok()

        if (rtc > dawntijd) and (rtc < sunrisetijd):
            watishetnubuiten = "begint te klaren dawn"
            #print(watishetnubuiten)
            try:
                GPIO.output(dag0nacht1, 0)
                GPIO.output(schemer, 1)
            except:
                print("gpio-err klaren")


        elif (rtc > sunrisetijd) and (rtc < sunsettijd):
            watishetnubuiten = "dag"
            #print(watishetnubuiten)
            try:
                GPIO.output(dag0nacht1, 0)
                GPIO.output(schemer, 0)
            except:
                print("gpio-err dag")

        elif (rtc > sunsettijd) and (rtc < dusktijd):
            watishetnubuiten = "begint te donkeren"
            #print(watishetnubuiten)
            #dawntijd = dawntijd.replace(year=2000)
            #print(f'      edited dawntijd {dawntijd}')
            try:
                GPIO.output(dag0nacht1, 0)
                GPIO.output(schemer, 1)
            except:
                print("gpio-err donkeren")

        elif (rtc > dusktijd) and (rtc < dawntijdmorgen):
            watishetnubuiten = "nacht en paseren middernacht"
            #print(watishetnubuiten)
            #getzonneklok()
            try:
                GPIO.output(dag0nacht1, 1)
                GPIO.output(schemer, 0)
            except:
                print("gpio-err middernacht")

        elif (rtc > dusktijd) :
            watishetnubuiten = "nacht vroege ochtend"
            #print(watishetnubuiten)
            try:
                GPIO.output(dag0nacht1, 1)
                GPIO.output(schemer, 0)
            except:
                print("gpio-err vroegemorgen")


        sleep(1.5)
        print("loop")
        toontabellen()


except KeyboardInterrupt:
    print("KeyboardInterrupt cleaning gpio")
    # GPIO netjes afsluiten.
    GPIO.cleanup()