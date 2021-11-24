from datetime import datetime
from pytz import timezone
import pytz
format = "%Y-%m-%d %H:%M:%S %Z%z"

# Current time in UTC
now_utc = datetime.now()
print(now_utc.strftime(format))

# Convert to Asia/Kolkata time zone
now_asia = now_utc.astimezone(timezone('Europe/Brussels'))
print(now_asia.strftime(format))

vt = now_utc.astimezone(timezone('Europe/Brussels'))
print(vt.strftime(format))


lokalertc = pytz.utc.localize(datetime.now())
print(lokalertc)
# 2021-11-23 07:36:12.214774+01:00

# Convert to Asia/Kolkata time zone
vtt = datetime.now().astimezone(timezone('Europe/Brussels'))
print(vtt.strftime(format))