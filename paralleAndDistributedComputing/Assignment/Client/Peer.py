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

stop_thread = False

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

        print ("waiting for connections from other peers...")

        #Stop the thread if we need to
        global stop_thread
        if stop_thread:
            break
        
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
            print("Peer service is running in background to serve the file")
            action = input("Press 1 : To stop the peer service.")
            stop_thread = True if action == "1" else False
            break

if __name__ =="__main__":
    t1 = threading.Thread(target=registerMetadata)
 
    t1.start()
    time.sleep(3)
    print("This Peer is ready to serve file : %s \n" %fileName)
    

    downoadFiles()


    t1.join()

    

    
 
    

'''
def getUserInput():
    data = input("""Press 1 : To download new file from server : \n
Press 2 : To serve as Peer server for other clients : """)

    return data

data = getUserInput()
while (data):
    if int(data) == 1:
        fname = input("Enter file name to download : ")
        Client.downloadFileFromPeer(fname)
    elif (int(data) == 2):
        print("Serving as peer service...\n")
        try:
            serveAsPeer(host, port)
        except:
            print("Stopped serving as peer service for file : %s" %fileName)
    else:
        print("\n!!Closing the service!!\n")
        break

    data = getUserInput()

'''