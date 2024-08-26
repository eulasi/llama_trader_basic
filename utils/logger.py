import logging
import os
from datetime import datetime

# Ensure the logs directory exists
logs_directory = 'logs'
if not os.path.exists(logs_directory):
    os.makedirs(logs_directory)
    print(f"Created logs directory: {logs_directory}")


# Function to create a log file name with a timestamp
def get_log_filename_with_timestamp(base_name="trading"):
    timestamp = datetime.now().astimezone().strftime("%Y-%m-%d_%H:%M:%S")
    return os.path.join(logs_directory, f"{base_name}_{timestamp}.log")


# Configure the logger with a log file name that includes a timestamp
log_filename = get_log_filename_with_timestamp()
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def log_message(message, level=logging.INFO):
    logging.log(level, message)
