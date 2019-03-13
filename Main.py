import pandas as pd
import requests
import json
import pickle
import datetime as dt
from pandas.io.json import json_normalize
from geopy.geocoders import Nominatim

#%% Set defaults

darksky_url = "https://api.darksky.net/forecast"
darksky_suffix = "?lang=es&units=si&exclude=currently,minutely,hourly,alerts,flags"
time_suffix = "T00:00:00"
first_date = dt.date(2018, 12, 31)
requests_per_loop = 950

# Allow user to choose location and get coordinates
user_location = input("Set your desired location: ")
geoloc = Nominatim(user_agent="finfeo")
coordinates = geoloc.geocode(user_location)
latitude, longitude = coordinates.latitude, coordinates.longitude
location = coordinates.address

#%% Get API key and define request loop

with open("API_key.txt", "r") as f:
    key = f.read()


def request_loop(date_start, raw_arg):
    date_list = [date_start - dt.timedelta(days=x) for x in range(0, requests_per_loop)]
    date_list_str = [str(x) + time_suffix for x in date_list]
    for dates in date_list_str:
        get = requests.get(
            f"{darksky_url}/{key}/{latitude},{longitude},{dates}{darksky_suffix}"
        ).text
        reqs_aux = json.loads(get)
        raw_arg.append(reqs_aux)
    # Pickle requested dates so they are not requested again
    pickle.dump(raw_arg, open("raw.p", "wb"))


#%% If requests have been pickled, get the earliest date and rerun loop

try:
    raw = pickle.load(open("raw.p", "rb"))
except:
    print("No previous data")
    raw = []
    request_loop(first_date, raw)
else:
    print("Using previously loaded data")
    date_aux = [
        dt.datetime.utcfromtimestamp(y["daily"]["data"][0]["time"]).date() for y in raw
    ]
    first_date = min(date_aux) - dt.timedelta(days=1)
    request_loop(first_date, raw)

#%% Parse requests into dataframes and concatenate

df = [json_normalize(x["daily"]["data"]) for x in raw]
df = pd.concat(df, axis=0, ignore_index=True, sort=False)

#%% Include coordinates in dataframe, convert time and drop unneeded columns

df_proc = df
df_proc["Latitude"] = latitude
df_proc["Longitude"] = longitude
df_proc["time"] = pd.to_datetime(df_proc["time"], unit="s")
df_proc = df_proc[
    [
        "time",
        "Latitude",
        "Longitude",
        "temperatureHigh",
        "temperatureLow",
        "temperatureMax",
        "temperatureMin",
        "apparentTemperatureHigh",
        "apparentTemperatureLow",
        "apparentTemperatureMax",
        "apparentTemperatureMin",
        "precipIntensity",
        "precipIntensityMax",
        "precipProbability",
        "humidity",
        "windGust",
        "windSpeed",
        "summary",
    ]
]
