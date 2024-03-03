import grpc
from addition_pb2_grpc import AdditionStub
from addition_pb2 import AdditionRequest

channel = grpc.insecure_channel("localhost:50059")
stub = AdditionStub(channel)
request = AdditionRequest(a=1, b=2)
print(stub.Addn(request))