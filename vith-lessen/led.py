from astral import LocationInfo  # in raspi terminal doe :sudo pip install astral

loc = LocationInfo(name='Dp-projects', region='Ingelmunster', timezone='Europe/Brussels', latitude=50.938527,
                   longitude=3.779109)
print(loc)
# LocationInfo(name='SJC', region='CA, USA', timezone='America/Los_Angeles',
#   latitude=37.3713439, longitude=-121.944675)
print(loc.observer)
# Observer(latitude=37.3713439, longitude=-121.944675, elevation=0.0)

import datetime
from astral.sun import sun

s = sun(loc.observer, date=datetime.date(2021, 11, 14), tzinfo=loc.timezone)
for key in ['dawn', 'dusk', 'noon', 'sunrise', 'sunset']:
    print(f'{key:10s}:', s[key])
