import time
import board
import neopixel
import math
import busio

from adafruit_led_animation.animation.rainbow import Rainbow

# Define the number of pixels in the LED strips.
NUM_PIXELS_1 = 86
NUM_PIXELS_2 = 15
NUM_PIXELS_3 = 46

# Define the colors to be used in the wave effect.
COLOR1 = (200, 0, 200)
COLOR2 = (0, 0, 200)

# Define the speed of the wave effect.
SPEED = 5

# Define the length of each color segment.
BLUE_SEG_LEN = 8
PURPLE_SEG_LEN = 8

# Initialize the NeoPixel strips.
pixels1 = neopixel.NeoPixel(board.GP2, NUM_PIXELS_1, brightness=0.5, auto_write=False)
pixels2 = neopixel.NeoPixel(board.GP3, NUM_PIXELS_2, brightness=0.5, auto_write=False)
pixels3 = neopixel.NeoPixel(board.GP4, NUM_PIXELS_3, brightness=0.5, auto_write=False)

# Initialize the serial communication.
uart = busio.UART(board.GP0, board.GP1, baudrate=9600)

# Initialize the rainbow animation.
rainbow = Rainbow(pixels1, speed=0.1, period=5)
rainbow = Rainbow(pixels2, speed=0.1, period=5)
rainbow = Rainbow(pixels3, speed=0.1, period=5)

# Initialize the mode variable.
mode = "wave"

# Define the wave effect function.
def wave(color1, color2, speed, blue_len, purple_len):
    # Calculate the current time.
    t = time.monotonic() * speed

    # Loop through each pixel in the first strip.
    for i in range(NUM_PIXELS_1):
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
    for i in range(NUM_PIXELS_2):
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
    for i in range(NUM_PIXELS_3):
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

    # Update the LED strips.
    pixels1.show()
    pixels2.show()
    pixels3.show()

# Loop forever and run the wave or rainbow animation.
while True:
    # Check if there is any data received over serial communication.
    if uart.in_waiting > 0:
        # Read the data from the serial communication.
        data = uart.read(1)

        # Check if the data is "E".
        if data == "E":
            # Switch to the rainbow animation mode.
            mode = "rainbow"

    # Check the current animation mode.
    if mode == "wave":
        # Run the wave animation.
        wave(COLOR1, COLOR2, SPEED, BLUE_SEG_LEN, PURPLE_SEG_LEN)

    elif mode == "rainbow":
        # Run the rainbow animation.
        rainbow.animate()
