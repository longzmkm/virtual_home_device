class DeviceSensor(object):
    name = None
    type = None

    def __init__(self, path, name, sensor_nu, unit, key):
        self.data_file_path = path
        self.sensor_name = name
        self.sensor_nu = sensor_nu
        self.unit = unit
        self.key = key

    def __str__(self):
        return 'name:%s, type:%s' % (self.name, self.type)

    def get_data(self):
        # 统一规定所有获取数据的方式都是使用
        raise NotImplementedError
