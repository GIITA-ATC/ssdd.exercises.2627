#!/usr/bin/python3
"Usage: {0} <server_host:port> <n1> <n2>"

import socket
import struct
import sys


if len(sys.argv) != 4:
    print(__doc__.format(sys.argv[0]))
    sys.exit(1)

host, port = sys.argv[1].split(':')
port = int(port)
num1 = int(sys.argv[2])
num2 = int(sys.argv[3])

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    data = struct.pack("!ii", num1, num2)
    s.sendto(data, (host, port))

    data = s.recv(1024)
    result = struct.unpack("!i", data)[0]

    print(f"Result: {result}")
