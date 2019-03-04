import pandas as pd
import requests
import json

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

vars = ['time','summary','temperatureMin','temperatureMax','apparentTemperatureMin',
        'apparentTemperatureMax','precipIntensity','precipIntensityMax',
        'precipProbability','cloudCover','humidity','windSpeed','windGust']

df = []
for i in vars:
    df_aux = pd.DataFrame({'Date': [date],
                 i: [raw['daily']['data'][0][i]],
                }).set_index('Date')
    df.append(df_aux)

df1 = pd.concat(df, axis=1)
df1['Latitude'] = latitude
df1['Longitude'] = longitude
df1['time'] = pd.to_datetime(df1['time'], unit='s')
