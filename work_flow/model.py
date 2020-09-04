# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)
from device.models import XiaoMiSensor
from pipeline.mqtt.model import MqttClient


class MqttXiaoMiSensor(object):

    def __init__(self, name, host, port):
        self.sensor = XiaoMiSensor(name=name, )
        self.mqtt_client = MqttClient(host=host, port=port)

    def run(self):
        data = self.sensor.get_data()
        self.mqtt_client.send_data(data=data)
