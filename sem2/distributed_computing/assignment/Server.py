
import os
import sys
from flask import Flask, request
from jsonrpcserver import dispatch, Result, Success, method
from fileServer import FileServer

#from jsonrpcserver.exceptions import InvalidParams

app = Flask(__name__)

fileServer = FileServer()

@app.route('/')
def index():
    return 'Welcom to File Server!!'

@app.route('/file/<string:path>')
def get_file_from_server(path):
    data = request.headers
    return fileServer.get_file_from_server(path, data)


@app.route('/rpc', methods=["POST"])
def rpc():
    #print(request.data)
    return dispatch(request.data.decode())

@method
def addfile(filename, data) ->Result:
    print("Adding file to server : %s" %filename)
    fileServer.add_file_to_server(filename, data)
    return Success("OK")


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 80)
