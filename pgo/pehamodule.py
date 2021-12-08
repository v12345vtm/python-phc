

class pehamodule:
    def __init__(self):
        self.overzichtallemodules = set()

    def setData(self, rs485pakket):
        rs485pakket=rs485pakket.upper()

        #inputcontrole ,en crc doen
        tabel = rs485pakket.split(' ')
        if len(tabel) < 5:
            print("ongeldig datapakket korter dan 5bytes")
            return

        checked_crc = crcberekenen( " ".join(tabel[0:-2]))
        if checked_crc != rs485pakket and False:
            print("ongeldig datapakket gezien crc error")
            return
        a_antalbytesdievolgen =  int(bin(int(tabel[1], 16))[2:].zfill(8)[4:8],2)
        a_adres =  tabel[0]
        a_togglebit =  bin(int(tabel[1], 16))[2:].zfill(8)[0]
        self.overzichtallemodules.add(a_adres)
        self.togglebit = a_togglebit






        pass


######################################################################
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


  return " ".join(tabelcrcberekenen)
#####################end functie crc berekenen



#respons_analyser("45 82 01 02 a0 07") #  relaismod fb nieuwe fw
#respons_analyser("45 02 01 02 4c 0b") #  relaismod fb nieuwe fw
zekeringkastvol = pehamodule()
zekeringkastvol.setData("45 82 01 02 a0 07")
zekeringkastvol.setData("46 82 01 02 a0 07")




print("CLASS PEHAMODULE IN ONTWIKKELNG")



#alleINPUTModules = [p1, p2]


'''for x in alleINPUTModules:
    if x.adres == 0:
        print(f'ja {x.name}')



htyhx =   [m for m in alleINPUTModules if m.adres == 0]
'''

