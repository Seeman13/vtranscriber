import logging


class LoggerService:
    @staticmethod
    def setup_logger():
        """
        Консольлог.
        """
        logger = logging.getLogger('app_logger')
        logger.setLevel(logging.DEBUG)

        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(log_format)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger
