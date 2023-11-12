import ClientMetadata


class RegisterService:
    def __init__(self):
        self.clientdata = {}

    def RegisterClientInfo(self,fileName, clientMetaData):

        self.clientdata[fileName] = clientMetaData

    def GetClientData(self, fileName):
        if self.clientdata.get(fileName, None):
            return self.clientdata[fileName]
        return None

    def DeregisterClientInfo(self, fileName):
        del self.clientdata[fileName]



