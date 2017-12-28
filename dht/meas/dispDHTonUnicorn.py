#!/usr/bin/python -u
# -*- coding: utf-8 -*-

# Fetches last record from SQLite DB and displays data 
# on Unicorn pHAT 4x8 RGB LED matrix.
# The DB should contain a table 'temps' with columns 
# 'timestamp', 'temp', and 'humid'.
#
# Two example visualisations implemented in:
#   dispMeas  - displays temperature and humidity as two horizontal bars 
#               with height and colour dependent on parameter values
#   dispMeas2 - displays temperature, humidity, and time (see details below)



# for sqlite
import sqlite3 as sql

# for unicorn hat
import unicornhat as unicorn

# other default
import sys
import time
from datetime import datetime as dt

# handles colour conversion
# from:
# https://github.com/vaab/colour
# sudo pip install colour
from colour import Color

# SQLite DB file location
DBFILE = '/var/www/dhtlog.db'

# max/min temp and humid
# this is to set bounds for display
# based on past measurements
MINTEMP = 17.0
MAXTEMP = 27.0
NSTEPSTEMP = 20

MINHUMID = 38.0
MAXHUMID = 78.0
NSTEPHUMID = 20

# important! add this to RGB value; otherwise pixels won't light up
COLOFFSET = 30

# This piece is from:
# http://zetcode.com/db/sqlitepythontutorial/
# Fetches last row from db specified by inDBname
def getDBrow(inDBname):
	try:
		conn=sql.connect(inDBname)
	
		# dictionary cursor
		conn.row_factory = sql.Row
	
		curs=conn.cursor()
	
		curs.execute("SELECT * FROM temps WHERE timestamp = (SELECT MAX(timestamp) FROM temps);")
	
		lrow = curs.fetchone()
	
		return lrow['temp'], lrow['humid']

	except sql.Error, e:
	
		print "Error %s:" % e.args[0]
		sys.exit(1)

	finally:
	
		if conn:
			conn.close()

# Visualisation of two parameters on an 8x4 RGB LED matrix (Pimoroni Unicorn pHAT)
# The two parameters are shown as two-rows-high horizontal bars.
# Both parameters are discretized into 8 bins beween respective MIN and MAX values.
def dispMeas(inHatWidth, inHatHeight, inMeas1, inMeas2):
	
	locHalfHeight = int(round(inHatHeight / 2))
	
	# print inMeas1 in rows 1 and 2
	# this is treated as Temperature
	# print inMeas2 in rows 3 and 4
	# this is treated as Humidity
	
	# clip measurements
	if inMeas1 < MINTEMP:
		inMeas1 = MINTEMP

	if inMeas1 > MAXTEMP:
		inMeas1 = MAXTEMP
	
	if inMeas2 < MINHUMID:
		inMeas2 = MINHUMID

	if inMeas2 > MAXHUMID:
		inMeas2 = MAXHUMID
	
	# setting colour gradients for Temperature
	ccRed = Color("red")
	ccBlue = Color("blue")
	locPal1 = list(ccBlue.range_to(ccRed, inHatWidth))

	# setting colour gradients for Humidity
	ccGreen = Color("green")
	ccOrange = Color("orange")
	locPal2 = list(ccRed.range_to(ccGreen, inHatWidth))
	

	# inMeas1 discretised as number of pixels out of max pixel width of the display
	locMeas1px = int(round((inMeas1 - MINTEMP) / (MAXTEMP - MINTEMP) * (inHatWidth - 1) + 1))
	print inMeas1, locMeas1px

	# print inMeas2 in rows 3 and 4
	locMeas2px = int(round((inMeas2 - MINHUMID) / (MAXHUMID - MINHUMID) * (inHatWidth - 1) + 1))
	print inMeas2, locMeas2px
	

	for yy in range(0, locHalfHeight):
		for xx in range(locMeas1px):
			locCols = locPal1[xx].rgb
			r = locCols[0] * 255
			g = locCols[1] * 255
			b = locCols[2] * 255
			r = max(0, min(255, r + COLOFFSET))
			g = max(0, min(255, g + COLOFFSET))
			b = max(0, min(255, b + COLOFFSET))

			unicorn.set_pixel(xx, yy, int(r), int(g), int(b))
			#print xx, yy, int(r), int(g), int(b)
			
		unicorn.show()
		time.sleep(0.1)

	for yy in range(locHalfHeight, inHatHeight):
		for xx in range(locMeas2px):
			locCols = locPal2[xx].rgb
			r = locCols[0] * 255
			g = locCols[1] * 255
			b = locCols[2] * 255
			r = max(0, min(255, r + COLOFFSET))
			g = max(0, min(255, g + COLOFFSET))
			b = max(0, min(255, b + COLOFFSET))

			unicorn.set_pixel(xx, yy, int(r), int(g), int(b))
			#print xx, yy, int(r), int(g), int(b)
			
		unicorn.show()
		time.sleep(0.1)
	
