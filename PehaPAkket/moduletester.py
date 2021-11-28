


import w3ctest
w3ctest.greeting("Jonathan")

from talk_to_peha_modules import  Create_Instruction_for_PehaModule
d= Create_Instruction_for_PehaModule("a").wat_is_uw_status()
e= Create_Instruction_for_PehaModule("ff")
f= e.adres
r="classAskModuleFB werkt"

from crc_calc import CrcCalc
object1 = CrcCalc("ff 01 01") #werkt
crcgewenst = CrcCalc("45 01 07").crcberekenen()
zoektuit = CrcCalc("45 02 00 03 1D 03" , 1)

import inputmodules
mod_a = inputmodules.InputModule(name="wijnkist", adres="0" , togglebit= "0", status_knop_low="04", status_knop_high=None, status_led_low=None, status_led_high=None, terugmeldingen=None)





import send_and_recieve_rs232
tgeldig= send_and_recieve_rs232.zendenontvang("45 01 01" , "geldig" )
print(f'moduletester  met een verzonnen  geldige respons tgeldig {tgeldig}')

tbrol= send_and_recieve_rs232.zendenontvang("45 01 01" , "brol" )
print(f'moduletester  met een verzonnen  geldige respons tbrol {tbrol}')

tmislukt= send_and_recieve_rs232.zendenontvang("45 01 01" , "mislukt" )
print(f'moduletester  met een verzonnen  geldige respons tmislukt {tmislukt}')


stopdebug = 1