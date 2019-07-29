from datetime import datetime

from protocol import make_response
from decorators import token_required


@token_required
def server_time_controller(request):
    return make_response(request, 200, datetime.now().timestamp())
