import RPi.GPIO as GPIO
import time
from datetime import datetime
from datetime import time as dt_time

light_channel = 24
water_channel = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(light_channel, GPIO.OUT)
GPIO.setup(water_channel, GPIO.OUT)

GPIO.output(light_channel, False)
GPIO.output(water_channel, False)
