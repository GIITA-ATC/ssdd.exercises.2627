#!/usr/bin/env python3

import grpc
from concurrent import futures

import math_pb2
import math_pb2_grpc


class MathService(math_pb2_grpc.MathServicer):
    def add(self, request, context):
        result = sum(request.numbers)
        return math_pb2.Response(result=result)

    def multiply(self, request, context):
        result = 1
        for n in request.numbers:
            result *= n
        return math_pb2.Response(result=result)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
math_pb2_grpc.add_MathServicer_to_server(MathService(), server)
server.add_insecure_port('[::]:10001')
server.start()

try:
    print("\nWaiting for a request...")
    server.wait_for_termination()

except KeyboardInterrupt:
    server.stop(0)
