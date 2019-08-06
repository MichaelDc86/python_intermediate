def validate_request(request):
    if 'action' in request and 'time' in request:
        return True
    else:
        return False


def make_response(request, code, data=None):
    return {
        'data': data,
        'time': request.get('time'),
        'action': request.get('action'),
        'code': code,
    }
