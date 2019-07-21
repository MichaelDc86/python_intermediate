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
sock.connect(
    (default_config.get('host'), default_config.get('port'),)
)

print(f'Client was started')

data = input('Enter data:  ')

sock.send(data.encode())
print(f'Client sent data: {data}')
b_response = sock.recv(1024)
print(b_response.decode())
