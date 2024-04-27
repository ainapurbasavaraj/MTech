
from config_loader import keys, Methods
from common import ServerRequestData, get_ip_by_hostname, getHostname

class RequestBuilder:

    def __init__(self, node, config, req_args, endpoint, method) -> None:
        self.requestData : ServerRequestData = ServerRequestData()
        self.node = node
        self.config = config
        self.req_args = req_args
        self.method = method
        self.endPoint = endpoint

    def buildUrl(self):
        base_url = 'http://%s' %(self.config[self.node])
        self.requestData.url = base_url + '/' + self.config[keys.SERVICE_NAME] + '/' + self.endPoint
        self.requestData.method = self.method
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
