#!/usr/bin/env python3

import sys
from requests import get, post, delete

URL = 'http://localhost:5001/reservations'


def show(response):
    data = response.json()
    if not response.ok:
        print(f'Error {response.status_code}: {data["message"]}')
    elif isinstance(data, list):
        print(f'Reservas: {len(data)}')
        for r in data:
            print(f'  {r}')
    else:
        print(data)


args = sys.argv[1:]
op = args[0] if args else ''

if op == 'request' and len(args) == 5:
    show(post(URL, data={'time': args[1], 'diners': args[2],
                         'name': args[3], 'phone': args[4]}))
elif op == 'check' and len(args) == 2:
    show(get(f'{URL}/{args[1]}'))
elif op == 'cancel' and len(args) == 2:
    show(delete(f'{URL}/{args[1]}'))
elif op == 'list':
    show(get(URL))
else:
    print('Uso: client.py request <yyyy-MM-ddTHH:mm> <comensales> <nombre> <telefono>')
    print('     client.py check|cancel <id>')
    print('     client.py list')
