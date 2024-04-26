import os
import json

def loadconfig():
    configFile = os.path.join('config', 'content_provider_config.json')
    with open (configFile, 'r') as f:
        return json.loads(f.read())


class keys:
    TOKEN = 'token'
    TOKEN_BEARER = 'token-bearer'
    NUM_NODES = 'num-nodes'
    SERVICE_NAME = 'service-name'
    NODE = 'node'
    SEQUENCE_NUMBER = 'sequence-number'
    CONTENT_TYPE = 'content-type'
    TOKEN_QUEUE = 'token-queue'

class Methods:
    POST = 'POST'
    GET = 'GET'