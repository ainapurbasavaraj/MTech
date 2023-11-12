import socket
import json
import RegisterService as regService
import ClientMetadata as CMetaData
 
#Initialize register service
rService = regService.RegisterService()

# Initialize Socket Instance
sock = socket.socket()
print ("Socket created successfully.")

# Defining port and host
port = 8800
host = ''

# binding to the host and port
sock.bind((host, port))

# Accepts up to 1000 connections
sock.listen(1000)
print('Socket is listening...')

while True:
    # Establish connection with the clients.
    con, addr = sock.accept()
    print('Connected with ', addr)

    # Get data from the client
    data = con.recv(1024)
    jdata = json.loads(data.decode())

    #If request is to register peer metadata
    if jdata.get('Register', None):
        registerData = jdata['Register']
        cData = CMetaData.ClientMetadata(registerData["Ip"], registerData["Port"], registerData["FileName"])
        rService.RegisterClientInfo(registerData["FileName"],cData)
        con.send("OK".encode())
    #If request is to get peer metadata
    elif jdata.get('File', None):
        metadata = rService.GetClientData(jdata['File'])
        con.send(metadata.getJsonMetadata().encode())
    
    print('Send data to client success!')

    con.close()