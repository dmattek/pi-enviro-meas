# IR input sensor TSOP38238

## Connecting IR sensor

Follow instructions on [RPi Geek](http://www.raspberry-pi-geek.com/Archive/2014/03/Controlling-your-Pi-with-an-infrared-remote).

Three pins in the sensor (when looking at the front, from left to right) connect to:

 - OUT - GPIO18 (pin 12)
 - GND - ground
 - VS  - 3.3V
 
## Getting IR sensor to work

Follow instructions on [RPi Geek](http://www.raspberry-pi-geek.com/Archive/2014/03/Controlling-your-Pi-with-an-infrared-remote/(offset)/2).

Updated steps [here](https://gist.github.com/prasanthj/c15a5298eb682bde34961c322c95378b).

```
sudo apt-get install lirc liblircclient-dev
```

Add the following lines to '/etc/modules' file

```
lirc_dev
lirc_rpi gpio_in_pin=18
```

This is important! Uncomment in `/boot/config.txt`:
```
dtoverlay=lirc-rpi,gpio_in_pin=18
```


Edit `/etc/lirc/hardware.conf` by adding following lines:
```
 LIRCD_ARGS="--uinput --listen"
 LOAD_MODULES=true
 DRIVER="default"
 DEVICE="/dev/lirc0"
 MODULES="lirc_rpi"
```


Update the following lines in `/etc/lirc/lirc_options.conf`
```
driver    = default
device    = /dev/lirc0
```

```
sudo /etc/init.d/lircd stop
sudo /etc/init.d/lircd start
```

Check status to make lirc is running:
```
sudo /etc/init.d/lircd status
```
