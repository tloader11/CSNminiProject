import _thread

#from GPIOServerSide import *


def Login(helper,data):
    username_length = data[1]
    username = ""
    for i in range(2,username_length+2):
        username += chr(data[i])

        password_length = data[username_length+2]
        password = ""
        for i in range(username_length+3,password_length+username_length+3):
            password += chr(data[i])
    print("Login Packet with credentials: "+ username + " , " + password)
    if(username == "loginnaam" and password == "TestPass12345"):
        helper.cID = 1
        helper.loggedin = True
    elif(username == "login2" and password == "Pass2"):
        helper.cID = 2
        helper.loggedin = True

def AlarmGoing(helper,data):
    if(helper.armed == False): return   #If system is disarmed, the alarm won't work when a sensor is activated.
    print("registering alarm")

    helper.alarm_triggered = True
    helper.timer = 12 #time in sec.
    type_alarm = data[1]

    _thread.start_new_thread(helper.RunAlarmTriggerTimer, ()) #start countdown timer.

    if type_alarm==1:
        print("alarm type 1")
    elif type_alarm==2:
        print("alarm type 2")
    elif type_alarm==3:
        print("alarm type 3")
    elif type_alarm==4:
        print("alarm type 4")
    elif type_alarm==5:
        print("alarm type 5")

def AlarmDisarm(helper):
    helper.alarm_triggered = False
    helper.timer = 0 #time in sec.
    helper.armed = False

def AlarmArm(helper):
    helper.alarm_triggered = False
    helper.timer = 0 #time in sec.
    helper.armed = True
    #armed()


def ProcessPacket(helper,data, aes_encryptor):
    #print(data[0]) #bytes in char
    print("encrypted packet", data)
    packet = aes_encryptor.decrypt(data[1:data[0]+1])
    print("Decrypted packet", packet)
    if(packet[0]==0):           #login packet -> process login
        Login(helper,packet)
    elif(packet[0]==1):         #registering alarm -> process alarm
        AlarmGoing(helper,packet)
    elif(packet[0]==2):
        AlarmDisarm(helper)
    elif(packet[0]==3):
        AlarmArm(helper)

    if(len(data[1:data[0]+1])+1 != len(data)):
            ProcessPacket(helper,data[data[0]+1:],aes_encryptor)
