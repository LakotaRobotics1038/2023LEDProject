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
ColorMode_Rainbow = 4

Nothing = 0
Confirmed = 1
Cone = 2
Cube = 3

IndicatorMode = Nothing
ColorMode = ColorMode_1038 # Initialize
BluePurpleLength = 16

serial = usb_cdc.data
uart = busio.UART(board.GP0, board.GP1, baudrate=9600)

switch = DigitalInOut(board.GP11)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

xAnimationFrame = 0
topRightAnimationFrame = 0
bottomRightAnimationFrame = 0
bottomLeftAnimationFrame = 0
topLeftAnimationFrame = 0
nichKnackAnimationFrame = 0
mainAnimationFrame = 0

# Define the number of pixels in the LED strips.
RIGHT_SIDE = 150
NICH_KNACK = 260
LEFT_SIDE = 51
LEFT_SIDE_FIX = 100
X_FRAME = 42

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

def SetXHeight(x,r,g,b):
    if (x <= 14):
       pixels5[x - 1]    = (r,g,b)   #Southwest
       pixels5[28 - x] = (r,g,b)   #Southeast
    else: 
       pixels5[19 + x] = (r,g,b)   #Northwest
       pixels5[49 - x] = (r,g,b)   #Northeast

def SetRightLowHeight(x,r,g,b):
    if (x <= 3): #74 is the total height
       pixels1[102 + x] = (r,g,b) #Southwest
       pixels1[103 - x] = (r,g,b) #Southeast
    else:
       pixels1[103 + x] = (r,g,b) #Northwest
       pixels1[149 - x] = (r,g,b) #Northeast

def SetRightHighHeight(x,r,g,b):
   if (x <=7):
      pixels1[x + 90] = (r,g,b)
      pixels1[91 - x] = (r,g,b)
   else:
      pixels1[x - 9] = (r,g,b)
      pixels1[92 - x] = (r,g,b)

def SetLeftLowHeight(x,r,g,b):
    if (x <= 25): #74 is the total height
       pixels3[25 - x] = (r,g,b) #Northwest
       pixels3[25 + x] = (r,g,b) #Northeast     

def SetLeftFixHighHeight(x,r,g,b):
   if (x <=7):
      pixels4[x + 90] = (r,g,b)
      pixels4[91 - x] = (r,g,b)
   else:
      pixels4[x - 9] = (r,g,b)
      pixels4[92 - x] = (r,g,b)

def SetNichKnackHeight(x,r,g,b):
   if (x <=8):
      pixels2[8 - x] = (r,g,b)
      pixels2[7 + x] = (r,g,b)

def SetMainHeight(x,r,g,b):
   if (x<=22): # Lower
      SetLeftLowHeight(x,r,g,b)

   if (22<x) and (x<26): # Nich Knack
      SetLeftLowHeight(x,r,g,b)
      SetRightLowHeight(x,r,g,b)
      SetNichKnackHeight(x-22,r,g,b)
   
   if (26<x<30): #Upper
      SetLeftFixHighHeight(x-25,r,g,b)
      SetRightHighHeight(x-25,r,g,b)
      SetNichKnackHeight(x-22,r,g,b)
      SetLeftLowHeight(x,r,g,b)
   
   if (30<x<40):
      SetLeftFixHighHeight(x,r,g,b)
      SetRightHighHeight(x,r,g,b)
      SetXHeight(x-30,r,g,b)

# def FillAllianceColor():
#    if (Alliance == "R" ):
#       for i in range(35, 48):         
#          pixels1[i] = (255, 0, 0)
#          pixels4[i] = (255, 0, 0)
#    if (Alliance == "B" ):
#       for i in range(35, 48):
#          pixels1[i] = (0, 0, 255)
#          pixels4[i] = (0, 0, 255)   

