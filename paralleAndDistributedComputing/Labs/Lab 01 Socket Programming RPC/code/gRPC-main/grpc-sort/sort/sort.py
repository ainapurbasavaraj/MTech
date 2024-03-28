from concurrent import futures
import grpc

from sort_pb2 import SortResponse
import sort_pb2_grpc

import base64
import numpy as np

class SortServicer(sort_pb2_grpc.SortServiceServicer):
    def Sort(self, request, context):
        nums_b64 = base64.decodebytes(request.numbers)
        nums = np.frombuffer(nums_b64, dtype=np.float64)
        print("Sorting: ", nums)
        nums_sorted = np.sort(nums)
        return SortResponse(numbers=base64.b64encode(nums_sorted))
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sort_pb2_grpc.add_SortServiceServicer_to_server(SortServicer(), server)
    server.add_insecure_port('[::]:51051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
