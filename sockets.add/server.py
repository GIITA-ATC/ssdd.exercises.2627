#!/usr/bin/python3

import socket
import struct


port = 10001

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(('', port))

    while 1:
        print("\nWaiting for a request...")

        data, client = s.recvfrom(1024)
        num1, num2 = struct.unpack("!ii", data)
        result = num1 + num2
        s.sendto(struct.pack('!i', result), client)

        print(f"{client} :: {num1} + {num2} = {result}")
