class DeviceSensor(object):
    name = None
    type = None
    serialNum = None

    def __unicode__(self):
        return 'name:%s, type:%s' % (self.name, self.type)
