import yaml
import zlib
from socket import socket
from argparse import ArgumentParser
import json
from datetime import datetime
import hashlib
import threading

from Cryptodome.Cipher import AES
from Crypto import Random

from log.client_log_config import get_logger


def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')


class TypedProperty:

    def __init__(self, name):
        self.name = name
        self.args = None

    default_config = {
        'host': 'localhost',
        'port': 8000,
        'buffersize': 1024
    }

    def __get__(self, instance, cls):
        parser = ArgumentParser()

        parser.add_argument(
            '-c', '--config', type=str, required=False, help='Sets config file path'
        )
        self.args = parser.parse_args()
        if self.args.config:
            with open(self.args.config) as file:
                config_ = yaml.load(file, Loader=yaml.Loader)
                self.default_config.update(config_)

        return self.default_config.get(self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        raise AttributeError("Невозможно удалить атрибут")


class ConfigClient:

    host = TypedProperty('host')
    port = TypedProperty('port')
    buffersize = TypedProperty('buffersize')

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

    def __enter__(self):
        if not self.sock:
            self.sock = socket()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        message = 'Client shut down.'
        if exc_type:
            if exc_type is not KeyboardInterrupt:
                message = f'Client stopped with error {exc_type} {exc_val}!'
        self.logger.info(message)
        self.sock.close()
        return True

    def socket_bind(self):
        self.sock = socket()
        self.sock.connect(
            (self.host, self.port,)
        )
        self.logger.info(f'Client was started')

    def read(self, sock_, buffersize_):
        while True:
            try:
                compressed_response = sock_.recv(buffersize_)
                b_response = zlib.decompress(compressed_response)
                encrypted_request = json.loads(b_response)

                """decryption"""
                """create cipher"""

                key_raw = encrypted_request.get('key')
                key = int_to_bytes(key_raw)
                encode_list = encrypted_request.get('encode_list')
                encode_list = list(map(lambda x: int_to_bytes(x), encode_list))
                nonce, tag, ciphertext = [x for x in encode_list]

                cipher = AES.new(key, AES.MODE_EAX, nonce)

                """decryption part"""

                decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
                decrypted_response = encrypted_request.copy()
                decrypted_response['data'] = decrypted_data.decode()
                self.logger.info(f'RESPONSE: {decrypted_response}')
            except ConnectionAbortedError:
                client.logger.info(f'Client broke the connection.')
                break

    def write(self, sock_):
        hash_obj = hashlib.sha256()
        hash_obj.update(
            str(datetime.now().timestamp()).encode()
        )

        action = input('Specify action: ')
        id_req = None
        data = None
        if 'update' in action:
            id_req = input('Specify id of message to update: ')
            data = input('Enter data to update message:  ')
        elif 'delete' in action:
            id_req = input('Specify id of message to delete: ')
        else:
            data = input('Enter data:  ')

        """encryption"""
        """create cipher"""

        key_bytes = 16
        key = Random.get_random_bytes(key_bytes)
        key_int = int_from_bytes(key)
        cipher = AES.new(key, AES.MODE_EAX)

        """encoding part"""
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())
        encode_list = [x for x in (cipher.nonce, tag, ciphertext)]
        encode_list = list(map(lambda x: int_from_bytes(x), encode_list))

        request = {
            'encode_list': encode_list,
            'key': key_int,
            'id_req': id_req,
            # 'data': encrypted_data,
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


"""left this commented lines for myself(another solution)"""

# client = Client()
# client.socket_bind()
#
# try:
#     client.read_write()
#
# except KeyboardInterrupt:
#     client.sock.close()
#     client.logger.info(f'Client shutdown.')

"""solution with context manager(added __enter__ and __exit__ to Client)"""

with Client() as client:
    client.socket_bind()
    client.read_write()
