'''
This is client service responsible for
1.  Create connection to server and get the peer metadata serving the requested file.
2.  Decode the peer metadata and connect to Peer service to download the requested file.
'''

import sys
import json
import os
import shutil
import Config
from Communication import SocketCommunication as mySocket

# total arguments
n = len(sys.argv)
filename = sys.argv[1] if n > 1 else None
if not filename:
    print("File name is not passed as command line argument")
    exit(0)

def getPeerServerDetails(filename):
    port = Config.getServerPort()
    host = Config.getServerIp()
    SendData = '{"File" : "%s"}' %(filename)

    mySock = mySocket()
    peerServerDetails = mySock.communicate(host, port, SendData)
    return peerServerDetails


def downloadFile(peerServerDetails):
    print("Peer server details : %s " %peerServerDetails)
    if peerServerDetails == "None":
        print("Input file is not served by any peer currently!")
        return

    serverDetails = json.loads(peerServerDetails)
    ip = serverDetails["Ip"]
    port = serverDetails["Port"]
    filename = serverDetails["FileName"]

    mySock = mySocket()
    mySock.connect(ip, int(port))
    SendData = '%s' %(filename)
    mySock.send(SendData)

    line = mySock.receive()

    if not os.path.exists("downloaded-data"):
        os.mkdir("downloaded-data")
    fname = 'downloaded-%s' %(filename)
    file = open(fname, 'wb')
    
    while(line):
        file.write(line.encode())
        line = mySock.receive()

    print('File %s downloaded to %s.\n\n' %(filename,fname))

    file.close()
    mySock.closeConnection()


def downloadFileFromPeer(fileName=None):
    downloadFile(getPeerServerDetails(fileName))


if __name__ =="__main__":
    downloadFileFromPeer(filename)