class PehaCRC:
  def __init__(mysillyobject, inputstring, calcCRC0_findCRC1 = 0):
    mysillyobject.string_inputstring = inputstring.upper().rstrip().lstrip()
    mysillyobject.list_inputstring = mysillyobject.string_inputstring.split(' ')
    mysillyobject.calcCRC0_findCRC1vth = calcCRC0_findCRC1 * 2
    mysillyobject.crc1 = None
    mysillyobject.crc2 = None
    mysillyobject.list_outputstring = list()
    mysillyobject.crcgezienop = None  # als we veel data zien willen we kunnen detecteren waar de crc begin
    tabelcrcberekenen = None
    #mysillyobject.inputcontrole()
    #mysillyobject.watmoetergebeuren()
    if mysillyobject.inputcontrole():
        mysillyobject.watmoetergebeuren()

  def watmoetergebeuren(mysillyobject):
      global tabelcrcberekenen
      if mysillyobject.calcCRC0_findCRC1vth == 0:
          print(f'gewoon crc zeggen aan de klant')
          tabelcrcberekenen =  mysillyobject.string_inputstring.split(' ')
          mysillyobject.crcberekenen()
      else:
          print(f'waar zie je crc in de gevens zitten')
          mysillyobject.waarissie()


  def inputcontrole(mysillyobject):
    global tabelcrcberekenen
    aaa = mysillyobject.string_inputstring.upper().replace(" ", "")
    try:
        yy = int(aaa, 16)
        print("inputcontrole ok --- calculating")
        #tabelcrcberekenen =  mysillyobject.string_inputstring.split(' ')
        #mysillyobject.crcberekenen()
        return True
    except:
        print(f'ongeldige inputstring {mysillyobject.string_inputstring.upper()}')
        mysillyobject.calcCRC0_findCRC1vth = None
        mysillyobject.list_outputstring = None
        return False


  def getorigdata(abc):
    print(f'the klasse bezit deze globaldata is:  {abc.calcCRC0_findCRC1vth}')

  def waarissie(mysillyobject):
      global tabelcrcberekenen
      str = mysillyobject.string_inputstring
      tabel = str.split(" ")
      if "C0" in tabel: tabel.remove("C0")
      if "C1" in tabel: tabel.remove("C1")
      tabelcrcberekenen = list( )  # creer lege list om die dan aan de crccalculator te voeden


      for elementen, new_val  in enumerate(tabel):
          #print(f'{elementen} : {new_val} vith wil deze testen:{mysillyobject.list_inputstring }')
          tabelcrcberekenen.append(new_val) #stiekem byte erbij
          mysillyobject.crcberekenen() #we steken stiekem een byte bij voor de crc te doen op berekenen
          #print(f'  tabel                {tabel[ 0:elementen+3 ]}')
          vastewaarden = tabel[ 0:elementen+3 ]
          calculatedlist = mysillyobject.list_outputstring

          if vastewaarden == calculatedlist:
              print(f'we hebben een crc gevonden in een string op pos {elementen+1} : {mysillyobject.crc1} {mysillyobject.crc2}  ')
              mysillyobject.crcgezienop = elementen+1
              return
          else:
              print(f'data bekeken en er zat geen crc in ')


          fgerfr=5

  def getcalcCRC0_findCRC1(abc):
      print("the calcCRC0_findCRC1 is:" + abc.str_inputstring)

  def toString(mysillyobject):
      print(    f' \n\t\t\t mysillyobject.str_inputstring = {mysillyobject.str_inputstring} '
            f' \n\t\t\t mysillyobject.calcCRC0_findCRC1vth = {mysillyobject.calcCRC0_findCRC1vth}'
            f' \n\t\t\t mysillyobject.crc1 = {mysillyobject.crc1}'
            f' \n\t\t\t mysillyobject.crc2 = {mysillyobject.crc2}'
            f' \n\t\t\t mysillyobject.inputerror = {mysillyobject.inputerror}'
            f'')

  def crcberekenen(mysillyobject  ):
      global tabelcrcberekenen
      #if ext != None: tabelcrcberekenen = ext.split(' ')
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
      #tabelcrcberekenen.append(crcdeel1)
      #tabelcrcberekenen.append(crcdeel2)
      mysillyobject.crc1 = crcstring[5] + crcstring[6]
      mysillyobject.crc2 = crcstring[3] + crcstring[4]
      mysillyobject.list_outputstring = tabelcrcberekenen.copy()
      mysillyobject.list_outputstring.append(crcstring[5] + crcstring[6])
      mysillyobject.list_outputstring.append(crcstring[3] + crcstring[4])
      return mysillyobject.list_outputstring
      print(f'list_outputstring out={mysillyobject.list_outputstring}')
  #####################end functie crc berekenen



p1 = PehaCRC("FE 00 21 00 00 02", 0) #reken crc uit
p2 = PehaCRC("00 01 02 06 FC 00 01 00 14 DF 45 01 06 E9 85 45 02 00 02 94 12", 1) #zeg waar de crc begint
p3 = PehaCRC("45 81 06 25 09 45 82 00 03 F1 0F" ,1)  #busrs485 uitgmod 45
p4 = PehaCRC("46 01 01", 0) #reken crc uit


