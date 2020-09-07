import random


class DeviceSensor(object):
    name = None
    type = None
    fluctuation_level = 0.05

    def __init__(self, name, sensor_nu, unit, key):
        self.sensor_name = name
        self.sensor_nu = sensor_nu
        self.unit = unit
        self.key = key

    def __str__(self):
        return 'name:%s, type:%s' % (self.name, self.type)

    def get_topic(self):
        return 'zigebee2mqtt/%s' % self.sensor_nu

    def status_topic(self):
        return 'zigebee2mqtt/%s/status' % self.sensor_nu

    def get_data(self, value):
        # 统一规定所有获取数据的方式都是使用
        value = self.fluctuation(value=value)
        data = {
            self.key: value
        }
        return data

    def fluctuation(self, value):
        return round(random.uniform(value * (1 - self.fluctuation_level), value * (1 + self.fluctuation_level)), 2)
