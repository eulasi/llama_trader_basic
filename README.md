# Alpaca Trading Bot Vol.1

This project contains a set of tools and scripts to automate trading using the Alpaca API.

## Setup

1. Clone the repository:
git clone https://github.com/eulasi/llama_trader_basic.git
cd alpaca_trading_bot

2. Install the required dependencies:
pip install -r requirements.txt

3. Configure your Alpaca API keys:
Update the `config/credentials.py` file with your API key and secret.

4. Run the trading bot

5. Run back tests

### Streamlined Workflow

1. **Historical Data Collection:** To fetch and save historical data for analysis or backtesting.
   - Run `historical_data.py` periodically or as needed to fetch historical data.
     ```sh
     python historical_data.py
     ```

2. **Backtesting:** To backtest your trading strategies using historical data.
   - Run `backtest.py` when you want to perform backtesting on your strategies.
     ```sh
     python backtest.py
     ```

3. **Automated Trading:** To run your trading bot at specified times.
   - Run `trading_schedule.py` to automate your trading bot to execute at specified times. This is the primary script you’ll keep running during live trading.
     ```sh
     python trading_schedule.py
     ```

4. **Live Data Collection (Optional):** To fetch and save live data at regular intervals.
   - Run `live_data.py` to collect live market data. This can be run in parallel with your trading bot if you need real-time data.
     ```sh
     python live_data.py
     ```

## Strategies

### Moving Average Crossover
This strategy buys when the short-term moving average crosses above the long-term moving average and sells when it crosses below.

### Mean Reversion
This strategy buys when the current price is significantly below the mean price and sells when it is significantly above the mean price.

## License

This project is licensed under the MIT License.