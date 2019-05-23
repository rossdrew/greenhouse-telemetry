import csv
import datetime
import Adafruit_DHT

from time import sleep

sensor = Adafruit_DHT.AM2302
pin = 4


def get_readings():
    humidity, temp = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temp is not None:
        # TODO record
        return humidity, temp
    else:
        print('ERROR: Failure retrieving Humidity/Temp')


# Record Loop
with open('data.csv', mode='a+') as data_file:
    csv_file = csv.writer(data_file, delimiter=',')
    while True:
        # sleep(60)
        time = datetime.datetime.now()
        h, t = get_readings()
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(t, h))
        csv_file.writerow([time, t, h])

