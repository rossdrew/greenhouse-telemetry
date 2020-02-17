
import datetime
import configparser

from time import sleep
from persistance.filestore import FileStore
from datasource.am2302 import AM2302DataSource
from datasource.weather import OpenWeatherMapDataSource
from datasource.cpu import CPU
#from datasource.test_data_source import TestClimateDataSource
from persistance.influxDb import InfluxDBStore, TimeSeriesMeasurementEntry

# Setup
config = configparser.RawConfigParser()
config.read('config.properties')

location = config.get('Weather', 'location')
open_weather_map_app_id = config.get('Weather', 'open_weather_map_app_id')

weather_data_source = OpenWeatherMapDataSource(location, open_weather_map_app_id)
#test_data_source = TestClimateDataSource()
am2302_data_source = AM2302DataSource(pin=config.get('AM2302', 'pin'))

file_store = FileStore()
influx_db_store = InfluxDBStore('TelemetryHistory')

cpu = CPU()
#######


while True:
    time = datetime.datetime.now()
    wH, wT = weather_data_source.read()
    #ghH, ghT = test_data_source.read()
    ghH, ghT = am2302_data_source.read()
    print("Greenhouse Temp: {0}, Weather Temp: {1}".format(ghT, wT))

    greenhouse = TimeSeriesMeasurementEntry(measurement='am2302',
                                            tags={"update": "whole",
                                                  "device": "am2302",
                                                  "location": "gh1"},
                                            fields={"temp": float(ghT),
                                                    "humidity": float(ghH)})
    greenhouse_data_persisted = influx_db_store.persist(greenhouse.to_record())
    file_store.persist(time, ghH, ghT)

    weather = TimeSeriesMeasurementEntry(measurement='weather',
                                         tags={"update": "whole",
                                               "device": "openweathermap",
                                               "location": "inverkeithing"},
                                         fields={"temp": float(wT),
                                                 "humidity": float(wH)}
                                         )
    weather_data_persisted = influx_db_store.persist(weather.to_record())

    print("[{0}] Greenhouse: {1}, Weather: {2}".format(time,
                                                       ("PERSISTED" if greenhouse_data_persisted else "ERR"),
                                                       ("PERSISTED" if weather_data_source else "ERR"),
                                                      )
          )

    cpu_data = TimeSeriesMeasurementEntry(measurement="cpu",
                                          tags={"device": "cpu"},
                                          fields={"temp": cpu.read()})

    cpu_data_persisted = influx_db_store.persist(cpu_data.to_record())

    sleep(60)
