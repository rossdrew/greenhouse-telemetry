import requests

from http import HTTPStatus
from persistance.influxDb import InfluxDBStore, TimeSeriesMeasurementEntry


class OpenWeatherMapDataSource:
    def __init__(self, location, app_id):
        self.location = location
        self.app_if = app_id
        self.url = 'https://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units=metric'.format(location,
                                                                                                         app_id)

    def read(self):
        try:
            resp = requests.get(self.url)
            if resp.status_code == HTTPStatus.OK:
                weather_data = resp.json()
                humidity = weather_data['main']['humidity']
                temp = weather_data['main']['temp']
                return humidity, temp
            else:
                print("ERROR: Fetching datasource: {0}".format(resp))
                return None, None
        except requests.exceptions.RequestException as e:
            print("Exception while retrieving weather information: {0}".format(e))
        return None, None

    def read_fields(self):
        h, t = self.read()
        if h is not None and t is not None:
            return {"humidity": h, "temp": t}
        else:
            return {}


class ClimateConverter:
    """
    Tool for converting OpenWeatherMapDataSource to persistence formats, such as time series
    """
    def __init__(self, climate_data_source):
        self.data_source = climate_data_source

    def get_time_series_reading(self):
        """
        :return: a TimeSeriesMeasurementEntry for 'weather' containing 'temp' and 'humidity'
        """
        return TimeSeriesMeasurementEntry(measurement='weather',
                                          tags={"update": "whole",
                                                "device": "openeathermap",
                                                "location": self.data_source.location},
                                          fields=self.data_source.read_fields())
