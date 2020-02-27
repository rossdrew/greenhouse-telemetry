from gpiozero import CPUTemperature

from persistance.influxDb import InfluxDBStore, TimeSeriesMeasurementEntry


class CPU:
    """
    Represents CPU as a data source
    """
    def __init__(self):
        self.cpu = CPUTemperature()

    def temperature(self):
        return float(self.cpu.temperature)

    def read_fields(self):
        t = self.read()
        if t is not None:
            return {"temp": t}
        else:
            return {}


class CPUConverter:
    """
        Tool for converting CPU to persistence formats, such as time series
    """
    def __init__(self, cpu_data_source):
        self.data_source = cpu_data_source

    def get_time_series_reading(self):
        """
        :return: a TimeSeriesMeasurementEntry for 'weather' containing 'temp' and 'humidity'
        """
        return TimeSeriesMeasurementEntry(measurement='cpu',
                                          tags={"device": "cpu",
                                                "location": "raspi"},
                                          fields=self.data_source.read_fields())
