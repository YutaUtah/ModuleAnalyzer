from pystats.logger.logger import Logger


def logging_check():
    logger = Logger(__name__).logger
    logger.info('hello')
