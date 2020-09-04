# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)


class CheckOutSetting(object):

    def __init__(self, path):
        self.path = path

    def mqtt_check(self):
        pass

    def modbus_check(self):
        pass

    def sensor_check(self):
        pass

    def data_file_check(self):
        pass

    def run(self):
        try:
            pass
        except Exception as e:
            print('xxx')
