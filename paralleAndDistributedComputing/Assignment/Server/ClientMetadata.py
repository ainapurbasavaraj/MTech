class ClientMetadata:
    def __init__(self, ip, port, file):
        self.ip = ip
        self.port = port
        self.file = file

    def getIp(self):
        return self.ip
    
    def getPort(self):
        return self.port

    def getFile(self):
        return self.file

    def getJsonMetadata(self):
        return '{"Ip" : "%s", "Port" : "%s", "FileName" : "%s"}' %(self.ip, self.port, self.file)

