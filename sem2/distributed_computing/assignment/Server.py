
import os
from flask import Flask
from jsonrpcserver import dispatch, result, Success
#from jsonrpcserver.exceptions import InvalidParams

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcom to File Server!!'

@app.route('/file/<string:path>')
def get_file_from_server(path):
    fileServer = FileServer()
    return fileServer.get_file_from_server(path)


@app.route('/rpc/addfile')
def rpc(request):
    print(request.data)
    response = dispatch(request.data)
    return result(response)

@dispatch
def addfile(filename, data):
    print(filename)
    fileServer = FileServer()
    fileServer.add_file_to_server(filename, data)
    return Success()

class FileServer:

    def __init__(self, storagePath, configPath) -> None:

        self.storagePath = storagePath
        # Holds list of files server has
        self.filesList = []
        #stores the list of files server has in filesystem.
        #self.filesList and self.fileInfo has same info but
        #self.fileList is in memory and self.fileInfo is on disk.
        # This is required to keep the data when server crashes.
        self.metadataFile = os.path.join(configPath, 'metadata.txt' )

    
    def add_file_to_server(self, filename, data):

        filePath = os.path.join(self.storagePath, filename)
        with open(filePath, 'w') as f:
            f.write(data)
        #append the list
        self.filesList.append(filename)
        with open(self.metadataFile, 'w') as f:
            f.write(filename)

    
    def get_file_from_server(self, file):
        absFilePath = os.path.join(self.storagePath,file)
        if os.path.exists(absFilePath):
            with open(absFilePath, 'r') as f:
                return f.read()
        else:
            #contact other servers
            return self.get_data_from_other_servers(file)

    def get_data_from_other_servers(self, file):
        pass


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 8080)