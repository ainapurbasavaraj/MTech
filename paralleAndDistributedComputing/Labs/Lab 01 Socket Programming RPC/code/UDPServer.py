from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
#The beginning of UDPServer is similar to UDPClient. It also imports the 
#socket module, also sets the integer variable serverPort to 12000, and also 
#creates a socket of type SOCK_DGRAM (a UDP socket). T
serverSocket.bind(('', serverPort))
#The above line binds (that is, assigns) the port number 12000 to the server’s socket. 
#Thus, in UDPServer, the code (written by the application developer) is explicitly 
#assigning a port number to the socket. In this manner, when anyone sends a packet to 
#port 12000 at the IP address of the server, that packet will be directed to this socket
print("The server is ready to receive")
while True:
    #UDPServer then enters a while loop; the while loop will allow UDPServer to receive 
    #and process packets from clients indefinitely. In the while loop, UDPServer waits for 
    #a packet to arrive

   message, clientAddress = serverSocket.recvfrom(2048)
    #This line of code is similar to what we saw in UDPClient. When a packet arrives 
    #at the server’s socket, the packet’s data is put into the variable message and the
    #packet’s source address is put into the variable clientAddress. The variable 
    #clientAddress contains both the client’s IP address and the client’s port number. 
    #Here, UDPServer will make use of this address information, as it provides a return 
    #address, similar to the return address with ordinary postal mail. With this source 
    #address information, the server now knows to where it should direct its reply.
   print("Message from ",clientAddress, ": ",message)
   modifiedMessage = message.decode().upper()
    #This line is the heart of our simple application. It takes the line sent by the client and, 
    #after converting the message to a string, uses the method upper() to capitalize it.
   serverSocket.sendto(modifiedMessage.encode(),clientAddress)
    #This last line attaches the client’s address (IP address and port number) to the capitalized message (after converting the string to bytes), and sends the resulting packet into 
    #the server’s socket