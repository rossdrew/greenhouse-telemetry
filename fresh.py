import configparser

from datasource.am2302 import AM2302DataSource
from datasource.mcp3008 import Mcp3008Adc

config = configparser.RawConfigParser()
config.read('config.properties')

print("--- AM2302 (temperature/humidity) ---")
am2302_data_source = AM2302DataSource(pin=config.getint('AM2302', 'pin'))
humidity, temperature = am2302_data_source.read()

if humidity is None or temperature is None:
    print("FAILED to read AM2302 -- check VCC/GND/DATA wiring and the pull-up resistor")
else:
    print("Temp: {0:.1f} C, Humidity: {1:.1f}%".format(temperature, humidity))
    if not (-10 <= temperature <= 50):
        print("  WARNING: temperature reading looks out of plausible range")
    if not (0 <= humidity <= 100):
        print("  WARNING: humidity reading looks out of plausible range")

print("\n--- MCP3008 (ADC) ---")
mcp = Mcp3008Adc()
readings = [mcp.read_adc(channel) for channel in range(8)]
print("Channel readings (0-1023): {0}".format(readings))

soil_channel = config.getint('Soil', 'adc_channel')
soil_reading = readings[soil_channel]
if soil_reading in (0, 1023):
    print("  WARNING: channel {0} is pinned at {1} -- check wiring "
          "(floating input, or a short to GND/VCC)".format(soil_channel, soil_reading))
else:
    print("  Soil channel {0}: {1} (cover/uncover the sensor and re-run -- "
          "this value should change)".format(soil_channel, soil_reading))
