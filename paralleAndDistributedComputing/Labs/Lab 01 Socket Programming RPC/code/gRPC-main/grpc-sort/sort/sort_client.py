import grpc
from sort_pb2 import SortRequest
from sort_pb2_grpc import SortServiceStub
import base64
import numpy as np

channel = grpc.insecure_channel("localhost:51051")
stub = SortServiceStub(channel)
nums = np.array([45, 23, 89, 11, 80, 23, 1], dtype=np.float64)
enc_nums = base64.b64encode(nums)
request = SortRequest(numbers = enc_nums)
print(np.frombuffer(base64.decodebytes((stub.Sort(request)).numbers), dtype=np.float64))
