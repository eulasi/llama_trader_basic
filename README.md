# Alpaca Trading Bot Vol.1

This project contains a set of tools and scripts to automate trading using the Alpaca API.

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

1. **backtest.py:**
   - **Purpose:** To backtest your trading strategies using historical data.
   - **Run:** When you want to test how your strategies would have performed in the past.

2. **schedule.py:**
   - **Purpose:** To run your trading bot at specified times.
   - **Run:** When you want to automate your trading bot to run at specific times each trading day.

3. **historical_data.py:**
   - **Purpose:** To fetch and save historical data for analysis or backtesting.
   - **Run:** When you need to update or gather historical data.

4. **live_data.py:**
   - **Purpose:** To fetch and save live data at regular intervals.
   - **Run:** When you need to collect real-time data for live trading or analysis.

### Running the Scripts

- **backtest.py:** Run this script when you want to perform backtesting on your strategies.
- **historical_data.py:** Run this script periodically or as needed to fetch historical data.
- **live_data.py:** Run this script to collect live market data. This can be run in parallel with your trading bot if you need real-time data.
- **schedule.py:** Run this script to automate your trading bot to execute at specified times. This is the primary script you’ll keep running during live trading.

### Streamlined Workflow

1. **Historical Data Collection:**
   - Run `historical_data.py` as needed to fetch historical data.
     ```sh
     python historical_data.py
     ```

2. **Backtesting:**
   - Run `backtest.py` to test your strategies with historical data.
     ```sh
     python backtest.py
     ```

3. **Automated Trading:**
   - Run `schedule.py` to execute your trading bot at specified times.
     ```sh
     python schedule.py
     ```

4. **Live Data Collection (Optional):**
   - Run `live_data.py`  if you need real-time data for analysis.
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