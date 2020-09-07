# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)
import asyncio
import time

from data.models import CsvData
from hapi.device.xiaomi.models import DeviceXiaoMiSensor
from hapi.pipeline.mqtt.model import MqttClient
from threading import Thread


def async_call(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()

    return wrapper


class MqttXiaoMiSensor(object):

    def __init__(self, name, port, sensor_nu, unit, key, **kwargs):
        self.sensor = DeviceXiaoMiSensor(name=name, sensor_nu=sensor_nu, unit=unit, key=key)
        self.mqtt_client = MqttClient(port=port)
        self.source_data = CsvData(kwargs=kwargs.get('kwargs'))

    @async_call
    def run(self):
        data = self.source_data.get_data()
        for data in data[self.source_data.data_source_col]:
            time.sleep(1)
            data = self.sensor.get_data(value=data)
            topic = self.sensor.get_topic()
            self.mqtt_client.send_data(topic=topic, data=data)