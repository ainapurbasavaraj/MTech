
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
        self.workers = self.config[keys.NUM_NODES]

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

    def update_token_queue(self, data):
        data = json.loads(data)
        print("Updating token queue %s " %data)
        token_list = data[keys.TOKEN_QUEUE]
        token_queue = deque()
        [token_queue.append(i) for i in token_list]
        self.token_queue = token_queue
        return {}

    def request_token(self, node):
        #print("Sending request to node : %s\n" %node)
        if node == self.node:
            #print("Don't send request to itself.. returning\n")
            return {}
        requestBody = dict()
        requestBody[keys.NODE] = self.node
        requestBody[keys.SEQUENCE_NUMBER] = self.RN[self.node]
        requestBody[keys.LN_SEQUENCE] = self.LN[self.node]
        try:
            builder = RequestBuilder(node, self.config, requestBody, 'request-token', Methods.POST)
            requestData = builder.build()
            return RequestHandler.Request(requestData)
        except Exception as e:
            print("Not able to connect to node %s, error : %s" %(node, str(e)))
            return {}

    def lock(self):
        #print("\nTrying to enter critical section...")
        print("\n Acquiring lock....")
        #increment the RN
        self.increment_rn()
        # Check if I am the token-bearer
        if self.token_bearer == self.node:
            print("I am the token bearer. No need to ask permission.")
            return True
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executror:

                future_to_send = {
                    executror.submit(self.request_token, node): 
                    node for node in self.RN.keys()
                    }

                for future in concurrent.futures.as_completed(future_to_send):
                    response = future.result()

                    #Update the token-bearer after successfully receiving info
                    token = response.get(keys.TOKEN_QUEUE)
                    if token and token[0] == self.node:
                        self.token_bearer = self.node
                        print("TOKEN RECEIVED :  %s" %response)
                    
                        #update the token queue with token queue from response
                        token_queue = deque()
                        [token_queue.append(i) for i in token]
                        self.token_queue = token_queue

                        # remove the node from the token queue
                        self.token_queue.popleft()
                        return True

            while True:
                if self.token_queue and self.token_queue[0] == self.node:
                    self.token_bearer = self.node
                    self.token_queue.popleft()
                    return True
        return False


    def display(self):
        print("\n*** Current Data state ***")
        print('\ntoken_queue : %s ' %self.token_queue)
        print('\ntoken_bearer : %s ' %self.token_bearer)
        print('\nRN : %s' %self.RN)
        print('\nLN : %s' %self.LN)
                    
    def unlock(self):
        self.increment_ln()
        
        if self.token_queue:
            node = self.token_queue[0]
            requestBody = dict()
            self.token_bearer = node
            requestBody[keys.NODE] = self.node
            requestBody[keys.TOKEN_QUEUE] = [token for token in self.token_queue]
            try:
                builder = RequestBuilder(node, self.config, requestBody, 'release-token', Methods.POST)
                requestData = builder.build()
                RequestHandler.Request(requestData)
            except Exception as e:
                print("Not able to connect to node %s, error : %s" %(node, str(e)))
                #return {}
        self.display()


    def process(self, data):
        #print(data)
        data = json.loads(data)
        #update RN with max of (RN[i], sequence_number)
        requestingNode = data[keys.NODE]
        self.RN[requestingNode] = \
            max(self.RN[requestingNode], 
            data[keys.SEQUENCE_NUMBER])

        self.LN[requestingNode] = \
                max(self.LN[requestingNode], data[keys.LN_SEQUENCE])
        # Check if token is present with me and send reply accordingly.
        return self.reply(requestingNode)
    
    def reply(self, requestingNode):

        response = dict()
        if self.token_bearer == self.node and \
            self.RN[requestingNode] == self.LN[requestingNode]+1:
            #self.token_bearer = requestingNode
            self.token_queue.append(requestingNode)
            
            # check if current process completed its critical section
            # Then only send token
            if self.RN[self.node] == self.LN[self.node]:
                self.token_bearer = self.token_queue[0]
                response[keys.TOKEN] = self.config[keys.TOKEN]
                response[keys.NODE] = self.node
                response[keys.TOKEN_QUEUE] = [token for token in self.token_queue]


        self.display()

        #print("*****sending response***** \n")
        import pprint
        pp = pprint.PrettyPrinter(depth=4)
        #pp.pprint(response)
        return json.dumps(response)
                    
 
