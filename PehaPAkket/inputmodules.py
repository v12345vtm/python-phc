'''
0x01  0xff       =  "broadcastpatroon outg mod start op")
0x02  0xff  0x00 =    "INPUTbroadcastpatroon start op"
0x02  0xff  0xfc =    "mmc/busschak broadcastpatroon start op"
'''



class InputModule:
  def __init__(self, name, adres , togglebit , status_knop_low , status_knop_high  = None, status_led_low  = None, status_led_high = None , terugmeldingen = None):
    self.name = name  #vb geschakelde priezen
    self.adres = adres #0tot 31
    self.togglebit = togglebit #0of1
    self.status_knop_low = status_knop_low #byteinfo
    self.status_knop_high = status_knop_high
    self.status_led_low = status_led_low
    self.status_led_high = status_led_high
    self.adres = adres
    #self.hexbytetobits("0f") #debugtester
    self.list_binair_knop_low =  self.__hexbytetobits(status_knop_low)
    self.list_binair_knop_high = self.__hexbytetobits(status_knop_high)
    self.list_binair_led_low = self.__hexbytetobits(status_led_low)
    self.status_led_high = self.__hexbytetobits(status_led_high)
    self.terugmeldingen = None


    xxxx=86


  def get_togglebit(self):
    return self.togglebit


  def get_kanaal_status(self ,kanaal):
    if  0<=kanaal <= 7 :
      temp = self.list_binair_knop_low[kanaal]
    if 8 <= kanaal <= 15:
      if self.list_binair_knop_high == None:
        print(f'module {self.adres} knop {kanaal} is onbestaande , ')
        return None
      temp = self.list_binair_knop_high(kanaal)
      kanaal=kanaal-8
    print(f'getkanaal_status module"{self.adres}" met knop{kanaal} is {temp}')
    return temp

  def getkanaal_leduitgangen(self ,kanaal):
    ledstatus = "vith"
    #print(f'module {self.adres} led {kanaal} is {knop}')
    return ledstatus

  def __hexbytetobits(self ,kanaal):
    if kanaal == None: return None #inputcontrole
    tabelcrcberekenen = list( )
    binairgetal = (int(kanaal, 16))
    binairgetal = binairgetal+ 256  #voorloopnul ervoor
    string_bytes = bin(binairgetal)
    string_bytes = string_bytes[::-1] #byte omkeren 0e element vooraanlinks zetten ipv achteraanrechts
    string_bytes = string_bytes[0:8] #0b wegdoen
    for bit in range(0,8):
        tabelcrcberekenen.append(string_bytes[ bit])
    print(f'hexbytetobits-moduleadres "{self.adres}" met data{kanaal} bit00.00 staat bewust links!  {string_bytes}')
    return tabelcrcberekenen #een lijst met alle bits
    eferfrf=6


  def getname(self ):
    print(f'my name is {self.name} ')
    return self.name




#each object in class inputmodule had a unique adress
p1 = InputModule(name="wijnkist", adres="0", togglebit="0", status_knop_low="04", status_knop_high=None, status_led_low=None, status_led_high=None, terugmeldingen=None)

p2 = InputModule("virt", "1" , "0" , "af" , "1" , "4" , "8" )


for knop in range(0,16):
  d=85
  #print(p1.get_kanaal_status(knop))


testchannelzero = p1.get_kanaal_status(0)
testchanneltogglebit = p1.get_togglebit()

print(p1.name)
#print(p1.adres)



#alleINPUTModules = [p1, p2]


'''for x in alleINPUTModules:
    if x.adres == 0:
        print(f'ja {x.name}')



htyhx =   [m for m in alleINPUTModules if m.adres == 0]
'''

