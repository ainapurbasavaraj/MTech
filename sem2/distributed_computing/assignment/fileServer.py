
import os
import requests

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
            self.otherServerIpList.extend(f.read().splitlines())


    def add_file_to_server(self, filename, data):

        filePath = os.path.join(self.storagePath, filename)
        with open(filePath, 'w') as f:
            f.write(data)
        #append the list
        self.filesList.append(filename)
        with open(self.metadataFile, 'w') as f:
            f.write(filename)

    
    def get_file_from_server(self, file, base_url):
        absFilePath = os.path.join(self.storagePath,file)
        if os.path.exists(absFilePath):
            with open(absFilePath, 'r') as f:
                return f.read()
        else:
            #contact other servers
            return self.get_data_from_other_servers(file, base_url)

    def get_data_from_other_servers(self, file, base_url):
        
        for host in self.otherServerIpList:
            url = 'http://%s/file/%s' %(host, file)
            print(url)
            print(base_url)
            if url == base_url:
                print("Already visited this url {}".format(url))
                continue

            result = requests.get(url)
            if result.text:
                return result.text
        
        return "KO"
        
        