while True: 
   #print(topRightAnimationFrame)
   print(switch.value)
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
         IndicatorMode = Confirmed
      if (Incoming == b'Y'):
         print("Cone")
         IndicatorMode = Cone
      if (Incoming == b'P'):
         print("Cube")
         IndicatorMode = Cube
      if (Incoming == b'#'):
         print("1038")
         ColorMode = ColorMode_1038
      if (Incoming == b'!'):
         print("Rainbow")
         ColorMode = ColorMode_Rainbow
      if (Incoming == b'D'):
         print("Disabled")
         ColorMode = ColorMode_1038
         IndicatorMode = Nothing

   if (ColorMode == ColorMode_1038):
       time.sleep(0.05)
       
       if (1 == 1):  # Old Stuff
         for j in range(RIGHT_SIDE):         
            pixels1[j] = (0, 0, 200) # Assume everything is blue
         for j in range (bottomRightAnimationFrame,bottomRightAnimationFrame+11):
               if j <=24:
                  SetRightLowHeight(j,200, 0, 200)
               else:
                  SetRightLowHeight(j-24, 200, 0, 200)
         bottomRightAnimationFrame = bottomRightAnimationFrame + 1
         if bottomRightAnimationFrame > 24:
            bottomRightAnimationFrame = 0

         for j in range (topRightAnimationFrame, topRightAnimationFrame+25):
               if j <=49:
                  SetRightHighHeight(j,200, 0, 200)
               else:
                  SetRightHighHeight(j-49, 200, 0, 200)
         topRightAnimationFrame = topRightAnimationFrame + 1
         if topRightAnimationFrame > 49:
            topRightAnimationFrame = 0

         for j in range(LEFT_SIDE_FIX):
               pixels4[j] = (0, 0, 200) # Assume everything is blue
         for j in range (topLeftAnimationFrame, topLeftAnimationFrame+25):
               if j <=49:
                  SetLeftFixHighHeight(j,200, 0, 200)
               else:
                  SetLeftFixHighHeight(j-49, 200, 0, 200)
         topLeftAnimationFrame = topLeftAnimationFrame + 1
         if topLeftAnimationFrame > 49:
            topLeftAnimationFrame = 0
         
         for j in range(LEFT_SIDE):         
               pixels3[j] = (0, 0, 200) # Assume everything is blue
         for j in range (bottomLeftAnimationFrame,bottomLeftAnimationFrame+11):
               if j <=24:
                     SetLeftLowHeight(j,200, 0, 200)
               else:
                     SetLeftLowHeight(j-24, 200, 0, 200)
         bottomLeftAnimationFrame = bottomLeftAnimationFrame + 1
         if bottomLeftAnimationFrame > 24:
            bottomLeftAnimationFrame = 0

         # # for i in range(0, NICH_KNACK):         
         # #    if (((i + AnimationFrame) % (BluePurpleLength * 2)) >= BluePurpleLength):
         # #       pixels2[i] = (200,0,200)
         # #    else:
         # #       pixels2[i] = (0,0,200)
         # # for i in range(0, LEFT_SIDE):         
         # #    if (((i + AnimationFrame) % (BluePurpleLength * 2)) >= BluePurpleLength):
         # #       pixels3[i] = (200,0,200)
         # #    else:
         # #       pixels3[i] = (0,0,200)
         # # for i in range(0, LEFT_SIDE_FIX):         
         # #    if (((i + AnimationFrame) % (BluePurpleLength * 2)) >= BluePurpleLength):
         # #       pixels4[i] = (200,0,200)
         # #    else:
         # #       pixels4[i] = (0,0,200)
         # # for i in range(0, X_FRAME):         
         # #    if (((i + AnimationFrame) % (BluePurpleLength * 2)) >= BluePurpleLength):
         # #       pixels5[i] = (200,0,200)
         # #    else:
         # #       pixels5[i] = (0,0,200)
         
         for j in range(X_FRAME):
            pixels5[j] = (0, 0, 200) # Assume everything is blue
         for j in range(xAnimationFrame,xAnimationFrame+11):
            if j <= 21:
               SetXHeight(j,200, 0, 200)
            else:
               SetXHeight(j-22, 200, 0, 200)
         xAnimationFrame = xAnimationFrame + 1
         if xAnimationFrame > 21:
            xAnimationFrame = 0

         for j in range(NICH_KNACK):
            pixels2[j] = (0, 0, 200) # Assume everything is blue
         for j in range(nichKnackAnimationFrame,nichKnackAnimationFrame+11):
            if j <= 21:
               SetNichKnackHeight(j,200, 0, 200)
            else:
               SetNichKnackHeight(j-22, 200, 0, 200)
         nichKnackAnimationFrame = nichKnackAnimationFrame + 1
         if nichKnackAnimationFrame > 21:
            nichKnackAnimationFrame = 0
            
       else: # New stuff
         for j in range(0,RIGHT_SIDE): #really 359
            pixels1[j] = (0, 0, 200)

         for j in range(0,NICH_KNACK): #really 359
            pixels2[j] = (0, 0, 200)

         for j in range(0,LEFT_SIDE):
            pixels3[j] = (0, 0, 200)

         for j in range(0,LEFT_SIDE_FIX):
            pixels4[j] = (0, 0, 200)

         for j in range(0,X_FRAME):
            pixels5[j] = (0, 0, 200)

         for j in range(mainAnimationFrame,mainAnimationFrame+11):
            if j <= 21:
               SetMainHeight(j,200, 0, 200)
            else:
               SetMainHeight(j-22, 200, 0, 200)
         mainAnimationFrame = mainAnimationFrame + 1
         if mainAnimationFrame > 69:
            mainAnimationFrame = 0

   if (IndicatorMode == Cube):
      if (switch.value == False):
         for i in range(35, 48):
            pixels1[i] = (200, 0, 200)
            pixels4[i] = (200, 0, 200)
      else:
            for i in range(35, 48):
               pixels1[i] = (0, 0, 0)
               pixels4[i] = (0, 0, 0)

   if (IndicatorMode == Cone): 
      if (switch.value == False):
         for i in range(35, 48):
            pixels1[i] = (254, 214, 0)
            pixels4[i] = (254, 214, 0)
      else:
            for i in range(35, 48):
               pixels1[i] = (0, 0, 0)
               pixels4[i] = (0, 0, 0)

   if (IndicatorMode == Confirmed):
      for i in range(35, 48):
         pixels1[i] = (0, 255, 0)
      for i in range(35, 48):
         pixels4[i] = (0, 255, 0)

   if (ColorMode == ColorMode_Rainbow):
      time.sleep(0.05)
      for i in range(0, 149):                  
         rc_index = (i * 256 // RIGHT_SIDE) + AnimationFrame * 16
         pixels1[i] = colorwheel(rc_index & 255)
      for i in range(0, NICH_KNACK):                  
         rc_index = (i * 256 // NICH_KNACK) + AnimationFrame * 16
         pixels2[i] = colorwheel(rc_index & 255)
      for i in range(0, LEFT_SIDE):                  
         rc_index = (i * 256 // LEFT_SIDE) + AnimationFrame * 16
         pixels3[i] = colorwheel(rc_index & 255)
      for i in range(0, LEFT_SIDE_FIX):                  
         rc_index = (i * 256 // LEFT_SIDE_FIX) + AnimationFrame * 16
         pixels4[i] = colorwheel(rc_index & 255)
      for i in range(0, X_FRAME):                  
         rc_index = (i * 256 // X_FRAME) + AnimationFrame * 16
         pixels5[i] = colorwheel(rc_index & 255)

   # FillAllianceColor()
   
   pixels1.show()
   pixels2.show()
   pixels3.show()
   pixels4.show()
   pixels5.show()

   AnimationFrame = AnimationFrame + 1
   if AnimationFrame > 63:
      AnimationFrame = 0
      if (IndicatorMode == Confirmed):  # After a little while of "Green", go back to 1038 animation
         IndicatorMode = Nothing
         ColorMode = ColorMode_1038
   #time.sleep(0.05)