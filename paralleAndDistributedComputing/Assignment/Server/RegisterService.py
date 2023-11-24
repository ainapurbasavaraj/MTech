import ClientMetadata as CMetaData

class RegisterService:
    '''
    This class provides interface for registering and deregistering peer metadata
    and stores it.
    '''
    def __init__(self):
        self.clientdata = {}

    def RegisterClientInfo(self, registerData):
        '''
        Decode and stores the peer metadata
        '''
        cData = CMetaData.ClientMetadata(registerData["Ip"], registerData["Port"], registerData["FileName"])
        fileName = registerData["FileName"]

        #If file is already being served by other peer, Then dont register again
        if self.clientdata.get(fileName, None):
            print("This file is already registered by peer : %s" %(self.clientdata[fileName]))
            return -1

        self.clientdata[fileName] = cData
        return 0

    def GetClientData(self, fileName):
        if self.clientdata.get(fileName, None):
            return self.clientdata[fileName]
        return None

    def DeregisterClientInfo(self, fileName):
        if self.clientdata.get(fileName, None):
            del self.clientdata[fileName]



