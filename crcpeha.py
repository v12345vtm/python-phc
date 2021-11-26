# [TX] * C0 * FE * 00 * 21 * 00 * 00 * 02 * 74 * BE * C1
# [RX]  * C0 * 00 * FE * 21 * 01 * 93 * 4B * C1 *
# https://github.com/v12345vtm/python-phc

tabelcrcberekenen = list(())  # creer lege list
tabelcheckfb = list(())  # creer lege list


def crcberekenen(pehacmd):
    global tabelcrcberekenen
    pehacmd = pehacmd.upper()
    tabelcrcberekenen = pehacmd.split(' ')
    print(f'tabelcrcberekenen in={tabelcrcberekenen}' )
    tempcrc  = int(65535)
    for x in tabelcrcberekenen:
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
    tabelcrcberekenen.append(crcdeel1)
    tabelcrcberekenen.append(crcdeel2)
    print(f'tabelcrcberekenen out={tabelcrcberekenen}' )
#####################end functie crc berekenen



def findCRCinString(tecontrolerenstring):
    tecontrolerenstring = tecontrolerenstring.upper()
    tabelcheckfb = tecontrolerenstring.split(' ')
    print(f'tabelcheckfb in={tabelcheckfb}' )
    #remove start en stopbytes indien ze er zijn (C0 en c1 ) afkappen
    if "C0" in tabelcheckfb: tabelcheckfb.remove("C0")
    if "C1" in tabelcheckfb: tabelcheckfb.remove("C1")
    # remove de ontvangen crc  afkappen omdat we em willen heruitrekenen
    #temp = tabelcheckfb.copy()
    print(f'tabelcheckfb test={tabelcheckfb}')
    runningled =""

    for elementen, new_val in enumerate(tabelcheckfb):
        #print(f'elementen ={new_val}')
        runningled = runningled + " " + new_val + " "
        runningled = runningled.rstrip()
        runningled = runningled.lstrip()
        ffh=58
#####################start

crcberekenen("FE 00 21 00 00 02") # uitkomst moet 'FE', '00', '21', '00', '00', '02', '74', 'BE' zijn
#findCRCinString( "c0 00 fe 21 01 93 4b c1") # uitkomst  ja of neen zijn met optioneel de cr  93 4b of

recieved = "c000fe2101934bc1"






