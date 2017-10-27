import _thread

#from GPIOServerSide import *
import csn_server_php_helper


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
        print("Druk Button")
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
    helper.breached = False

def AlarmArm(helper):
    helper.alarm_triggered = False
    helper.timer = 0 #time in sec.
    helper.armed = True
    helper.breached = False
    #armed()


def ProcessPacket(helper,data, aes_encryptor,clients):
    """
        helper = the instance of csn_server_helper that called this function.
        data = raw TCP packet, unsplitted.
        aes_encryptor = pre-initialized AES de/encryptor
        clients = list of all connected clients, managed in csn_cli_server, passed through for the PHP server interface.
    """
    #print(data[0]) #bytes in char
    print("encrypted packet", data)
    if len(data[1:data[0]+1]) % 64 != 0:    #AES blocks are 64byte in length each. If the packet isn't a multiple of 64 -> un-encrypted packet.
        #php packet, process different!
        packet = data[1:data[0]+1]          #data[0] = packet length. So the packet itself starts at 1, till data[0], (+1 needed for the way [x:z] works.)
        if(packet[0]==60):
            #packet >=60 == PHP!!!!!
            csn_server_php_helper.ProcessPHP(helper.c,clients)  #writes all clients' status to the socket.
    else:
        packet = aes_encryptor.decrypt(data[1:data[0]+1])       #packet is encrypted. Decrypt the packet (logic explained in if block applies)
        print("Decrypted packet", packet)
        if(packet[0]==0):           #login packet -> process login
            Login(helper,packet)
        elif(packet[0]==1):         #registering alarm -> process alarm
            AlarmGoing(helper,packet)
        elif(packet[0]==2):         #disarm packet -> disarm alarm
            AlarmDisarm(helper)
        elif(packet[0]==3):         #Arm packet -> update clients' status to armed
            AlarmArm(helper)

    if(len(data[1:data[0]+1])+1 != len(data)):
            ProcessPacket(helper,data[data[0]+1:],aes_encryptor)    #incoming data had more than 1 packet. Remove already processed data and re-run loop for the next packet.
