#!/usr/bin/python3

from jsonrpcclient import request
import requests
import os, time
import json
import common
import sys
import threading


#url = 'http://localhost:80/rpc'
hostname = common.getHostname()
base_url = common.get_ip_by_hostname(hostname)
url = 'http://%s/rpc' %(base_url)

content = os.path.join(os.getcwd(), 'content_provider')
if not os.path.exists(content):
    os.mkdir(content)

def watch_content(node, handler):
    path_to_watch = content
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])
    while 1:
        time.sleep (10)
        after = dict ([(f, None) for f in os.listdir (path_to_watch)])
        added = [f for f in after if not f in before]
        for file in added:
            print("added file : %s" %file)
            with open(os.path.join(content,file), 'r') as f:
                data = f.read()
            
            params ='{"filename" : "%s", "data": "%s"}' %(file,data)
            params = json.loads(params, strict=False)
            print("%s wants to enter in to critical section." %(node))
            handler.lock()
            result = requests.post(url, json=request('addfile', params=params))
            print("Releasing the critical section")
            handler.unlock()
            print(result.json())
        before = after


def start_thread(node, handler):
    thread = threading.Thread(target=watch_content, args=(node, handler))
    thread.start()