# Wetter weekends

This script gets historical weather data for a location (right now Montevideo, Uruguay) by leveraging Dark Sky's API, which allows for 1000 free calls per day. The script allows requests to be saved and reused at a later day in order to circumvent the free API limitation.

The end-game for this project is to prove (or reject) the hypothesis that weather during weekends sucks compared to weekdays in Uruguay, and whether this is true for other cities in the region.

Resources exist for historical weather data in Uruguay (see for example [INIA's Banco Agroclimático](http://www.inia.uy/gras/Clima/Banco-datos-agroclimatico/)). However, the goal is obtain comparable data for several locations around the world, which is why I'm using a single source.
