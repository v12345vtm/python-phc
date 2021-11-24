#!/usr/bin/env python
from time import sleep
try:
    import serial
except:
    print("geen seral op gpio  '/dev/ttyAMA0' = uart toont geenc0 in fb  en ; '/dev/ttyUSB0'")

try:
    ser = serial.Serial(        port='/dev/ttyUSB0',        baudrate = 19200,        parity=serial.PARITY_NONE,        stopbits=serial.STOPBITS_ONE,        bytesize=serial.EIGHTBITS,       timeout=1    )

    counter=0
    feedbackTabelVanPeha = list(())  # creer lege list
    #ser.write(b'\n\nhello from python\n' )

    ser.flush()
    #ser.write(b'\xc0\xfe\x00\x21\x00\x00\x02\x74\xbe\xc1')  #  C0 FE 00 21 00 00 02 74 BE C1




    while 1:
        #ser.write(b'\xc0\xfe\x00\x21\x00\x00\x02\x74\xbe\xc1')  # C0 FE 00 21 00 00 02 74 BE C1
        sleep(0.1)
        commando = "C0 FE 00 21 00 00 02 74 BE C1"
        zendtabel = commando.split(' ')
        for el in zendtabel:
            d = int(el ,16)
            dd = bytes([d])
            ser.write(dd)
            #print(el)

        #x = ser.read_until(b'\xc1').hex()
        #x= ser.read_all().hex()
        bytesToRead = ser.inWaiting()


        while ser.inWaiting() > 0:
            feedbackTabelVanPeha.clear() #wistabel
            for aantalelementen in range(0, bytesToRead):
                x = ser.read().hex()
                feedbackTabelVanPeha.append(x)
        print(feedbackTabelVanPeha)
            #print(aantalelementen)
        #print(f'{x }')
        #ser.flush()
        sleep(5)
        counter=counter+1
        print(f'counter {counter}')

except:
    print("geen seral op gpio  ofwel :exit prog , run on raspi instead/interpreter")