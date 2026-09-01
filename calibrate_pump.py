import configparser
import sys
import time

import RPi.GPIO as GPIO

DEFAULT_RUN_SECONDS = 10.0

config = configparser.RawConfigParser()
config.read('config.properties')
water_channel = config.getint('Watering', 'water_channel')
max_pump_seconds = config.getint('Watering', 'max_pump_seconds')

run_seconds = float(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_RUN_SECONDS
run_seconds = min(run_seconds, max_pump_seconds)

GPIO.setmode(GPIO.BCM)
GPIO.setup(water_channel, GPIO.OUT)
GPIO.output(water_channel, False)

try:
    input('Place the pump outlet into a measuring container, then press Enter to run it for '
          '{0}s...'.format(run_seconds))
    GPIO.output(water_channel, True)
    time.sleep(run_seconds)
finally:
    GPIO.output(water_channel, False)

volume_ml = float(input('Measured volume collected (ml): '))
ml_per_second = volume_ml / run_seconds

print('\nPaste this into config.properties under [Watering]:')
print('ml_per_second = {0:.2f}'.format(ml_per_second))

GPIO.cleanup()
