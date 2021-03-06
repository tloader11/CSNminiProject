import importlib.util

import _thread

try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
except ImportError:
    import FakeRPi.GPIO as GPIO

import time


class GPIOClientSide:

    #pin layout
    ledGroen = 6
    ledRood = 5
    knopje = 4
    knopje2 = 22
    breached = False
    armed = True

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ledRood, GPIO.OUT)
        GPIO.setup(self.ledGroen, GPIO.OUT)
        GPIO.setup(self.knopje, GPIO.IN,pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.knopje2, GPIO.IN,pull_up_down=GPIO.PUD_UP)

    def disarm(self):
        GPIO.output(self.ledRood,False)
        GPIO.output(self.ledGroen,True)

    def arm(self):
        GPIO.output(self.ledRood,True)
        GPIO.output(self.ledGroen,False)

    def alarm(self):
        GPIO.output(self.ledRood, True)
        #print("Rood True")     #DEBUG
        time.sleep(1)
        GPIO.output(self.ledRood, False)
        #print("Rood False")    #DEBUG
        time.sleep(1)

    #checks if one of the buttons is pressed, called from csn_cli_client in a separate thread.
    def DoButtonCheck(self):
        while True:
            if GPIO.input(self.knopje) == True or GPIO.input(self.knopje2) == True:
                print(GPIO.input(self.knopje))
                print("KNOPJE INGEDRUKT -> breached: true")
                self.breached = True

