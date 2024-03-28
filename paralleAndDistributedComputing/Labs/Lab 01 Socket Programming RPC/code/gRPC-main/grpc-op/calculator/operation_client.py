import grpc
from operation_pb2 import OperationRequest
from operation_pb2_grpc import CalculatorStub

channel = grpc.insecure_channel("localhost:56001")
stub = CalculatorStub(channel)
request = OperationRequest(op="*", a=21, b=50)
print(stub.Calculate(request))