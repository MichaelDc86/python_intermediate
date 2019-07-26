from protocol import validate_request
from datetime import datetime

TIME = datetime.now().timestamp()

CODE = 200

REQUEST = {
    'action': 'test',
    'time': TIME,
    'data': 'message'
}


BAD_REQUEST = {
    'time': TIME,
    'data': 'message'
}


def test_validate_request():
    assert validate_request(REQUEST)
    assert not validate_request(BAD_REQUEST)
