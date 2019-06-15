from influxdb import InfluxDBClient


class InfluxDBStore:
    """
    Representation for an InfluxDB database
    """
    def __init__(self,
                 table,
                 server='localhost',
                 port=8086,
                 user='root',
                 password='root'):
        self.table = table
        self.server = server
        self.port = port
        self.user = user
        self.password = password

    def persist(self, time_series_measurement_entry):
        with InfluxDBClient(self.server,
                            self.port,
                            self.user,
                            self.password,
                            self.table) as db_client:
            write_success = db_client.write_points(time_series_measurement_entry)
            if not write_success:
                print("Failed to write entry {0}".format(time_series_measurement_entry))
            return write_success


class TimeSeriesMeasurementEntry:
    """
    Time series measurement data which can be converted to a formatted entry
    """
    def __init__(self,
                 measurement,
                 tags={},
                 fields={}):
        self.measurement = measurement
        self.tags = tags
        self.fields = fields

    def __str__(self):
        return "{0} measurement. tags:{1}, fields{2}".format(self.measurement, self.tags, self.measurement)

    def to_record(self):
        return [
            {
                "measurement": self.measurement,
                "tags": self.tags,
                #"time": "2009-11-10T23:00:00Z",
                "fields": self.fields
            }
        ]

