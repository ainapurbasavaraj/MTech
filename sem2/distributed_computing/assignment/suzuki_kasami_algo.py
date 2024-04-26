
from collections import deque
from config_loader import keys, Methods
import requests
from request_builder import RequestBuilder
from request_handler import RequestHandler
import concurrent.futures
import json
import os


class SuzukiKasami():

    def __init__(self, node, config) -> None:
        self.node = node
        self.config = config
        self.init_rn()
        self.init_ln()
        self.token_queue = deque()
        self.token_bearer = self.config[keys.TOKEN_BEARER]
        self.workers = self.config[keys.NUM_NODES] - 1

    def init_rn(self):
        self.RN = dict()
        for i in range(self.config[keys.NUM_NODES]):
            self.RN['node%s' %str(i+1)] = 0

    def init_ln(self):
        self.LN = dict()
        for i in range(self.config[keys.NUM_NODES]):
            self.LN['node%s' %str(i+1)] = 0

    def increment_rn(self):
        self.RN[self.node] = self.RN[self.node] + 1
    
    def increment_ln(self):
        self.LN[self.node] = self.LN[self.node] + 1

    def request_token(self, node):
        requestBody = dict()
        requestBody[keys.NODE] = self.node
        requestBody[keys.SEQUENCE_NUMBER] = self.RN[self.node]
        try:
            builder = RequestBuilder(node, self.config, requestBody, Methods.POST)
            requestData = builder.build()
            return RequestHandler.Request(requestData)
        except Exception as e:
            print("Not able to connect to node %s, error : %s" %(node, str(e)))
            return {}

    def lock(self):
        print("Trying to enter critical section...")
        # Check if I am the token-bearer
        if self.token_bearer == self.node:
            print("I am the token bearer. No need to ask permission.")
            return True
        else:
            #increment the RN
            self.increment_rn()
            #send this sequence info to other nodes
            for node in self.RN.keys():
                if node is not self.node:
                    print("connecting node : %s, My node : %s" %(node, self.node))
                    response = self.request_token(node)
            #with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executror:

             #   future_to_send = {
             #       executror.submit(self.request_token, node): 
             #       node for node in self.RN.keys()
             #       if node is not self.node}

             #   for future in concurrent.futures.as_completed(future_to_send):
             #       response = future_to_send

                    print("RECEIVED RESPONSE : %s" %response)
                    #Update the token-bearer after successfully receiving info
                    if response.get(keys.TOKEN):
                        self.token_bearer = self.node
                        print("TOKEN RECEIVED : %s" %response.get(keys.TOKEN))
                
                        #update the token queue with token queue from response
                        self.token_queue.extend(response[keys.TOKEN_QUEUE])

                        # remove the node from the token queue
                        self.token_queue.remove(self.node)
                        return True
        return False


                    
    def unlock(self):
        self.increment_ln()

    def process(self, data):
        print(data)
        data = json.loads(data)
        #update RN with max of (RN[i], sequence_number)
        requestingNode = data[keys.NODE]
        self.RN[requestingNode] = \
            max(self.RN[requestingNode], 
            data[keys.SEQUENCE_NUMBER])

        # Check if token is present with me and send reply accordingly.
        return self.reply(requestingNode)
    
    def reply(self, requestingNode):

        response = dict()
        print(self.token_bearer)
        print(self.RN[requestingNode])
        print(self.LN[requestingNode])
        if self.token_bearer == self.node and \
            self.RN[requestingNode] == self.LN[requestingNode]+1:
            self.token_bearer = requestingNode
            self.token_queue.append(requestingNode)
            
            response[keys.TOKEN] = self.config[keys.TOKEN]
            response[keys.TOKEN_QUEUE] = [token for token in self.token_queue]

        print("sending response : %s" %response)
        return json.dumps(response)
                    
 
