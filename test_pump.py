import RPi.GPIO as GPIO
import time
import sys

water_channel = 23
duration_seconds = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0

GPIO.setmode(GPIO.BCM)
GPIO.setup(water_channel, GPIO.OUT)

try:
	print('Pump ON for {0}s...'.format(duration_seconds))
	GPIO.output(water_channel, True)
	time.sleep(duration_seconds)
finally:
	GPIO.output(water_channel, False)
	print('Pump OFF')
	GPIO.cleanup()
