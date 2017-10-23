import socket               # Import socket module

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
print(encrypted_message)
#my_bytes = bytearray(encrypted_message)

lengte = bytearray()
lengte.append(len(encrypted_message))
my_bytes = lengte + encrypted_message
s.send(my_bytes)



sensor = bytearray()
sensor.append(1)
sensor.append(5)
mssg = aes_encryptor.encrypt(sensor.decode())
output = bytearray({len(mssg)}) + mssg
print(output)
s.send(output)

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
