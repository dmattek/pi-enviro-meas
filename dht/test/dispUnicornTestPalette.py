#!/usr/bin/python -u
# -*- coding: utf-8 -*-

# https://github.com/vaab/colour
from colour import Color

# for unicorn hat
import unicornhat as unicorn

import time


COLOFFSET = 0

unicorn.set_layout(unicorn.PHAT)
unicorn.rotation(0)
unicorn.brightness(0.3)
hatWidth,hatHeight=unicorn.get_shape()


cc1 = Color(rgb = (1,0,0))
cc2 = Color(rgb = (0.95, 0, 0.05))
locPal1 = list(cc1.range_to(cc2, hatWidth * hatHeight))

print locPal1

ii = 0

for yy in range(hatHeight):
	for xx in range(hatWidth):
			locCols = locPal1[ii].rgb
			ii = ii + 1
			r = locCols[0] * 255
			g = locCols[1] * 255
			b = locCols[2] * 255
			r = max(0, min(255, r + COLOFFSET))
			g = max(0, min(255, g + COLOFFSET))
			b = max(0, min(255, b + COLOFFSET))

			unicorn.set_pixel(xx, yy, int(r), int(g), int(b))
			print ii-1, xx, yy, int(r), int(g), int(b)



unicorn.show()

time.sleep(10)
