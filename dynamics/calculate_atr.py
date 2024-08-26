import numpy as np
import pandas as pd


def calculate_atr(data, period=21):  # 14 or 21
    """
    Calculate the Average True Range (ATR) for a given set of data.

    Parameters:
        data (list): List of historical price bars.
        period (int): The period over which to calculate the ATR (default is 21).

    Returns:
        float: The calculated ATR value.
    """
    if len(data) < period + 1:
        raise ValueError("Not enough data points to calculate ATR.")

    high_prices = np.array([bar._raw['h'] for bar in data])
    low_prices = np.array([bar._raw['l'] for bar in data])
    close_prices = np.array([bar._raw['c'] for bar in data])

    # Calculate the True Range (TR)
    tr1 = high_prices[1:] - low_prices[1:]
    tr2 = np.abs(high_prices[1:] - close_prices[:-1])
    tr3 = np.abs(low_prices[1:] - close_prices[:-1])

    true_ranges = np.maximum(np.maximum(tr1, tr2), tr3)

    # Calculate the ATR
    atr = np.mean(true_ranges[-period:])
    return atr
