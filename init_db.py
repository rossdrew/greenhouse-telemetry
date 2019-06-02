from influxdb import InfluxDBClient

dbClient = InfluxDBClient('localhost', 8086, 'root', 'root', 'TelemetryHistory')
dbClient.drop_database('TelemetryHistory')
dbClient.create_database('TelemetryHistory')
