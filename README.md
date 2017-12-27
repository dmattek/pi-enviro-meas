# Measure and visualise environmental conditions

This git contains: 

 - python scripts to measure:
	
	- temperature and humidity using [DHT-22](https://www.modmypi.com/blog/am2302-temphumidity-sensor) (also named as AM2302) sensor,
	- visible and IR light intensity using [TSL2561](https://www.adafruit.com/product/439) sensor.
 
 - cgi python scripts to visualise measurements through the web page (adapted from [Building an SQLite temperature logger](http://raspberrywebserver.com/cgiscripting/rpi-temperature-logger/building-an-sqlite-temperature-logger.html))
 

## Getting DHT sensor to work

Install Adafruit Python DHT Sensor Library from:
https://github.com/adafruit/Adafruit_Python_DHT

Make sure the sensor works and provides correct readings by executing

```
	sudo ./AdafruitDHT.py 2302 4
```

in `Adafruit_Python_DHT/examples` folder. The second parameter (`4`) is the GPIO pin to which the sensor is hooked. Change it if connected to a different GPIO.

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


## Set up the SQLite database

This part is inspired and adapted from [Building an SQLite temperature logger](http://raspberrywebserver.com/cgiscripting/rpi-temperature-logger/building-an-sqlite-temperature-logger.html).


