#!/usr/bin/python3

import requests
import os
import common
import json

hostname = common.getHostname()
base_url = common.get_ip_by_hostname(hostname)
base_url = 'http://%s' %(base_url)
base_path = os.path.join(os.getcwd(), 'downloaded_files')

filename = input("Enter filename to download : ")

file = filename
visited_hosts = []
headers = '{"Content-Type": "application/json; charset=utf-8", "visited": "%s"}' %hostname
headers = json.loads(headers)
get_file_url = "{base_url}/file/{filename}".format(base_url=base_url, filename=file)

try:
    result = requests.get(get_file_url,headers=headers)
except Exception as e:
    print("Exception in connecting to server {}".format(e))
else:
    if result.text != "KO":
        common.downloadFile(base_path, filename, result.text)
    else:
        print("file not found on server")
    
