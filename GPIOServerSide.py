import Adafruit_CharLCD as LCD
import time

import importlib.util
try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
except ImportError:
    import FakeRPi.GPIO as GPIO

# Pin Config:

ledGroen = 2
ledRood = 3
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledRood, GPIO.OUT)
GPIO.setup(ledGroen, GPIO.OUT)

lcd_rs        = 25
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 18
lcd_d7        = 22
lcd_backlight = 1
# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2
# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
lcd_columns, lcd_rows, lcd_backlight)

triggered = []

def armed(helper):
    triggered.remove(helper.cID)
    helper.disarmed_lcd_showed = False
    if len(triggered) > 0:
        lcd.clear()
        s = ""
        for cID in triggered: s+=str(cID)+" "
        lcd.message("Clients\nBreached:"+s)
    else:
        lcd.clear()
        lcd.message('All clients\nOK')
        GPIO.output(ledRood,False)
        GPIO.output(ledGroen,True)


def lcd_text(text):
    lcd.clear()
    lcd.message(text)

def disarm(helper):
    print(helper.disarmed_lcd_showed)
    if helper.disarmed_lcd_showed == False:
        triggered.remove(helper.cID)
        lcd.message("Client "+helper.cID+"\nDisarmed")
        helper.disarmed_lcd_showed = True
        time.sleep(2)

def alarm(helper):
    triggered.append(helper.cID)
    lcd.clear()
    lcd.message('Alarm triggerd:\nClient: {}'.format(helper.cID))
    GPIO.output(ledGroen,False)
    GPIO.output(ledRood, True)
    time.sleep(1)
    GPIO.output(ledRood, False)
    time.sleep(1)

'''
armed()
time.sleep(5)
alarm(3)
time.sleep(5)
GPIO.output(ledGroen,False)
lcd.clear()
'''
