import sys

from loguru import logger


class LoggerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerSingleton, cls).__new__(cls)
            cls._instance.configure_logger()
        return cls._instance

    def configure_logger(self):
        # Remove the default handler
        logger.remove()

        # Add a console handler
        logger.add(
            sys.stdout,
            level="INFO",
            format="<green>{time}</green> | <level>{level}</level> | <level>{message}</level>",
        )

        # Add a file handler with rotation and retention
        logger.add(
            "logs/app.log",
            rotation="10 MB",
            retention="10 days",
            compression="zip",
            level="DEBUG",
        )

        # Assign the configured logger to an instance attribute
        self.logger = logger
