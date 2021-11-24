# [TX] * C0 * FE * 00 * 21 * 00 * 00 * 02 * 74 * BE * C1
# [RX]  * C0 * 00 * FE * 21 * 01 * 93 * 4B * C1 *
# https://github.com/v12345vtm/python-phc




def crcberekenen(pehacmd):
    global tabel
    tabel = pehacmd.split(' ')
    print(tabel)
    tempcrc  = int(65535)
    for x in tabel:
        yy =  int(x, 16)
        tempcrc = tempcrc ^ yy  #65281 dan 4470 dan 5761 dan 38295 dan 57507 dan 38771
        #print(f'tempcrc xor {tempcrc}')
        for r in range(0, 8):
            #print("nu 8x schuiven met bytes %d" % (r))
            een = int(1)
            som = tempcrc &  een
            #print(som)
            #print(tempcrc)
            if (som == 1):
                tempcrc = tempcrc >> 1
                tempcrc = tempcrc  ^ 33800 # 0x8408 polynoom
                #print(f'tempcrcmetpluynoom {tempcrc}')
            else:
                tempcrc = int(tempcrc / 2)
                #print(f'tempcrcdeel 2 {tempcrc}')

    tempcrc = tempcrc ^ 65535 #laaste grote berekening

    tempcrc = tempcrc + 65536 #postprocessing ,voorloopnul  ervoor , zorg dat je altijd 5 karkters hebt , waarvan de 4 rechtse de crc zijn
    CRCstring = str(tempcrc)
    #print(f'result tempcrc= {tempcrc}')
    crcstring = str(hex(tempcrc)).upper()
    crcdeel1 = crcstring[5] + crcstring[6]
    crcdeel2 = crcstring[3]+ crcstring[4]
    tabel.append(crcdeel1)
    tabel.append(crcdeel2)
    print(tabel)
#####################end functie crc berekenen



#####################start
commando = "FE 00 21 00 00 02"
verwachtecrc = "74 be"
crcberekenen(commando)

recieved = "c000fe2101934bc1"

eerest = tabel[0]





x=1