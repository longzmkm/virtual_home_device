# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)
from device.xiaomi.models import DeviceXiaoMiSensor
from pipeline.mqtt.model import MqttClient


class WorkFlow(object):
    sensor_type = None
    protocol = None

    def __init__(self, name, host, port):
        self.sensor = DeviceSensor.get(sensor=self.sensor_type)
        self.client = Client.get(self.protocol)

    def run(self):
        data = self.sensor
        self.client.send_data(data=data)


class MqttXiaoMiSensor(WorkFlow):
    sensor_type = 'xiaomi'
    protocol = 'mqtt'
