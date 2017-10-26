import socket               # Import socket module

import sys

import time

import _thread

import GPIOClientSide

from csn_aes_crypto import csn_aes_crypto

s = socket.socket()         # Create a socket object
host = "192.168.1.27"                   # Get local machine name
port = 666                  # Reserve a port for your service.
s.connect((host, port))

aes_encryptor = csn_aes_crypto("OurSuperSecretAEScryptoValueGreatSucces")

breached = False

username = "loginnaam"
password = "TestPass12345"
my_bytes = bytearray()
my_bytes.append(0)
my_bytes.append(len(username))
my_bytes.extend(map(ord, username))
my_bytes.append(len(password))
my_bytes.extend(map(ord, password))

encrypted_message = aes_encryptor.encrypt(my_bytes.decode())

lengte = bytearray()
lengte.append(len(encrypted_message))
my_bytes = lengte + encrypted_message
s.send(my_bytes)
print("Logged in to server as alarm Client. Commands will now be processed by this server.")

x = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    x.bind(("", 667))
except socket.error as msg:
    print('Bind failed. Error Code : ', msg)
    sys.exit()

#Start listening on socket
x.listen(3)
print('Socket now listening')

def TriggerAlarm(alarm_type, c=None):
    global aes_encryptor
    if c==None:
        global s
    else:
        s = c
    sensor = bytearray()
    sensor.append(1)
    sensor.append(alarm_type)
    mssg = aes_encryptor.encrypt(sensor.decode())
    output = bytearray({len(mssg)}) + mssg
    print("Got Trigger Request, sending:",output)
    global breached
    breached = True
    s.send(output)

def Disarm(c=None):
    if c==None:
        global s
    else:
        s = c
    global aes_encryptor
    disarm = bytearray()
    disarm.append(2)
    mssg = aes_encryptor.encrypt(disarm.decode())
    output = bytearray({len(mssg)}) + mssg
    print("Got Disarm Request, sending:",output)
    global breached
    breached = False
    s.send(output)

def Arm(c=None):
    if c==None:
        global s
    else:
        s = c
    disarm = bytearray()
    disarm.append(3)
    mssg = aes_encryptor.encrypt(disarm.decode())
    output = bytearray({len(mssg)}) + mssg
    print("Got Arm Request, sending:",output)
    global breached
    breached = False
    s.send(output)

gpio_controller = GPIOClientSide.GPIOClientSide()
status = 0
def ButtonController():
        global status
        while True:
            if gpio_controller.breached and gpio_controller.armed:
                #print("AlarmLoop")
                gpio_controller.alarm()
                if status != 1:
                    status = 1
                    try:
                        TriggerAlarm(1)
                    except:
                        continue
            elif gpio_controller.armed:
                #print("ArmLoop")
                gpio_controller.arm()
                if status != 0:
                    status = 0
                    try:
                        Arm()
                    except:
                        continue
            elif gpio_controller.armed == False:
                #print("DisarmedLoop")
                gpio_controller.disarm()
                if status != 2:
                    status = 2
                    try:
                        Disarm()
                    except:
                        continue

_thread.start_new_thread(ButtonController, ())
_thread.start_new_thread(gpio_controller.DoButtonCheck, ())

gpio_controller.armed = True
print("arm")
time.sleep(5)
gpio_controller.breached = True
print("alarm")
time.sleep(7)
gpio_controller.armed = False
gpio_controller.breached = False
print("disarm")
time.sleep(5)
gpio_controller.armed = True
print("arm")
time.sleep(5)

#now keep talking with the client
while 1:
    conn, addr = x.accept()                                 #wait to accept a connection - blocking call
    print('Connected from ' + addr[0] + ':' + str(addr[1]))
    connected = True
    if True: #(addr[0]=='127.0.0.1'):   #only accept connections from localhost (local webserver) otherwise remote injection is possible.
        while connected:
            try:
                data = conn.recv(1024)
                #print(data)
                if(len(data)>0):
                    print(data)
                    if(data[0]==1):
                        TriggerAlarm(data[1],s)
                        gpio_controller.breached = True
                    elif(data[0]==2):
                        Disarm(s)
                        gpio_controller.breached = False
                        gpio_controller.armed = False
                    elif(data[0]==3):
                        Arm(s)
                        gpio_controller.armed = True
                        gpio_controller.breached = False
                    elif(data[0]==4):
                        status_p = bytearray()
                        status_p.append(status)
                        print("Sending Status Byte, sending:",status_p)
                        global breached
                        breached = False
                        conn.send(status_p)
                    connected = False
                    conn.close()
                else:
                    connected = False
            except:
                gpio_controller.armed = True
                gpio_controller.breached = True
                print("A LOT of possible errors here.")
                #print(sys.exc_traceback())
