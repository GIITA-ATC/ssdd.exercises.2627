#!/usr/bin/env python3

from datetime import datetime
from flask import Flask, request
from flask_restful import Resource, Api, abort

app = Flask(__name__)
api = Api(app)

CAPACITY = 40
reservations = {}
next_id = 1


def get_or_404(res_id):
    if res_id not in reservations:
        abort(404, message=f'La reserva {res_id} no existe')
    return reservations[res_id]


class Reservation(Resource):
    def get(self, res_id):
        return get_or_404(res_id)

    def delete(self, res_id):
        get_or_404(res_id)
        del reservations[res_id]
        return {'message': f'Reserva {res_id} cancelada'}


class ReservationList(Resource):
    def get(self):
        return list(reservations.values())

    def post(self):
        global next_id
        try:
            time = datetime.fromisoformat(request.form['time'])
            diners = int(request.form['diners'])
            name = request.form['name']
            phone = request.form['phone']
        except (KeyError, ValueError):
            abort(400, message='Faltan campos o no son válidos (time, diners, name, phone)')

        if diners <= 0:
            abort(400, message='Número de comensales no válido')
        if time < datetime.now():
            abort(400, message='La fecha ya ha pasado')
        if not 20 <= time.hour < 23:
            abort(400, message='Fuera del horario de cena (20:00-23:00)')

        day = time.date().isoformat()
        occupied = sum(r['diners'] for r in reservations.values()
                       if r['time'].startswith(day))
        if occupied + diners > CAPACITY:
            abort(409, message=f'No hay plazas ese día (quedan {CAPACITY - occupied})')

        r = {'id': next_id, 'time': time.isoformat(), 'diners': diners,
             'name': name, 'phone': phone}
        reservations[next_id] = r
        next_id += 1
        return r, 201


api.add_resource(ReservationList, '/reservations')
api.add_resource(Reservation, '/reservations/<int:res_id>')


if __name__ == '__main__':
    app.run(debug=True, port=5001, threaded=False)
