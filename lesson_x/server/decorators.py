import logging
import inspect

from functools import wraps

from protocol import make_response

module_logger = logging.getLogger('main_server.decorators')


def log(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        logger = logging.getLogger("main_server.decorators.add")
        # print(inspect.stack())
        logger.debug(f'{func.__name__} called from file {inspect.stack()[2][1]} from line {inspect.stack()[2][2]} '
                     f'by function {inspect.stack()[2][3]}'
                     f' with args: {request}')
        return func(request, *args, **kwargs)
    return wrapper


def token_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # logger = logging.getLogger("main_server.decorators.add")
        # logger.info('IN THE TOKEN!!!!!!!!!!!!!!!')
        if 'token' not in request:
            return make_response(request, 403, 'Access denied')
        return func(request, *args, **kwargs)
    return wrapper

