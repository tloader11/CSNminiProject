import importlib.util

import _thread

try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
except ImportError:
    import FakeRPi.GPIO as GPIO

import time


class GPIOClientSide:

    ledGroen = 5
    ledRood = 6
    knopje = 17
    breached = False

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ledRood, GPIO.OUT)
        GPIO.setup(self.ledGroen, GPIO.OUT)
        GPIO.setup(self.knopje, GPIO.IN)
        _thread.start_new_thread(self.DoButtonCheck(), ())

    def disarm(self):
        GPIO.output(self.ledRood,False)
        GPIO.output(self.ledGroen,True)

    def arm(self):
        GPIO.output(self.ledRood,True)
        GPIO.output(self.ledGroen,False)

    def alarm(self):
        self.breached
        while True:
            if self.breached:
                GPIO.output(self.ledRood, True)
                time.sleep(1)
                GPIO.output(self.ledRood, False)
                time.sleep(1)
            else: break
        self.arm()

    def DoButtonCheck(self):
        while True:
            if GPIO.input(self.knopje):
                breached = True
                self.alarm()
