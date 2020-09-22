# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)
import random
import string

import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe


def generate_number():
    return ''.join(random.sample(string.ascii_letters + string.digits, 16))


def call_back():
    print('I am call back')


if __name__ == '__main__':
    client = mqtt.Client(client_id=generate_number())
    client.connect(host='localhost', port=1883, keepalive=60)
    payload = {}
    client.publish(topic='topic', payload=payload, qos=1)

    subscribe.callback(call_back, "zigbee2mqtt/zigbeeserver/+/zigbee2mqtt/bridge/log",
                       hostname='localhost', port=1883,
                       client_id=generate_number(),
                       keepalive=60)
