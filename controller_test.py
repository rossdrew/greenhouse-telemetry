import time
import unittest

from controller import GreenhouseController, PumpBusyError


class FakeGpio:
    BCM = 'BCM'
    OUT = 'OUT'

    def __init__(self):
        self.mode = None
        self.setup_calls = []
        self.outputs = {}

    def setmode(self, mode):
        self.mode = mode

    def setup(self, channel, direction):
        self.setup_calls.append((channel, direction))

    def output(self, channel, value):
        self.outputs[channel] = bool(value)


class FakeAm2302:
    def __init__(self, humidity=55.0, temperature=21.0):
        self.humidity = humidity
        self.temperature = temperature

    def read(self):
        return self.humidity, self.temperature


class GreenhouseControllerTest(unittest.TestCase):
    def _make_controller(self, **overrides):
        kwargs = dict(
            gpio=FakeGpio(),
            light_channel=24,
            water_channel=23,
            am2302=FakeAm2302(),
            max_pump_seconds=20,
            default_pump_seconds=5,
        )
        kwargs.update(overrides)
        return GreenhouseController(**kwargs), kwargs['gpio']

    def test_initializes_outputs_off(self):
        controller, gpio = self._make_controller()
        self.assertEqual(gpio.outputs[24], False)
        self.assertEqual(gpio.outputs[23], False)

    def test_status_reports_sensor_and_switch_state(self):
        controller, gpio = self._make_controller(am2302=FakeAm2302(60.0, 22.5))
        status = controller.status()
        self.assertEqual(status['humidity'], 60.0)
        self.assertEqual(status['temperature'], 22.5)
        self.assertFalse(status['light_on'])
        self.assertFalse(status['pump_on'])
        self.assertIsNone(status['pump_seconds_remaining'])

    def test_set_light_toggles_gpio_and_state(self):
        controller, gpio = self._make_controller()

        self.assertTrue(controller.set_light(True))
        self.assertTrue(gpio.outputs[24])
        self.assertTrue(controller.status()['light_on'])

        self.assertFalse(controller.set_light(False))
        self.assertFalse(gpio.outputs[24])
        self.assertFalse(controller.status()['light_on'])

    def test_water_defaults_to_configured_seconds(self):
        controller, gpio = self._make_controller(default_pump_seconds=3)
        applied = controller.water()
        self.assertEqual(applied, 3)
        self.assertTrue(gpio.outputs[23])
        controller.shutdown()

    def test_water_is_clamped_to_max_pump_seconds(self):
        controller, gpio = self._make_controller(max_pump_seconds=10)
        applied = controller.water(999)
        self.assertEqual(applied, 10)
        controller.shutdown()

    def test_water_rejects_non_positive_seconds(self):
        controller, gpio = self._make_controller()
        with self.assertRaises(ValueError):
            controller.water(0)

    def test_water_turns_pump_off_after_duration(self):
        controller, gpio = self._make_controller()
        controller.water(0.05)
        self.assertTrue(gpio.outputs[23])
        time.sleep(0.2)
        self.assertFalse(gpio.outputs[23])
        self.assertFalse(controller.status()['pump_on'])

    def test_water_while_already_running_raises(self):
        controller, gpio = self._make_controller()
        controller.water(1)
        with self.assertRaises(PumpBusyError):
            controller.water(1)
        controller.shutdown()

    def test_shutdown_cancels_pending_timer_and_turns_outputs_off(self):
        controller, gpio = self._make_controller()
        controller.set_light(True)
        controller.water(5)

        controller.shutdown()

        self.assertFalse(gpio.outputs[24])
        self.assertFalse(gpio.outputs[23])
        self.assertFalse(controller.status()['light_on'])
        self.assertFalse(controller.status()['pump_on'])


if __name__ == '__main__':
    unittest.main()
