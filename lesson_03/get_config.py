import yaml

data = {
    'host': 'localhost',
    'port': 80,
    'buffersize': 512
}

with open('config.yaml', 'w') as file:
    yaml.dump(data, file, Dumper=yaml.Dumper)
