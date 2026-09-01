import RPi.GPIO as GPIO
import configparser
import time
from datetime import datetime
from datetime import time as dt_time
import signal, sys

from datasource.am2302 import AM2302DataSource
from datasource.mcp3008 import Mcp3008Adc
from datasource.soil_moisture import SoilMoistureDataSource

config = configparser.RawConfigParser()
config.read('config.properties')

light_channel = 24
water_channel = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(light_channel, GPIO.OUT)
GPIO.setup(water_channel, GPIO.OUT)

mcp = Mcp3008Adc()
am2302 = AM2302DataSource(pin=config.getint('AM2302', 'pin'))
soil = SoilMoistureDataSource(
	mcp,
	adc_channel=config.getint('Soil', 'adc_channel'),
	dry_adc=config.getint('Soil', 'dry_adc'),
	wet_adc=config.getint('Soil', 'wet_adc'),
	min_valid_adc=config.getint('Soil', 'min_valid_adc'),
	max_valid_adc=config.getint('Soil', 'max_valid_adc'))

# Handler for Ctrl+C halt
def signal_hander(sig, frame):
	print('\nHard exit time, closing connections...')
	print('1/3 Forcing sunset...')
	GPIO.output(light_channel, False)
	print('2/3 Prohibiting rain...')
	GPIO.output(water_channel, False)
	print('3/3 Cleaning up environmental connections...')
	GPIO.cleanup()
	sys.exit(0)

sunrise = dt_time(8,30)
sunset = dt_time(20,00)

signal.signal(signal.SIGINT, signal_hander)

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print('Starting life cycle at {}'.format(current_time))

light_on = False
water_flowing = False

while True:
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	
	if sunrise < now.time() < sunset:
		if not light_on:
			print('Sun up at {}'.format(current_time))
			GPIO.output(light_channel, True)
			light_on = True
	elif light_on: #Sun isn't up and light is on
		print('Sun down at {}'.format(current_time))
		GPIO.output(light_channel, False)
		light_on = False

	humidity, temperature = am2302.read()
	raw_adc, moisture_percent = soil.read()

	temp_str = '{0:.1f} C'.format(temperature) if temperature is not None else 'N/A'
	humidity_str = '{0:.1f}%'.format(humidity) if humidity is not None else 'N/A'
	moisture_str = '{0:.1f}%'.format(moisture_percent) if moisture_percent is not None else 'N/A'

	print('\t {0} Temp: {1}, Humidity: {2}, Soil moisture: {3} (raw {4})'.format(
		current_time, temp_str, humidity_str, moisture_str, raw_adc))

	time.sleep(60)




		
