import threading
import time


class PumpBusyError(Exception):
    """Raised when a water request arrives while the pump is already running."""


class GreenhouseController:
    """
    Owns the light and pump GPIO outputs and the temperature/humidity sensor, and exposes the
    read/write operations the REST API needs. `gpio` and `am2302` are injected so this can be
    unit tested without hardware.
    """
    def __init__(self, gpio, light_channel, water_channel, am2302, max_pump_seconds, default_pump_seconds):
        self.gpio = gpio
        self.light_channel = light_channel
        self.water_channel = water_channel
        self.am2302 = am2302
        self.max_pump_seconds = max_pump_seconds
        self.default_pump_seconds = default_pump_seconds

        self._lock = threading.Lock()
        self._light_on = False
        self._pump_timer = None
        self._pump_off_at = None

        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setup(self.light_channel, self.gpio.OUT)
        self.gpio.setup(self.water_channel, self.gpio.OUT)
        self.gpio.output(self.light_channel, False)
        self.gpio.output(self.water_channel, False)

    def status(self):
        humidity, temperature = self.am2302.read()
        with self._lock:
            pump_seconds_remaining = None
            if self._pump_off_at is not None:
                pump_seconds_remaining = max(0.0, self._pump_off_at - time.monotonic())
            return {
                'temperature': temperature,
                'humidity': humidity,
                'light_on': self._light_on,
                'pump_on': self._pump_off_at is not None,
                'pump_seconds_remaining': pump_seconds_remaining,
                'max_pump_seconds': self.max_pump_seconds,
                'default_pump_seconds': self.default_pump_seconds,
            }

    def set_light(self, on):
        on = bool(on)
        with self._lock:
            self.gpio.output(self.light_channel, on)
            self._light_on = on
        return on

    def water(self, seconds=None):
        seconds = self.default_pump_seconds if seconds is None else float(seconds)
        if seconds <= 0:
            raise ValueError('seconds must be positive')
        seconds = min(seconds, self.max_pump_seconds)

        with self._lock:
            if self._pump_timer is not None:
                raise PumpBusyError('Pump is already running')

            self.gpio.output(self.water_channel, True)
            self._pump_off_at = time.monotonic() + seconds
            self._pump_timer = threading.Timer(seconds, self._stop_pump)
            self._pump_timer.daemon = True
            self._pump_timer.start()

        return seconds

    def _stop_pump(self):
        with self._lock:
            self.gpio.output(self.water_channel, False)
            self._pump_timer = None
            self._pump_off_at = None

    def shutdown(self):
        with self._lock:
            if self._pump_timer is not None:
                self._pump_timer.cancel()
            self._pump_timer = None
            self._pump_off_at = None
            self.gpio.output(self.light_channel, False)
            self.gpio.output(self.water_channel, False)
            self._light_on = False
