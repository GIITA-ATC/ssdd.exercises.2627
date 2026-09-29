#!/usr/bin/python3
"Usage: {0} <server_host:port> {{add|mul}} <n1> <n2> [n3 ...]"

import sys
import socket
import struct


if len(sys.argv) < 2:
    print(__doc__.format(sys.argv[0]))
    sys.exit(1)

host, port = sys.argv[1].split(':')
port = int(port)
operation = sys.argv[2]
numbers = [int(x) for x in sys.argv[3:]]

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    data_format = f'!3s{len(numbers)}h'
    data = struct.pack(data_format, operation.encode(), *numbers)

    s.sendto(data, (host, port))

    data = s.recv(1024)
    result = struct.unpack('!i', data)[0]

    print(f"Result: {result}")
