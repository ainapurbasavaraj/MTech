import socket
import sys
import RegisterPeerMetaData
import Client
import time
import threading

# total arguments
n = len(sys.argv)

if n < 3:
    print("Invalid number of arguments passed")
    raise Exception("Invalid number of arguments passed") 

port = sys.argv[1]
host = ''
fileName = "%s" %(sys.argv[2])

def serveAsPeer(host, port):
    # Initialize Socket Instance
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print ("Socket created successfully.")

    # binding to the host and port
    sock.bind((host, int(port)))

    # Accepts up to 10 connections
    sock.listen(10)
    #print('Socket is listening...')

    while True:
        # Establish connection with the clients.

        #print ("waiting for connections from other peers...")
        
        con, addr = sock.accept()
        #print('Connected with ', addr)

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

def registerMetadata():
    #Register to server as peer service to serve this file
    RegisterPeerMetaData.registerPeerMetadata(port, fileName)
    serveAsPeer(host, port)


def downoadFiles():
    while(True):
        fname = input("Enter file name to download : ")
        Client.downloadFileFromPeer(fname)
        action = input("Download More files?(y/n) : ")
        if (action != 'y'):
            break

if __name__ =="__main__":
    t1 = threading.Thread(target=registerMetadata)
    
    t1.daemon = True
    t1.start()
    time.sleep(3)
    print("This Peer is ready to serve file : %s \n" %fileName)
    
    downoadFiles()
    print("Peer service is running in background to serve the file")
    action = input("Press ctrl-c : To stop the peer service.")

    t1.join()