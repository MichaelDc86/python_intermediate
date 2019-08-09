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


def read(sock_, connections_, requests_, buffersize):
    try:
        bytes_request = r_client.recv(buffersize)
    except (ConnectionResetError,):
        # except Exception:
        try:
            connections_.remove(sock_)
        except ValueError:
            pass
    else:
        if bytes_request:
            requests_.append(bytes_request)


def write(sock_, connections_, response_):
    try:
        sock_.send(response_)
    except Exception:
        connections_.remove(sock_)


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

    connections = []
    requests = []

    while True:
        try:
            client, address = sock.accept()
            connections.append(client)
            logger.info(f'Client was connected with {address[0]}:{address[1]} | Connections: {connections}')
        except BlockingIOError:
            pass

        if connections:
            rlist, wlist, xlist = select.select(
                connections, connections, connections, 0
            )
            for r_client in rlist:
                r_thread = threading.Thread(
                    target=read, args=(
                        r_client,
                        connections,
                        requests,
                        default_config.get('buffersize')
                    )
                )
                r_thread.start()

            if requests:
                b_request = requests.pop()
                b_response = handle_default_request(b_request, logger)

                for w_client in wlist:
                    w_thread = threading.Thread(
                        target=write, args=(
                            w_client,
                            connections,
                            b_response,
                        )
                    )
                    w_thread.start()

except KeyboardInterrupt:
    logger.info('Server shutdown')
