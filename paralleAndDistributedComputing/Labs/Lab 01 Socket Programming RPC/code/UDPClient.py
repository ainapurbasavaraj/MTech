from socket import *
#The socket module forms the basis of all network communications in Python.

serverName = 'localhost'
serverPort = 12000
#Here, we provide a string containing either the IP address of the server (e.g., “128.138.32.126”) 
#or the hostname of the server (e.g., “cis.poly.edu”). If we use the hostname, then a 
#DNS lookup will automatically be performed to get the IP address.) The second line 
#sets the integer variable serverPort to 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
#This line creates the client’s socket, called clientSocket. The first parameter indicates the address family; in particular, AF_INET indicates that the 
#underlying network is using IPv4.
#The second parameter indicates that the socket is of 
#type SOCK_DGRAM, which means it is a UDP socket (rather than a TCP socket)

message = input('Input lowercase sentence:')
#input() is a built-in function in Python. When this command is executed, the user 
#at the client is prompted with the words “Input lowercase sentence:” The user then 
#uses her keyboard to input a line, which is put into the variable message

clientSocket.sendto(message.encode(),(serverName, serverPort))
#In the above line, we first convert the message from string type to byte type, as we 
#need to send bytes into a socket; this is done with the encode() method. The 
#method sendto() attaches the destination address (serverName, serverPort) 
#to the message and sends the resulting packet into the process’s socket, 
#clientSocket

modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
#With the above line, when a packet arrives from the Internet at the client’s socket, the 
#packet’s data is put into the variable modifiedMessage and the packet’s source 
#address is put into the variable serverAddress. The variable serverAddress
#contains both the server’s IP address and the server’s port number. 
#The method recvfrom also takes the buffer size 2048 as input

print(modifiedMessage.decode())
#This line prints out modifiedMessage on the user’s display, after converting the message from bytes to string. 
#It should be the original line that the user typed, but now 
#capitalized
clientSocket.close()
#This line closes the socket. The process then terminates.