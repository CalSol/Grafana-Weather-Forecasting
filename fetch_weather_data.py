import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below

# trying out processing hourly data
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 37.8719,
	"longitude": -122.2591,
	"hourly": ["temperature_2m", "relative_humidity_2m", "is_day", "apparent_temperature", "precipitation", "rain", "weather_code", "cloud_cover", "wind_speed_10m", "wind_direction_10m"],
	"forecast_days": 5, # initially 1
	"wind_speed_unit": "ms",
}

# asking the api for data
responses = openmeteo.weather_api(url, params = params)

# OG code
# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")




# same thing as old code, but now fetching hourly data instead
hour = response.Hourly()
hour_temperature_2m = hour.Variables(0).ValuesAsNumpy()
hour_relative_humidity_2m = hour.Variables(1).ValuesAsNumpy()
hour_is_day = hour.Variables(2).ValuesAsNumpy()
hour_apparent_temperature = hour.Variables(3).ValuesAsNumpy()
hour_precipitation = hour.Variables(4).ValuesAsNumpy()
hour_rain = hour.Variables(5).ValuesAsNumpy()
hour_weather_code = hour.Variables(6).ValuesAsNumpy()
hour_cloud_cover = hour.Variables(7).ValuesAsNumpy()
hour_wind_speed_10m = hour.Variables(8).ValuesAsNumpy()
hour_wind_direction_10m = hour.Variables(9).ValuesAsNumpy()

# creating a dictionary to store our data
# pd.date range -> building a list of time intervals, hour 1, hour 2 etc.
hourly_data = {
    "date": pd.date_range(
        start=pd.to_datetime(hour.Time(), unit="s", utc=True),
        end=pd.to_datetime(hour.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hour.Interval()),
        inclusive="left",
    )
}

# inputting info into dictionary
hourly_data["temperature_2m"] = hour_temperature_2m
hourly_data["relative_humidity_2m"] = hour_relative_humidity_2m
hourly_data["is_day"] = hour_is_day
hourly_data["apparent_temperature"] = hour_apparent_temperature
hourly_data["precipitation"] = hour_precipitation
hourly_data["rain"] = hour_rain
hourly_data["weather_code"] = hour_weather_code
hourly_data["cloud_cover"] = hour_cloud_cover
hourly_data["wind_speed_10m"] = hour_wind_speed_10m
hourly_data["wind_direction_10m"] = hour_wind_direction_10m

# converting to table and printing
hourly_dataframe = pd.DataFrame(data=hourly_data)
print(hourly_dataframe)
