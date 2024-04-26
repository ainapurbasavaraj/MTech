
import os
import requests
import platform
import json
import common

class FileServer:

    def __init__(self) -> None:

        self.storagePath = os.path.join(os.getcwd(), 'Files')
        # Holds list of files server has
        self.filesList = []
        #stores the list of files server has in filesystem.
        #self.filesList and self.fileInfo has same info but
        #self.fileList is in memory and self.fileInfo is on disk.
        # This is required to keep the data when server crashes.
        configPath = os.path.join(os.getcwd(), 'config')
        self.metadataFile = os.path.join(configPath, 'metadata.txt' )
        self.ipConfigPath = os.path.join(configPath, 'ServerIp.txt')
        self.otherServerIpList = []
        self.register_peer_servers()

    
    def register_peer_servers(self):
        with open(self.ipConfigPath,'r') as f:
            cur_node = platform.node()
            data = f.read()
            data = json.loads(data)
            self.otherServerIpList.extend(data[cur_node])


    def add_file_to_server(self, filename, data):

        filePath = os.path.join(self.storagePath, filename)
        with open(filePath, 'w') as f:
            f.write(data)
        #append the list
        self.filesList.append(filename)
        with open(self.metadataFile, 'w') as f:
            f.write(filename)

    
    def get_file_from_server(self, file_name, headers):
        absFilePath = os.path.join(self.storagePath,file_name)
        if os.path.exists(absFilePath):
            with open(absFilePath, 'r') as f:
                return f.read()
        # else:
            #contact other servers
            # return self.get_data_from_other_servers(file_name, headers)
        return "KO"

    def get_data_from_other_servers(self, file_name, headers):
        
        for host in self.otherServerIpList:
            url = 'http://%s/file/%s' %(common.get_ip_by_hostname(host), file_name)
            if isinstance(headers,str):
                headers = json.loads(headers)
                visited_hosts = headers.get('Visited', "")
            else:
                visited_hosts = headers.get('Visited', "") 

            if host in visited_hosts.split(','):
                print("Already visited this host {}".format(host))
                continue
            try:
                visited_hosts = "%s,%s"%(visited_hosts,host)
                headers = '{"Visited": "%s"}'%(visited_hosts)
                headers = json.loads(headers)
                print("Visiting nearest server %s from %s" %(host,common.getHostname()))
                result = requests.get(url=url, headers=headers)
            except Exception as e:
                print("Failed to connect to server %s with exception %s" %(url,e))
            else:
                if result.text != "KO":
                    common.downloadFile(self.storagePath,file_name,result.text)
                return result.text
        
        return "KO"
        
