import yaml
import select
import threading
from socket import socket
from argparse import ArgumentParser
from handlers import handle_default_request

import sys
import os

try:
    sys.path.append(os.getcwd() + '\\log')
    from serever_log_config import get_logger
except ModuleNotFoundError:
    sys.path.append(os.getcwd() + '/log')
    from serever_log_config import get_logger


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


class ConfigServer:

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


class Server:
    connections = []
    requests = []

    def __init__(self):
        self.host = ConfigServer().host
        self.port = ConfigServer().port
        self.buffersize = ConfigServer().buffersize
        self.logger = ConfigServer().get_logger_()
        self.sock = None

    def socket_bind(self):
        self.sock = socket()
        self.sock.bind(
            (self.host, self.port,)
        )
        if sys.platform == 'linux':
            self.sock.setblocking(False)  # for nix
        elif sys.platform == 'win32':
            self.sock.settimeout(0)  # for windows
        self.sock.listen(5)

        self.logger.info(f'Server was started on {self.host}:{self.port}')

    def accept(self):
        client, address = self.sock.accept()
        self.connections.append(client)
        self.logger.info(f'Client was connected with {address[0]}:{address[1]} | Connections: {self.connections}')

    def read(self, sock_, connections_, requests_, buffersize):
        try:
            bytes_request = sock_.recv(buffersize)
        except (ConnectionAbortedError, ConnectionResetError):
            try:
                connections_.remove(sock_)
            except ValueError:
                pass
        else:
            if bytes_request:
                requests_.append(bytes_request)

    def write(self, sock_, connections_, response_):
        try:
            sock_.send(response_)
        except Exception:
            connections_.remove(sock_)

    def read_write(self):
        if self.connections:
            rlist, wlist, xlist = select.select(
                self.connections, self.connections, self.connections, 0
            )
            for r_client in rlist:
                r_thread = threading.Thread(
                    target=self.read, args=(
                        r_client,
                        self.connections,
                        self.requests,
                        self.buffersize
                    )
                )
                r_thread.start()

            if self.requests:
                b_request = self.requests.pop()
                b_response = handle_default_request(b_request, self.logger)

                for w_client in wlist:
                    w_thread = threading.Thread(
                        target=self.write, args=(
                            w_client,
                            self.connections,
                            b_response,
                        )
                    )
                    w_thread.start()


try:

    server = Server()
    server.socket_bind()

    while True:
        try:
            server.accept()
        except BlockingIOError:
            pass

        server.read_write()

except KeyboardInterrupt:
    server.logger.info('Server shutdown')
