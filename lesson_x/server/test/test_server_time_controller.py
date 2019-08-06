from datetime import datetime

from server_time.controllers import server_time_controller

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


def test_server_time_controller():
    response = server_time_controller(REQUEST)
    RESPONSE.update({'data': response.get('data')})
    assert response == RESPONSE
