from functools import reduce
from protocol import make_response
from database import Session

from decorators import log, token_required
from .models import Message


@token_required
@log
def echo_controller(request):
    data = request.get('data')
    session = Session()
    message = Message(content=data, users_id=1)
    session.add(message)
    session.commit()

    return make_response(request, 200, data)


@token_required
@log
def get_messages_controller(request):
    messages = get_all_messages()

    return make_response(request, 200, messages)


@token_required
@log
def update_messages_controller(request):
    session = Session()
    message = get_item(request, session)

    message.content += '/updated/'
    session.add(message)
    session.commit()

    messages = get_all_messages()

    return make_response(request, 200, messages)


@token_required
@log
def delete_message_controller(request):
    session = Session()
    message = get_item(request, session)
    session.delete(message)
    session.commit()
    messages = get_all_messages()
    id_deleted = request['data']
    messages.append({'deleted': f'message with id {id_deleted} was deleted!'})

    return make_response(request, 200, messages)


def get_item(request, session):

    try:
        message = session.query(Message).filter(Message.id == int(request['data'])).first()
    except ValueError:
        response = 'Input id of message to update(must be digit)'
        return make_response(request, 400, response)
    return message


def get_all_messages():
    session = Session()

    messages = reduce(
        lambda value, item: value + [{'content': item.content, 'created': item.created.strftime("%Y-%m-%d-%H.%M.%S")}],
        session.query(Message).all(),
        []
    )

    return messages
