'''
0x01  0xff       =  "broadcastpatroon outg mod start op")
0x02  0xff  0x00 =    "INPUTbroadcastpatroon start op"
0x02  0xff  0xfc =    "mmc/busschak broadcastpatroon start op"
'''


class askFB:
  def __init__(self,   adres  ):
    self.adres = adres  #vb0-255

  def hexbytetobits(self ,kanaal):
    if kanaal == None: return None #inputcontrole
    tabelcrcberekenen = list( )
    kanaal[::-1] #string achterstevoren keren
    print(f'hex2bits {kanaal} is ff = 1111 1111')
    binairgetal = (int(kanaal, 16))
    binairgetal = binairgetal+ 256  #voorloopnul ervoor
    string_bytes = bin(binairgetal)
    for bit in range(3,11):
        tabelcrcberekenen.append(string_bytes[ bit])
    return tabelcrcberekenen #een lijst met alle bits

#each object in class inputmodule had a unique adress


p4 = askFB("46") #reken crc uit

df=5



