import socket
import json
import RegisterService as regService
 
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
        ret = rService.RegisterClientInfo(registerData)
        if ret != 0:
            con.send("Failure in registering file".encode())
        else:
            con.send("OK".encode())
    #If request is to get peer metadata
    elif jdata.get('File', None):
        metadata = rService.GetClientData(jdata['File'])
        data = None
        if metadata:
            data = metadata.getJsonMetadata().encode()
        else:
            print("This file is not served by any peer")
            data = "None".encode()
        con.send(data)

    elif jdata.get('Deregister', None):
        deRegisterData = jdata['Deregister']
        rService.DeregisterClientInfo(deRegisterData["FileName"])
        con.send("OK".encode())
    
    print('Send data to client success!')

    con.close()