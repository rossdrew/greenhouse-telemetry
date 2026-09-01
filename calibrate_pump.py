import configparser
import csv
import datetime
import os
import sys
import time

import RPi.GPIO as GPIO

DEFAULT_RUN_SECONDS = 5.0
HISTORY_FILE = 'pump_calibration_history.csv'
HISTORY_FIELDS = ['timestamp', 'voltage', 'run_seconds', 'volume_ml', 'ml_per_second']


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, newline='') as f:
        return [row for row in csv.DictReader(f)]


def append_history(row):
    write_header = not os.path.exists(HISTORY_FILE)
    with open(HISTORY_FILE, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=HISTORY_FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerow(row)


def fit_linear(points):
    """
    Least-squares fit of ml_per_second = slope * voltage + intercept.
    :param points: [(voltage, ml_per_second), ...]
    :return: (slope, intercept), or None if the points don't span more than one voltage.
    """
    n = len(points)
    sum_x = sum(v for v, _ in points)
    sum_y = sum(r for _, r in points)
    sum_xy = sum(v * r for v, r in points)
    sum_xx = sum(v * v for v, _ in points)

    denominator = n * sum_xx - sum_x ** 2
    if denominator == 0:
        return None

    slope = (n * sum_xy - sum_x * sum_y) / denominator
    intercept = (sum_y - slope * sum_x) / n
    return slope, intercept


config = configparser.RawConfigParser()
config.read('config.properties')
water_channel = config.getint('Watering', 'water_channel')
max_pump_seconds = config.getint('Watering', 'max_pump_seconds')

run_seconds = float(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_RUN_SECONDS
run_seconds = min(run_seconds, max_pump_seconds)

voltage = float(input('Input voltage powering the pump right now (V): '))

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
    GPIO.cleanup()

volume_ml = float(input('Measured volume collected (ml): '))
ml_per_second = volume_ml / run_seconds

append_history({
    'timestamp': datetime.datetime.now().isoformat(timespec='seconds'),
    'voltage': voltage,
    'run_seconds': run_seconds,
    'volume_ml': volume_ml,
    'ml_per_second': '{0:.4f}'.format(ml_per_second),
})

print('\nThis reading ({0}V): {1:.2f} ml/s'.format(voltage, ml_per_second))
print('Paste this into config.properties under [Watering] if you want a single fixed rate:')
print('ml_per_second = {0:.2f}'.format(ml_per_second))
print('pump_voltage = {0}'.format(voltage))

history = load_history()
points = [(float(row['voltage']), float(row['ml_per_second'])) for row in history]
distinct_voltages = {v for v, _ in points}

print('\n{0} calibration reading(s) so far in {1}:'.format(len(points), HISTORY_FILE))
for row in history:
    print('  {0}V -> {1} ml/s (recorded {2})'.format(
        row['voltage'], row['ml_per_second'], row['timestamp']))

if len(distinct_voltages) >= 2:
    slope, intercept = fit_linear(points)
    print('\nLinear fit across {0} distinct voltages:'.format(len(distinct_voltages)))
    print('  ml_per_second = {0:.4f} * voltage + {1:.4f}'.format(slope, intercept))
    print('  e.g. at {0}V -> {1:.2f} ml/s'.format(voltage, slope * voltage + intercept))
else:
    print('\nRun this again at a different voltage to start fitting a voltage -> ml/s model.')
