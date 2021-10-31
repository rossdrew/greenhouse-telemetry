import RPi.GPIO as GPIO
import time
from datetime import datetime
from datetime import time as dt_time
import signal, sys

#sudo pip install adafruit-mcp30008
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

light_channel = 24
water_channel = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(light_channel, GPIO.OUT)
GPIO.setup(water_channel, GPIO.OUT)

# Software SPI configuration:
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

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
	elif light_on:
		print('Sun down at {}'.format(current_time))
		GPIO.output(light_channel, False)
		light_on = False
		
	readings = [0]*8
	for i in range(8):
		readings[i] = mcp.read_adc(i)
	print('\t {} Water level: {}'.format(current_time, readings[0]))
	time.sleep(0.5)
		
	time.sleep(60)

#test_run()



		
