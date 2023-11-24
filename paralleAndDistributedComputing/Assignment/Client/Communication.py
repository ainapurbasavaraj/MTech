
import socket


class SocketCommunication:
    '''
    This class provider interface to communicate via sockets 
    '''

    def __init__(self):
        # Initialize Socket Instance
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip, port):
        
        # Connect socket to the host and port
        self.sock.connect((ip, port))

    def send(self, data):
        self.sock.send(data.encode())

    def receive(self):
        line = self.sock.recv(1024)
        rData = line.decode()
        return rData

    def sendAndReceive(self, data):

        #Send and receive data from server
        self.send(data)
        rData = self.receive()
        self.closeConnection()

        return rData

    def closeConnection(self):
        #close the connection
        self.sock.close()

    def communicate(self, ip, port, data):
        #This is wrapper function to facilitate complete communication.
        self.connect(ip, port)
        rData = self.sendAndReceive(data)
        self.closeConnection()
        return rData