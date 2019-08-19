import yaml
import zlib
from socket import socket
from argparse import ArgumentParser
import json
from datetime import datetime
import hashlib
import threading
import time

import sys
import os

try:
    sys.path.append(os.getcwd() + '\\log')
    from client_log_config import get_logger
except ModuleNotFoundError:
    sys.path.append(os.getcwd() + '/log')
    from client_log_config import get_logger


def read(sock_, buffersize_):
    while True:
        compressed_response = sock_.recv(buffersize_)
        b_response = zlib.decompress(compressed_response)
        logger.info(f'RESPONSE: {b_response.decode()}')


logger = get_logger()

parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str, required=False, help='Sets config file path'
)

args = parser.parse_args()

default_config = {
    'host': 'localhost',
    'port': 8000,
    'buffersize': 1024
}

if args.config:
    with open(args.config) as file:
        config = yaml.load(file, Loader=yaml.Loader)
        default_config.update(config)


def write(sock_):
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
    logger.debug(f'Client sent data: {data}')


sock = socket()
sock.connect(
    (default_config.get('host'), default_config.get('port'),)
)
logger.info(f'Client was started')

try:
    read_thread = threading.Thread(
        target=read,
        args=(
            sock,
            default_config.get('buffersize')
        )
    )
    read_thread.start()
    while True:
        # time.sleep(1)
        write(sock)


except KeyboardInterrupt:
    sock.close()
    print(f'Client shutdown.')
