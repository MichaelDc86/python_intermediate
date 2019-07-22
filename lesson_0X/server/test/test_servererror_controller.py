from servererror.controllers import servererror_controller
from datetime import datetime

TIME = datetime.now().timestamp()

REQUEST = {
    'action': 'test',
    'time': TIME,
    'data': 'message'
}


# def test_servererror_controller():
    # try:
    #     servererror_controller(REQUEST)
    # except Exception('Server Error'):
    #     return True
    # assert servererror_controller(REQUEST) == raise Exception('Server Error')
