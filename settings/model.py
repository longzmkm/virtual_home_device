# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)
import logging
import yaml
import os
import subprocess

from data.models import CsvData

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger(__name__)


class CheckOutSetting(object):
    yaml_info = {}
    data_file = {}

    sensor_info = []
    out_put = []

    mqtt_settings = {}

    def __init__(self, path):
        self.path = path

    def data_source_filename(self):
        file_name_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(file_name_path, 'data_source')
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            self.data_file.update({file: file_path})

    def read_yaml(self):
        self.data_source_filename()
        f = open(self.path, 'r', encoding='utf-8')
        self.yaml_info = yaml.load(f, yaml.FullLoader)

    def check_single_mqtt_sensor(self, data):
        # 单个传感器检测
        # 传感器 必须包含 1.数据源  env 2.传感器编号  numb 3.值的类型 values
        logger.debug('start check sensor  name:%s , numb:%s' % (data.get('name'), data.get('numb')))
        temp = {}
        for k, v in data.items():
            if k == 'env' and v in self.data_file.keys():
                temp.update({'file_name': v})
                temp.update({'file_path': self.data_file.get(v)})
            elif k == 'numb':
                temp.update({'sensor_nu': v})
            elif k == 'name':
                temp.update({'name': v})
            elif k == 'numb_col':
                temp.update({'numb_col': v})

            elif k == 'values':
                if len(v) != 1:
                    logger.info('数据配置错误')
                else:
                    temp.update({'data_source_col': v[0].get('data_source_col')})
                    temp.update({'key': v[0].get('key')})
                    temp.update({'unit_type_col': v[0].get('unit_type_col')})
                    temp.update({'unit': v[0].get('unit')})
                    temp.update({'datetime_col': v[0].get('datetime_col')})

        temp.update({'mqtt_settings': self.mqtt_settings})

        return temp

    def check_mqtt_setting(self):
        key = {'iterval', 'host', 'broker_port'}
        if set(self.yaml_info.get('mqtt_setting').keys()).issubset(key):
            logger.info('mqtt check success')
            self.mqtt_settings = self.yaml_info.get('mqtt_setting')
        else:
            logger.info('mqtt check fail')

    def mqtt_sensor_check(self):
        self.check_mqtt_setting()
        for sensor in self.yaml_info.get('mqtt', []):
            self.sensor_info.append(self.check_single_mqtt_sensor(sensor))
        self.check_data_file()

    def modbus_check(self):
        logger.info('modbus_check')

    def check_data_file(self):
        for data in self.sensor_info:
            # TODO 这个地方根据选择不同的数据类型， 分别要做出不同的判断
            logger.info(data)
            CsvData.check(kwargs=data)

        logger.info('data_file_check')

    def finish(self):
        # TODO  现在只做了mqtt 的设置检查， 还要补充modbus的数据
        self.out_put = self.sensor_info
        return self.sensor_info

    def run(self):
        try:
            # 读取yaml文件
            self.read_yaml()
            logger.debug('Read yaml file content: %s ' % self.yaml_info)
            checks = [f for f in dir(self) if f.endswith('_check')]
            for check in checks:
                func = getattr(self, check, False)
                func()
            self.finish()
            return self.out_put
        except Exception as e:
            import traceback
            logger.error(traceback.format_exc())
