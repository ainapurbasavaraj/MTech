
from config_loader import keys, Methods
from common import ServerRequestData, get_ip_by_hostname, getHostname

class RequestBuilder:

    def __init__(self, node, config, req_args, method) -> None:
        self.requestData : ServerRequestData = ServerRequestData()
        self.node = node
        self.config = config
        self.req_args = req_args
        self.method = method
        self.endPoint = 'request-token'

    def get_ip_port(self):
        ip_file = os.path.join('config', 'content_server_ip.txt')
        with open(ip_file, 'r') as f:
            data = f.read()
            iplist = data.split()
            ip_port = [node.split('=') for node in iplist if self.node in iplist]
            return ip_port[0]

    def buildUrl(self):
        hostname = self.node
        #base_url = 
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
