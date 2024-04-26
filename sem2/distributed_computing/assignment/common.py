import socket
import os

'''
This is the config file to configure server ip address and port that client service has to connect to.

'''

from dataclasses import dataclass, field

@dataclass
class ServerRequestData:
    method : str = None
    url    : str = None
    header : dict = field(default_factory = dict)
    body   : dict = field(default_factory = dict)

SERVER_IP =  "localhost" #Change it to private ip address of server in lab env
SERVER_PORT = "8800" 

def get_ip_by_hostname(name):
    return socket.gethostbyname(name)

def getServerIp():
    return SERVER_IP

def getServerPort():
    return int(SERVER_PORT)

def getHostname():
    return socket.gethostname()
  
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

def downloadFile(base_path, filename, data):
    if not os.path.exists(base_path):
        os.mkdir(base_path)
    path = os.path.join(base_path, filename)
    if os.path.exists(path):
        os.remove(path)
    print("downloading file to %s" %path)

    with open(path, 'a') as f:
        f.write(data)

