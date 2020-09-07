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
        t = 0
        flush = 3
        while True:
            for d in data:
                time.sleep(flush)
                payload = self.sensor.get_data(value=d)
                topic = self.sensor.get_topic()
                self.mqtt_client.send_data(topic=topic, data=payload)
                t += flush
                if t > 60:
                    # 定时发送 设备在线状态 并且重新建立连接
                    self.mqtt_client.send_data(topic=self.sensor.status_topic(), data='online')
                    self.mqtt_client.flush_client()
                    t = 0

