#!/usr/bin/python -u


# for unicorn hat
import unicornhat as unicorn

import sys
import time

COLOFFSET = 30

NUMS = (
        (((1,1,1),(1,1,1)), ((1,1,1),(1,1,1)), ((1,1,1),(1,1,1)), ((1,1,1),(1,1,1))), 
        (((0,0,0),(1,1,1)), ((1,1,1),(1,1,1)), ((0,0,0),(1,1,1)), ((0,0,0),(1,1,1))), 
        (((1,1,1),(1,1,1)), ((0,0,0),(1,1,1)), ((1,1,1),(0,0,0)), ((1,1,1),(1,1,1))), 
        (((1,1,1),(1,1,1)), ((0,0,0),(1,1,1)), ((0,0,0),(1,1,1)), ((1,1,1),(1,1,1))), 
        (((1,1,1),(0,0,0)), ((1,1,1),(1,1,1)), ((0,0,0),(1,1,1)), ((0,0,0),(1,1,1))), 
        (((1,1,1),(1,1,1)), ((1,1,1),(0,0,0)), ((0,0,0),(1,1,1)), ((1,1,1),(1,1,1))), 
        (((1,1,1),(1,1,1)), ((1,1,1),(0,0,0)), ((1,1,1),(1,1,1)), ((1,1,1),(1,1,1))), 
        (((1,1,1),(1,1,1)), ((0,0,0),(1,1,1)), ((1,1,1),(0,0,0)), ((1,1,1),(0,0,0))), 
        (((1,1,1),(1,1,1)), ((0,0,0),(0,0,0)), ((0,0,0),(0,0,0)), ((1,1,1),(1,1,1))), 
        (((1,1,1),(1,1,1)), ((1,1,1),(1,1,1)), ((0,0,0),(1,1,1)), ((1,1,1),(1,1,1)))
        )

def setUniPxNum(inNum, inCol, inXoffset):
    if inNum in range(10):
        locNumTab = NUMS[inNum]
      	print(locNumTab)
  
        for xx in range(2):
            for yy in range(4):
			print("Setting pixel", xx, yy)
    			r = locNumTab[yy][xx][0] * inCol[0]
    			g = locNumTab[yy][xx][1] * inCol[1]
    			b = locNumTab[yy][xx][2] * inCol[2]
    			r = max(0, min(255, r + COLOFFSET))
    			g = max(0, min(255, g + COLOFFSET))
    			b = max(0, min(255, b + COLOFFSET))
        	        unicorn.set_pixel(xx + inXoffset, yy, int(r), int(g), int(b))

	unicorn.show()

    else:
        print("Error: a 0-9 number required")

def main():
	print("Start")
	# set params for unicorn hat
	unicorn.set_layout(unicorn.PHAT)
	unicorn.rotation(0)
	unicorn.brightness(0.3)
	hatWidth,hatHeight=unicorn.get_shape()

	for xx in range(10):
		print("Showing number", xx)
		unicorn.clear()
		setUniPxNum(xx,(255,0,0),4)
		time.sleep(3)

if __name__ == '__main__':
  try:
	  while True:
		  main()
  except KeyboardInterrupt:
	pass
  finally:
	pass

