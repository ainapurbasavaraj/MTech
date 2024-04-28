
import os
import requests
import platform
import json
import common
from check_hash import hashfile

class FileServer:

    def __init__(self) -> None:

        self.storagePath = os.path.join(os.getcwd(), 'Files')
        # Holds list of files server has
        self.filesList = []

        # Store the hash of the files
        self.hashdict = dict()
        dir_list = os.listdir(self.storagePath)
        for file in dir_list:
            self.hashdict[hashfile(os.path.join(self.storagePath,file))] = file


        #stores the list of files server has in filesystem.
        #self.filesList and self.fileInfo has same info but
        #self.fileList is in memory and self.fileInfo is on disk.
        # This is required to keep the data when server crashes.
        configPath = os.path.join(os.getcwd(), 'config')
        #self.metadataFile = os.path.join(configPath, 'metadata.txt' )
        #self.ipConfigPath = os.path.join(configPath, 'ServerIp.txt')
        self.otherServerIpList = []
        #self.register_peer_servers()

    
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
        
        if hashfile(filePath) in self.hashdict:
            print("File already present in the server.. Discarding it")
            os.remove(filePath)
            return

        self.hashdict[hashfile(filePath)] = filename

        print("File %s added to server." %(filePath))

    
    def get_file_from_server(self, file_name, headers):
        absFilePath = os.path.join(self.storagePath,file_name)
        if os.path.exists(absFilePath):
            with open(absFilePath, 'r') as f:
                return f.read()
        return "KO"

