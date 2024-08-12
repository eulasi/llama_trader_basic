import logging

import schedule
import time
from subprocess import call
from utils.logger import log_message


def run_trading_bot():
    try:
        log_message("Starting trading bot")
        call(["python", "main.py"])
        log_message("Trading bot finished execution")
    except Exception as e:
        log_message(f"Error running trading bot: {str(e)}", level=logging.ERROR)


def main():
    # Schedule tasks
    schedule.every().day.at("09:30").do(run_trading_bot)
    schedule.every().day.at("11:30").do(run_trading_bot)
    schedule.every().day.at("15:00").do(run_trading_bot)

    log_message("Scheduled trading bot tasks")

    try:
        # Run the scheduled tasks
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        log_message("Trading bot scheduler stopped manually")


if __name__ == "__main__":
    main()
