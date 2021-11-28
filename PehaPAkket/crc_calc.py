class CrcCalc:
    def __init__(mysillyobject, inputstring ):
        mysillyobject.string_inputstring = inputstring.upper().rstrip().lstrip()
        mysillyobject.crcgezienop = None



    def waarissie(mysillyobject):
        global tabelcrcberekenen
        str = mysillyobject.string_inputstring
        tabel = str.split(" ")
        if "C0" in tabel: tabel.remove("C0")
        if "C1" in tabel: tabel.remove("C1")
        tabelcrcberekenen = list()  # creer lege list om die dan aan de crccalculator te voeden

        for elementen, new_val in enumerate(tabel):
            print(f'{elementen} : {new_val} vith wil deze testen: ')
            tabelcrcberekenen.append(new_val)  # stiekem byte erbij in list
            mysillyobject.string_inputstring = " ".join(tabelcrcberekenen) #table2string separated with spaces
            eerstebytemetcrc = mysillyobject.crcberekenen()  # we steken stiekem een byte bij voor de crc te doen op berekenen
            listtemp = eerstebytemetcrc.split()
            vastewaarden = tabel[0:elementen + 3]
            print(f'  vastewaarden {tabel[ 0:elementen+3 ]}')
            print(f'          temp {listtemp}')


            if vastewaarden == listtemp:
                print(f'we hebben een crc  op pos {elementen + 1} :    ')
                mysillyobject.crcgezienop = elementen + 1

                #restore onze origine variabelen
                mysillyobject.string_inputstring = " ".join(listtemp)

                #mysillyobject.string_outputstring = " ".join(listtemp[0:elementen+1])

                hh=75


                return " ".join(listtemp[0:elementen+1]) #de tabel in string vorm zonder crc
            else:
                print(f'data bekeken en er zat geen crc in ')

            fgerfr = 5


    def strip_crc(self  ):
        self.waarissie()
        return self.waarissie()



    def crcberekenen(mysillyobject  ):
        tabelcrcberekenen = mysillyobject.string_inputstring.split(' ')
        tempcrc = int(65535)
        for x in tabelcrcberekenen:
            yy = int(x, 16)
            tempcrc = tempcrc ^ yy  # 65281 dan 4470 dan 5761 dan 38295 dan 57507 dan 38771
            # print(f'tempcrc xor {tempcrc}')
            for r in range(0, 8):  # print("nu 8x schuiven met bytes %d" % (r))
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
        print(f'string-crccaloutput= {" ".join(tabelcrcberekenen)}')
        mysillyobject.string_outputstring = " ".join(tabelcrcberekenen)
        return " ".join(tabelcrcberekenen) #table2string separated with spaces

    #####################end functie crc berekenen
stripedvangeldigecrc = CrcCalc("45 02 00 03 1D 03").strip_crc()
waar = CrcCalc("45 02 00 03 1D 03").waarissie()

#object1 = CrcCalc("45 02 06") #werkt
#p1 = CrcCalc("cc").crcberekenen()  # reken crc uit werkt

deeb = 88



