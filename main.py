import logging

from strategies.moving_average_crossover import moving_average_crossover
from strategies.mean_reversion import mean_reversion
from utils.logger import log_message


def main():
    try:
        log_message("Starting trading bot")

        # Uncomment the strategy you want to test
        moving_average_crossover()
        # mean_reversion()

        log_message("Trading bot finished execution")
    except Exception as e:
        log_message(f"Error: {str(e)}", level=logging.ERROR)


if __name__ == "__main__":
    main()
