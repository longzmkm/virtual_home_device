# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)
import logging
import subprocess
import os
import yaml

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='ha.log',
                    filemode='w')
_LOGGER = logging.getLogger(__name__)
YAML_FILE = "settings/foo.yaml"


def start_mqtt_broker(port):
    full_start_cmd = "sudo mosquitto -c /etc/mosquitto/mosquitto.conf -v -d -p {}".format(port)
    print(full_start_cmd)
    return subprocess.getstatusoutput(full_start_cmd)


if __name__ == '__main__':
    # 1.检测yaml 文件
    # 2.检测数据源正确性
    # 3.初始化各种连接方式
    # 4.初始化设备
    # 5.读取数据
    file_name_path = os.path.split(os.path.realpath(__file__))[0]
    yamlPath = os.path.join(file_name_path, YAML_FILE)
    f_open = None
    try:
        f_open = open(yamlPath, 'r', encoding='utf-8')
    except IOError as e:
        _LOGGER.error(e)
        exit(1)
    input_data = f_open.read()
    content = yaml.load(input_data, Loader=yaml.FullLoader)

    has_mqtt_device = content['mqtt']
    if has_mqtt_device is not None:
        mqtt_list = []
        broker_port = content['mqtt_setting']['broker_port']
        exe_result = start_mqtt_broker(broker_port)
        obj =WorkFlow.get('xiaomi','mqtt','deviceserial','devicetype')
        obj = obj(name=,)
        _LOGGER.info(("exe_result:", exe_result))
        mqtt_devices = content['mqtt']
        for sensor in mqtt_devices:

            print(sensor['name'])

