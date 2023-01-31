import logging

logging.basicConfig(level='INFO', format='[%(asctime)s] %(levelname)s | %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('email_service_logger')


def log(msg):
    """
    logs a message
    """
    logger.info(msg)


def error(msg):
    """
    logs a message as an error
    """
    logger.error(msg)
