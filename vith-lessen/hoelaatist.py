
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
numeteen = datetime.now().strftime("%H:%M:%S")

#print("now =", now)

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string)