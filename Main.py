import pandas as pd
import requests
import json
import pickle
from pandas.io.json import json_normalize
import datetime as dt

latitude = -34.915
longitude = -56.165
first_date = dt.date(2018, 12, 31)
num_days = 6

time_suffix = 'T00:00:00'
darksky_url = 'https://api.darksky.net/forecast'
darksky_suffix = '?lang=es&units=si&exclude=currently,minutely,hourly,alerts,flags'

with open('API_key.txt','r') as f:
    key = f.read()

def request_loop(date_start, raw_arg, df_arg):
    date_list = [date_start - dt.timedelta(days=x) for x in range(0, num_days)]
    date_list_str = [str(x) + time_suffix for x in date_list]
    for dates in date_list_str:
        get = requests.get(f'{darksky_url}/{key}/{latitude},{longitude},{dates}{darksky_suffix}').text
        reqs_aux = json.loads(get)
        raw_arg.append(reqs_aux)
        df_date = json_normalize(raw_arg[date_list_str.index(dates)]['daily']['data'])
        df_arg.append(df_date)
    pickle.dump(raw_arg, open('raw.p', 'wb'))
    pickle.dump(df_arg, open('df.p', 'wb'))
    
try:
    df = pickle.load(open('df.p', 'rb'))
    raw = pickle.load(open('raw.p', 'rb'))
except:
    print('No previous data')
    df = []
    raw = []
    request_loop(first_date, raw, df)
else:
    print('Using previously loaded data')
    df_aux = pd.concat(df, axis=0, ignore_index=True, sort=False)
    first_date = dt.datetime.utcfromtimestamp(min(df_aux['time'])).date() - dt.timedelta(days=1)
    request_loop(first_date, raw, df)
    df = pd.concat(df, axis=0, ignore_index=True, sort=False)    

df_proc = df
df_proc['Latitude'] = latitude
df_proc['Longitude'] = longitude
df_proc['time'] = pd.to_datetime(df_proc['time'], unit='s')
df_proc = df_proc[['time','Latitude','Longitude','temperatureHigh','temperatureLow','temperatureMax',
        'temperatureMin','apparentTemperatureHigh','apparentTemperatureLow','apparentTemperatureMax',
        'apparentTemperatureMin','precipIntensity','precipIntensityMax','precipProbability','humidity',
        'windGust','windSpeed','summary']]