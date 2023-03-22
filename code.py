import time
import board
import neopixel
import math
import busio
import random

from adafruit_led_animation.animation.rainbow import Rainbow

# Define the number of pixels in the LED strips.
RIGHT_SIDE = 151
NICH_KNACK = 15
LEFT_SIDE = 151
LEFT_SIDE_FIX = 100
X_FRAME = 69

# Define the colors to be used in the wave effect.
COLOR1 = (200, 0, 200)
COLOR2 = (0, 0, 200)

# Define the speed of the wave effect.
SPEED = 2

# Define the length of each color segment.
BLUE_SEG_LEN = 4
PURPLE_SEG_LEN = 4

# Initialize the NeoPixel strips.
pixels1 = neopixel.NeoPixel(board.GP2, RIGHT_SIDE, brightness=0.8, auto_write=False)
pixels2 = neopixel.NeoPixel(board.GP3, NICH_KNACK, brightness=0.8, auto_write=False)
pixels3 = neopixel.NeoPixel(board.GP4, LEFT_SIDE, brightness=0.8, auto_write=False)
pixels4 = neopixel.NeoPixel(board.GP5, LEFT_SIDE_FIX, brightness=0.8, auto_write=False)
pixels5 = neopixel.NeoPixel(board.GP6, X_FRAME, brightness=0.8, auto_write=False)


# Initialize the serial communication.
uart = busio.UART(board.GP0, board.GP1, baudrate=9600)

# Initialize the rainbow animation.
rainbow = Rainbow(pixels1, speed=0.1, period=5)
rainbow = Rainbow(pixels2, speed=0.1, period=5)
rainbow = Rainbow(pixels3, speed=0.1, period=5)
rainbow = Rainbow(pixels4, speed=0.1, period=5)

# Initialize the mode variable.
mode = "wave"

# Define the wave effect function.
def wave(color1, color2, speed, blue_len, purple_len):
    # Calculate the current time.
    t = time.monotonic() * speed

    # Loop through each pixel in the first strip.
    for i in range(RIGHT_SIDE):
        # Calculate the sine value for the current pixel.
        sine_value = math.sin(i * 0.5 + t)

        # Set the pixel color based on the sine value and segment length.
        if i % (blue_len + purple_len) < blue_len:
            if sine_value > 0:
                pixels1[i] = tuple(int(c * sine_value) for c in color1)
            else:
                pixels1[i] = tuple(int(c * abs(sine_value)) for c in color2)
        else:
            if sine_value > 0:
                pixels1[i] = tuple(int(c * sine_value) for c in color2)
            else:
                pixels1[i] = tuple(int(c * abs(sine_value)) for c in color1)

    # Loop through each pixel in the second strip.
    for i in range(NICH_KNACK):
        # Calculate the sine value for the current pixel.
        sine_value = math.sin(i * 0.5 + t)

        # Set the pixel color based on the sine value and segment length.
        if i % (blue_len + purple_len) < blue_len:
            if sine_value > 0:
                pixels2[i] = tuple(int(c * sine_value) for c in color1)
            else:
                pixels2[i] = tuple(int(c * abs(sine_value)) for c in color2)
        else:
            if sine_value > 0:
                pixels2[i] = tuple(int(c * sine_value) for c in color2)
            else:
                pixels2[i] = tuple(int(c * abs(sine_value)) for c in color1)

                    # Loop through each pixel in the second strip.
    for i in range(LEFT_SIDE):
        # Calculate the sine value for the current pixel.
        sine_value = math.sin(i * 0.5 + t)

        # Set the pixel color based on the sine value and segment length.
        if i % (blue_len + purple_len) < blue_len:
            if sine_value > 0:
                pixels3[i] = tuple(int(c * sine_value) for c in color1)
            else:
                pixels3[i] = tuple(int(c * abs(sine_value)) for c in color2)
        else:
            if sine_value > 0:
                pixels3[i] = tuple(int(c * sine_value) for c in color2)
            else:
                pixels3[i] = tuple(int(c * abs(sine_value)) for c in color1)

                                    # Loop through each pixel in the second strip.
    for i in range(LEFT_SIDE_FIX):
        # Calculate the sine value for the current pixel.
        sine_value = math.sin(i * 0.5 + t)

        # Set the pixel color based on the sine value and segment length.
        if i % (blue_len + purple_len) < blue_len:
            if sine_value > 0:
                pixels4[i] = tuple(int(c * sine_value) for c in color1)
            else:
                pixels4[i] = tuple(int(c * abs(sine_value)) for c in color2)
        else:
            if sine_value > 0:
                pixels4[i] = tuple(int(c * sine_value) for c in color2)
            else:
                pixels4[i] = tuple(int(c * abs(sine_value)) for c in color1)

                                   # Loop through each pixel in the second strip.
    for i in range(X_FRAME):
        # Calculate the sine value for the current pixel.
        sine_value = math.sin(i * 0.5 + t)

        # Set the pixel color based on the sine value and segment length.
        if i % (blue_len + purple_len) < blue_len:
            if sine_value > 0:
                pixels5[i] = tuple(int(c * sine_value) for c in color1)
            else:
                pixels5[i] = tuple(int(c * abs(sine_value)) for c in color2)
        else:
            if sine_value > 0:
                pixels5[i] = tuple(int(c * sine_value) for c in color2)
            else:
                pixels5[i] = tuple(int(c * abs(sine_value)) for c in color1)

    # Update the LED strips.
    pixels1.show()
    pixels2.show()
    pixels3.show()
    pixels4.show()
    pixels5.show()

# Define the yellow color.
YELLOW = (200, 100, 0)
PURPLE = (200, 0, 200)

# Define the function to set all the LEDs to flashing yellow.
def flashing_yellow():
    # Turn off all the pixels first.
    pixels1.fill((0, 0, 0))
    pixels2.fill((0, 0, 0))
    pixels3.fill((0, 0, 0))
    pixels4.fill((0, 0, 0))
    pixels5.fill((0, 0, 0))
    pixels1.show()
    pixels2.show()
    pixels3.show()
    pixels4.show()
    pixels5.show()

# Loop forever and run the wave or rainbow animation.
while True:

    # Check if there is any data received over serial communication.
    if uart.in_waiting > 0:
        # Read the data from the serial communication.
        data = uart.read(1)

        # Check if the data is "E".
        if data == "E":
            mode = "rainbow"

    # Check the current animation mode.
    if mode == "wave":
        # Run the wave animation.
        wave(COLOR1, COLOR2, SPEED, BLUE_SEG_LEN, PURPLE_SEG_LEN)

    elif mode == "rainbow":
        # Run the rainbow animation.
        rainbow.animate()
