from threading import Thread
import socket

import sys

import csn_server_helper

host = ""
port = 666                  # used by the original Doom and by trojans. Should be free.
s = socket.socket()         # Create a socket object
s.bind((host, port))        # Bind to the port

global clients
clients = list()

def ListenThread(c,addr):
    global clients
    isConnected = True
    helper = csn_server_helper.ServerHelper(c,addr)
    clients.append(helper)
    while isConnected:
        try:
            data = c.recv(1024)
            #print(data)
            if(len(data)>0):
                print(data)
                helper.CheckPacket(data)
        except:
            print("Unexpected error:", sys.exc_info(), sys.exc_traceback())
            try:
                clients.remove(helper)
            except:
                print("Unexpected error:", sys.exc_info())
                return

while True:
    #always listen for new connections
    s.listen(5)
    c, addr = s.accept()
    print ('Got connection from', addr)
    threadz = Thread(target = ListenThread, args = (c, addr)).start()

