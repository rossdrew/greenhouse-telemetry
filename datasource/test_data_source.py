import random


class TestClimateDataSource:
    """
    A testing datasource source for climate which generates random values
    """
    def read(self):
        """
        :return: [Humidity, Temperature] values.  Either or both can be None
        """
        return random.uniform(0, 100), random.uniform(10, 40)


class TestSoilMoistureDataSource:
    """
    A testing datasource for soil moisture which generates random values, matching the
    shape of SoilMoistureDataSource.read()
    """
    def __init__(self, force_fault=False):
        self.force_fault = force_fault

    def read(self):
        """
        :return: (raw_adc, moisture_percent). Both are None when force_fault is set, so the
                 sensor fail-safe path is exercisable without hardware.
        """
        if self.force_fault:
            return None, None
        return random.randint(0, 1023), random.uniform(0, 100)