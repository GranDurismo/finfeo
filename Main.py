from pprint import pprint
from pandas.io.json import json_normalize
import pandas as pd
import requests
import json

with open('API key.txt','r') as key:
    key = key.read()
    
latitude = -34.915
longitude = -56.165
date = '2017-01-01T00:00:00'
r = requests.get('https://api.darksky.net/forecast/%s/%s,%s,%s' %(key, latitude, longitude, date) + 
                 '?lang=es&units=si&exclude=currently,minutely,hourly,alerts,flags')
pprint(r.json())