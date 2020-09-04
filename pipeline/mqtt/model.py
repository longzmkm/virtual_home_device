# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)
import json
import random
import string

import paho.mqtt.client as mqtt


class Client(object):
    name = None


class MqttClient(Client):
    name = 'mqtt'

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def generate_number(self):
        return ''.join(random.sample(string.ascii_letters + string.digits, 16))

    def __enter__(self):
        self.client = mqtt.Client(client_id=self.generate_number())
        self.client.connect(host=self.host, port=self.port, keepalive=60)
        return self

    def send_data(self, topic, data):
        self.client.publish(topic=topic, payload=data)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(exc_type)


if __name__ == '__main__':
    with MqttClient(host=1111, port=1883) as s:
        s.send_data()
        raise Exception
