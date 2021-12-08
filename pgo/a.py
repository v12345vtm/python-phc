import responsanalyzer #zegt adhv lange fb respons welke module stand er telkens is
import pehamodule

hoe_traag_antwoord_de_peha= 0.1 # in seconden  ;zeker niet korter dan 0.1s , want peha moet je laten uitspreken als hij antwoord
hoelangwillenwenogextrawachtenoppeharespons  = 5
##Comment out de poort die je niet wil gebruiken

com_portraspi = "/dev/ttyUSB0" #usb to db9 convertor
#com_portraspi = "/dev/ttyUSB1" #rs485 adaptor
#com_portraspi = "/dev/ttyAMA0" #gpio uart met een max3232 adaptor

com_portwin = "COM9"

#init
serielepoort = ""
lijstmetpaketjes= list()

from time import sleep #bestaat op win en raspi
import serial #bestaat op win10 en raspi , en pyserial nemen !!!!!!
import sys
import time



print(time.strftime("%H:%M:%S", time.localtime()))

#print(sys.executable) #/usr/bin/python3 bij raspi  en C:\Users\vith\AppData\Local\Programs\Python\Python39\python.exe
print( (time.time() * 1000))
machine = ""
beschikbare_poorten = list()
beschikbare_poorten_metomschrijving = list()
zekeringkastvol = pehamodule.pehamodule()
zekeringkastvol.setData("45 82 01 02 a0 07")
zekeringkastvol.setData("46 82 01 02 a0 07")
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
        print (f'selected port={com_portraspi}')
    except Exception as e:
        print(f"{e} , raspi kent geen serial of geen dev/tty poorten ")

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
        print(f'\n\t\tSELECTED PORT={com_portwin}')
    except Exception as e:
        print(f" {e}   ,of win10 kent geen WMI bibliotheek of heeft  geen COMpoorten")

print( (time.time() * 1000))
for uarts in   beschikbare_poorten_metomschrijving:
    print(f' gevonden op {machine} : poort:{uarts} ')
print( (time.time() * 1000))



def opencompoort():
    global serielepoort
    if machine == "raspi":
        if com_portraspi in beschikbare_poorten:
            serielepoort = serial.Serial(port=com_portraspi, baudrate=19200, parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_TWO, bytesize=serial.EIGHTBITS, timeout=1)
            print("linuxcomport OPEN")
        else:
            print("geen geldige linuxcomport")


    if machine == "windows":
        if (com_portwin in beschikbare_poorten):
            serielepoort = serial.Serial(port=com_portwin, baudrate=19200, parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_TWO, bytesize=serial.EIGHTBITS, timeout=1)
            print("comport OPEN")

        else:
            print("geen geldige wincomport")


###############################
def main():
    while 1:
        try:
            pollingcompoort()

            #print("\nHOOFDPROGRAMMA")
            #sleep(2)
            # print(zend("44 82 01 3f 7d f1"))  # wat is u firmware

            for x in range(0, 256):
                hexadres = "%0.2X" % x
                p1 = str(hexadres) + " 01 01"
                # zend(crcberekenen(p1))
                # print(p1)
            # Optional, but recommended: sleep 10 ms (0.01 sec) once per loop to let
            # other threads on your PC run during this time.
            time.sleep(0.01)

        except Exception as e:
            print(e)
            print("pollingserial.py eeiwigelus")





###############################

def pollingcompoort():
    global serielepoort , lijstmetpaketjes
    if serielepoort.inWaiting() > 0:
        sleep(hoe_traag_antwoord_de_peha)
        starttijd = time.time() * 1000
        hoeveelbytekregenwebinnen = serielepoort.inWaiting()
        #print("ik krijg xxx bytes binnen als respons : " + str(serielepoort.inWaiting()) + "\n")
        feedback="" #wistabel
        for aantalelementen in range(0, serielepoort.inWaiting()):
            x = serielepoort.read().hex()
            feedback = feedback + " " + x
            #print(feedback)
            if serielepoort.inWaiting() ==0:
                #print("\n")
                #print(feedback)
                stoptijd = time.time() * 1000
                duurtijd = stoptijd - starttijd
                rtctimestamp= time.strftime("%H:%M:%S", time.localtime())
                print(f" {rtctimestamp} ,ik krijg xxx bytes binnen als respons : " + str(hoeveelbytekregenwebinnen) + ":  " +str(feedback)+" " +"en dat duurde millisec" + str(duurtijd)  )

                #we kunnen nu de fb verkappen , da kan lang zijn, dat kan kort zijn in aantal rs485paketjes
                #sleep(6)
                try:
                    if hoeveelbytekregenwebinnen < 5:
                        print("we kregen geen volledig rs485pakt of enkel wat storing binnen")
                        feedback = "brol"
                    else:
                        #de respons is nu een crc validated lijst met paketjes
                        lijstmetpaketjes =  verkaplangantwoordvanpeha(feedback)
                except Exception as e:
                    print(e)
                    print("error door functie:verkaplangerespons zijn schuld")

                #print(lijstmetpaketjes)
                for pakketje in lijstmetpaketjes:
                    responsanalyzer.respons_analyser(pakketje)
                    #print(pakketje)

                erx=7878


    #sleep(2)
    #print(".")
    #print(zend("44 82 01 3f 7d f1"))  # wat is u firmware
    #hoofdprogramma() #run hoofdprogrammafunctie

