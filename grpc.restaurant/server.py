#!/usr/bin/env python3

import random
import grpc
from concurrent import futures
from google.protobuf import empty_pb2

import app_pb2
import app_pb2_grpc


class ReservationsService(app_pb2_grpc.ReservationsServicer):
    def __init__(self):
        self.reservations = {}

    def _get_or_404(self, id, context):
        if not id:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                'Missing reservation ID'
            )

        if id not in self.reservations:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                'Reservation not found'
            )

    def _validate_new_reservation(self, req, context):
        missing = []
        if not req.HasField("time"):  missing.append("time")
        if req.number_of_diners <= 0: missing.append("number_of_diners")
        if not req.client_name:       missing.append("client_name")
        if not req.contact_phone:     missing.append("contact_phone")
        if missing:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                f"Missing or invalid fields: {', '.join(missing)}"
            )

    def makeReservation(self, request, context):
        self._validate_new_reservation(request, context)

        reservation = app_pb2.Reservation(
            id = random.randint(10000, 99999),
            time = request.time,
            number_of_diners = request.number_of_diners,
            client_name = request.client_name,
            contact_phone = request.contact_phone
        )
        self.reservations[reservation.id] = reservation

        print(f'{context.peer()} :: Make {reservation.id}')
        return reservation

    def checkReservation(self, request, context):
        self._get_or_404(request.id, context)

        print(f'{context.peer()} :: Check {request.id}')
        return self.reservations[request.id]

    def cancelReservation(self, request, context):
        self._get_or_404(request.id, context)

        del self.reservations[request.id]
        print(f'{context.peer()} :: Cancel {request.id}')
        return empty_pb2.Empty()

    def listReservations(self, _, context):
        print(f'{context.peer()} :: List')
        return app_pb2.ReservationsList(
            reservations = list(self.reservations.values())
        )


print("Bootstrapping gRPC server...")

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
app_pb2_grpc.add_ReservationsServicer_to_server(ReservationsService(), server)
server.add_insecure_port('[::]:10001')

server.start()
print(f'Server started...')

try:
    server.wait_for_termination()
except KeyboardInterrupt:
    print("Stopping server...")
    server.stop(0)
