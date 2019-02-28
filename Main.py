import pandas as pd
import requests
import json

with open('API key.txt','r') as key:
    key = key.read()
    
latitude = -34.915
longitude = -56.165
date = '2017-01-01T00:00:00'
r = requests.get('https://api.darksky.net/forecast/%s/%s,%s,%s' %(key, latitude, longitude, date) + 
                 '?lang=es&units=si&exclude=currently,minutely,hourly,alerts,flags').text
raw = json.loads(r)

vars = ['time','summary','temperatureMin','temperatureMax','apparentTemperatureMin',
        'apparentTemperatureMax','precipIntensity','precipIntensityMax',
        'precipProbability','cloudCover','humidity','windSpeed','windGust']

df = []
for i in vars:
    df_aux = pd.DataFrame({'Date': [date],
                 'Latitude': [raw['latitude']],
                 'Longitude': [raw['longitude']],
                 i: [raw['daily']['data'][0][i]],
                }).set_index('Date')
    df.append(df_aux)
df = pd.concat(df, axis=1)
df['time'] = pd.to_datetime(df['time'], unit='s')

