def validate_request(request):
    """
    Function to validate simple client request
    :param request: raw client request
    :return: bool value - validation solution

    - Example::
        {'action': 'echo', 'time': ''}
    """
    if 'action' in request and 'time' in request:
        return True
    else:
        return False


def make_response(request, code, data=None):
    """
    Function for preparing a request
    :param request: client request
    :param code: server-answer code
    :param data: server-answer data
    :return: dictionary request
    """
    return {
        'data': data,
        'time': request.get('time'),
        'action': request.get('action'),
        'code': code,
    }
