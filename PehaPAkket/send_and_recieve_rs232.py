hoe_traag_antwoord_de_peha= 0.1 # in seconden  ;zeker niet korter dan 0.1s , want peha moet je laten uitspreken als hij antwoord
hoelangwillenwenogextrawachtenoppeharespons  = 5
##Comment out de poort die je niet wil gebruiken

#com_portraspi = "/dev/ttyUSB0" #usb to db9 convertor
com_portraspi = "/dev/ttyUSB1" #rs485 adaptor
#com_portraspi = "/dev/ttyAMA0" #gpio uart met een max3232 adaptor

com_portwin = "COM8"
#deze file is gebaseert op rs485debugmoos.py , die als beta tester diende


from time import sleep #bestaat op win en raspi
import serial #bestaat op win10 en raspi , en pyserial nemen !!!!!!
import sys

#print(sys.executable) #/usr/bin/python3 bij raspi  en C:\Users\vith\AppData\Local\Programs\Python\Python39\python.exe
machine = ""
beschikbare_poorten = list()
beschikbare_poorten_metomschrijving = list()
if "/" in  (sys.executable) : machine = "raspi"
if ":" in  (sys.executable) : machine = "windows"

#print(machine)


if machine == "raspi":
    try:
        import serial.tools.list_ports  # op raspi bestaat dit om de comport /dev/tty/USB te vinden
        tty = ( (serial.tools.list_ports.comports()))  # raspi comportd
        for raspicomport in tty:
            #print(raspicomport)
            str_ttyport = str(raspicomport).split(" ")

            beschikbare_poorten.append(str_ttyport[0])
            beschikbare_poorten_metomschrijving.append(raspicomport)
    except Exception as e:
        print(
            f" {e} , raspi kent geen serial of geen dev/tty poorten")

if machine == "windows":
    try:
        import wmi  # WMI voor win10laptop om u compoort te vinden COM
        query = "SELECT * FROM Win32_PnPEntity WHERE Name LIKE '%(COM%)'"
        coms = wmi.WMI().query(query)
        for com in coms:
            #print(com.Name) #vb 'USB-SERIAL CH340 (COM8)'
            str_comport = com.name
            startpos =  str_comport.find("(")
            stoppos = str_comport.find(")")
            str_comport = str_comport[startpos+1:stoppos]
            beschikbare_poorten.append(str_comport)
            beschikbare_poorten_metomschrijving.append(com.name)
    except Exception as e:
        print(
            f" {e}   ,of win10 kent geen WMI bibliotheek of heeft  geen COMpoorten")


for uarts in   beschikbare_poorten_metomschrijving:
    print(f'             gevonden op {machine} : poort:{uarts}')


def zendenontvang(commando , doe_alsof_er_een_peha_antwoord = None):
    if doe_alsof_er_een_peha_antwoord == "geldig":
        return "45 02 00 03 1D 03"

    if doe_alsof_er_een_peha_antwoord == "brol":
        return "FF FF 00 21 AF CD"

    if doe_alsof_er_een_peha_antwoord == "mislukt":
        return None

    try:
        if machine == "raspi":
            if com_portraspi in beschikbare_poorten:
                ser = serial.Serial(            port=com_portraspi,            baudrate = 19200,            parity=serial.PARITY_NONE,            stopbits=serial.STOPBITS_TWO,            bytesize=serial.EIGHTBITS,            timeout=1)
            else:
                print("geen geldige linuxcomport")
                return None

        if machine == "windows":
            if(com_portwin in beschikbare_poorten):
                ser = serial.Serial(            port=com_portwin,            baudrate = 19200,            parity=serial.PARITY_NONE,            stopbits=serial.STOPBITS_TWO,            bytesize=serial.EIGHTBITS,            timeout=1)
            else:
                print("geen geldige wincomport")
                return None

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

        while ser.inWaiting() ==0:
            for x in range (0,ser.inWaiting()+1):
                sleep(hoe_traag_antwoord_de_peha)
                timoutvanwachten = timoutvanwachten -1
                if timoutvanwachten ==0:
                    return None #exit functie

        while ser.inWaiting() > 0:
            feedbackTabelVanPeha.clear() #wistabel
            for aantalelementen in range(0, ser.inWaiting()):
                x = ser.read().hex()
                feedbackTabelVanPeha.append(x)
        ser.close()

        return " ".join(feedbackTabelVanPeha)

    except Exception as e:
        print(f"{e}  ")






for x in range (0,10):
    print(zendenontvang("45 01 01 56 F1" , "virt")  )
    print(zendenontvang("45 81 01 9A 7D"))