# Visualisation of 3 parameters on an 8x4 RGB LED matrix (Pimoroni Unicorn pHAT)
# The two parameters, inMaas1 and inMeas2 are shown as 4-rows-high vertical bars on left and right of the matrix
# The 3rd parameter visualised is time provided by inH (hours) and inM (minutes)

def dispMeas2(inHatWidth, inHatHeight, inMeas1, inMeas2, inH, inM):
	
	# print inMeas1 in column 1
	# this is treated as Temperature
	# print inMeas2 in column 8
	# this is treated as Humidity
	
	# clip measurements
	if inMeas1 < MINTEMP:
		inMeas1 = MINTEMP

	if inMeas1 > MAXTEMP:
		inMeas1 = MAXTEMP
	
	if inMeas2 < MINHUMID:
		inMeas2 = MINHUMID

	if inMeas2 > MAXHUMID:
		inMeas2 = MAXHUMID
	
	# setting colour gradients for Temperature
	cc1 = Color("red")
	cc2 = Color("blue")
	locPal1 = list(cc2.range_to(cc1, NSTEPSTEMP))

	# setting colour gradients for Humidity
	cc1 = Color("red")
	cc2 = Color("blue")
	locPal2 = list(cc1.range_to(cc2, NSTEPHUMID))
	
	# setting colour gradient for time
	# here, the entire wheel is looped
	# since the main loop is run every 10 minutes,
	# the discretisation is 24 hours x 6
	cc1 = Color(rgb = (1,0,0))
	cc2 = Color(rgb = (0.95,0,0.05))
	locPal3 = list(cc1.range_to(cc2, 3*48))

	# inMeas1 discretised
	locMeas1px = int(round((inMeas1 - MINTEMP) / (MAXTEMP - MINTEMP) * NSTEPSTEMP - 1))
	print "T=", inMeas1, "indx=", locMeas1px

	# inMeas2 discretised
	locMeas2px = int(round((inMeas2 - MINHUMID) / (MAXHUMID - MINHUMID) * NSTEPHUMID - 1))
	print "H=", inMeas2, "indx=", locMeas2px
	
	# inMeas3 discretised
	locMeas3px = inH * 6 + int(round(inM / 10.)) - 1
	print "H", inH, "M", inM, "indx=", locMeas3px
	

	r = locPal1[locMeas1px].red * 255
	g = locPal1[locMeas1px].green * 255
	b = locPal1[locMeas1px].blue * 255
	r = max(0, min(255, r + COLOFFSET))
	g = max(0, min(255, g + COLOFFSET))
	b = max(0, min(255, b + COLOFFSET))

	print int(r), int(g), int(b)

	xx = 0
	for yy in range(inHatHeight):
		unicorn.set_pixel(xx, yy, int(r), int(g), int(b))
			
	unicorn.show()
	time.sleep(0.1)

	r = locPal2[locMeas2px].red * 255
	g = locPal2[locMeas2px].green * 255
	b = locPal2[locMeas2px].blue * 255
	r = max(0, min(255, r + COLOFFSET))
	g = max(0, min(255, g + COLOFFSET))
	b = max(0, min(255, b + COLOFFSET))

	print int(r), int(g), int(b)

	xx = inHatWidth - 1
	for yy in range(inHatHeight):
		unicorn.set_pixel(xx, yy, int(r), int(g), int(b))
			
	unicorn.show()
	time.sleep(0.1)
	
	
	r = locPal3[locMeas3px].red * 255
	g = locPal3[locMeas3px].green * 255
	b = locPal3[locMeas3px].blue * 255
	r = max(0, min(255, r + COLOFFSET))
	g = max(0, min(255, g + COLOFFSET))
	b = max(0, min(255, b + COLOFFSET))

	print int(r), int(g), int(b)
	
	for xx in range(2, inHatWidth-2):
		for yy in range(inHatHeight):			
			unicorn.set_pixel(xx, yy, int(r), int(g), int(b))
			
			
	unicorn.show()
	time.sleep(0.1)
		
		
def main():
	# set params for unicorn hat
	unicorn.set_layout(unicorn.PHAT)
	unicorn.rotation(0)
	unicorn.brightness(0.3)
	hatWidth,hatHeight=unicorn.get_shape()


	# get latest measurements from DB
	measT, measH = getDBrow(DBFILE)
		
	# get current time
	currT = dt.now()
	
	# display measurements on unicorn hat
	dispMeas2(hatWidth, hatHeight, measT, measH, currT.hour, currT.minute)
	
	# repeat every 10'
	# that's the frequency at which database is updated
	time.sleep(600)
	
if __name__ == '__main__':
  try:
	  while True:
		  main()
  except KeyboardInterrupt:
	pass
  finally:
	pass
