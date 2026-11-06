import time

from open_meteo_python import get_current_weather
from logger import WeatherInfluxLogger


INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "YOUR_TOKEN" #TO-DO
INFLUX_ORG = "YOUR_ORG" #TO-DO
INFLUX_BUCKET = "weather" #TO-DO


logger = WeatherInfluxLogger(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG,
    bucket=INFLUX_BUCKET
)


try:

    while True:
        weather = get_cuttent_weather() #grabs the 'current' weather from open meteo, saves into variable
        logger.log_weather(weather)
        print("Weather written to InfluxDB:",weather)
        # 15 minutes
        time.sleep(900) #How often we refresh data

except KeyboardInterrupt:
    print("Weather logger stopped.") #Message for when system is disconnted 

finally:
    logger.close() #finished using system
