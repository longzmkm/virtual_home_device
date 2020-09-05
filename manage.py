# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)
from discovery import auto_discover
import logging
from settings.model import CheckOutSetting
import os

from work_flow.xiaomi_sensor.model import MqttXiaoMiSensor

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    YAML_FILE = 'settings/foo.yaml'
    file_name_path = os.path.split(os.path.realpath(__file__))[0]
    path = os.path.join(file_name_path, YAML_FILE)

    obj = CheckOutSetting(path=path)
    for x in obj.run():
        logger.info(x)
        MqttXiaoMiSensor()
    # 1.检测yaml 文件
    # 2.检测数据源正确性
    # 3.初始化各种连接方式
    # 4.初始化设备
    # 5.读取数据
