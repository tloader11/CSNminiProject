import time

import _thread


class ServerHelper:
    c = None
    addr = None
    loggedin = False
    alarm_triggered = False
    timer = 0

    def __init__(self,c,addr):
        self.c = c
        self.addr = addr

    def CheckPacket(self, data):
        print(data[0]) #bytes in char
        extra_test = data[1:data[0]+1]
        if(extra_test[0]==0):
            username_length = extra_test[1]
            username = ""
            for i in range(2,username_length+2):
                username += chr(extra_test[i])

            password_length = extra_test[username_length+2]
            password = ""
            for i in range(username_length+3,password_length+username_length+3):
                password += chr(extra_test[i])
            print("Login Packet with credentials: "+ username + " , " + password)
            if(username == "loginnaam" and password == "TestPass12345"):
                self.loggedin = True

        elif(extra_test[0]==1 and self.loggedin):
            print("registering alarm")

            self.alarm_triggered = True
            self.timer = 5 #time in sec.
            type_alarm = extra_test[1]

            _thread.start_new_thread(self.RunAlarmTriggerTimer, ()) #start countdown timer.

            if type_alarm==1:
                print("alarm type 1")
            elif type_alarm==2:
                print("alarm type 2")
            elif type_alarm==5:
                print("alarm type 5")


        elif(extra_test[0]==2 and self.loggedin):
            print("Disarm package. Stopping timer.")
            self.alarm_triggered = False
            self.timer = 0

        if(len(extra_test)+1 != len(data)):
            self.CheckPacket(data[data[0]+1:])

    def RunAlarmTriggerTimer(self):
        while(self.alarm_triggered == True and self.timer > 0):

            print("Timing:",self.timer)

            time.sleep(1)
            self.timer -= 1
        if(self.alarm_triggered == True and self.timer == 0):
            self.PoundAlarm()

    def PoundAlarm(self):
        print("Alarm gaat af!!!")
