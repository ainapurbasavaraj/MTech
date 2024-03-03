from concurrent import futures
import grpc

from addition_pb2 import(
    AdditionResponse,
)
import addition_pb2_grpc

class AdditionService(addition_pb2_grpc.AdditionServicer):
    def Addn(self, request, context):
        return AdditionResponse(result=(request.a + request.b))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    addition_pb2_grpc.add_AdditionServicer_to_server(AdditionService(), server)
    server.add_insecure_port("[::]:50059")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()