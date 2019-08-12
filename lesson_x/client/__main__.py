import yaml
import zlib
from socket import socket
from argparse import ArgumentParser
import json
from datetime import datetime
import hashlib
import threading

import sys
import os

try:
    sys.path.append(os.getcwd() + '\\log')
    from client_log_config import get_logger
except ModuleNotFoundError:
    sys.path.append(os.getcwd() + '/log')
    from client_log_config import get_logger


class TypedProperty:

    default_config = {
        'host': 'localhost',
        'port': 8000,
        'buffersize': 1024
    }

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        return self.default_config.get(self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        raise AttributeError("Невозможно удалить атрибут")


class ConfigClient:

    host = TypedProperty('host')
    port = TypedProperty('port')
    buffersize = TypedProperty('buffersize')

    def __init__(self):
        self.args = None

    default_config = {
        'host': 'localhost',
        'port': 8000,
        'buffersize': 1024
    }

    def update_default_config(self):
        parser = ArgumentParser()

        parser.add_argument(
            '-c', '--config', type=str, required=False, help='Sets config file path'
        )
        self.args = parser.parse_args()
        if self.args.config:
            with open(self.args.config) as file:
                config_ = yaml.load(file, Loader=yaml.Loader)
                self.default_config.update(config_)

    @classmethod
    def get_logger_(cls):
        logger_ = get_logger()
        return logger_


class Client:

    def __init__(self):
        self.host = ConfigClient().host
        self.port = ConfigClient().port
        self.buffersize = ConfigClient().buffersize
        self.logger = ConfigClient().get_logger_()
        self.sock = None

    def socket_bind(self):
        self.sock = socket()
        self.sock.connect(
            (self.host, self.port,)
        )
        self.logger.info(f'Client was started')

    def read(self, sock_, buffersize_):
        while True:
            compressed_response = sock_.recv(buffersize_)
            b_response = zlib.decompress(compressed_response)
            self.logger.info(f'RESPONSE: {b_response.decode()}')

    def write(self, sock_):
        hash_obj = hashlib.sha256()
        hash_obj.update(
            str(datetime.now().timestamp()).encode()
        )

        action = input('Specify action: ')
        data = input('Enter data:  ')

        request = {
            'data': data,
            'time': datetime.now().timestamp(),
            'action': action,
            'token': hash_obj.hexdigest(),
        }

        s_request = json.dumps(request)
        request_compressed = zlib.compress(s_request.encode())
        sock_.send(request_compressed)
        self.logger.debug(f'Client sent data: {data}')

    def read_write(self):
        read_thread = threading.Thread(
            target=self.read,
            args=(
                self.sock,
                self.buffersize
            )
        )
        read_thread.start()
        while True:
            self.write(self.sock)


client = Client()
client.socket_bind()

try:
    client.read_write()

except KeyboardInterrupt:
    client.sock.close()
    client.logger.info(f'Client shutdown.')
