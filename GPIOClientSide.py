import RPi.GPIO as GPIO
import time

# Pin Config
import csn_cli_client

ledGroen = 2
ledRood = 3
knopje = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledRood, GPIO.OUT)
GPIO.setup(ledGroen, GPIO.OUT)
GPIO.setup(knopje, GPIO.IN)

def disarm():
    GPIO.output(ledRood,False)
    GPIO.output(ledGroen,True)
    time.sleep(5)
    arm()

def arm():
    GPIO.output(ledRood,True)
    GPIO.output(ledGroen,False)

def alarm():
    while True:
        if csn_cli_client.breached:
            GPIO.output(ledRood, True)
            time.sleep(1)
            GPIO.output(ledRood, False)
            time.sleep(1)
        else: break
    arm()
if GPIO.input(knopje):
    alarm()
#arm()
#time.sleep(5)
#alarm()
#time.sleep(5)
#disarm()
#GPIO.cleanup()
