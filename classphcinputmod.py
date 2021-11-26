'''
0x01  0xff       =  "broadcastpatroon outg mod start op")
0x02  0xff  0x00 =    "INPUTbroadcastpatroon start op"
0x02  0xff  0xfc =    "mmc/busschak broadcastpatroon start op"
'''



class inputmodule:
  def __init__(self, name, adres , togglebit , status_knop_low , status_knop_high  = None, status_led_low  = None, status_led_high = None , terugmeldingen = None):
    self.name = name  #vb geschakelde priezen
    self.adres = adres #0tot 31
    self.togglebit = togglebit #0of1
    self.status_knop_low = status_knop_low #byteinfo
    self.status_knop_high = status_knop_high
    self.status_led_low = status_led_low
    self.status_led_high = status_led_high
    self.adres = adres
    self.hexbytetobits("f1") #debugtester
    self.list_binair_knop_low =  self.hexbytetobits(status_knop_low)
    self.list_binair_knop_high = self.hexbytetobits(status_knop_low)
    self.list_binair_led_low = self.hexbytetobits(status_led_low)
    self.status_led_high = self.hexbytetobits(status_led_high)
    self.terugmeldingen = None


    xxxx=86


  def getkanaal_ingangen(self ,kanaal):
    knop = "1"
    print(f'module {self.adres} knop {kanaal} is {knop}')
    return knop

  def getkanaal_leduitgangen(self ,kanaal):
    led = "1"
    print(f'module {self.adres} led {kanaal} is {knop}')
    return led

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
    eferfrf=6


  def getname(self ):
    print(f'my name is {self.name} ')
    return self.name




#each object in class inputmodule had a unique adress
p1 = inputmodule(name="wijnkist", adres=0, togglebit=0, status_knop_low="0f", status_knop_high=None, status_led_low=None, status_led_high=None, terugmeldingen=None)

p2 = inputmodule("virt", 1 , 0 , "af" , "af" , "a1" , "a2" )

testa = p1.getkanaal_ingangen(4)
testb = p1.getkanaal_ingangen(5)
print(p1.name)
print(p1.adres)

print("i want to print name of object with the adres = 'adres0'  + how can my script know how much object exist + maybe i need inputcheck in classconstructor to avoid creating object with same adres")



#alleINPUTModules = [p1, p2]


'''for x in alleINPUTModules:
    if x.adres == 0:
        print(f'ja {x.name}')



htyhx =   [m for m in alleINPUTModules if m.adres == 0]
'''

