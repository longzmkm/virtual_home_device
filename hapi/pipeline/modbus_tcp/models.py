# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)

import modbus_tk.modbus_tcp as modbus_tcp
import modbus_tk.defines as cst
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger(__name__)


class ModbusToTcp(object):

    def __init__(self, slave, port):
        self.host = '192.168.207.110'
        self.slave = slave
        self.port = port
        self.server = None

    def create_client(self, block_name):
        client = modbus_tcp.TcpServer(address=self.host, port=self.port)
        client.start()
        server = client.add_slave(self.slave)
        logger.info('create block_name: %s ,slave: %s ' % (block_name, self.slave))
        # server.add_block(block_name, cst.HOLDING_REGISTERS, self.register, 4)
        self.server = server
        return self

    def send_data(self, slave, block_name, register, data, max_register):
        if block_name not in self.server._blocks.keys():
            logger.debug('Modbus send data -> block_name: %s ,register:%s, max_register:%s' % (block_name, register, max_register))
            self.server.add_block(str(block_name), cst.HOLDING_REGISTERS, register, max_register)
        if data:
            logger.debug('Modbus send data -> block_name: %s ,register:%s, data:%s' % (block_name, register, data))
            self.server.set_values(str(block_name), register, data)
