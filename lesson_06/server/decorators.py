import logging

from functools import wraps

logger = logging.getLogger('decorators')


def log(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        logger.debug(f'{func.__name__}: {request}')
        return func(request, *args, **kwargs)
    return wrapper
