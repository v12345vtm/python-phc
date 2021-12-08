'''
0x01  0xff       =  "broadcastpatroon outg mod start op")  vb 45 01 FF A7 EF    en doe em zwijgen met =   45 03 FE 03 FF F3 B4
0x02  0xff  0x00 =    "INPUTbroadcastpatroon start op"
0x02  0xff  0xfc =    "mmc/busschak broadcastpatroon start op"

vb  broadcat           zwijg!
5F 01 FF 48 19        5F 03 FE 00 FF 73 66
46 01 FF C3 00        46 03 FE 00 FF 57 83
00 02 FF 00 A6 B6     00 06 FE FF 00 00 02 12 C6 D7  met initialisatie welke inputs mogen werken



1	status vragen 	00 01 01
2	ein>0 (Der Taster am Kanal wurde gedrückt)
3	aus<0 (der Taster wurde losgelassen nachdem er kürzer als eine Sekunde gedrückt war)
4	ein>1 (der Taster ist schon länger als eine Sekunde gedrückt)	00 01 04
5	aus>1 (der Taster wurde losgelassen nachdem er länger als eine Sekunde gedrückt war)	00 01 05
6	ein>2 (der Taster ist schon länger als zwei Sekunde gedrückt)	00 01 06
7	aus (der Taster wurde losgelassen)	00 01 07


Funktion 	Bedeutung
2	LED im Taster einschalten
3	LED im Taster ausschalten


00 02 FF 00 A6 B6   00 04 FE FF 00 00 05 C5  = niks geprogd
00 02 FF 00 A6 B6   00 05 FE FF 00 00 02 29 80 = 0.0 geprogd
00 02 FF 00 A6 B6   00 05 FE FF 00 00 12 A8 90 = 0.01 geprogd mt functie2
00 02 FF 00 A6 B6   00 05 FE FF 00 00 22 2B A1  =0.02 geprogd mt functie2
00 02 FF 00 A6 B6   00 05 FE FF 00 00 32 AA B1 = 0.03 geprogd mt functie2aan>0

00 02 FF 00 A6 B6   00 05 FE FF 00 80 F2 6A FB = 0.15 geprogd met functie2

00 02 FF 00 A6 B6   00 06 FE FF 00 80 02 F2 24 3C   0.0 (02) en 0.15 (f2) met functie2
00 02 FF 00 A6 B6   00 07 FE FF 00 00 02 12 F2 B7 06   0.0(00) en 0.1(12) en 0.15 (f2)  met functie2


fb antw 00 04 01 FF 00 80 DF 84




welke busschak : fw heb je?
20 02 01 3F 99 16                                 20 09 01 3F 56 32 43 E1 01 20 20 21 70
vraag =                 antw = v1.32


'''


def respons_analyser(rs485data):
    print(f"er was op de rs485 :{rs485data} we gaan er vanuit dat crc juist is:")
    tabel = rs485data.split()
    fromadres =  int(tabel[0], 16)
    temp = bin(int(tabel[1], 16))[2:].zfill(8) #str2binair
    aantalbytesdievolgen =  int(temp[4:8],2)
    str2bin = bin(int(tabel[1], 16))[2:].zfill(8)
    togglebit = str2bin[0]
    crc1 = tabel[-2]
    crc2 = tabel[-1]
    print(f"\t togglebit:{togglebit} ")
    print(f"\t aantlbytesdievolgen:{aantalbytesdievolgen} ")



    ###########################################
    if 0<= int(fromadres  ) <=31:
        print(f"\t {fromadres}=inputmod")

        if aantalbytesdievolgen ==1:
            print(f"\t {fromadres}=iemand drukt op een knop")

        if aantalbytesdievolgen == 4:
            print(f"\t {tabel[3]}=leduit0-7")
            print(f"\t {tabel[2]}=todo")
            print(f"\t {tabel[4]}=knop0-7")
            print(f"\t {tabel[5]}=knop8-15")
            temph = bin(int(tabel[5], 16))[2:].zfill(8)  # str2binair
            templ = bin(int(tabel[4], 16))[2:].zfill(8)  # str2binair
            ledl = bin(int(tabel[3], 16))[2:].zfill(8)  # str2binair
            print(f"\t {temph} {templ}   =inputs0.15-0.0   en {ledl}  =leds0.7 -0.0")




##########################
    if 32<= int(fromadres) <=63:
        print(f"\t {fromadres}=mmc/ir/busschak mod")

        if aantalbytesdievolgen ==1:
            print(f"\t {fromadres}=iemand drukt op een knop")

        if aantalbytesdievolgen == 9:
            print(f"\t {fromadres}=iemand  vroeg welke fw ik heb")
            print(f"\t versie {tabel[2]}.{tabel[5]}")

        if aantalbytesdievolgen == 10:

            print(f"\t {tabel[2]}=knop0-7")
            print(f"\t {tabel[3]}=led naastknop")
            print(f"\t {tabel[4]}=leduit0-7")
            print(f"\t {tabel[6]}=byte veldverlichting is 0of1")
            print(f"\t {tabel[5]}=todo")
            print(f"\t {tabel[7]}=knop8-15")
            print(f"\t {tabel[8]}=terugmelding?todo_")
            print(f"\t {tabel[9]}=terugmelding?todo a")
            print(f"\t {tabel[10]}=terugmelding?todo b")
            print(f"\t {tabel[11]}=terugmelding?todo c")

            templ = bin(int(tabel[4], 16))[2:].zfill(8)  # str2binair
            ledl = bin(int(tabel[3], 16))[2:].zfill(8)  # str2binair
            veldverlichting = bin(int(tabel[6], 16))[2:].zfill(8)  # str2binair
            print(f"\t {templ}   =inputs0.7-0.0   // {ledl}  =leds0.7 -0.0  // {veldverlichting} centraallichtvlak"  )



