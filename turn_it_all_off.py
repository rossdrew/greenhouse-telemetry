import RPi.GPIO as GPIO
import time
from datetime import datetime
from datetime import time as dt_time

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

GPIO.output(light_channel, False)
GPIO.output(water_channel, False)
