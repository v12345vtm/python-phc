
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()

#print("now =", now)

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string)

# !/bin/python

# importeer de GPIO bibliotheek.
import RPi.GPIO as GPIO
# Importeer de time biblotheek voor tijdfuncties.
from time import sleep

# Zet de pinmode op Broadcom SOC.
GPIO.setmode(GPIO.BCM)
# Zet waarschuwingen uit.
GPIO.setwarnings(False)


klaardonker = 4
sunrise =18

# Zet de GPIO pin als uitgang.
GPIO.setup(klaardonker, GPIO.OUT)
GPIO.setup(sunrise, GPIO.OUT)

try:
    while True:
        # Zet de LED aan.  io3 is altijd hoog standaat
        GPIO.output(klaardonker, 1)
        GPIO.output(sunrise, 1)
        # Wacht een seconde.
        sleep(1)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("date and time =", dt_string)
        # Zet de LED uit.
        GPIO.output(klaardonker, 0)
        GPIO.output(sunrise, 0)
        # Wacht een seconde.
        sleep(1)

except KeyboardInterrupt:
    # GPIO netjes afsluiten.
    GPIO.cleanup()