import configparser
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

SAMPLES = 10
SAMPLE_DELAY_SECONDS = 0.2

SPI_PORT = 0
SPI_DEVICE = 0


def average_reading(mcp, channel):
    total = 0
    for _ in range(SAMPLES):
        total += mcp.read_adc(channel)
        time.sleep(SAMPLE_DELAY_SECONDS)
    return total / SAMPLES


config = configparser.RawConfigParser()
config.read('config.properties')
channel = config.getint('Soil', 'adc_channel')

mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

input('Place the sensor in dry air/soil, then press Enter...')
dry_adc = average_reading(mcp, channel)
print('Dry reading: {0}'.format(dry_adc))

input('Submerge the sensor in water, then press Enter...')
wet_adc = average_reading(mcp, channel)
print('Wet reading: {0}'.format(wet_adc))

print('\nPaste these into config.properties under [Soil]:')
print('dry_adc = {0}'.format(round(dry_adc)))
print('wet_adc = {0}'.format(round(wet_adc)))
