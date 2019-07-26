import json
import yaml
from socket import socket
from argparse import ArgumentParser
from protocol import validate_request, make_response
from resolvers import resolve

import sys
import os
sys.path.append(os.getcwd() + '\\log')
from serever_log_config import create_logger

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
sock.bind(
    (default_config.get('host'), default_config.get('port'),)
)
sock.listen(5)

host = default_config.get('host')
port = default_config.get('port')

logger.info(f'Server was started on {host}:{port}')
# print(f'Server was started on {host}:{port}')

data = input('Stop server?: y/n ')
if data == 'y':
    sock.close()

while True:
    client, address = sock.accept()
    logger.info(f'Client was connected with {address[0]}:{address[1]}')
    # print(f'Client was connected with {address[0]}:{address[1]}')

    b_request = client.recv(default_config.get('buffersize'))
    request = json.loads(b_request.decode())

    if validate_request(request):
        action_name = request.get('action')
        controller = resolve(action_name)
        # -----------------------------------------------
        if controller:

            try:
                logger.debug(f'Controller {controller} resolved with request: {request}')
                # print(f'Controller {controller} resolved with request: {request}')
                # response = make_response(request, 200, request.get('data'))
                response = controller(request)

            except Exception as err:
                logger.critical(f'Controller {controller} error: {err}')
                # print(f'Controller {controller} error: {err}')
                response = make_response(request, 500, 'Internal Server  Error!')
        # ------------------------------------------------
        else:
            logger.error(f'Controller {controller} not found!')
            # print(f'Controller {controller} not found!')
            response = make_response(request, 404, f'Action with name {action} is not supported!')

    else:
        logger.error(f'Wrong request!')
        # print(f'Wrong request!')
        response = make_response(request, 400, 'Wrong request format!')

    client.send(json.dumps(response).encode())
    client.close()

    data = input('Stop server?: y/n ')
    if data == 'y':
        break
