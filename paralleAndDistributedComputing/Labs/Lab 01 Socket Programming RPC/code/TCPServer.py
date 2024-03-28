from socket import *
serverPort = 12000

serverSocket = socket(AF_INET,SOCK_STREAM)
#As with TCPClient, the server creates a TCP socket. With TCP, serverSocket will be our 
# welcoming socket. After establishing this welcoming door, we will wait and listen for 
# some client to knock on the door
serverSocket.bind(('',serverPort))
#Similar to UDPServer, we associate the server port number, serverPort, with 
#this socket
serverSocket.listen(1)
#This line converts an active socket into welcoming socket. Inside TCP, the buffers are converted 
#to store connection objects instead of data. Argument is approaximately how many connections can be 
# accommodated in TCP conbnection buffer
print('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept()
    #When a client knocks on this door, the program invokes the accept() method for 
    #serverSocket, which creates a new socket in the server, called connectionSocket, 
    #dedicated to this particular client
    sentence = connectionSocket.recv(1024).decode()
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode()) 
    connectionSocket.close()