class DeviceSensor(object):
    name = None
    type = None

    def __unicode__(self):
        return 'name:%s, type:%s' % (self.name, self.type)
