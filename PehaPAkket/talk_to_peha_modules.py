'''
0x01  0xff       =  "broadcastpatroon outg mod start op")
0x02  0xff  0x00 =    "INPUTbroadcastpatroon start op"
0x02  0xff  0xfc =    "mmc/busschak broadcastpatroon start op"
'''
#45 01 06 = mod 45 ch1 omschakelen

class Create_Instruction_for_PehaModule:
  def __init__(self,   adres  ):
    if len(adres) == 1:
      self.adres = "0" + adres.upper()
    else:
      self.adres = adres  #vb0-255
      self.wat_is_uw_status()

  def wat_is_uw_status(self ):
    fb = self.adres + " 01 01"
    self.feedbackcommando = fb.upper()
    return self.feedbackcommando #een string vb "45 01 01"



  def omschakelen(self , kanaal ):
    fb = self.adres + " 01 01"
    self.feedbackcommando = fb.upper()
    print("onder construction vb je wil mod 45 , omschakelen kanaal7")
    return self.omschakelen  #een string vb "45 01 01"

#each object in class inputmodule had a unique adress


#p4 =  Create_Instruction_for_PehaModule("01").wat_is_uw_status() #reken crc uit
#pop =  Create_Instruction_for_PehaModule("cc")




