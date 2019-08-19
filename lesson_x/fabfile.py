from fabric.api import local


def server():
    local('python server')


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
