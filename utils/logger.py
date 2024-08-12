import logging
import os

# Ensure the logs directory exists
logs_directory = 'logs'
if not os.path.exists(logs_directory):
    os.makedirs(logs_directory)
    print(f"Created logs directory: {logs_directory}")

# Configure the logger
logging.basicConfig(
    filename=os.path.join(logs_directory, 'trading.log'),
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def log_message(message, level=logging.INFO):
    logging.log(level, message)
