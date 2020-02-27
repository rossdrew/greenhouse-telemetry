import datetime
import configparser

from time import sleep
from datasource.cpu import CPU, CPUConverter
from datasource.am2302 import AM2302DataSource, AM2303Converter
from datasource.weather import OpenWeatherMapDataSource, ClimateConverter
from persistance.influxDb import InfluxDBStore, TimeSeriesMeasurementEntry


class GreenhouseTelemetry:
    def __init__(self, store=None, *data_sources):
        assert store is not None
        self.data_sources = data_sources
        self.store = store

    def run(self):
        while True:
            time = datetime.datetime.now()
            for data_source in self.data_sources:
                data_source.get_time_series_reading()
                self.store.persist(data_source.to_record())
            sleep(60)


config = configparser.RawConfigParser()
config.read('config.properties')
location = config.get('Weather', 'location')
open_weather_map_app_id = config.get('Weather', 'open_weather_map_app_id')

weather_data_source = OpenWeatherMapDataSource(location, open_weather_map_app_id)
am2302_data_source = AM2302DataSource(pin=config.get('AM2302', 'pin'))
influx_db_store = InfluxDBStore('TelemetryHistory')
cpu_data_source = CPU()

weather = ClimateConverter(weather_data_source)
inner_climate = AM2303Converter(am2302_data_source)
cpu = CPUConverter(cpu_data_source)

gh = GreenhouseTelemetry(weather, inner_climate, cpu, store=influx_db_store)
