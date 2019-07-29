import logging
from logging.handlers import TimedRotatingFileHandler


def create_logger():
    logger = logging.getLogger('main_server')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(message)s')

    # handler = logging.FileHandler('log/server.log')
    # handler = logging.handlers.TimedRotatingFileHandler('log/server.log', when='s', interval=1, backupCount=3)
    handler = logging.handlers.TimedRotatingFileHandler('log/server.log', when='D', interval=1, backupCount=7)
    handler_console = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    logger.addHandler(handler)
    logger.addHandler(handler_console)
    return logger

