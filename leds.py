# v Imports/variables v#
import time
import rio_coms
import animations

lightCount = animations.qty
enabled = True


# v Between these are the only things you should change v#

# LED Signal Pin is set in animations, D21 to start
lightCount = 104  # Number of leds
mode = "Fade"  # "Rotate", "Fade", "Tower", or "Message" (or none for rainbow testing) right now
message = "Something mean about Sean"  # If running message code, message to convert
cycleDelay = 0.01 #0.01 for fade, 0.1 for rotate or message
hex1 = (200, 0, 200)
hex2 = (0, 0, 200)

# ^ Between these are the only things you should change ^#


# code that runs during the match
animations.setup(lightCount, mode, hex1, hex2, message)

while enabled:
    if rio_coms.disabled():
        enabled = False
    else:
        # input()                #only use when debugging, comment out otherwise

        # Runs the chosen LED program
        animations.run(mode, hex1, hex2)
        # you may need a delay for the lights depending on the number of sensors, comment it out if you don't
        time.sleep(cycleDelay)


# This runs after the robot is disabled
animations.rainbow_cycle(cycleDelay)
