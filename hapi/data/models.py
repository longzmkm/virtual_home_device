# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)
import pandas as pd


class CsvData(object):
    data = None

    def __init__(self, *args, **kwargs):
        self.path = kwargs.get('kwargs', {}).get('file_path')
        self.cols = [kwargs.get('kwargs', {}).get(x) for x in kwargs.get('kwargs', {}).keys() if x.endswith('_col')]
        # 传感器的编号
        self.numb_col = kwargs.get('kwargs', {}).get('numb_col')
        self.sensor_nu = kwargs.get('kwargs', {}).get('sensor_nu')

        # 传感器的单位
        self.unit_type_col = kwargs.get('kwargs', {}).get('unit_type_col')
        self.unit = kwargs.get('kwargs', {}).get('unit')

        self.data_source_col = kwargs.get('kwargs', {}).get('data_source_col')
        self.kwargs = kwargs

        self.read_data()

    def __str__(self):
        return str('(Sensor Name:%s -> %s, unit:%s -> %s) DATA  File Path:%s' % (
            self.sensor_nu,
            self.numb_col,
            self.unit,
            self.unit_type_col,
            self.path))

    def get_header(self):
        d = pd.read_csv(self.path, encoding='utf-8', header=0, nrows=0)
        return [x for x in d.columns]

    @classmethod
    def check(cls, *args, **kwargs):
        path = kwargs.get('kwargs', {}).get('file_path')
        d = pd.read_csv(path, encoding='utf-8', header=0, nrows=0)
        cols = [kwargs.get('kwargs', {}).get(x) for x in kwargs.get('kwargs', {}).keys() if x.endswith('_col')]
        header = [x for x in d.columns]
        if not set(cols).issubset(header):
            raise Exception('输入的行不存在')
        return True

    def read_data(self):
        data = pd.read_csv(self.path, usecols=self.cols, nrows=2000)
        data = data[data[self.numb_col] == self.sensor_nu]
        self.data = data[data[self.unit_type_col] == self.unit]

        return data

    def _get_data_by_rule(self, filter_col=None, filter_rule=None):

        return self.data

    def get_data(self):
        data = self._get_data_by_rule()
        return data


class TxtData(object):
    pass
