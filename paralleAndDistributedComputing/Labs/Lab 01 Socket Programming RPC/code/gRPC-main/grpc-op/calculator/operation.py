import grpc
import operation_pb2
import operation_pb2_grpc
from operation_pb2 import OperationResponse
from concurrent import futures

class CalculatorService(operation_pb2_grpc.CalculatorServicer):
    def Calculate(self, request, context):
        if(request.op=="+"):
            return OperationResponse(result=request.a + request.b)
        elif(request.op=="-"):
            return OperationResponse(result=request.a - request.b)
        elif(request.op=="/"):
            return OperationResponse(result=request.a / request.b)
        elif(request.op=="*"):
            return OperationResponse(result=request.a * request.b)
        else:
            context.abort(grpc.StatusCode.NOT_FOUND, "Operation not found")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    operation_pb2_grpc.add_CalculatorServicer_to_server(CalculatorService(), server)
    server.add_insecure_port("[::]:56001")
    server.start()
    server.wait_for_termination()

if __name__=='__main__':
    serve()