import logging


def create_logger():
    logger = logging.getLogger('main_client')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    handler = logging.FileHandler('log/client.log')
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    logger.addHandler(handler)
    return logger
