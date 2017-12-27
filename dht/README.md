# Measuring temperature and humidity with DHT-22 sensor


## Getting DHT sensor to work

Install Adafruit Python DHT Sensor Library from:
https://github.com/adafruit/Adafruit_Python_DHT

Make sure the sensor works and provides correct readings by executing

```
	sudo ./AdafruitDHT.py 2302 4
```

in `Adafruit_Python_DHT/examples` folder. The second parameter (`4`) is the GPIO pin to which the sensor is hooked. Change it if connected to a different GPIO.


## Set up SQLite database for DHT measurements

This part is inspired and adapted from [Building an SQLite temperature logger](http://raspberrywebserver.com/cgiscripting/rpi-temperature-logger/building-an-sqlite-temperature-logger.html).

The template of the database is located in `pi-enviro-meas/dht/meas/data/dhtlog_template.db`. You can copy it to its destination:

```
sudo cp pi-enviro-meas/dht/meas/data/dhtlog_template.db /var/www/dhtlog.db
```


Or you can create a new database:

```
sqlite3 dhtlog.db
```

with a table `temps` with fields `timestamp`, `temp`, and `humid`:

```
BEGIN;
CREATE TABLE temps (timestamp DATETIME, temp NUMERIC, humid NUMERIC);
COMMIT;
```

Then move `dhtlog.db` to `/var/www` directory.

The database is created and initialized. Now it's time to record data.

## Log temperature and humidity into SQLite database

Execute the python script to log parameters in the sqlite database:

```
sudo pi-enviro-meas/dht/meas/logdbDHT.py
```

Copy `webguidht.py` script from `pi-enviro-meas/dht/cgi-bin/` to `/usr/lib/cgi-bin/` directory. Make sure the scipt is executable (`sudo chmod +x /usr/lib/cgi-bin/webguidht.py`).

Open the plotting script in the web browser `http://pi-address/cgi-bin/webguidht.py`, you should see the plot with two data points corresponding to temperature and humidity logged by `logdbDHT.py` script.

## Set-up cron task to perform measurement every 10 minutes

[Cron](https://www.raspberrypi.org/documentation/linux/usage/cron.md) is a tool for configuring scheduled tasks on Unix systems.

Type:

```
crontab -e
```

Choose the editor and add the following line at the end of the file:

```
*/10 * * * * /home/pi/pi-enviro-meas/dht/meas/logdbDHT.sh
```

This will run shell script (which executes the python script `logdbDHT.py`) every 10 minutes in the background. No action required after reboot. The script will keep runnning as configured in crontab.

## Visualize on Unicorn pHAT

Install libraries by following instructions in https://github.com/pimoroni/unicorn-hat

Here I used:

```
\curl -sS https://get.pimoroni.com/unicornhat | bash
```

All libraries are installed in `~/Pimoroni` directory. Test the pHAT by running one of the examples in `Pimoroni/unicornhat/examples`.

Run the script in the backgroud (even after logout):

```
nohup sudo python pi-enviro-meas/dht/meas/dispDHTonUnicorn.py > nohup.out &
```

The output is redirected to `nohup.out` file.

Add the following line to crontab to start the visualization after reboot:

```
@reboot /home/pi/pi-enviro-meas/dht/meas/dispDHTonUnicorn.sh
```
