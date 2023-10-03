from datetime import datetime, timezone, timedelta
import logging, sys, os
from logging.handlers import RotatingFileHandler

LOG_FOLDER = "logs"
MAX_LOG_FILES = 5
MAX_LOG_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5MB in bytes

if not os.path.exists(LOG_FOLDER):
    os.mkdir(LOG_FOLDER)

# Define a UTC+8 timezone offset
UTC_OFFSET = timezone(timedelta(hours=8))

# New log file name
LOG_FILE = "log.log"

# Create a custom formatter that includes UTC+8 time and line number in the log messages
class Formatter(logging.Formatter):
    def __init__(self):
        super(Formatter, self).__init__(datefmt="%Y-%m-%d %H:%M:%S")

    def format(self, record):
        record.asctime = self.formatTime(record)
        log_line = f'[{record.asctime} UTC+8] [{record.levelname}] [{record.filename} line {record.lineno}] {record.msg}'
        return log_line

    def formatTime(self, record):
        return datetime.fromtimestamp(record.created, tz=timezone.utc).astimezone(UTC_OFFSET).strftime(self.datefmt)

# Create a formatter using the custom Formatter class with the desired date format
formatter = Formatter()

# Create a logger instance
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)  # Set the desired logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

# Create a file handler to log to a file
file_handler = RotatingFileHandler(
    os.path.join(LOG_FOLDER, LOG_FILE),
    maxBytes=MAX_LOG_FILE_SIZE_BYTES,
    backupCount=MAX_LOG_FILES,
    encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Create a console handler to log to the console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)  # Set the desired logging level for the console
console_handler.setFormatter(formatter)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
