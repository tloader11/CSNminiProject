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

#list of client ID's that are in 'alarming' state. Used for LCD displaying purposes.
triggered = set()

#used to prevent the LCD screen from flickering and constant updating.
ShowedMessageArmed = False
ShowedMessageDisarmed = False
ShowedMessageAlarm = False

def ClearLCD():
    """
        clears the LCD screen...
    """
    lcd.clear()

def armed(helper):
    """
        helper = instance of csn_server_helper. Has no real function anymore...
    """
    global ShowedMessageArmed,ShowedMessageAlarm,ShowedMessageDisarmed
    try:
        triggered.remove(helper.cID)        #client re-armed. Should not be in the list at all, so double-checking.
    except:
        pass
    helper.disarmed_lcd_showed = False      #not used anymore...
    if len(triggered) > 0 and ShowedMessageArmed==False:    #If the LCD message hasn't been updated yet: update.
        ShowedMessageArmed = True
        ShowedMessageDisarmed = False
        ShowedMessageAlarm = False
        lcd.clear()
        s = ""
        clientlist = list(triggered)
        for cID in clientlist:
            #print(cID)
            s+=str(cID)+" "
        lcd.message("Clients\nBreached:"+s)                 #sets the LCD text
    elif ShowedMessageArmed==False:                         #no alarms are triggered, all clients are OK.
        ShowedMessageArmed = True
        ShowedMessageDisarmed = False
        ShowedMessageAlarm = False
        lcd.clear()
        lcd.message('All clients\nOK')
        GPIO.output(ledRood,False)
        GPIO.output(ledGroen,True)


def lcd_text(text):
    lcd.clear()
    lcd.message(text)

def disarm(helper):
    """
        Updates the flags and prevents updates from other functions by blocking this sub-thread for 2secs.
        Turns on the green LED and turns the red LED off.
    """
    global ShowedMessageArmed,ShowedMessageAlarm,ShowedMessageDisarmed
    if ShowedMessageDisarmed == False:
        GPIO.output(ledRood,False)
        GPIO.output(ledGroen,True)
        try:
            triggered.remove(helper.cID)
        except:
            pass
        lcd.clear()
        lcd.message("Client "+str(helper.cID)+"\nDisarmed")
        helper.disarmed_lcd_showed = True
        ShowedMessageArmed = False
        ShowedMessageDisarmed = True
        ShowedMessageAlarm = False
        time.sleep(2)

def alarm(helper):
    """
        Adds the client to the list of triggered alarms. Sets the flags to alarm state as well if not done already.
        Makes the red LED blink as well
    """
    global ShowedMessageArmed,ShowedMessageAlarm,ShowedMessageDisarmed
    if ShowedMessageAlarm == False:
        triggered.add(helper.cID)
        lcd.clear()
        s = ""
        clientlist = list(triggered)
        for cID in clientlist:
            #print(cID)
            s+=str(cID)+" "
        lcd.message('Alarm triggerd:\nClient: {}'.format(s))
        ShowedMessageArmed = False
        ShowedMessageDisarmed = False
        ShowedMessageAlarm = True

    GPIO.output(ledGroen,False)
    GPIO.output(ledRood, True)
    time.sleep(1)
    GPIO.output(ledRood, False)
    time.sleep(1)

