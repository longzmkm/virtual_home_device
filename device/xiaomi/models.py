# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)
from device.models import DeviceSensor


class DeviceXiaoMiSensor(DeviceSensor):
    name = 'xiaomi'
    type = None

    def get_data(self):
        # 统一规定所有获取数据的方式都是使用
        raise NotImplementedError


def guang_zhao_sensor(DeviceXiaoMiSensor):
    type = 'guangzhao'
    def get_data(self):
        pass
