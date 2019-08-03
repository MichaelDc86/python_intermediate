from protocol import make_response
from decorators import token_required


@token_required
def servererror_controller(request):
    raise Exception('Server Error')
