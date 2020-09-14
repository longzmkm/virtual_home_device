# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)
import asyncio

from discovery import auto_discover
import logging
from pipeline.modbus_tcp.models import ModbusToTcp
from settings.models import CheckOutSetting
import os

from work_flow.xiaomi_sensor.model import MqttXiaoMiSensor, ModbusXiaoMiSensor

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    YAML_FILE = 'settings/foo.yaml'
    file_name_path = os.path.split(os.path.realpath(__file__))[0]
    path = os.path.join(file_name_path, YAML_FILE)

    obj = CheckOutSetting(path=path)
    sensors = obj.run()

    modbus_clinet = {}

    for dev in sensors.get('mqtt_sensor'):
        task = MqttXiaoMiSensor(name=dev.get('name'), port=dev.get('mqtt_settings').get('broker_port'),
                                sensor_nu=dev.get('sensor_nu'), unit=dev.get('unit'), key=dev.get('key'),
                                kwargs=dev)
        task.run()

    modbus = sensors.get('modbus_sensor')

    for slave, modbus_sensors in modbus.get('sensors').items():
        # 不同的线圈 要重新创建
        block_name = '%s' % slave
        client = modbus_clinet.get(block_name, None)
        iterval = modbus.get('settings').get('iterval', None)
        if not client:
            server = ModbusToTcp(slave=slave, host=modbus.get('settings').get('host'), port=modbus.get('settings').get('port'))
            client = server.create_client(block_name=block_name)
            modbus_clinet.update({block_name: client})
        task = ModbusXiaoMiSensor(modbus_client=client, slave=slave, registers=modbus_sensors, iterval=iterval)
        task.run()
    # 1.检测yaml 文件
    # 2.检测数据源正确性
    # 3.初始化各种连接方式
    # 4.初始化设备
    # 5.读取数据
