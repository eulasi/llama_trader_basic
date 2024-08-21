def dynamic_profit_threshold(volatility_percentage, atr, base_threshold=1.015):
    """
    Adjust the profit threshold based on volatility and ATR.
    :param volatility_percentage: Current volatility percentage of the stock.
    :param atr: The average true range of the stock.
    :param base_threshold: The base profit threshold.
    :return: Adjusted profit threshold.
    """
    # Example logic to adjust the profit threshold
    if volatility_percentage > 20:
        return base_threshold * 1.05  # Increase threshold by 5% if volatility is high
    elif atr > 2.0:  # Assuming ATR value greater than 2.0 is considered high
        return base_threshold * 1.03  # Increase threshold by 3% if ATR is high
    else:
        return base_threshold  # Default to the base threshold
