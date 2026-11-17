#!/usr/bin/python3

import paho.mqtt.client as mqtt
import json
import argparse


def print_hot_deal(deal):
    print(f'[!] HOT DEAL\n'
        + f'\t{deal["name"]} by {deal["developer"]} ({deal["type"]})\n'
        + f'\tOn sale with a {deal["discount"]}% discount\n\n')


def print_deal(deal):
    print(f'[ ] New deal\n'
        + f'\t{deal["name"]} by {deal["developer"]} ({deal["type"]})\n'
        + f'\tOn sale with a {deal["discount"]}% discount\n\n')


def on_message(client, userdata, msg):
    topics = msg.topic.split('/')

    deal = json.loads(msg.payload)
    deal['developer'] = topics[3]
    deal['type'] = topics[2]

    print_deal(deal) if deal['discount'] < 50 else print_hot_deal(deal)


parser = argparse.ArgumentParser(
    description='Subscribe to videogame deal notifications.')

parser.add_argument(
    '-d', '--developer',
    nargs='+',
    default=['+'],  # all developers
    help='Specify developer(s) of interest.',
    required=False)

parser.add_argument(
    '-t', '--type',
    nargs='+',
    default=['+'],  # all types of videogames
    help='Specify type(s) of videogames of interest.',
    required=False)

args = parser.parse_args()

subscriber = mqtt.Client()
subscriber.on_message = on_message
subscriber.connect('localhost')

for vg_type in args.type:
    for vg_developer in args.developer:
        subscriber.subscribe(
            # .lower() to avoid case-sensitivity (ex. RPG == rpg)
            f'videogames/deals/{vg_type.lower()}/{vg_developer.lower()}'
        )

print('Waiting for deals...')

try:
    subscriber.loop_forever()
except KeyboardInterrupt:
    print('EXIT')
