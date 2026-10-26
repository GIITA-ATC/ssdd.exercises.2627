#!/usr/bin/env python3
"Usage: {0} <server_host:port> {{add|mul}} <n1> <n2> [n3 ...]"

import sys
import grpc

import math_pb2
import math_pb2_grpc


if len(sys.argv) < 2:
    print(__doc__.format(sys.argv[0]))
    sys.exit(1)

server = sys.argv[1]
operation = sys.argv[2]
numbers = [int(x) for x in sys.argv[3:]]

channel = grpc.insecure_channel(server)
stub = math_pb2_grpc.MathStub(channel)

request = math_pb2.Request(numbers=numbers)
calc = stub.add if operation == 'add' else stub.multiply
response = calc(request)

print(f'Result: {response.result}')
