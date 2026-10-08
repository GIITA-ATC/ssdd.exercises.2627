#!/usr/bin/python3
"Usage: {0} <server_host:port> {{add|mul}} <n1> <n2> [n3 ...]"

import sys
import socket
import math_pb2 as math


if len(sys.argv) < 2:
    print(__doc__.format(sys.argv[0]))
    sys.exit(1)

host, port = sys.argv[1].split(':')
port = int(port)
operation = sys.argv[2]
numbers = [int(x) for x in sys.argv[3:]]

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    request = math.Request()
    request.numbers.extend(numbers)
    request.operation = 0 if operation == 'sum' else 1

    s.sendto(request.SerializeToString(), (host, port))

    data = s.recv(4096)
    response = math.Response()
    response.ParseFromString(data)

    print(f"Result: {response.result}")
