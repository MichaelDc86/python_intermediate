"""CRUD functionality for echo-controller"""
from functools import reduce
from protocol import make_response
from database import Session

from decorators import log, token_required
from .models import Message


@token_required
@log
def echo_controller(request):
    """
    Function for writing down to DB users message and gives back a response
    :param request: raw request from client
    :return: prepared response
    """
    data = request.get('data')
    session = Session()
    message = Message(content=data, user_id=1)
    session.add(message)
    session.commit()

    return make_response(request, 200, data)


@token_required
@log
def get_messages_controller(request):
    """
    Function to make response with all users messages from DB
    :param request: request
    :return: prepared response
    """
    messages = get_all_messages()

    return make_response(request, 200, messages)


@token_required
@log
def update_messages_controller(request):
    """
    Function that updates requested message with requested data
    :param request: request
    :return: response with list of all messages
    """
    session = Session()
    message = get_item(request, session)

    # message.content += '/updated/'
    message.content = request['data']
    session.add(message)
    session.commit()

    messages = get_all_messages()

    return make_response(request, 200, messages)


@token_required
@log
def delete_message_controller(request):
    """
    Function that deletes requested message
    :param request: request
    :return: response with id of deleted message
    """
    session = Session()
    message = get_item(request, session)
    session.delete(message)
    session.commit()
    messages = get_all_messages()
    id_deleted = request['id_req']
    messages.append({'deleted': f'message with id {id_deleted} was deleted!'})

    return make_response(request, 200, messages)


def get_item(request, session):
    """
    Function that returns message from DB filtered by its id getting from request
    :param request: request
    :param session: sqlalchemy session
    :return: message with requested id if exists else 400 response
    """

    try:
        message = session.query(Message).filter(Message.id == int(request['id_req'])).first()
    except ValueError:
        response = 'Input id of message to update(must be digit)'
        return make_response(request, 400, response)
    return message


def get_all_messages():
    """
    Function to get all messages fron DB
    :return: non-filtered list of all messages in DB
    """
    session = Session()

    messages = reduce(
        lambda value, item: value + [{'content': item.content, 'created': item.created.strftime("%Y-%m-%d-%H.%M.%S")}],
        session.query(Message).all(),
        []
    )

    return messages
