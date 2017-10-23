import socket               # Import socket module
from threading import Thread
s = socket.socket()         # Create a socket object
host = "127.0.0.1"                   # Get local machine name
port = 666                  # Reserve a port for your service.
s.connect((host, port))

username = "loginnaam"
password = "TestPass12345"
my_bytes = bytearray()
my_bytes.append(0)
my_bytes.append(len(username))
my_bytes.extend(map(ord, username))
my_bytes.append(len(password))
my_bytes.extend(map(ord, password))

lengte = bytearray()
lengte.append(len(my_bytes))
my_bytes = lengte + my_bytes
s.send(my_bytes)

sensor = bytearray()
sensor.append(2) #sensor length. Non-flexible
sensor.append(1)
sensor.append(5)
s.send(sensor)



disarm = bytearray()
disarm.append(1) #disarm length. Non-flexible
disarm.append(2)
s.send(disarm)


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
