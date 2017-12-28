# Measure and visualise environmental conditions

Tested on Raspberry Pi Zero.

This git contains: 

 - python scripts to measure:
	
	- temperature and humidity using [DHT-22](https://www.modmypi.com/blog/am2302-temphumidity-sensor) (also known as AM2302) sensor,
	- visible and IR light intensity using [TSL2561](https://www.adafruit.com/product/439) sensor,
 
 - cgi python scripts to visualise measurements via  web UI (adapted from [Building an SQLite temperature logger](http://raspberrywebserver.com/cgiscripting/rpi-temperature-logger/building-an-sqlite-temperature-logger.html)),
 
 - python script to visualise temperature, humidity and current time on Pimoroni's [Unicorn pHAT](https://shop.pimoroni.com/products/unicorn-phat), an 8x4 RGB LED matrix.
 

Environmental parameters are recorded in an SQLite database, which requires the entire setup to have an Apache web server and SQLite database installed on the system.

## Quick start

Assuming that the Apache server is running, the SQLite database is installed, and the home directory is `/home/pi`:

0. Get the repository from hithub:
```
git clone https://github.com/dmattek/pi-enviro-meas.git
```

This will create `pi-enviro-meas` in the folder from which the `git` command was executed. Note that all paths in scripts assume that the directory is located in `/home/pi`. Change paths in scripts accordingly if different!

1. Copy CGI scripts to default CGI directory of Apache server:
```
sudo cp pi-enviro-meas/dht/cgi-bin/webguidht.py /usr/lib/cgi-bin/.
sudo cp pi-enviro-meas/tsl2561/cgi-bin/webguilight.py /usr/lib/cgi-bin/.
```

2. Copy initialised databases:
```
sudo cp pi-enviro-meas/dht/data/dhtlog_template.db /var/www/dhtlog.db
sudo cp pi-enviro-meas/tsl2561/data/lightlog_template.db /var/www/lightlog.db
```

3. Add crontab jobs:

*/10 * * * * /home/pi/pi-enviro-meas/dht/meas/logdbDHT.sh
*/10 * * * * /home/pi/pi-enviro-meas/tsl2561/meas/logdbLight.sh
@reboot /home/pi/pi-enviro-meas/dht/meas/dispDHTonUnicorn.sh 


The result is the measurement of temperature and humidity from DHT-22 sensor logged to `/var/www/dhtlog.db`, and light intenisty (IR and visible) to `/var/www/lightlog.db` every 10 minutes. The temperature and humidity are fetched every 10 minutes from the `dhtlog.db` database and shown along with current time on Unicorn pHAT matrix as colour-coded bars. Environmental parameters can be viewed through web UI by pointing your browser to `http://you-pi-address/cgi-bin/webguidht.py` and `http://you-pi-address/cgi-bin/webguilight.py`.

## Set up Apache web server with CGI Python mod

Follow the instructions from [Run python script as cgi under apache2 server](https://www.raspberrypi.org/forums/viewtopic.php?t=155229).

Install Apache2 webserver:

```
	sudo apt-get install apache2 -y
```

Test Apache installation by typing the address of your Pi in a web browser. You should see a default page headlined by "It works!".


Enable mods in apache2 for cgi:

```
	sudo a2enmod cgid
	cd /etc/apache2/mods-enabled
	sudo ln -s /etc/apache2/mods-available/cgi.load
```
The default directory for cgi script is `/usr/lib/cgi-bin/`.

### Test CGI bash script

Test a simple bash CGI script by creating a `/usr/lib/cgi-bin/hello.cgi` file with the following contents:

```
	#!/bin/bash
	echo -e "Content-type: text/html\n\n"
	echo "<h1>Bash Script Test</h1>"
```
Make the script executable:

```
sudo chmod +x /usr/lib/cgi-bin/hello.cgi
```

Visit `http://pi-address/cgi-bin/hello.cgi`; you should see a big bold `Hello World` text.

### Test CGI Python script

Test a simple CGI Python script by creating a `/usr/lib/cgi-bin/pytest.cgi` file with the following contents:

```
	#!/usr/bin/python
	
	import cgi
	import cgitb
	cgitb.enable()

	print 'Content-type: text/html\n\n'
	print '<h1>Python Script Test</h1>'
```

Make the script executable:

```
sudo chmod +x /usr/lib/cgi-bin/pytest.cgi
```

Visit `http://pi-address/cgi-bin/pytest.cgi`; you should see a big bold `Python Script Test` text.

## Install SQLite

Run

```
sudo apt-get install sqlite3
```
