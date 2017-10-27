

def ProcessPHP(c,clients):
    """
        mostly self-explaining.
    """
    sendbytes = bytearray()
    for client in clients[:-1]:     #last item in the list = the PHP client itself, so not a real client. always removing that one from the results returned.
        sendbytes.append(client.cID)
        sendbytes.append(client.alarm_triggered)
        sendbytes.append(client.breached)
        sendbytes.append(client.armed)
    c.send(sendbytes)
    c.close()
