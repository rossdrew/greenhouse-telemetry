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