from time import sleep
try:
    import serial
except:
    print("geen seral op gpio  '/dev/ttyAMA0' = uart toont geenc0 in fb  en ; '/dev/ttyUSB0' en  rs485usb ; '/dev/ttyUSB1'")


hoe_traag_antwoord_de_peha= 0.1 # in seconden  ;zeker niet korter dan 0.1s , want peha moet je laten uitspreken als hij antwoord
hoelangwillenwenogextrawachtenoppeharespons  = 5
com_port0 = "/dev/ttyUSB0" #usb to db9 convertor
com_port1 = "/dev/ttyUSB1" #rs485 adaptor
com_port2 = "/dev/ttyAMA0" #gpio uart met een max3232 adaptor


def zendenontvang(commando):
    try:
        ser = serial.Serial(
            port=com_port1,
            baudrate = 19200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.EIGHTBITS,
            timeout=1    )

        feedbackTabelVanPeha = list()  # creer lege list
        timoutvanwachten = hoelangwillenwenogextrawachtenoppeharespons
        ser.flush()
        sleep(0.1)
        #commando = "45 01 01 56 F1"
        zendtabel = commando.split(' ')
        for el in zendtabel:
            d = int(el ,16)
            dd = bytes([d])
            ser.write(dd)

        #print(f'bytesToRead voor sleep {ser.inWaiting()}')
        #sleep(hoe_traag_antwoord_de_peha)
        #print(f'bytesToRead na sleep {ser.inWaiting()}')

        while ser.inWaiting() ==0:

            for x in range (0,ser.inWaiting()+1):
                sleep(hoe_traag_antwoord_de_peha)
                print(f"   {ser.inWaiting()}   ik wacht ff iets timout {timoutvanwachten}")
                timoutvanwachten = timoutvanwachten -1
                if timoutvanwachten ==0:
                    print(f"                         send{commando}  fb geen ")
                    feedbackTabelVanPeha = None
                    return



        while ser.inWaiting() > 0:
            feedbackTabelVanPeha.clear() #wistabel
            for aantalelementen in range(0, ser.inWaiting()):
                x = ser.read().hex()
                feedbackTabelVanPeha.append(x)
        print(f"                         send{commando}  fb{feedbackTabelVanPeha} ")
        ser.close()

        return " ".join(feedbackTabelVanPeha)

    except Exception as e:
        print(f"{e} \n of geen seral op gpio  ofwel :exit prog , run on raspi instead/interpreter")


for x in range (0,30):
    print(f'testzending a {x}')
    print(zendenontvang("45 01 01 56 F1"))
    print (f'testzending b {x}')
    print(zendenontvang("45 81 01 9A 7D"))


