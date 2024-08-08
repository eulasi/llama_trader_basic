import schedule
import time
from subprocess import call
from utils.logger import log_message

def run_trading_bot():
    log_message("Running trading bot")
    call(["python", "main.py"])

def main():
    # Schedule tasks
    schedule.every().day.at("09:30").do(run_trading_bot)
    schedule.every().day.at("11:30").do(run_trading_bot)
    schedule.every().day.at("15:00").do(run_trading_bot)

    log_message("Scheduled trading bot tasks")

    # Run the scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
