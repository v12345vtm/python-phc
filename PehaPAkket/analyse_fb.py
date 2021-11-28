'''
0x01  0xff       =  "broadcastpatroon outg mod start op")
0x02  0xff  0x00 =    "INPUTbroadcastpatroon start op"
0x02  0xff  0xfc =    "mmc/busschak broadcastpatroon start op"
'''

#42 02 01 04 5B 39 oudrelais
#44 88 01 00 81 00 00 01 01 20 B2 DB nieuwrelais
#4A 03 01 00 15 C0 7A jrm

class AnalyseDataFromPehaModule:
  def __init__(self,   datastring  ):
      self.datastring = datastring.upper().rstrip().lstrip()
      self.list_datastring = self.datastring.split(' ')
      self.moduleadres = self.__get_van_welke_module_komt_het()
      self.hoelang_is_antwoord = self.__get_hoelang_is_antwoord()
      self.typemodule = self.__get_type_vd_module()
      self.crcbytes = self.__getcrc()
      g=7


  def __get_van_welke_module_komt_het(self ):
    adres = self.list_datastring[0]
    return adres

  def __get_type_vd_module(self ):
    fb = "vith"
    return fb


  def __get_hoelang_is_antwoord( self ):
    fb = "vith"
    return fb

  def __getcrc( self ):
    size = len(self.list_datastring)
    x=self.list_datastring[size-2 :]
    self.nuttigedata = self.list_datastring[0  :size-2]
    return " ".join(x)




oudrelais = AnalyseDataFromPehaModule("42 02 01 04 5B 39") #oudrelais
nieuwrelais = AnalyseDataFromPehaModule("44 88 01 00 81 00 00 01 01 20 B2 DB")#nieuwrelais
jrm = AnalyseDataFromPehaModule("4A 03 01 00 15 C0 7A")#jrm