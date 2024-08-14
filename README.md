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
    - Run `trading_schedule.py` to automate your trading bot to execute at specified times. This is the primary script
      you’ll keep running during live trading.
      ```sh
      python trading_schedule.py
      ```

4. **Live Data Collection (Optional):** To fetch and save live data at regular intervals.
    - Run `live_data.py` to collect live market data. This can be run in parallel with your trading bot if you need
      real-time data.
      ```sh
      python live_data.py
      ```

## Strategies

### Moving Average Crossover

This strategy buys when the short-term moving average crosses above the long-term moving average and sells when it
crosses below.

### Mean Reversion

This strategy buys when the current price is significantly below the mean price and sells when it is significantly above
the mean price.

### Optimization Tips

#### Increase risk_percentage
   **What It Does**: Increasing the risk_percentage will increase the amount of capital you allocate to each trade. For
   instance, increasing it from 1% to 2% doubles the amount of money you're willing to risk on each trade.

   **Impact**: This will indeed increase the size of your positions, and hence, your potential profits. However, it also
   increases your exposure to losses. If a trade goes against you, the losses could be larger as well.

#### Review max_loss_per_trade and max_daily_loss:
   **What It Does**: These settings limit the amount you can lose on any single trade or in a single day. If these limits
   are too restrictive, they might be preventing you from taking on larger positions or holding onto trades that could
   turn profitable.

   **Impact**: Adjusting these values upward allows you to potentially stay in trades longer or take on bigger positions,
   which could result in larger profits.

#### Adjust the Volatility Threshold:
   **What It Does**: You mentioned that some trades are not being made because the calculated order quantity is zero,
   particularly when volatility is high. This conservative approach is reducing your exposure in volatile conditions.
   
   **Impact**: By allowing higher volatility trades to occur or by lowering the threshold for rejecting a trade due to
   volatility, you might see higher returns. However, this also increases the risk of losses during volatile periods.

#### Optimize Moving Average Parameters:
   **What It Does**: The short and long moving averages are crucial to your strategy. Tweaking these might allow your
   strategy to capture more profitable trades.

   **Impact**: Depending on market conditions, different moving average settings might perform better. Experiment with
   different short_window and long_window values to see if certain settings consistently produce better results.

#### Monitor and Analyze Backtest Results:
   **What It Does**: Analyze the trades where profits were either minimal or non-existent. Understanding why these trades
   were not profitable could lead to adjustments in your strategy that maximize gains.

   **Impact**: By fine-tuning your strategy based on historical data, you could increase the likelihood of hitting more
   profitable trades.

## License

This project is licensed under the MIT License.