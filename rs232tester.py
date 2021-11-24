#!/usr/bin/env python
from time import sleep
try:
 import serial
except:
 print("geen seral op gpio  '/dev/ttyAMA0' = uart toont geenc0 in fb  en ; '/dev/ttyUSB0'")

try:
 ser = serial.Serial(
  port='/dev/ttyUSB0',
  baudrate = 19200,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=None
 )
 counter=0
 #ser.write(b'\n\nhello from python\n' )

 ser.flush()
 #ser.write(b'\xc0\xfe\x00\x21\x00\x00\x02\x74\xbe\xc1')  #  C0 FE 00 21 00 00 02 74 BE C1




 while 1:
  ser.write(b'\xc0\xfe\x00\x21\x00\x00\x02\x74\xbe\xc1')  # C0 FE 00 21 00 00 02 74 BE C1
  #x = ser.read( )
  x = ser.read_until(b'\xc1').hex()
  # [TX] * C0 * FE * 00 * 21 * 00 * 00 * 02 * 74 * BE * C1
  #[RX]  * C0 * 00 * FE * 21 * 01 * 93 * 4B * C1 *
  #sleep(0.1)
  print(f'{x }')
  #ser.flush()
  sleep(5)
  counter=counter+1
  print(f'counter {counter}')

except:
 print("geen seral op gpio  ofwel :exit prog , run on raspi instead/interpreter")