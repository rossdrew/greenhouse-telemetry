import datetime
import configparser

from time import sleep
from persistance.filestore import FileStore
from datasource.am2302 import AM2302DataSource
from datasource.weather import OpenWeatherMapDataSource
from datasource.cpu import CPU
# from datasource.test_data_source import TestClimateDataSource
from persistance.influxDb import InfluxDBStore, TimeSeriesMeasurementEntry

# Setup
config = configparser.RawConfigParser()
config.read('config.properties')

deployment_name = config.get('Deploy', 'name')

location = config.get('Weather', 'location')
open_weather_map_app_id = config.get('Weather', 'open_weather_map_app_id')

weather_data_source = OpenWeatherMapDataSource(location, open_weather_map_app_id)
# test_data_source = TestClimateDataSource()
am2302_data_source = AM2302DataSource(pin=config.get('AM2302', 'pin'))

file_store = FileStore()
influx_db_store = InfluxDBStore('TelemetryHistory')

cpu = CPU()
#######


while True:
    time = datetime.datetime.now()
    wH, wT = weather_data_source.read()
    # ghH, ghT = test_data_source.read()
    ghH, ghT = am2302_data_source.read()
    print("Greenhouse Temp: {0}, Weather Temp: {1}".format(ghT, wT))

    greenhouse = TimeSeriesMeasurementEntry(measurement='am2302',
                                            tags={"update": "whole",
                                                  "device": "am2302",
                                                  "deployment": deployment_name},
                                            fields={"temp": float(ghT),
                                                    "humidity": float(ghH)})
    greenhouse_data_persisted = influx_db_store.persist(greenhouse.to_record())
    file_store.persist(time, ghH, ghT)

    if wH is not None and wT is not None:
        weather = TimeSeriesMeasurementEntry(measurement='weather',
                                             tags={"update": "whole",
                                                   "device": "openweathermap",
                                                   "location": location,
                                                   "deployment": deployment_name},
                                             fields={"temp": float(wT),
                                                     "humidity": float(wH)}
                                             )
        weather_data_persisted = influx_db_store.persist(weather.to_record())
    else:
        weather_data_persisted = False

    cpu_data = TimeSeriesMeasurementEntry(measurement="cpu",
                                          tags={"device": "cpu",
                                                "deployment": deployment_name},
                                          fields={"temp": cpu.temperature()})

    cpu_data_persisted = influx_db_store.persist(cpu_data.to_record())

    print("[{0}] Greenhouse: {1}, Weather: {2}, CPU: {3}".format(time,
                                                                 ("PERSISTED" if greenhouse_data_persisted else "ERR"),
                                                                 ("PERSISTED" if weather_data_source else "ERR"),
                                                                 ("PERSISTED" if cpu_data_persisted else "ERR"),
                                                                 )
          )

    sleep(60)
