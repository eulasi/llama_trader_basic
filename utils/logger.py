import logging
import os
from datetime import datetime

# Ensure the logs directory exists
logs_directory = 'logs'
if not os.path.exists(logs_directory):
    os.makedirs(logs_directory)
    print(f"Created logs directory: {logs_directory}")


# Function to create a unique log file name
def get_unique_log_filename(base_name="trading.log"):
    log_path = os.path.join(logs_directory, base_name)
    if os.path.exists(log_path):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        base_name = f"trading_{timestamp}.log"
    return os.path.join(logs_directory, base_name)


# Configure the logger with a unique log file name
log_filename = get_unique_log_filename()
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def log_message(message, level=logging.INFO):
    logging.log(level, message)
