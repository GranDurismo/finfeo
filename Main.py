import pandas as pd
import numpy as np
import requests
import json
from pandas.io.json import json_normalize
from datetime import date, timedelta

with open('API key.txt','r') as key:
    key = key.read()
    
latitude = -34.915
longitude = -56.165

date_end = date(2018, 12, 31)
num_days = 950
num_chunks = 5

date_list = [date_end - timedelta(days=x) for x in range(0, num_days*num_chunks)]
date_chunks = np.array_split(date_list, num_chunks)

raw = []
for i in date:
    get = requests.get('https://api.darksky.net/forecast/%s/%s,%s,%s' %(key, latitude, longitude, i) + 
                     '?lang=es&units=si&exclude=currently,minutely,hourly,alerts,flags').text
    reqs_aux = json.loads(get)
    raw.append(reqs_aux)

df_raw = []
for i in date:
    df_date = json_normalize(raw[date.index(i)]['daily']['data'])
    df_raw.append(df_date)
df = pd.concat(df_raw, axis=0, ignore_index=True, sort=False)

df_proc = df
df_proc['Latitude'] = latitude
df_proc['Longitude'] = longitude
df_proc['time'] = pd.to_datetime(df_proc['time'], unit='s')
df_proc = df_proc[['time','Latitude','Longitude','temperatureHigh','temperatureLow','temperatureMax',
        'temperatureMin','apparentTemperatureHigh','apparentTemperatureLow','apparentTemperatureMax',
        'apparentTemperatureMin','precipIntensity','precipIntensityMax','precipProbability','humidity',
        'windGust','windSpeed','summary']]