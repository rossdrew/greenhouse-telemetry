import configparser
import signal
import sys

import RPi.GPIO as GPIO
from flask import Flask, jsonify, request

from controller import GreenhouseController, PumpBusyError
from datasource.am2302 import AM2302DataSource
from datasource.mcp3008 import Mcp3008Adc
from datasource.soil_moisture import SoilMoistureDataSource

light_channel = 24
water_channel = 23

config = configparser.RawConfigParser()
config.read('config.properties')

am2302 = AM2302DataSource(pin=config.getint('AM2302', 'pin'))

mcp = Mcp3008Adc()
soil_moisture = SoilMoistureDataSource(
    mcp,
    adc_channel=config.getint('Soil', 'adc_channel'),
    dry_adc=config.getint('Soil', 'dry_adc'),
    wet_adc=config.getint('Soil', 'wet_adc'),
    min_valid_adc=config.getint('Soil', 'min_valid_adc'),
    max_valid_adc=config.getint('Soil', 'max_valid_adc'),
)

controller = GreenhouseController(
    gpio=GPIO,
    light_channel=light_channel,
    water_channel=water_channel,
    am2302=am2302,
    soil_moisture=soil_moisture,
    max_pump_seconds=config.getint('Watering', 'max_pump_seconds'),
    default_pump_seconds=config.getint('Watering', 'default_pump_seconds', fallback=5),
)

app = Flask(__name__)


def _shutdown(sig, frame):
    print('\nShutting down, turning off light and pump...')
    controller.shutdown()
    GPIO.cleanup()
    sys.exit(0)


signal.signal(signal.SIGINT, _shutdown)
signal.signal(signal.SIGTERM, _shutdown)


@app.get('/api/status')
def get_status():
    return jsonify(controller.status())


@app.post('/api/light')
def set_light():
    body = request.get_json(silent=True) or {}
    if 'on' not in body:
        return jsonify(error="'on' (boolean) is required"), 400
    light_on = controller.set_light(bool(body['on']))
    return jsonify(light_on=light_on)


@app.post('/api/water')
def water():
    body = request.get_json(silent=True) or {}
    seconds = body.get('seconds')
    try:
        applied_seconds = controller.water(seconds)
    except PumpBusyError as e:
        return jsonify(error=str(e)), 409
    except (TypeError, ValueError):
        return jsonify(error="'seconds' must be a positive number"), 400
    return jsonify(watering_seconds=applied_seconds)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
