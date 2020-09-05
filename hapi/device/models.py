class DeviceSensor(object):
    name = None
    type = None

    def __unicode__(self):
        return 'name:%s, type:%s' % (self.name, self.type)

    def get_data(self):
        # 统一规定所有获取数据的方式都是使用
        raise NotImplementedError
