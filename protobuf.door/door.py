#!/usr/bin/python3

import sys
import socket
from door_pb2 import ControlMessage, ResponseMessage

SOCKET_PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 10001


class Door:
    CLOSED = ResponseMessage.ALREADY_CLOSED
    OPEN = ResponseMessage.ALREADY_OPEN

    def __init__(self):
        self.status = Door.CLOSED
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', SOCKET_PORT))
        print(f'Server listening on port {SOCKET_PORT}')

    def run(self):
        while True:
            data, client = self.sock.recvfrom(4096)
            request = ControlMessage()
            request.ParseFromString(data)
            print(f'Request received from {client}')

            response = ResponseMessage()
            response.id = request.id

            if request.command == ControlMessage.CHECK_STATUS:
                response.result = self.status

            if request.command == ControlMessage.OPEN:
                response.result = self.open(request.mode, request.time)

            if request.command == ControlMessage.CLOSE:
                response.result = self.close()

            self.sock.sendto(response.SerializeToString(), client)

    def open(self, mode, time):
        if self.status == Door.OPEN:
            print(f'[!] Door already open.')
            return ResponseMessage.ALREADY_OPEN

        # Implement something for random errors and time
        self.status = Door.OPEN
        print(f'[-] Door open. Mode: {mode}. Time: {time}')
        return ResponseMessage.OK

    def close(self):
        if self.status == Door.CLOSED:
            print(f'[!] Door already closed.')
            return ResponseMessage.ALREADY_CLOSED

        # Implement something for random errors
        self.status = Door.CLOSED
        print('[-] Door closed.')
        return ResponseMessage.OK


if __name__ == '__main__':
    server = Door()
    server.run()
