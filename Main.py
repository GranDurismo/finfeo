import pandas as pd
import requests
import json
from pandas.io.json import json_normalize

with open('API key.txt','r') as key:
    key = key.read()
    
latitude = -34.915
longitude = -56.165
date = ['2017-01-01T00:00:00', '2016-01-01T00:00:00']

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