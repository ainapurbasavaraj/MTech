
from config_loader import keys, Methods
from common import ServerRequestData

class RequestBuilder:

    def __init__(self, node, config, req_args, method) -> None:
        self.requestData : ServerRequestData = ServerRequestData()
        self.node = node
        self.config = config
        self.req_args = req_args
        self.method = method

    def buildUrl(self):
        self.requestData.url = self.config[self.node] + self.config[keys.SERVICE_NAME]
        return self

    def buildBody(self):
        if self.method == Methods.POST:
            self.requestData.body = self.req_args

        return self

    def buildHeader(self):
        self.requestData.header[keys.CONTENT_TYPE] = 'application/json'
    
    def build(self):
        self.buildUrl().buildBody().buildHeader()
        return self.requestData
