#!/usr/bin/python3

import json
import time
import paho.mqtt.client as mqtt

from videogames import deals


def build_event(vg_data):
    return {
        "name": vg_data["name"],
        "discount": vg_data["discount"],
    }


publisher = mqtt.Client()
publisher.connect('127.0.0.1')

print('Publishing videogame deals')

for vg_data in deals:
    publisher.publish(
        f'videogames/deals/{vg_data["type"].lower()}/{vg_data["developer"].lower()}',
        json.dumps(build_event(vg_data))
    )

    print('.', end='', flush=True)  # end='' to avoid printing a newline
    time.sleep(1)

publisher.disconnect()
