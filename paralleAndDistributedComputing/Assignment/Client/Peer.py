import socket
import sys
import RegisterPeerMetaData
import Client

def serveAsPeer(host, port):
    # Initialize Socket Instance
    sock = socket.socket()
    #print ("Socket created successfully.")

    # binding to the host and port
    sock.bind((host, int(port)))

    # Accepts up to 10 connections
    sock.listen(10)
    #print('Socket is listening...')

    while True:
        # Establish connection with the clients.

        print ("waiting for connections from other peers...")
        
        con, addr = sock.accept()
        print('Connected with ', addr)

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



# total arguments
n = len(sys.argv)

if n < 3:
    print("Invalid number of arguments passed")
    raise Exception("Invalid number of arguments passed") 

# Defining port and host
port = sys.argv[1]
host = ''

fileName = "%s" %(sys.argv[2])

#Register to server as peer service to serve this file
RegisterPeerMetaData.registerPeerMetadata(port, fileName)

print("This Peer is ready to serve file : %s" %fileName)

def getUserInput():
    data = input("""Press 1 if you want to download new file from server : \n
Press 2 if you want to serve as Peer server for other clients : """)

    return data

data = getUserInput()
while (data):
    if int(data) == 1:
        fname = input("Enter file name to download : ")
        Client.downloadFileFromPeer(fname)
    elif (int(data) == 2):
        print("Serving as peer service...")
        try:
            serveAsPeer(host, port)
        except:
            print("Stopped serving as peer service for file : %s" %fileName)
    else:
        print("!!Closing the service!!")
        break

    data = getUserInput()