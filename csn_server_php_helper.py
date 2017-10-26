
def ProcessPHP(c,clients):
    #print(clients)
    sendbytes = bytearray()
    for client in clients[:-1]:
        sendbytes.append(client.cID)
        sendbytes.append(client.alarm_triggered)
        sendbytes.append(client.breached)
        sendbytes.append(client.armed)
    c.send(sendbytes)
    c.close()
