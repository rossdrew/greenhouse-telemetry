import Adafruit_DHT


class AM2302DataSource:
    """
    A datasource source for climate (temperature, humidity) information
    """
    def __init__(self, pin=4):
        self.sensor = Adafruit_DHT.AM2302
        self.pin = pin

    def read(self):
        """
        :return: [Humidity, Temperature] values.  Either or both can be None
        """
        return Adafruit_DHT.read_retry(self.sensor, self.pin)
