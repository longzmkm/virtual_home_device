import random
from threading import Thread
import json

def async_call(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()

    return wrapper


class DeviceSensor(object):
    name = None
    type = None
    fluctuation_level = 0.05
    status = 'off'

    def __init__(self, name, sensor_nu, unit, key):
        self.sensor_name = name
        self.sensor_nu = sensor_nu
        self.unit = unit
        self.key = key

    def __str__(self):
        return 'name:%s, type:%s' % (self.name, self.type)

    def get_topic(self):
        return 'zigebee2mqtt/%s' % self.sensor_nu

    def online_topic(self):
        return 'zigebee2mqtt/%s/online' % self.sensor_nu

    def status_topic(self):
        return 'zigebee2mqtt/%s/status' % self.sensor_nu

    def set_topic(self):
        return 'zigebee2mqtt/%s/set' % self.sensor_nu

    @async_call
    def get_paylod_set_status(self, client, userdata, message):
        payload = message.payload.decode('utf-8')
        if payload in ['on', 'off']:
            self.status = payload
            userdata.send_data(topic=self.status_topic(), data=self.status)
        return True

    def get_data(self, value):
        # 统一规定所有获取数据的方式都是使用
        value = self.fluctuation(value=value)
        data = {
            self.key: value
        }
        return data

    def fluctuation(self, value):
        return round(random.uniform(value * (1 - self.fluctuation_level), value * (1 + self.fluctuation_level)), 2)
