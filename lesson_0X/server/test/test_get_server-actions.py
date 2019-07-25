from echo.controllers import echo_controller
# from messenger.controllers import messenger_controller
from server_time.controllers import server_time_controller
from servererror.controllers import servererror_controller

import resolvers


SERVER_ACTIONS = {
    'echo': echo_controller,
    'empty': 'messenger_controller',
    'server_time': server_time_controller,
    'servererror': servererror_controller,
}


def test_get_server_actions():
    assert resolvers.get_server_actions() == SERVER_ACTIONS
