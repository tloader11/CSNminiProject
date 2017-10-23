import RPi.GPIO as GPIO
import time

# Pin Config
ledGroen = 2
ledRood = 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledRood, GPIO.OUT)
GPIO.setup(ledGroen, GPIO.OUT)

def disarm():
    GPIO.output(ledRood,False)
    GPIO.output(ledGroen,True)
    time.sleep(5)
    arm()

def arm():
    GPIO.output(ledRood,True)
    GPIO.output(ledGroen,False)

def alarm():
    x = 0
    while True:
        if x < 10:
            GPIO.output(ledRood, True)
            time.sleep(1)
            GPIO.output(ledRood, False)
            time.sleep(1)
            x += 1
        else: break
    arm()
arm()
time.sleep(5)
alarm()
time.sleep(5)
disarm()
GPIO.cleanup()
