import configparser
import time

from datasource.mcp3008 import Mcp3008Adc

SAMPLES = 10
SAMPLE_DELAY_SECONDS = 0.2


def average_reading(mcp, channel):
    total = 0
    for _ in range(SAMPLES):
        total += mcp.read_adc(channel)
        time.sleep(SAMPLE_DELAY_SECONDS)
    return total / SAMPLES


config = configparser.RawConfigParser()
config.read('config.properties')
channel = config.getint('Soil', 'adc_channel')

mcp = Mcp3008Adc()

input('Place the sensor in dry air/soil, then press Enter...')
dry_adc = average_reading(mcp, channel)
print('Dry reading: {0}'.format(dry_adc))

input('Submerge the sensor in water, then press Enter...')
wet_adc = average_reading(mcp, channel)
print('Wet reading: {0}'.format(wet_adc))

print('\nPaste these into config.properties under [Soil]:')
print('dry_adc = {0}'.format(round(dry_adc)))
print('wet_adc = {0}'.format(round(wet_adc)))
