import time
import board
import digitalio
import busio
import usb_cdc
import neopixel
from rainbowio import colorwheel
from digitalio import DigitalInOut, Direction, Pull

ORDER = neopixel.GRB
Alliance = "" # "R"ed or "B"lue or "" Unknown 
AnimationFrame = 0

ColorMode_1038 = 0
ColorMode_Cone = 1
ColorMode_Cube = 2
ColorMode_Confirmed = 3
ColorMode_Ukraine = 4
ColorMode_Rainbow = 5

ColorMode = ColorMode_1038 # Initialize
BluePurpleLength = 8

serial = usb_cdc.data
uart = busio.UART(board.GP0, board.GP1, baudrate=9600)

switch = DigitalInOut(board.GP11)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

# Define the number of pixels in the LED strips.
RIGHT_SIDE = 151
NICH_KNACK = 15
LEFT_SIDE = 151
LEFT_SIDE_FIX = 100
X_FRAME = 69

pixels1 = neopixel.NeoPixel(board.GP2, RIGHT_SIDE, brightness=0.8, auto_write=False)
pixels2 = neopixel.NeoPixel(board.GP3, NICH_KNACK, brightness=0.8, auto_write=False)
pixels3 = neopixel.NeoPixel(board.GP4, LEFT_SIDE, brightness=0.8, auto_write=False)
pixels4 = neopixel.NeoPixel(board.GP5, LEFT_SIDE_FIX, brightness=0.8, auto_write=False)
pixels5 = neopixel.NeoPixel(board.GP6, X_FRAME, brightness=0.8, auto_write=False)

def GetChar():                   # Get any color change requests from the USB or RoboRio serial port
   Result = ""
   if serial and serial.in_waiting > 0:
      byte = serial.read(1)
      print("USB: ", byte)
      Result = byte
   if uart.in_waiting > 0:        
      byte = uart.read(1)
      print("RoboRio: ", byte)
      Result = byte
   return Result if Result else ""

def FillAllianceColor():
   if (Alliance == "R" ):
      for i in range(35, 48):         
         pixels1[i] = (255, 0, 0)
         pixels4[i] = (255, 0, 0)
   if (Alliance == "B" ):
      for i in range(35, 48):
         pixels1[i] = (0, 0, 255)
         pixels4[i] = (0, 0, 255)   

while True: 
   Incoming = GetChar()
   if Incoming != "":
      if (Incoming == b'R'):
         print("Red")
         Alliance = "R"
      if (Incoming == b'B'):
         print("Blue")
         Alliance = "B"
      if (Incoming == b'G'):
         print("Green")
         ColorMode = ColorMode_Confirmed
         AnimationFrame = 0
      if (Incoming == b'Y'):
         print("Cone")
         ColorMode = ColorMode_Cone
         AnimationFrame = 0
      if (Incoming == b'P'):
         print("Cube")
         ColorMode = ColorMode_Cube
         AnimationFrame = 0
      if (Incoming == b'U'):
         print("Ukraine")
         ColorMode = ColorMode_Ukraine
      if (Incoming == b'#'):
         print("1038")
         ColorMode = ColorMode_1038
      if (Incoming == b'!'):
         print("Rainbow")
         ColorMode = ColorMode_Rainbow

   if (ColorMode == ColorMode_Cube):
      if (switch.value):
         for i in range(0, 35):
            pixels1[i] = (152, 51, 250)
            pixels4[i] = (152, 51, 250)
      else:
         for i in range(0, 35):
            pixels1[i] = (0, 0, 0)
            pixels4[i] = (0, 0, 0)

   if (ColorMode == ColorMode_Cone): 
      if (switch.value):
         for i in range(0, 35):
            pixels1[i] = (254, 214, 0)
            pixels4[i] = (254, 214, 0)
      else:
         for i in range(0, 35):
            pixels1[i] = (0, 0, 0)
            pixels4[i] = (0, 0, 0)

   if (ColorMode == ColorMode_Ukraine):
      for i in range(0, 17):         
         pixels1[i] = (254,214,0)
         pixels1[i+18] = (0,197,187) 
         pixels4[i] = (254,214,0)
         pixels4[i+18] = (0,197,187) 

   if (ColorMode == ColorMode_1038):
      for i in range(0, RIGHT_SIDE):         
         if (((i + AnimationFrame) % (BluePurpleLength * 2)) >= BluePurpleLength):
            pixels1[i] = (128,0,128)
         else:
            pixels1[i] = (0,0,128)

   if (ColorMode == ColorMode_Confirmed):
      for i in range(0, RIGHT_SIDE):         
         pixels1[i] = (0, 214, 0)
      for i in range(0, LEFT_SIDE_FIX):                           
         pixels4[i] = (0, 214, 0)      

   if (ColorMode == ColorMode_Rainbow):
      for i in range(0, RIGHT_SIDE):                  
         rc_index = (i * 256 // RIGHT_SIDE) + AnimationFrame * 16
         pixels1[i] = colorwheel(rc_index & 255)

   FillAllianceColor()
   
   pixels1.show()
   pixels2.show()
   pixels3.show()
   pixels4.show()
   pixels5.show()

   AnimationFrame = AnimationFrame + 1
   if AnimationFrame > 15:
      AnimationFrame = 0
      if (ColorMode == ColorMode_Confirmed):  # After a little while of "Green", go back to 1038 animation
         ColorMode = ColorMode_1038