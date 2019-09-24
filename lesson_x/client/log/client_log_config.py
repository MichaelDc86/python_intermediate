import logging


def create_logger():
    logger = logging.getLogger('main_client')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    handler = logging.FileHandler('client/log/client.log')
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    handler_console = logging.StreamHandler()

    logger.addHandler(handler)
    logger.addHandler(handler_console)
    return logger


def get_logger():
    logger_in = create_logger()
    return logger_in
