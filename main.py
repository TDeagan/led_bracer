# CircuitPython demo - NeoPixel

import touchio
import board
import neopixel
import time

touch0 = touchio.TouchIn(board.A1)
touch1 = touchio.TouchIn(board.A2)
pixpin = board.D1
numpix = 4
strip = neopixel.NeoPixel(pixpin, numpix, brightness=0.3, auto_write=False)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0) or (pos > 255):
        return (0, 0, 0)
    if (pos < 85):
        return (int(pos * 3), int(255 - (pos*3)), 0)
    elif (pos < 170):
        pos -= 85
        return (int(255 - pos*3), 0, int(pos*3))
    else:
        pos -= 170
        return (0, int(pos*3), int(255 - pos*3))

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(len(strip)):
            idx = int ((i * 256 / len(strip)) + j)
            strip[i] = wheel(idx & 255)
        strip.write()
        time.sleep(wait)
		
def nrider_cycle(wait,r,g,b):
	j =len(strip)-1
	while True:
		for i in range(len(strip)):
			strip.fill((0, 0, 0))
			strip[i] = (r,g,b)
			strip.write()
			time.sleep(wait)
		for i in range(len(strip)):
			strip.fill((0, 0, 0))
			strip[j-i] = (r,g,b)
			strip.write()
			time.sleep(wait)
		if touch0.value:
			return 0
			break
		if touch1.value:
			return 1
			break
		
while True:
	touch_rtn = nrider_cycle(0.05, 255,   0,   0)
	if touch_rtn:
		touch_rtn = nrider_cycle(0.05,   0, 255,   0)
	if touch_rtn:
		touch_rtn = nrider_cycle(0.05,   0,   0, 255)
	
	if not touch_rtn:
		while touch0.value:
			rainbow_cycle(0.001)    # rainbowcycle with 1ms delay per step
			if touch1.value:
				break