###############################




def zend(commando  ):
    try:
        feedbackTabelVanPeha = list()  # creer lege list
        serielepoort.flush()
        sleep(0.1)
        #print(f'commando {commando}')
        #commando = "45 01 01 56 F1"
        zendtabel = commando.split(' ')
        for el in zendtabel:
            d = int(el ,16)
            dd = bytes([d])
            serielepoort.write(dd)
        sleep(hoe_traag_antwoord_de_peha)
        return  commando + " :zend gelukt"

    except Exception as e:
        print(e)
        return  commando + ":zend mislukt"


###############################


def verkaplangantwoordvanpeha(langestring):
    trimmed = langestring.upper().rstrip().lstrip()
    strtabel = trimmed.split(" ")
    tabel = list()
    for el in strtabel:
        tabel.append(int(el, 16)) #decimaale notatie
    while tabel[0] == 0:
        tabel.pop(0) #remove first element if its 0
    str2bin = bin(tabel[1])[2:].zfill(8)
    alleantwoordenineenlijst = list()
    while len(tabel)>0:
        #potentieele data pakketjes (rs485pakket)
        i=0
        tempaantaalbytesdievolgen = tabel[i+1] & int(15)  #decimaal #indien togglebit is 1 , doe em weg
        #als aantalbytesdievolgen groter is dan 8F , kan dat niet zijn
        if tempaantaalbytesdievolgen > 15: #paketten kunnen officieel niet langer zijn dan 15data bytes
            print("skip deze")
            tabel.pop(0)
            strtabel.pop(0)
            if len(tabel) <5:
                print("we hebben brol over")
                tabel.clear()
                strtabel.clear()

        else:



            tempalldata = ""
            tempcrc =""
            for aantalbytesdata in range (i ,i + tempaantaalbytesdievolgen):
                #print(strtabel[i+2+ aantalbytesdata])
                tempalldata =  tempalldata + " " +strtabel[i+2 +aantalbytesdata]
            tempcrc = tempcrc + " "   +strtabel[aantalbytesdata+2+1 ] + " " +strtabel[aantalbytesdata+1+3 ]

            a_adres = strtabel[i]
            a_aantaalbytesdievolgen=  strtabel[i+1]
            a_data= tempalldata
            a_crc = tempcrc
            a_gekniptefb = a_adres +" "+a_aantaalbytesdievolgen  +a_data + a_crc
            #print(a_gekniptefb)


            #we gaan testen of de crc klopt
            checkedpakket = crcberekenen( a_adres +" "+a_aantaalbytesdievolgen  +a_data)

            if checkedpakket == a_gekniptefb:
                alleantwoordenineenlijst.append(a_gekniptefb)
                print("checked and verified by verisure")
            else:
                print(f"ongeldig pakket({a_gekniptefb})  weggesmeten by verisure")


            alleantwoordenineenlijst.append(a_gekniptefb)
            alleantwoordenineenlijst = list(dict.fromkeys(alleantwoordenineenlijst)) #remove duplicates
            print(alleantwoordenineenlijst)

            #wis gevonden pakketje uit lange respons
            for bytes in range(0,tempaantaalbytesdievolgen +4):
                tabel.pop(0)
                strtabel.pop(0)
            xx= 77

    return alleantwoordenineenlijst


#######################


def crcberekenen(ext  ):
  tabelcrcberekenen=list()
  tabelcrcberekenen = ext.split(' ')
  #tabelcrcberekenen = mysillyobject.split(' ')

  tempcrc = int(65535)
  for x in tabelcrcberekenen:
      yy = int(x, 16)
      tempcrc = tempcrc ^ yy  # 65281 dan 4470 dan 5761 dan 38295 dan 57507 dan 38771
      # print(f'tempcrc xor {tempcrc}')
      for r in range(0, 8): # print("nu 8x schuiven met bytes %d" % (r))
          som = tempcrc & int(1)
          if (som == 1):
              tempcrc = tempcrc >> 1
              tempcrc = tempcrc ^ 33800  # 0x8408 polynoom
          else:
              tempcrc = int(tempcrc / 2)

  tempcrc = tempcrc ^ 65535  # laaste grote berekening
  tempcrc = tempcrc + 65536  # postprocessing ,voorloopnul  ervoor , zorg dat je altijd 5 karkters hebt , waarvan de 4 rechtse de crc zijn
  CRCstring = str(tempcrc)
  # print(f'result tempcrc= {tempcrc}')
  crcstring = str(hex(tempcrc)).upper()
  crcdeel1 = crcstring[5] + crcstring[6]
  crcdeel2 = crcstring[3] + crcstring[4]
  tabelcrcberekenen.append(crcdeel1)
  tabelcrcberekenen.append(crcdeel2)

  #print(f'crc={tabelcrcberekenen}')
  return " ".join(tabelcrcberekenen)
#####################end functie crc berekenen





















if __name__ == '__main__':
    opencompoort()
    main()
