# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)
import asyncio
import time

from data.models import CsvData
from device.xiaomi.models import DeviceXiaoMiSensor
from pipeline.mqtt.model import MqttClient
from threading import Thread
import paho.mqtt.subscribe as subscribe

from pipeline.modbus_tcp.models import ModbusToTcp


def async_call(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()

    return wrapper


class MqttXiaoMiSensor(object):
    iterval = 5

    def __init__(self, name, host, port, sensor_nu, unit, key, **kwargs):
        self.port = port
        self.sensor = DeviceXiaoMiSensor(name=name, sensor_nu=sensor_nu, unit=unit, key=key)
        self.mqtt_client = MqttClient(host=host, port=port)
        self.source_data = CsvData(kwargs=kwargs.get('kwargs'))
        iterval = kwargs.get('kwargs').get('mqtt_settings', {}).get('iterval', False)
        # 如果没有给默认的刷新时间  就直接给5秒
        self.iterval = iterval if iterval else 5

    @async_call
    def run(self):
        data = self.source_data.get_data()
        self.set_status()
        t = 0
        self.mqtt_client.send_data(topic=self.sensor.status_topic(), data=self.sensor.status)
        while True:
            for d in data:
                time.sleep(self.iterval)
                payload = self.sensor.get_data(value=d)
                topic = self.sensor.get_topic()
                self.mqtt_client.send_data(topic=topic, data=payload)
                t += self.iterval
                if t > 60:
                    # 定时发送 设备在线状态 并且重新建立连接
                    self.mqtt_client.send_data(topic=self.sensor.status_topic(), data=self.sensor.status)
                    self.mqtt_client.flush_client()
                    t = 0

    @async_call
    def set_status(self):
        subscribe.callback(self.sensor.get_paylod_set_status, self.sensor.set_topic(),
                           hostname=self.mqtt_client.host, port=self.port,
                           userdata=self.mqtt_client,
                           client_id=self.mqtt_client.generate_number(),
                           keepalive=60)


class ModbusXiaoMiSensor(object):
    iterval = 5

    def __init__(self, modbus_client, slave, registers, iterval):
        self.modbus_client = modbus_client
        self.slave = slave
        self.registers = registers
        # self.source_data = CsvData(kwargs=kwargs.get('kwargs'))
        # iterval = kwargs.get('kwargs').get('modbus_settings', {}).get('iterval', False)
        # 如果没有给默认的刷新时间  就直接给5秒
        self.iterval = iterval if iterval else 5
        self.max_len = 0
        self.data = None
        self.register_list = [x.get("register") for x in registers]
        self.max_register = max(self.register_list)

    def get_data(self):
        temp = {}
        # 获取所有的数据
        for register in self.registers:
            data = CsvData(kwargs=register)
            temp.update({register.get('register'): list(data.data)})

        # 获取最大的长度
        for v in temp.values():
            if self.max_len <= len(v):
                self.max_len = len(v)

        # 数据补全
        result = {}
        for k, v in temp.items():
            v += [None for i in range(self.max_len - len(v))]
            result.update({k: v})

        self.data = result
        return result

    @async_call
    def run(self):
        t = 1
        self.get_data()
        while t < self.max_len:
            time.sleep(self.iterval)
            for register in self.register_list:
                block_name = '%s' % self.slave
                self.modbus_client.send_data(slave=self.slave, block_name=block_name, register=register,
                                             data=self.data.get(register)[t], max_register=self.max_register)

            t += 1
            if t > self.max_len:
                t = 0
