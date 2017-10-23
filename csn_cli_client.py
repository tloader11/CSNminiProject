import socket               # Import socket module

import sys

from csn_aes_crypto import csn_aes_crypto

s = socket.socket()         # Create a socket object
host = "127.0.0.1"                   # Get local machine name
port = 666                  # Reserve a port for your service.
s.connect((host, port))

aes_encryptor = csn_aes_crypto("OurSuperSecretAEScryptoValueGreatSucces")


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
x.listen(1)
print('Socket now listening')


def TriggerAlarm(s,alarm_type):
    global aes_encryptor
    sensor = bytearray()
    sensor.append(1)
    sensor.append(5)
    mssg = aes_encryptor.encrypt(sensor.decode())
    output = bytearray({len(mssg)}) + mssg
    print("Got Trigger Request, sending:",output)
    s.send(output)

def Disarm(s):
    global aes_encryptor
    disarm = bytearray()
    disarm.append(2)
    mssg = aes_encryptor.encrypt(disarm.decode())
    output = bytearray({len(mssg)}) + mssg
    print("Got Disarm Request, sending:",output)
    s.send(output)

#now keep talking with the client
while 1:
    conn, addr = x.accept()                                 #wait to accept a connection - blocking call
    print('Connected from ' + addr[0] + ':' + str(addr[1]))
    connected = True
    if(addr[0]=='127.0.0.1'):   #only accept connections from localhost (local webserver) otherwise remote injection is possible.
        while connected:
            try:
                data = conn.recv(1024)
                #print(data)
                if(len(data)>0):
                    print(data)
                    if(data[0]==1):
                        TriggerAlarm(s,data[1])
                    if(data[0]==2):
                        Disarm(s)
                    connected = False
                    conn.close()
                else:
                    connected = False
            except:
                print("Error receiving data")
                print(sys.exc_traceback())





'''
disarm = bytearray()
disarm.append(1) #disarm length. Non-flexible
disarm.append(2)
s.send(disarm)
'''

#bytez =b'0'
#bytez +=b'10'
#s.send(bytez + bytes("testtestte".encode("utf8")))
'''
while True:
    bytez = b''
    bytez +=b'0'
    bytez +=b'10'
    s.send(bytez + bytes("testtestte".encode("utf8")))
    #s.send(bytes(input(),'utf-8'))
'''
