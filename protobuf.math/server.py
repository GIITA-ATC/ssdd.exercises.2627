#!/usr/bin/python3
import socket
import math_pb2 as math


def mul(numbers):
    result = 1
    for n in numbers:
        result *= n
    return result


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(('', 10001))

    while 1:
        print("\nWaiting for a request...")
        data, client = s.recvfrom(4096)

        request = math.Request()
        request.ParseFromString(data)

        calc = sum if request.operation == math.Request.SUM else mul
        result = calc(request.numbers)

        response = math.Response(result=result)
        s.sendto(response.SerializeToString(), client)
        print(f"{client} :: {request.operation} result = {result}")
