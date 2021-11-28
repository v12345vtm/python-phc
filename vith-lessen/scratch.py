import wmi #WMI voor win10laptop om u compoort te vinden

query = "SELECT * FROM Win32_PnPEntity WHERE Name LIKE '%(COM%)'"
coms  = wmi.WMI().query(query)

for com in coms:
    print(com.Name)