import board
import neopixel
import time
import sys

#cycle = 0
#rotateCheck = 0
qty = 104
#offset = 0
digits = []
#firstRun = True
primary = True
leds = neopixel.NeoPixel(board.D12, qty, auto_write = False)

# sets up the message to run in binary
def messageSetup(message):
    global digits
    res = "".join(format(ord(i), "b") for i in message)
    for i in res:
        digits.append(i)


# actually runs the binary message
def message(colorA, colorB):
    global digits
    global qty
    for i in range(qty):
        if digits[i] == "0":
            leds[i] = colorA
        if digits[i] == "1":
            leds[i] = colorB
    digits = digits[1:] + digits[:1]
    leds.show()


# Rotates between 2 colors
def rotate():
    #global rotateCheck
    leds[qty - 1] = leds[0]
    for i in range(qty - 1):
        leds[i] = leds[i + 1]

def tower(point):
    #global rotateCheck
    leds[qty - 1] = leds[point]
    leds[0] = leds[point-1]
    for i in range(qty - 1):
        if i > 0 and i < point:
            leds[i] = leds[(2*point)-i]
        else:
            leds[i] = leds[i + 1]

def fadeSetup(c1, c2):
    rDiff = (c1[0] - c2[0]) / (qty//2)
    gDiff = (c1[1] - c2[1]) / (qty//2)
    bDiff = (c1[2] - c2[2]) / (qty//2)
    for i in range(qty):
        if i <= qty//2:
            leds[i] = (c1[0] - rDiff*i, c1[1] - gDiff*i, c1[2] - bDiff*i)
        else:
            leds[i] = (leds[i-1][0] + rDiff, leds[i-1][1] + gDiff, leds[i-1][2] + bDiff)

def rotateSetup(colorA, colorB, length, section):
    global primary
    for i in range(length):
        if i % section == 0:
            primary = not primary
        if primary:
            leds[i] = colorA # - rotateCheck] = colorA
        else:
            leds[i] = colorB # - rotateCheck] = colorB


def setup(len=10, mode="Rotate", colorA=(125, 0, 200), colorB=(0, 0, 255), message=""):
    if mode == "Message":
        messageSetup(message)
    elif mode == "Fade":
        fadeSetup(colorA, colorB)
    else:
        rotateSetup(colorA, colorB, len, 4)


#fun pretty estop code

def run(mode, colorA, colorB):
    if mode == "Message":
        message(colorA, colorB)
    elif mode == "Rotate" or mode == "Fade":
        rotate()
    elif mode == "Tower":
        tower(20)
    else:
        rainbow_cycle(0)
    leds.show()


# GAY!! fun pretty estop code
def rainbow_cycle(wait):
    while True:
        global qty
        for j in range(255):
            for i in range(qty):
                pixel_index = (i * 256 // qty) + j
                leds[i] = wheel(pixel_index & 255)
            leds.show()
#time.sleep(wait)

# Wheel is used by the rainbow to...rainbow
def wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)





def twistIt(pos):
    if pos < 0 or pos > 255:
        r = b = 0
    elif pos < 128:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, b)