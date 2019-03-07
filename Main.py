import pandas as pd
import numpy as np
import requests
import json
from pandas.io.json import json_normalize
from datetime import date, timedelta

latitude = -34.915
longitude = -56.165
date_end = date(2018, 12, 31)
num_days = 3
num_chunks = 2

time_suffix = 'T00:00:00'
darksky_url = 'https://api.darksky.net/forecast'
darksky_suffix = '?lang=es&units=si&exclude=currently,minutely,hourly,alerts,flags'

with open('API_key.txt','r') as f:
    key = f.read()
    
date_list = [date_end - timedelta(days=x) for x in range(0, num_days*num_chunks)]
date_list_str = [str(x) + time_suffix for x in date_list]
date_chunks = np.array_split(date_list_str, num_chunks)

raw = []
for i in range(0, num_chunks):
    for dates in date_chunks[i]:
        get = requests.get(f'{darksky_url}/{key}/{latitude},{longitude},{dates}{darksky_suffix}').text
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