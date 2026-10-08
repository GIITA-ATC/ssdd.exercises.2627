#!/usr/bin/python3

import socket
import argparse
from door_pb2 import ControlMessage, ResponseMessage

REQUEST_ID = 1  # Implement something to define request ID

class Controller:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (host, port)

    def handle_request(self, request):
        self.sock.sendto(
            request.SerializeToString(),
            self.server_address
        )

        data = self.sock.recv(4096)
        response = ResponseMessage()
        response.ParseFromString(data)

        self.sock.close()
        return response

    def check_status(self):
        request = ControlMessage()
        request.id = REQUEST_ID
        request.command = ControlMessage.CHECK_STATUS
        return self.handle_request(request)

    def open_door(self, mode=ControlMessage.VEHICLE, time=None):
        request = ControlMessage()
        request.id = REQUEST_ID
        request.command = ControlMessage.OPEN
        request.time = time
        request.mode = ControlMessage.VEHICLE
        if mode == 'pedestrian':
            request.mode = ControlMessage.PEDESTRIAN

        return self.handle_request(request)

    def close_door(self):
        request = ControlMessage()
        request.id = REQUEST_ID
        request.command = ControlMessage.CLOSE
        return self.handle_request(request)


def main():
    controller = Controller(args.host, args.port)

    if args.command == 'status':
        response = controller.check_status()

    if args.command == 'open':
        response = controller.open_door(args.mode, args.time)

    if args.command == 'close':
        response = controller.close_door()

    print(f'Result: {ResponseMessage.Result.Name(response.result)}')


parser = argparse.ArgumentParser(description='Door Controller')

parser.add_argument("host", help="Host address of the server")
parser.add_argument("port", type=int, help="Port number of the server")
subparsers = parser.add_subparsers(dest='command', help='Commands', metavar='COMMAND')

open_parser = subparsers.add_parser('open', help='Open door')
open_parser.add_argument('-t', '--time', type=int, default=0, help='Time to keep the door open in seconds')
open_parser.add_argument('-m', '--mode', choices=['vehicle', 'pedestrian'], default='vehicle', help='Mode to open the door')

close_parser = subparsers.add_parser('close', help='Close door')
get_parser = subparsers.add_parser('status', help='Check door status')

args = parser.parse_args()

main()
