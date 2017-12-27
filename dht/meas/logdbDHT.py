#!/usr/bin/python

# for sqlite
import sqlite3

# for DHT sensor
import sys
import Adafruit_DHT

import datetime

import time

# sensor definition
DHTsensor = Adafruit_DHT.AM2302
DHTpin = 4

# SQLite DB file location
DBFILE = '/var/www/dhtlog.db'

# store the temperature in the database
def logDB(inTemp, inHumid):

    conn=sqlite3.connect(DBFILE)
    curs=conn.cursor()

    curs.execute("INSERT INTO temps values(datetime('now'), (?), (?))", (inTemp, inHumid,))

    # commit the changes
    conn.commit()

    conn.close()

def checkValIn(inVal, inMin, inMax):
    if inVal >= inMin and inVal <= inMax:
        return 1
    else:
        return 0

def main():
  # Main program block

  DHThum = -1.0
  DHTtemp = -1.0
  maxIt = 10
  currIt = 0
  
  while ((checkValIn(DHThum, 0, 100) == 0) or (checkValIn(DHTtemp, 0, 40) == 0)) and (currIt < maxIt):
     currIt += 1 
     DHThum, DHTtemp = Adafruit_DHT.read_retry(DHTsensor, DHTpin)
     time.sleep(1)   

  # Output to command line
  # print('{0:s},\t{1:0.1f},\t{2:0.1f}'.format(currT.strftime('%Y-%m-%d %H:%M'), DHTtemp, DHThum))

  # Log into sqlite DB
  logDB(DHTtemp,DHThum) 

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    pass
