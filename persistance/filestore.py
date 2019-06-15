import csv


class FileStore:
    """
    Representation for a File store
    """

    def __init__(self, file='datasource.csv', delimiter=','):
        self.file = file
        self.delimiter = delimiter

    def persist(self, time, humidity, temp):
        with open(self.file, mode='a+') as data_file:
            csv_file = csv.writer(data_file, delimiter=self.delimiter)
            csv_file.writerow([time, humidity, temp])
