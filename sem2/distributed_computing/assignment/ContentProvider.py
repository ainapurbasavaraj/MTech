#!/usr/bin/python3

from jsonrpcclient import request
import requests
import os, time
import json
import common
import sys
import threading


#url = 'http://localhost:80/rpc'
hostname = "node2"
base_url = common.get_ip_by_hostname(hostname)
url = 'http://%s/rpc' %(base_url)


def watch_content(node, handler):
    print("Watching content in a thread....")
    contentdir = os.path.join(os.getcwd(), node)
    content = os.path.join(contentdir, 'content_provider')
    path_to_watch = content
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])
    while True:

        time.sleep(10)
        after = dict ([(f, None) for f in os.listdir (path_to_watch)])
        added = [f for f in after if not f in before]
        for counter, file in enumerate(added):
            print("New file detected on content server : %s" %file)
            with open(os.path.join(content,file), 'r') as f:
                data = f.read()
            
            params ='{"filename" : "%s", "data": "%s"}' %(file,data)
            params = json.loads(params, strict=False)
            print("%s wants to enter in to critical section." %(node))
            if handler.lock():
                print("Got the token, Adding file %s to server : %s" %(file, url))
                time.sleep(100)
                result = requests.post(url, json=request('addfile', params=params))
                print("\nFile added to server, Releasing the lock... ")
                handler.unlock()
                #print(result.json())
            if counter == len(added)-1:
                print("\n***************************************")
                print("Waiting for new content....\n")
        before = after


def start_thread(node, handler):
    thread = threading.Thread(target=watch_content, args=(node, handler))
    thread.setDaemon(True)
    thread.start()
