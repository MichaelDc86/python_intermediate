import yaml
import select
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

try:
    sock = socket()
    sock.bind(
        (default_config.get('host'), default_config.get('port'),)
    )
    # sock.setblocking(False)  # for nix
    sock.settimeout(0)  # for windows
    sock.listen(5)

    host = default_config.get('host')
    port = default_config.get('port')

    logger.info(f'Server was started on {host}:{port}')

    # data = input('Stop server?: y/n ')
    # if data == 'y':
    #     sock.close()
    #     logger.info('Server shutdown')

    connections = []
    requests = []
    disconnect_client = None

    while True:
        try:
            client, address = sock.accept()
            print(client)
            connections.append(client)
            logger.info(f'Client was connected with {address[0]}:{address[1]} | Connections: {connections}')
        except BlockingIOError:
            pass

        if disconnect_client:
            print('------------------------------------------------')
            print(f'disconnect_client {disconnect_client}')
            print('------------------------------------------------')
            print(f'Connections BEFORE DELETE {connections}')
            print('------------------------------------------------')
            print(f'LENGHT OF CONNECTIONS BEFORE {len(connections)}')
            print('------------------------------------------------')
            connections.remove(disconnect_client)
            print(f'Connections After DELETE {connections}')
            print(f'LENGHT OF CONNECTIONS AFTER {len(connections)}')
            print('------------------------------------------------')
            disconnect_client = None

        if connections:
            rlist, wlist, xlist = select.select(
                connections, connections, connections, 0
            )
            # print(connections)
            for r_client in rlist:
                print(rlist)
                print(wlist)
                # print(xlist)
                try:
                    b_request = r_client.recv(default_config.get('buffersize'))
                    requests.append(b_request)
                except (ConnectionAbortedError, ConnectionResetError) as err:
                    disconnect_client = r_client

            if requests:

                print(requests)
                b_request = requests.pop()
                b_response = handle_default_request(b_request, logger)

                for w_client in wlist:
                    w_client.send(b_response)

            # data = input('Stop server?: y/n ')
            # if data == 'y':
            #     logger.info('Server shutdown')
            #     break
except KeyboardInterrupt:
    logger.info('Server shutdown')
