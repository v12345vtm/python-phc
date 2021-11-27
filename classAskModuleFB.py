'''
0x01  0xff       =  "broadcastpatroon outg mod start op")
0x02  0xff  0x00 =    "INPUTbroadcastpatroon start op"
0x02  0xff  0xfc =    "mmc/busschak broadcastpatroon start op"
'''


class AskModuleFB:
  def __init__(self,   adres  ):
    if len(adres) == 1:
      self.adres = "0" + adres.upper()
    else:
      self.adres = adres  #vb0-255
      self.setfeedbackcommando()

  def setfeedbackcommando(self ):
    fb = self.adres + " 01 01"
    self.feedbackcommando = fb.upper()
    return self.feedbackcommando #een string vb "45 01 01"

#each object in class inputmodule had a unique adress


p4 =  AskModuleFB("01").setfeedbackcommando() #reken crc uit
pop =  AskModuleFB("cc")
df=5



