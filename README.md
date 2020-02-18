# Greenhouse Telemetry

_Some code experimenting with greenhouse telemetry and featured in my  [Greenhouse blog series](https://dev.to/rossdrew/technology-choices-in-monitoring-a-greenhouse-2ppf)_



![Grafana Screenshot Sample](./img/First%20Run.png?raw=true)

## Controller

Current using a Rasberry Pi 3 Model B v1.2 with Python.  Currently written in Python, this may change. 

## Temp/Humidity

We are using the [AM2302](https://cdn-shop.adafruit.com/datasheets/Digital+humidity+and+temperature+sensor+AM2302.pdf) wired as follows

```
VCC -> Pi Pin 1
GND -> Pi Pin 6
DATA -> Pi Pin 7
``` 

and the [Adafruit Python Drivers](https://github.com/adafruit/Adafruit_Python_DHT) which can be set up as follows

(1) Clone the drivers repo
```bash
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
```

(2) Make sure python is up to date
```bash
sudo apt-get upgrade
sudo apt-get install build-essential python-dev
```

(3) Install the Adafruit drivers
```bash
sudo python setup.py install
```

(4) Run the test to make sure it worked
```bash
cd examples
sudo ./AdafruitDHT.py 2302 4
```

## Local Temp/Humidity

Local weather data is retrieved from [OpenWeatherMap](https://openweathermap.org/) API and recorded to DB for each reading for comparison.

## Running Telemetry

Run the peripheral read loop

```bash
python read_cycle_v2.py
```

which will start to fill up data.csv and a specified InfluxDB, then run the Http server

```bash
python http_interface.py
```

which will provide test charts on http://{ip-address}:{port}/report generated from file based data.

Running in a test environment (not on a Raspberry Pi with a AM2302 sensor) will require swapping out the used of `TestClimateDataSource` for the `AM2302DataSource`.  I'm yet to figure out a nice way to automate this.

## Recording

Data is recorded to a local InfluxDB and local sensors are also recorded to a local file in CSV format.

#### Sample File Data

```
2019-05-24 12:55:30.221564,25.899999618530273,43.29999923706055
2019-05-24 12:56:30.807389,26.0,43.29999923706055
2019-05-24 12:57:31.394122,26.0,43.79999923706055
2019-05-24 12:58:31.980609,25.899999618530273,43.599998474121094
2019-05-24 12:59:32.566356,25.700000762939453,43.29999923706055
2019-05-24 13:00:33.143378,25.700000762939453,43.70000076293945
2019-05-24 13:01:33.729952,25.100000381469727,45.900001525878906
2019-05-24 13:02:34.316845,24.5,47.5
2019-05-24 13:03:34.903718,24.0,48.900001525878906
2019-05-24 13:04:35.490432,23.700000762939453,49.79999923706055
```

#### Sample Weather JSON Data

```json
{
	"coord": {
		"lon": -0,
		"lat": 0
	},
	"weather": [
		{
			"id": 500,
			"main": "Rain",
			"description": "light rain",
			"icon": "10d"
		}
	],
	"base": "stations",
	"main": {
		"temp": 10.49,
		"pressure": 1014,
		"humidity": 66,
		"temp_min": 8,
		"temp_max": 12.22
	},
	"visibility": 10000,
	"wind": {
		"speed": 3.1,
		"deg": 240
	},
	"clouds": {
		"all": 75
	},
	"dt": 1559121266,
	"sys": {
		"type": 1,
		"id": 1442,
		"message": 0.0063,
		"country": "GB",
		"sunrise": 1559101162,
		"sunset": 1559162573
	},
	"timezone": 3600,
	"id": 1,
	"name": "Location",
	"cod": 1
}
```

## Setup

##### Install [InfluxDB](https://gist.github.com/boseji/bb71910d43283a1b84ab200bcce43c26): 

```bash
curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
lsb_release -a
```

And with the Linux release codename

```bash
sudo apt install apt-transport-https
echo "deb https://repos.influxdata.com/debian <CODENAME> stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt update
sudo apt-get install influxdb
```

##### Start InfluxDD

```bash
sudo service influxdb start
```

or automatically run on startup

```bash
sudo systemctl enable influxdb
```

##### Install [Grafana](https://pimylifeup.com/raspberry-pi-grafana/)

```bash
wget https://dl.grafana.com/oss/release/grafana_6.6.0_armhf.deb
sudo dpkg -i grafana_6.6.0_armhf.deb
```

##### Start Grafana

```bash
sudo systemctl start grafana-server
```
 
or automatically run on startup
 
```bash
sudo systemctl enable grafana-server
```

Should be running on <server>:3000

##### Setup a Python environment

```bash
python3 -m venv .venv
.venv/bin/pip3 install -r requirements.txt
.venv/bin/pip3 install RPi.GPIO
```

### Developing / Debugging

Install sshfs, link development machine to Pi by mounting the source directory and open in development environment

```bash
dnf install sshfs
mkdir /mnt/pi/gh
sshfs pi@<PI_IP>:/mnt/pi/gh /home/src/pi/gh
```

### Plans

- Add power generation and usage monitoring
- Add light sensors, window state/control and perhaps automated watering
- Add camera
