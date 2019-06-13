import csv
import datetime
import requests
import Adafruit_DHT
import configparser

from time import sleep
from http import HTTPStatus
from influxdb import InfluxDBClient

config = configparser.RawConfigParser()
config.read('config.properties')

sensor = Adafruit_DHT.AM2302
pin = config.get('AM2302', 'pin')

location = config.get('Weather', 'location')
open_weather_map_app_id = config.get('Weather', 'open_weather_map_app_id')


def get_weather_readings():
    url = 'https://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units=metric'.format(location,
                                                                                                open_weather_map_app_id)
    try:
        resp = requests.get(url)
        if resp.status_code == HTTPStatus.OK:
            weather_data = resp.json()
            print(weather_data)
            humidity = weather_data['main']['humidity']
            temp = weather_data['main']['temp']
            return humidity, temp
        else:
            print("ERROR: Fetching data. resp")
            return None, None
    except requests.exceptions.RequestException as e:
        print("Exception while retrieving weather information: {0}".format(e))
        return None, None


def get_am2302_readings():
    """
    :return: (humidity_reading, temperature_reading)
    """
    humidity, temp = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temp is not None:
        return humidity, temp
    else:
        print('ERROR: Failure retrieving Humidity/Temp')


def record_reading_to_db(humidity_reading, temp_reading):
    """
    Record the humidity_reading and time_reading for the given time in a time series database
    """
    db_client = InfluxDBClient('localhost', 8086, 'root', 'root', 'TelemetryHistory')
    record_entry = [
        {
            "measurement": "am2302",
            "tags": {
                "update": "whole",
                "device": "am2302",
                "location": "gh1"
            },
            #"time": "2009-11-10T23:00:00Z",
            "fields": {
                "temp": float(temp_reading),
                "humidity": float(humidity_reading)
            }
        }
    ]
    write_success = db_client.write_points(record_entry)
    print("Written!" if write_success else "ERROR: Not Written!")
    db_client.close()


def record_weather_to_db(humidity_reading, temp_reading):
    db_client = InfluxDBClient('localhost', 8086, 'root', 'root', 'TelemetryHistory')
    record_entry = [
        {
            "measurement": "weather",
            "tags": {
                "update": "whole",
                "device": "openweathermap",
                "location": "inverkeithing"
            },
            #"time": "2009-11-10T23:00:00Z",
            "fields": {
                "temp": float(temp_reading),
                "humidity": float(humidity_reading)
            }
        }
    ]
    write_success = db_client.write_points(record_entry)
    print("Written!" if write_success else "ERROR: Not Written!")


def record_reading_to_file(time, humidity_reading, time_reading):
    """
    Record the humidity_reading and time_reading for the given time in a local file
    """
    with open('data.csv', mode='a+') as data_file:
        csv_file = csv.writer(data_file, delimiter=',')
        print('@{0}, Saved: Temp={1:0.1f}*  Humidity={2:0.1f}%'.format(time, time_reading, humidity_reading))
        csv_file.writerow([time, time_reading, humidity_reading])


while True:
    """
    Main program loop
    """
    time = datetime.datetime.now()
    h, t = get_am2302_readings()
    hE, tE = get_weather_readings()
    print('Read @{0}: Temp={1:0.1f}*  Humidity={2:0.1f}%'.format(time, t, h))
    # Make sure measurements are not invalid reading
    if 0 <= h <= 100:
        record_reading_to_db(h, t)
        record_reading_to_file(time, h, t)
        if hE is not None:
            record_weather_to_db(hE, tE)
        sleep(60)
