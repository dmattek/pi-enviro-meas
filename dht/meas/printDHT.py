# for DHT sensor
import sys
import Adafruit_DHT

import datetime

# sensor definition
DHTsensor = Adafruit_DHT.AM2302
DHTpin = 4

def main():
  # Main program block

  DHThum, DHTtemp = Adafruit_DHT.read_retry(DHTsensor, DHTpin)
  currT = datetime.datetime.now()

  print('{0:s},\t{1:0.1f},\t{2:0.1f}'.format(currT.strftime('%Y-%m-%d %H:%M'), DHTtemp, DHThum))
  

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    pass
