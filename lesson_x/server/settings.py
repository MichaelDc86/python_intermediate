import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INSTALLED_MODULES = (
    'auth',
    'echo',
    'messenger',
    'server_time',
    'servererror',
)

CONNECTION_STRING = 'sqlite:///data.db'
