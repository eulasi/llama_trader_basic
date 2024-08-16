# Alpaca Trading Bot Vol.1

This project contains a set of tools and scripts designed to automate trading using the Alpaca API. The bot is equipped
with a moving average crossover strategy, and it has been optimized for both live and paper trading. The bot also
includes robust risk management, performance tracking, and scheduling features.

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/eulasi/llama_trader_basic.git
   cd alpaca_trading_bot
   ```

2. **Install the required dependencies**
   ```bash
   pip install -r requirements.txt
   ```
#### 3. **Configure your Alpaca API keys**
   - Update the config/credentials.py file with your API key and secret.
   - Ensure you set the correct BASE_URL depending on whether you are using paper or live trading.

#### 4. **Modify Parameters**
   - Modify parameters to suit your trading needs
   ```shell
   def moving_average_crossover(
          short_window=10,           # Short moving average window. Suggested: 10 (can vary based on the market's speed)
          long_window=30,            # Long moving average window. Suggested: 30 (provides a more stable trend indicator)
          min_volatility=0.5,        # Minimum volatility threshold. Suggested: 0.5 (filters out low volatility environments)
          max_volatility=50.0,       # Maximum volatility threshold. Suggested: 50.0 (to avoid excessive risk in high volatility)
          volatility_adjustment=True, # Whether to adjust order sizes based on volatility. Suggested: True (helps manage risk)
          profit_threshold=1.02,     # Profit target threshold (2% above entry). Suggested: 1.02 (adjust based on risk appetite)
          stop_loss_threshold=0.98,  # Stop-loss threshold (2% below entry). Suggested: 0.98 (adjust to limit potential losses)
          trailing_stop_loss=0.95    # Trailing stop-loss as a percentage of the highest price reached. Suggested: 0.95 (5% trailing stop)
   )
     
       risk_manager = RiskManager(
          max_loss_per_trade=75,   # Maximum loss allowed per trade. Suggested: 1% of initial capital (e.g., $100 for $10,000 capital)
          max_daily_loss=300,       # Maximum loss allowed per day. Suggested: 5% of initial capital (e.g., $500 for $10,000 capital)
          initial_capital=10000,    # Starting capital for the trading bot. Adjust based on your trading account size.
          risk_percentage=15        # Percentage of capital risked per trade. Suggested: 1-2% for conservative trading, up to 20% for aggressive trading.
   )
     
       target_profit = 75  # Adjusted target profit
       stop_loss_limit = -75  # Adjusted stop loss limit

   ```

#### 5. **Run the trading bot**
   - Execute the main.py file to start the bot for live or paper trading. The bot will execute based on the strategy and risk management settings configured.

#### 6. **Run back tests**
   - Use the backtesting script to simulate trades based on historical data before deploying your strategy in a live environment.

## Streamlined Workflow

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

## Strategy Optimization
To enhance the bot's performance, several key parameters can be adjusted:

### Increase risk_percentage

**What It Does**: Increasing the risk_percentage will increase the amount of capital you allocate to each trade. For
instance, increasing it from 1% to 2% doubles the amount of money you're willing to risk on each trade.

**Impact**: This will indeed increase the size of your positions, and hence, your potential profits. However, it also
increases your exposure to losses. If a trade goes against you, the losses could be larger as well.

### Review max_loss_per_trade and max_daily_loss:

**What It Does**: These settings limit the amount you can lose on any single trade or in a single day. If these limits
are too restrictive, they might be preventing you from taking on larger positions or holding onto trades that could
turn profitable.

**Impact**: Adjusting these values upward allows you to potentially stay in trades longer or take on bigger positions,
which could result in larger profits.

### Adjust the Volatility Threshold:

**What It Does**: You mentioned that some trades are not being made because the calculated order quantity is zero,
particularly when volatility is high. This conservative approach is reducing your exposure in volatile conditions.

**Impact**: By allowing higher volatility trades to occur or by lowering the threshold for rejecting a trade due to
volatility, you might see higher returns. However, this also increases the risk of losses during volatile periods.

### Optimize Moving Average Parameters:

**What It Does**: The short and long moving averages are crucial to your strategy. Tweaking these might allow your
strategy to capture more profitable trades.

**Impact**: Depending on market conditions, different moving average settings might perform better. Experiment with
different short_window and long_window values to see if certain settings consistently produce better results.

### Monitor and Analyze Backtest Results:

**What It Does**: Analyze the trades where profits were either minimal or non-existent. Understanding why these trades
were not profitable could lead to adjustments in your strategy that maximize gains.

**Impact**: By fine-tuning your strategy based on historical data, you could increase the likelihood of hitting more
profitable trades.

## Performance Tracking
The bot includes a PerformanceTracker to record trades, calculate profit and loss (PnL), and monitor other key performance metrics such as win rate and maximum drawdown. The performance data is saved in the data/performance_data directory for further analysis.

## License

This project is licensed under the MIT License.