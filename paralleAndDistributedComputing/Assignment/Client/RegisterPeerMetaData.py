'''
This is the helper function to
1. Connect to server and register its peer metadata to server.
2. Deregister peer metadata to server when peer service is going down.
'''

import urllib.request
import Config
from Communication import SocketCommunication as mySocket

local_ip = Config.getLocalIp()

print("Your local IP address is: ", local_ip)

def registerPeer(peerPort, filename):

    # Initialize Socket Instance
    sock = mySocket()

    # Defining port and host
    port = Config.getServerPort()
    host = Config.getServerIp()

    SendData = '''{"Register" : {
        "Ip" : "%s", 
        "Port" : "%s", 
        "FileName" : "%s"}}''' %(local_ip, peerPort, filename)
    print("Registering peer metadata..")
    print(SendData)
    
    data = sock.communicate(host, port, SendData)
    if data == "OK":
        print("Metadata registration successful!!")
    else:
        print("This file is already served by other peers")
        return -1
    
    return 0

def deRegisterPeer(peerPort, filename):

    # Initialize Socket Instance
    sock = mySocket()

    # Defining port and host
    port = Config.getServerPort()
    host = Config.getServerIp()

    SendData = '''{"Deregister" : {
        "Ip" : "%s", 
        "Port" : "%s", 
        "FileName" : "%s"}}''' %(local_ip, peerPort, filename)

    print("Deregistering peer metadata..")
    print(SendData)
    
    data = sock.communicate(host, port, SendData)
    if data == "OK":
        print("Metadata deregistration successful!!")
 