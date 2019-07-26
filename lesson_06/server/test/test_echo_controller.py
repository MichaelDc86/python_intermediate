from echo.controllers import echo_controller
from datetime import datetime

TIME = datetime.now().timestamp()

CODE = 200

REQUEST = {
    'action': 'test',
    'time': TIME,
    'data': 'message'
}

RESPONSE = {
    'action': 'test',
    'time': TIME,
    'data': 'message',
    'code': CODE
}


def test_echo_controller():
    assert echo_controller(REQUEST) == RESPONSE