###################################
    if 64 <= int(fromadres) <= 95:
        print(f" \t {fromadres}=uitg mod")

        if aantalbytesdievolgen ==1:
            print(f"\t we vragen me mijn feedback")


        if aantalbytesdievolgen ==2:
            print(f"\t oude fw")
            str2bin = bin(int(tabel[3], 16))[2:].zfill(8)
            print(f"\t {str2bin}={tabel[3]} =relais0.7 -0.0")

        if aantalbytesdievolgen == 4:
            print(f"\t  nieuwe fw")
            str2bin = bin(int(tabel[1], 16))[2:].zfill(8)
            print(f"\t {tabel[0]}=relaisstand todo")
            print(f"\t {tabel[0]}=terugmeldingenstand todo")
            print(f"\t {tabel[0]}=bedrijfsuren todo")

        if aantalbytesdievolgen == 3:
            print(f"\t  rolluikmod")
            str2bin = bin(int(tabel[1], 16))[2:].zfill(8)
            print(f"\t {tabel[2]}=geen staat van te maken todo")
            print(f"\t {tabel[3]}=geen staat van te maken  todo")
            print(f"\t {tabel[4]}=geen staat van te maken  todo")


        if aantalbytesdievolgen == 8:
            print(f"\t nieuwe fw")
            str2bin = bin(int(tabel[1], 16))[2:].zfill(8)
            print(f"\t {tabel[4]}=relaisstand")
            print(f"\t {tabel[0]}=terugmeldingenstand todo")
            print(f"\t {tabel[0]}=bedrijfsuren todo")
            relaisl = bin(int(tabel[4], 16))[2:].zfill(8)  # str2binair
            print(f"\t {relaisl}={tabel[4]} =relais0.7 -0.0")

        if aantalbytesdievolgen == 9:
            print(f"\t {fromadres}=iemand  vroeg welke fw ik heb")
            print(f"\t versie {tabel[8]}.{tabel[9]}")



##################################
    if 96 <= int(fromadres) <= 127:
        print(f"\t {fromadres}=anal mod")

###########################
    if 128<= int(fromadres) <=159:
        print(f"\t {fromadres}=multimod")

######################################
    if 160<= int(fromadres) <=191:
        print(f"\t {fromadres}=dimmermod")


        if aantalbytesdievolgen == 5:
            #print(f"\t  nieuwe fw")
            str2bin = bin(int(tabel[1], 16))[2:].zfill(8)
            print(f"\t {tabel[3]}=dim0stand ")
            print(f"\t {tabel[4]}=dim1stand ")
            print(f"\t {tabel[5]}=dim0terugmeld")
            print(f"\t {tabel[6]}=dim1terugmeld")
###########################
    if 192 <= int(fromadres) <= 223:
        print(f"\t {fromadres}=ongekend")
#######################
    if 224 <= int(fromadres) <= 255:
        print(f"\t {fromadres}=systeembox")



###########################################
    print("")
    x=7






#respons_analyser("4A 03 01 00 15 C0 7A") #  jrm jaloeziefb

#respons_analyser("00 04 01 FF 00 80 DF 84") #  inputmod fb
#respons_analyser("00 04 01 F7 00 00 15 C6 ") #  inputmod fb led 3 is uit rest leds is aan (f7)

#respons_analyser("45 02 00 03 1D 03") #  relaismod fb oude fw
#respons_analyser("44 88 01 00 80 00 00 01 01 20") #  relaismod fb nieuwe fw


#respons_analyser("45 82 01 02 a0 07") #  relaismod fb nieuwe fw
#respons_analyser("45 02 01 02 4c 0b") #  relaismod fb nieuwe fw


#respons_analyser("44 89 01 3F 18 4A ED EE 01 01 20 1D 05") #   outp44  zegt  dat er fw 1.1 in zit
#respons_analyser("20 09 01 3F 56 32 43 E1 01 20 20 21 70") #   busschakelaar20  zegt  dat er fw 1.32 in zit
#respons_analyser("20 8A 01 42 08 00 01 01 04 01 20 20 91 97") #   busschakelaar20  zegt  ledje aan is led01
#respons_analyser("5F 03 01 00 15 D4 E8") #   busschakelaar20  zegt  ledje aan is led01
#respons_analyser("A0 05 01 00 00 00 00 2D 76") #dim0.0
#respons_analyser("A0 05 01 FF FF 03 00 64 5F") #dim0.0

#respons_analyser("44 88 01 00 84 00 00 01 01 20 35 CF")
#respons_analyser("40 82 01 03 7E 78")
#respons_analyser("40 02 01 03 92 74")




'''40 82 01 03 7E 78
40 02 01 03 92 74 02 02 00 FE E1 6E
40 02 01 03 92 74
41 02 01 00 B2 5A
42 02 01 00 7F 7F
43 03 01 00 15 A4 2B
44 88 01 00 84 00 00 01 01 20 35 CF
A0 05 01 00 00 00 00 2D 76'''


n=4