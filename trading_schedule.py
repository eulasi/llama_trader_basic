import logging
import schedule
import time
from subprocess import call
from utils.logger import log_message


def run_trading_bot():
    try:
        start_time = time.time()
        log_message("Starting trading bot")
        call(["python", "main.py"])
        end_time = time.time()
        log_message(f"Trading bot finished execution in {end_time - start_time:.2f} seconds")
    except Exception as e:
        log_message(f"Error running trading bot: {str(e)}", level=logging.ERROR)


def main():
    # Schedule tasks based on optimal day trading times (Market open, mid-day reversal, and market close)
    schedule.every().day.at("09:30").do(run_trading_bot)  # Market open
    schedule.every().day.at("12:00").do(run_trading_bot)  # Mid-day (often reversal time)
    schedule.every().day.at("15:30").do(run_trading_bot)  # Last 30 minutes before market close

    log_message("Scheduled trading bot tasks")

    try:
        # Run the scheduled tasks
        while True:
            schedule.run_pending()
            log_message("Scheduler is running tasks...")
            time.sleep(1)
    except KeyboardInterrupt:
        log_message("Trading bot scheduler stopped manually")
    except Exception as e:
        log_message(f"Scheduler encountered an error: {str(e)}", level=logging.ERROR)


if __name__ == "__main__":
    main()
