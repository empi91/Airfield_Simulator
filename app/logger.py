"""Logging all important information/events during runtime"""

import logging
import sys

FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = "log.log"

class Logger:

    def get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(FORMATTER)
        return console_handler

    def get_file_handler(self):
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(FORMATTER)
        return file_handler

    def get_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.get_console_handler())
        logger.addHandler(self.get_file_handler())
        logger.propagate = False
        return logger


