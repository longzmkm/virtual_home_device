# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)
import logging
import socket

import paho.mqtt.client as mqtt
import json
import random
import string

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger(__name__)


class MqttClient(object):

    def __init__(self, port):
        self.host = 'localhost'
        self.port = port

        self._client = mqtt.Client(client_id=self.generate_number())
        self._client.connect(host='localhost', port=self.port, keepalive=60)

    def generate_number(self):
        return ''.join(random.sample(string.ascii_letters + string.digits, 16))

    def send_data(self, topic, data):
        logger.info('Send Mqtt host:%s,Port:%s, topic:%s ,payload:%s' % (self.host, self.port, topic, data))
        self._client.publish(topic=topic, payload=json.dumps(data), qos=1)

    def get_host_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()

        return ip
