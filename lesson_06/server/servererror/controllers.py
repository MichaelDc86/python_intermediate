from protocol import make_response


def servererror_controller(request):
    raise Exception('Server Error')
