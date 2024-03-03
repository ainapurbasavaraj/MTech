
from jsonrpcclient import request
import requests

url = 'http://localhost:8080/rpc'

result = requests.post(url, json=request('addfile', params={"filename" : "abc.txt", "data": "123456"}))
print(result.json())