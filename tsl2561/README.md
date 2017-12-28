# Measure visible and IR light intensity with TSL2561

## Enable I2C, SMBus
From: https://www.abelectronics.co.uk/kb/article/1/i2c--smbus-and-raspbian-linux

If you are using Raspian Linux 3.18 or later you need to go into the raspberry pi config utility and enable I2C.

```
sudo raspi-config
```

Select 5 Interfacing Options and then  P5 I2C. A prompt will appear asking Would you like the ARM I2C interface to be enabled?, select Yes, exit the utility and reboot your raspberry pi.

```
sudo reboot
```

Install `smbus` tools for python:

```
sudo apt-get install python-smbus python3-smbus python-dev python3-dev
sudo apt-get install i2c-tools
```

## Add measurements to the DB

```
sudo pi-enviro-meas/tsl2561/meas/logdbLight.py 
```

## Set-up cron task to perform measurement every 10 minutes

[Cron](https://www.raspberrypi.org/documentation/linux/usage/cron.md) is a tool for configuring scheduled tasks on Unix systems.

Type:

```
crontab -e
```

Choose the editor and add the following line at the end of the file:

```
*/10 * * * * /home/pi/pi-enviro-meas/tsl2561/meas/logdbLight.sh 
```

This will run shell script (which executes the python script `logdbDHT.py`) every 10 minutes in the background. No action required after reboot. The script will keep runnning as configured in crontab.
