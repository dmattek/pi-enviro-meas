#!/usr/bin/python

# for sqlite
import sqlite3

# for TSL sensor
import smbus

import datetime
import time

# SQLite DB file location
DBFILE = '/var/www/lightlog.db'

# store the temperature in the database
def logDB(inFull, inIR):

    conn=sqlite3.connect(DBFILE)
    curs=conn.cursor()

    curs.execute("INSERT INTO lightint values(datetime('now'), (?), (?))", (inFull, inIR, ))

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

  # Get I2C bus
  bus = smbus.SMBus(1)

  # TSL2561 address, 0x39(57)
  # Select control register, 0x00(00) with command register, 0x80(128)
  #		0x03(03)	Power ON mode
  bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)

  # TSL2561 address, 0x39(57)
  # Select timing register, 0x01(01) with command register, 0x80(128)
  #		0x02(02)	Nominal integration time = 402ms
  bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)

  time.sleep(0.5)

  # Read data back from 0x0C(12) with command register, 0x80(128), 2 bytes
  # ch0 LSB, ch0 MSB
  data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)

  # Read data back from 0x0E(14) with command register, 0x80(128), 2 bytes
  # ch1 LSB, ch1 MSB
  data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)

  # Convert the data
  ch0 = data[1] * 256 + data[0]
  ch1 = data1[1] * 256 + data1[0]

  # Output data to screen
#  print "Full Spectrum(IR + Visible) :%d lux" %ch0
#  print "Infrared Value :%d lux" %ch1
#  print "Visible Value :%d lux" %(ch0 - ch1)

  logDB(ch0, ch1) 

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    pass
