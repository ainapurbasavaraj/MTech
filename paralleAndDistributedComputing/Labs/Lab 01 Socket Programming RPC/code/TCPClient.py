from socket import *
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
#This line creates the client’s socket, called clientSocket. The first parameter 
#again indicates that the underlying network is using IPv4. The second parameter 
#indicates that the socket is of type SOCK_STREAM, which means it is a TCP socket
clientSocket.connect((serverName,serverPort))
#Recall that before the client can send data to the server (or vice versa) using a TCP 
#socket, a TCP connection must first be established between the client and server. The
#above line initiates the TCP connection between the client and server. The parameter 
#of the connect() method is the address of the server side of the connection. After 
#this line of code is executed, the three-way handshake is performed and a TCP connection 
# is established between the client and server
sentence = input('Input lowercase sentence:')
clientSocket.send(sentence.encode())
#The above line sends the sentence through the client’s socket and into the TCP 
#connection. Note that the program does not explicitly create a packet and attach the 
#destination address to the packet, as was the case with UDP sockets.
#Instead the client program simply drops the bytes in the string sentence into the TCP connection. 
modifiedSentence = clientSocket.recv(1024)
#The client then waits to receive bytes from the server.
#When characters arrive from the server, they get placed into the string 
#modifiedSentence. Characters continue to accumulate in modifiedSentence until the line ends 
# with a carriage return character
print('From Server: ', modifiedSentence.decode()) 
clientSocket.close()
#This last line closes the socket and, hence, closes the TCP connection between the 
#client and the server. It causes TCP in the client to send a TCP FIN message to TCP in 
#the server