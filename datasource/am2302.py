import Adafruit_DHT

from persistance.influxDb import InfluxDBStore, TimeSeriesMeasurementEntry


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

    def read_fields(self):
        h, t = self.read()
        if h is not None and t is not None:
            return {"humidity": h, "temp": t}
        else:
            return {}


class AM2303Converter:
    """
        Tool for converting AM2302DataSource to persistence formats, such as time series
    """
    def __init__(self, am2303_data_source):
        self.data_source = am2303_data_source

    def get_time_series_reading(self):
        """
        :return: a TimeSeriesMeasurementEntry for 'weather' containing 'temp' and 'humidity'
        """
        return TimeSeriesMeasurementEntry(measurement='inner climate',
                                          tags={"update": "whole",
                                                "device": "AM2302",
                                                "location": "GH1"},
                                          fields=self.data_source.read_fields())
