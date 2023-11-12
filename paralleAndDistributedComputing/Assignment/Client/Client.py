import socket
import sys
import json
import os
import shutil

# total arguments
n = len(sys.argv)
filename = sys.argv[1]


def getSocketConnection(ip, port):
    # Initialize Socket Instance
    sock = socket.socket()
    #print ("Socket created successfully.")

    # Connect socket to the host and port
    #print("Connect to %s : %s" %(ip, port))
    sock.connect((ip, port))
    #print('Connection Established.')

    return sock

def getPeerServerDetails(filename):
    port = 8800
    host = 'localhost'
    sock = getSocketConnection(host, port)
    SendData = '{"File" : "%s"}' %(filename)
    sock.send(SendData.encode())

    line = sock.recv(1024)
    peerServerDetails = line.decode()

    closeConnection(sock)
    return peerServerDetails


def closeConnection(sock):
    sock.close()


def downloadFile(peerServerDetails):
    print("Peer server details : %s " %peerServerDetails)
    serverDetails = json.loads(peerServerDetails)
    ip = serverDetails["Ip"]
    port = serverDetails["Port"]
    filename = serverDetails["FileName"]

    ip = 'localhost'
    sock = getSocketConnection(ip, int(port))
    SendData = '%s' %(filename)
    sock.send(SendData.encode())

    line = sock.recv(1024)

    if not os.path.exists("downloaded-data"):
        os.mkdir("downloaded-data")
    fname = 'downloaded-%s' %(filename)
    file = open(fname, 'wb')
    
    while(line):
        file.write(line)
        line = sock.recv(1024)

    print('File %s has been received successfully.' %fname)

    file.close()
    closeConnection(sock)


def downloadFileFromPeer(fileName=None):
    downloadFile(getPeerServerDetails(fileName))