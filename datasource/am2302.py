import time

import board
import adafruit_dht

READ_RETRIES = 15
RETRY_DELAY_SECONDS = 2.0


class AM2302DataSource:
    """
    A datasource source for climate (temperature, humidity) information
    """
    def __init__(self, pin=4):
        self.sensor = adafruit_dht.DHT22(getattr(board, 'D{0}'.format(pin)), use_pulseio=False)

    def read(self):
        """
        :return: [Humidity, Temperature] values.  Either or both can be None
        """
        for _ in range(READ_RETRIES):
            try:
                return self.sensor.humidity, self.sensor.temperature
            except RuntimeError:
                # Transient checksum/timing errors are normal for this sensor -- retry.
                time.sleep(RETRY_DELAY_SECONDS)
        return None, None
