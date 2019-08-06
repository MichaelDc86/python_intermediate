from echo.controllers import echo_controller
from server_time.controllers import server_time_controller
from servererror.controllers import servererror_controller

import resolvers

SERVER_ACTIONS = {
    'echo': echo_controller,
    'empty': 'messenger_controller',
    'server_time': server_time_controller,
    'servererror': servererror_controller,
}

ACTION_NAME = 'echo'


def test_resolve():
    assert resolvers.resolve(ACTION_NAME, SERVER_ACTIONS) == echo_controller
