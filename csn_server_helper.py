import time

import _thread

from csn_aes_crypto import csn_aes_crypto
from packet_processor import *
#from GPIOServerSide import *

class ServerHelper:
    c = None
    addr = None
    loggedin = False
    alarm_triggered = False
    timer = 0
    aes_encryptor = None
    cID = 0                         #client ID, used for LED color changing
    armed = True

    def __init__(self,c,addr):
        self.c = c
        self.addr = addr
        self.aes_encryptor = csn_aes_crypto("OurSuperSecretAEScryptoValueGreatSucces")
        #armed()

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

    def PoundAlarm(self):
        print("Client",self.cID,"breached! Please investigate!")
        #alarm(self) #needs to be fired in seperate thread, to prevent blocking on main thread of client.
