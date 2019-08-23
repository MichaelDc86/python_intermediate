from fabric.api import local


def server():
    local('python server')  # command with config: py server -c config.yaml


def server_conf(file):
    local(f'python server -c {file}')  # command: fab server_conf:file=name_of_file.yaml


def migrate():
    local('python server -m')


# def client(mode):
def client():
    local(f'python client')
    # local(f'python client --mode {mode}')


def test():
    local('pytest --cov-report term-missing --cov server')
    # local('pytest --cov-report term-missing --cov client')


def notebook():
    local('jupyter notebook')


def kill():
    local('lsof -t -i tcp:8000 | xargs kill -V')
