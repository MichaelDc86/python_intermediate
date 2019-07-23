import yaml
from socket import socket
from argparse import ArgumentParser
import json
from datetime import datetime

import sys
import os
sys.path.append(os.getcwd() + '\\log')
from client_log_config import create_logger

logger = create_logger()

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

sock = socket()
sock.connect(
    (default_config.get('host'), default_config.get('port'),)
)

logger.info(f'Client was started')
# print(f'Client was started')

action = input('Specify action: ')
data = input('Enter data:  ')

request = {
    'data': data,
    'time': datetime.now().timestamp(),
    'action': action,
}

s_request = json.dumps(request)

sock.send(s_request.encode())
logger.debug(f'Client sent data: {data}')
# print(f'Client sent data: {data}')
b_response = sock.recv(1024)
logger.info(f'RESPONSE: {b_response.decode()}')
# print(b_response.decode())
