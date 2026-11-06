from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

class WeatherInfluxLogger:

    def __init__(
        self,
        url,
        token,
        org,
        bucket
    ):

        self.url = url
        self.token = token
        self.org = org
        self.bucket = bucket

        self.client = InfluxDBClient(
            url=self.url,
            token=self.token,
            org=self.org
        )

        self.write_api = self.client.write_api(
            write_options=SYNCHRONOUS
        )


    def log_weather(self, weather):

        point = (
            Point("weather_current")

            .tag(
                "source",
                "open-meteo"
            )

            .tag(
                "location",
                "berkeley" #TO-DO: NO HARD CODING - eventually want the user to input coordinates 
            )

            .field(
                "temperature_2m",
                weather["temperature_2m"]
            )

            .field(
                "relative_humidity_2m",
                weather["relative_humidity_2m"]
            )

            .field(
                "is_day",
                weather["is_day"]
            )

            .field(
                "apparent_temperature",
                weather["apparent_temperature"]
            )

            .field(
                "precipitation",
                weather["precipitation"]
            )

            .field(
                "rain",
                weather["rain"]
            )

            .field(
                "weather_code",
                weather["weather_code"]
            )

            .field(
                "cloud_cover",
                weather["cloud_cover"]
            )

            .field(
                "wind_speed_10m",
                weather["wind_speed_10m"]
            )

            .field(
                "wind_direction_10m",
                weather["wind_direction_10m"]
            )

            .time(
                weather["timestamp"]
            )
        )

        self.write_api.write(
            bucket=self.bucket,
            org=self.org,
            record=point
        )


    def close(self):
        self.client.close()
