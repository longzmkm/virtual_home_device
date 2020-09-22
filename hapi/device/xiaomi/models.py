# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)
from device.models import DeviceSensor


class DeviceXiaoMiSensor(DeviceSensor):
    name = 'xiaomi'
    type = None


class IlluminationSensor(DeviceXiaoMiSensor):
    name = 'xiaomi'
    type = 'guangzhao'
