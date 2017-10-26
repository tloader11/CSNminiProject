import time

import _thread

import GPIOServerSide
from csn_aes_crypto import csn_aes_crypto
from packet_processor import *
from GPIOServerSide import *

class ServerHelper:
    c = None
    addr = None
    loggedin = False
    alarm_triggered = False
    timer = 0
    aes_encryptor = None
    cID = 0                         #client ID, used for LED color changing
    armed = True
    disarmed_lcd_showed = False
    breached = False


    def __init__(self,c,addr):
        self.c = c
        self.addr = addr
        self.aes_encryptor = csn_aes_crypto("OurSuperSecretAEScryptoValueGreatSucces")
        #armed()
        _thread.start_new_thread(self.ButtonController, ())

    def CheckPacket(self, data):
        if(len(data) == 0): return
        ProcessPacket(self,data,self.aes_encryptor)

    def RunAlarmTriggerTimer(self):
        while(self.alarm_triggered == True and self.timer > 0):

            print("Timing:",self.timer)

            time.sleep(1)
            self.timer -= 1
        if(self.alarm_triggered == True and self.timer == 0):
            self.PoundAlarm()
        elif(self.alarm_triggered == False and self.armed == True):
            lcd_text("All clients\nOK")
        elif(self.alarm_triggered == False and self.armed == False):
            lcd_text("Client "+str(self.cID)+"\nDisarmed")

    def PoundAlarm(self):
        GPIOServerSide.alarm(self)
        self.breached = True
        print("Client",self.cID,"breached! Please investigate!")
        #alarm(self) #needs to be fired in seperate thread, to prevent blocking on main thread of client.

    def ButtonController(self):
        while True:
            if self.breached and self.armed:
                #print("AlarmLoop")
                GPIOServerSide.alarm(self)
            elif self.armed:
                GPIOServerSide.armed(self)
            elif self.armed == False:
                GPIOServerSide.disarm(self)


