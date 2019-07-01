import yaml
from socket import socket
from argparse import ArgumentParser

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

print(f'Server was started on {host}:{port}')

while True:
    client, address = sock.accept()
    print(f'Client was connected with {address[0]}:{address[1]}')
    b_request = client.recv(1024)
    print(f'Client sent massage: {b_request.decode()}')
    client.send(b_request)
    client.close()
