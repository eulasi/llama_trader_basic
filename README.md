# Alpaca Trading Bot

This project contains a set of tools and scripts to automate trading using the Alpaca API.

## Directory Structure

alpaca_trading_bot/
├── config/
│ ├── config.py
│ ├── credentials.py
├── data/
│ ├── historical_data/
│ └── live_data/
├── logs/
│ ├── trading.log
├── strategies/
│ ├── init.py
│ ├── moving_average_crossover.py
│ └── mean_reversion.py
├── utils/
│ ├── init.py
│ ├── data_fetcher.py
│ ├── order_executor.py
│ ├── logger.py
├── main.py
├── backtest.py
├── requirements.txt
└── README.md

## Setup

1. Clone the repository:
git clone https://github.com/yourusername/alpaca_trading_bot.git
cd alpaca_trading_bot

2. Install the required dependencies:
pip install -r requirements.txt

3. Configure your Alpaca API keys:
- Update the `config/credentials.py` file with your API key and secret.

4. Run the trading bot

5. Run backtests

# Streamlined Workflow

## Strategies

### Moving Average Crossover
This strategy buys when the short-term moving average crosses above the long-term moving average and sells when it crosses below.

### Mean Reversion
This strategy buys when the current price is significantly below the mean price and sells when it is significantly above the mean price.

## Contributing

Feel free to fork this repository and contribute by submitting a pull request. 

## License

This project is licensed under the MIT License.

