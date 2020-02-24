import requests

from http import HTTPStatus


class OpenWeatherMapDataSource:
    def __init__(self, location, app_id):
        self.location = location
        self.app_if = app_id
        self.url = 'https://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units=metric'.format(location,
                                                                                                         app_id)

    def read(self):
        try:
            resp = requests.get(self.url)
            if resp.status_code == HTTPStatus.OK:
                weather_data = resp.json()
                humidity = weather_data['main']['humidity']
                temp = weather_data['main']['temp']
                return humidity, temp
            else:
                print("ERROR: Fetching datasource: {0}".format(resp))
        except requests.exceptions.RequestException as e:
            print("Exception while retrieving weather information: {0}".format(e))

        return None, None
