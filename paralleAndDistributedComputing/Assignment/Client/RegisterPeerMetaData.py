import socket
import urllib.request
import serverConfig

external_ip = urllib.request.urlopen('http://ip.42.pl/raw').read().decode('utf8')

print("Your public IP address is: ", external_ip)

def registerPeerMetadata(peerPort, filename):

    # Initialize Socket Instance
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket created successfully.")

    # Defining port and host
    port = serverConfig.getServerPort()
    host = serverConfig.getServerIp()

    # Connect socket to the host and port
    sock.connect((host, port))
    print('Connection Established.')

    SendData = '''{"Register" : {
        "Ip" : "%s", 
        "Port" : "%s", 
        "FileName" : "%s"}}''' %(external_ip, peerPort, filename)
    print("Registering peer metadata..")
    print(SendData)
    sock.send(SendData.encode())

    # Keep receiving data from the server
    line = sock.recv(1024)
    data = line.decode()
    if data == "OK":
        print("Metadata registration successful!!")
        
    sock.close()
    print('Connection Closed.')