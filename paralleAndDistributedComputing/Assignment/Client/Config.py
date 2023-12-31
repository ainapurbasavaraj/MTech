'''
This is the config file to configure server ip address and port that client service has to connect to.

'''

SERVER_IP =  "localhost" #Change it to private ip address of server in lab env
SERVER_PORT = "8800" 

def getServerIp():
    return SERVER_IP

def getServerPort():
    return int(SERVER_PORT)

import socket
  
def getLocalIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('192.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
