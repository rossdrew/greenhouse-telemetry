
### Install InfluxDB: https://gist.github.com/boseji/bb71910d43283a1b84ab200bcce43c26
`curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -`
`lsb_release -a`

Get release codename

`sudo apt install apt-transport-https`
`echo "deb https://repos.influxdata.com/debian <CODENAME> stable" | sudo tee /etc/apt/sources.list.d/influxdb.list`
`sudo apt update`
`sudo apt-get install influxdb`

#### start on startup
`sudo systemctl enable influxdb`

#### start
`sudo service influxdb start`

### Grafana: https://pimylifeup.com/raspberry-pi-grafana/
`wget https://dl.grafana.com/oss/release/grafana_6.6.0_armhf.deb`
`sudo dpkg -i grafana_6.6.0_armhf.deb`
#### start on startup 
`sudo systemctl enable grafana-server`

#### start
`sudo systemctl start grafana-server`

Should be running on <server>:3000

### Python setup
`python3 -m venv .venv`
`.venv/bin/pip3 install -r requirements.txt`
