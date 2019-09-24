from .controllers import (
    echo_controller,
    get_messages_controller,
    update_messages_controller,
    delete_message_controller
)

action_names = [
    {'action': 'echo', 'controller': echo_controller},
    {'action': 'read', 'controller': get_messages_controller},
    {'action': 'update', 'controller': update_messages_controller},
    {'action': 'delete', 'controller': delete_message_controller},
]
