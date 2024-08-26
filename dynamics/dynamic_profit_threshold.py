def dynamic_profit_threshold(volatility_percentage, atr, base_threshold=1.015):
    """
    Adjust the profit threshold based on volatility and ATR.
    :param volatility_percentage: Current volatility percentage of the stock.
    :param atr: The average true range of the stock.
    :param base_threshold: The base profit threshold.
    :return: Adjusted profit threshold.
    """
    adjusted_threshold = base_threshold

    # Adjust based on volatility
    if volatility_percentage > 20:
        adjusted_threshold *= 1.05  # Increase threshold by 5% if volatility is high

    # Adjust based on ATR
    if atr > 2.0:  # Assuming ATR value greater than 2.0 is considered high
        adjusted_threshold *= 1.03  # Increase threshold by 3% if ATR is high

    return adjusted_threshold
