import csv
import datetime
import Adafruit_DHT

from time import sleep
from influxdb import InfluxDBClient

sensor = Adafruit_DHT.AM2302
pin = 4


def get_readings():
    '''
    :return: (humidity_reading, temperature_reading)
    '''
    humidity, temp = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temp is not None:
        return humidity, temp
    else:
        print('ERROR: Failure retrieving Humidity/Temp')


def record_reading_to_db(humidity_reading, time_reading):
    '''
    Record the humidity_reading and time_reading for the given time in a time series database
    '''
    dbClient = InfluxDBClient('localhost', 8086, 'root', 'root', 'TelemetryHistory')
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
                "temp": time_reading,
                "humidity": humidity_reading
            }
        }
    ]
    write_success = dbClient.write_points(record_entry)
    print("Written!" if write_success else "ERROR: Not Written!")
    #loginRecords = dbClient.query('select * from am2302')
    #for point in loginRecords.get_points():
    #    print(point)
    #dbs = dbClient.get_list_database()
    #print(dbs)
    dbClient.close()


def record_reading_to_file(time, humidity_reading, time_reading):
    '''
    Record the humidity_reading and time_reading for the given time in a local file
    '''
    with open('data.csv', mode='a+') as data_file:
        csv_file = csv.writer(data_file, delimiter=',')
        print('@{0}, Saved: Temp={1:0.1f}*  Humidity={2:0.1f}%'.format(time, time_reading, humidity_reading))
        csv_file.writerow([time, time_reading, humidity_reading])


while True:
    '''
    Main program loop
    '''
    time = datetime.datetime.now()
    h, t = get_readings()
    print('Read @{0}: Temp={1:0.1f}*  Humidity={2:0.1f}%'.format(time, t, h))
    # Make sure measurements are not invalid reading
    if h >= 0 and h <= 100:
        record_reading_to_db(time, h, t)
        record_reading_to_file(time, h, t)
        sleep(60)
