#!/usr/bin/env python3

import sys
import random
import argparse
import grpc
from datetime import datetime, timezone
from google.protobuf import empty_pb2


import app_pb2
import app_pb2_grpc


class ReservationClient:
    def __init__(self, stub):
        self.stub = stub

    def call_remote(self, func, request):
        try:
            response = func(request)
        except grpc.RpcError as e:
            print(f'Error: {e.code().name} - {e.details()}')
            sys.exit(1)
        return response

    def makeReservation(self):
        request = app_pb2.NewReservationRequest(
            number_of_diners = random.randint(1, 10),
            client_name = 'John Doe',
            contact_phone = '555-555-555'
        )
        request.time.FromDatetime(datetime.now(tz=timezone.utc))

        try:
            response = self.stub.makeReservation(request)
        except grpc.RpcError as e:
            print(f'Error: {e.code().name} - {e.details()}')
            sys.exit(1)

        print(response)

    def checkReservation(self, id):
        try:
            response = self.stub.checkReservation(
                app_pb2.ReservationIdRequest(id=int(id))
            )
        except grpc.RpcError as e:
            print(f'Error: {e.code().name} - {e.details()}')
            sys.exit(1)

        print(response)

    def cancelReservation(self, id):
        try:
            response = self.stub.cancelReservation(
                app_pb2.ReservationIdRequest(id=int(id))
            )
        except grpc.RpcError as e:
            print(f'Error: {e.code().name} - {e.details()}')
            sys.exit(1)

        print('Reservation cancelled')

    def listReservations(self):
        response = self.stub.listReservations(empty_pb2.Empty())

        for reservation in response.reservations:
            print(reservation)


parser = argparse.ArgumentParser()
parser.add_argument('server', type=str)
parser.add_argument('-m', '--make', action='store_true')
parser.add_argument('-c', '--check', type=str, action='store')
parser.add_argument('-r', '--remove', type=str, action='store')
parser.add_argument('-l', '--list', action='store_true')
args = parser.parse_args()

channel = grpc.insecure_channel(args.server)
stub = app_pb2_grpc.ReservationsStub(channel)
client = ReservationClient(stub)

if args.make:
    client.makeReservation()
elif args.check:
    client.checkReservation(args.check)
elif args.remove:
    client.cancelReservation(args.remove)
else:
    client.listReservations()
