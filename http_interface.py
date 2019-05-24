import csv
import pygal  # Graph

from flask import Flask, render_template  # HTTP
from datetime import datetime

print("Greenhouse RasPi Server...")


# TODO data update with currentDataTime from http://worldclockapi.com/api/json/gmt/now
# or unixtime from http://worldtimeapi.org/api/timezone/Europe/London.txt

def read_data():
    time_range = []
    temperature_history = []
    humidity_history = []

    with open('data.csv', mode='r') as data_file:
        for row in csv.reader(data_file, delimiter=','):
            if len(row) < 3:
                 continue;
            time = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
            temp = float(row[1])
            humidity = float(row[2])
            print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temp, humidity))

            temperature_history.append((time, temp))
            humidity_history.append((time, humidity))
            time_range.append(time)

    return {
        'T': time_range,
        't': temperature_history,
        'h': humidity_history
    }


def test_chart():
    print("Generating Weekly Chart Test")

    data = read_data()
    # date_range = (data['T'][0], data['T'][len(data['T']) - 1])
    chart = pygal.DateTimeLine(x_label_rotation=35,
                               x_value_formatter=lambda dt: dt.strftime('%d, %b %I:%M:%S %p'))
    chart.add('Temp', data['t'])
    chart.add('Humidity', data['h'], secondary=True)

    return chart


app = Flask(__name__, template_folder='.')


@app.route('/report')
def home():
    chart = test_chart()
    chart_uri = chart.render_data_uri()
    return render_template('greenhouse.html', chart=chart_uri)


if __name__ == "__main__":
    app.run(debug=True, host="192.168.1.72") #192.168.1.72
