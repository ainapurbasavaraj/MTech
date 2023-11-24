'''
This is the main client service responsible for
1. Initialize the peer service, register peer service with server and run it in background.
2. Initialize client to start downloading files from peer.

This service can rund both peer service and client service based on user inputs.
Or, It can only be run as Peer service and Client service can run independently.
'''

import socket
import sys
import RegisterPeerMetaData as metaData
import Client
import time
import threading
from Communication import SocketCommunication as mySocket

# total arguments
n = len(sys.argv)

if n < 3:
    print("Invalid number of arguments passed")
    raise Exception("Invalid number of arguments passed") 

port = sys.argv[1]
host = ''
fileName = "%s" %(sys.argv[2])

#Used to stop the execution of thread and exit gracefully
stop_thread = False

def serveAsPeer(host, port):
    # Initialize Socket Instance
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.settimeout(0.2)
    # binding to the host and port
    sock.bind((host, int(port)))

    # Accepts up to 10 connections
    sock.listen(10)
    print("This Peer is ready to serve file.")

    global stop_thread
    while not stop_thread:
        # Establish connection with the clients.
        try:
            con, addr = sock.accept()
        except socket.timeout:
            pass
        else:
            # Get data from the client
            data = con.recv(1024)
            fileName = data.decode()

            # Read File in binary
            file = open(fileName, 'rb')
            line = file.read(1024)
            # Keep sending data to the client
            while(line):
                con.send(line)
                line = file.read(1024)
            
            file.close()
            con.close()

def startPeerService():
    #Register to server as peer service to serve this file
    ret = metaData.registerPeer(port, fileName)
    if ret != 0:
        print("No need to start Peer service!!")
        stop_thread = True
        return

    try:
        serveAsPeer(host, port)
    except:
        stop_thread = True
        metaData.deRegisterPeer(port, fileName)
        raise Exception("Exception in initializing Peer service")

        


def downoadFiles():
    while(True):
        action = input("Download file?(y/n) : ")
        if (action != 'y'):
            break
        fname = input("Enter file name to download : ")
        Client.downloadFileFromPeer(fname)
        

if __name__ =="__main__":

    #Init and start Peer service in a thread.
    t1 = threading.Thread(target=startPeerService)
    
    t1.daemon = True

    try:
        t1.start()
        time.sleep(3)
    except:
        print("There is an exception in starting Peer service")
        stop_thread = True
    
    downoadFiles()
    
    while not stop_thread:
        print("Peer service is running in background to serve the file")
        action = input("Press 1 : To stop the peer service gracefully!")
        if action == "1":
            stop_thread = True
            metaData.deRegisterPeer(port, fileName)
        else:
            downoadFiles()
            

    t1.join()