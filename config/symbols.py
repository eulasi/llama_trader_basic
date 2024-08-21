#  S&P List Optimized
symbol_list = [
    "MSFT", "TSLA", "V", "WMT", "JPM", "BAC", "CSCO", "ABT", "ORCL", "CRM",
    "INTC", "TMUS", "AMD", "TXN", "QCOM", "UNP", "MDT", "MS", "AXP", "PLD",
    "AMT", "CAT", "IBM", "AMAT", "SYK", "C", "ADP", "GE", "ZTS", "CB", "MDLZ",
    "MMC", "ADI", "MU", "HCA", "EW", "CSX", "ICE", "TJX", "FCX", "PGR",
    "SHW", "WM", "CL", "GD", "FISV", "BSX", "ITW", "ATVI", "F", "ETN", "GM",
    "EMR", "COF", "FTNT", "MAR", "ECL", "FDX", "AIG", "LHX", "DXCM", "IQV",
    "CTSH", "STZ", "DOW", "TRV", "KR", "WELL", "NXPI", "ADSK", "APH", "PRU",
    "RSG", "AFL", "DLR", "SPG", "TEL", "HPQ", "HLT", "ANET", "ALL", "BK",
    "BKR", "AJG", "GPN", "X", "CARR", "MCHP", "DLTR", "VRSK", "DD", "TT",
    "AVB", "ABC", "EQR", "YUM", "ROST", "OTIS", "AAPL", "PG", "ABBV", "DIS",
    "VZ", "LOW", "CME", "OXY", "PAYX", "MPC", "CDNS", "KMB", "VLO", "WMB",
    "NUE", "RMD", "PEG", "EA"
]

# List for account starting with $250.00
symbol_list_250 = [
    "AAPL",  # Technology - High volume, stable
    "AMD",  # Technology - Popular in day trading
    "F",  # Automotive - Lower price, high volume
    "GE",  # Industrial - Lower price, stable
    "C",  # Financial - High volume, moderate price
    "NIO",  # Automotive - Electric vehicle sector
    "PLUG",  # Energy - Clean energy sector
    "GPRO",  # Technology - Lower price, high volatility
    "SIRI",  # Communication - Low price, high volume
    "SNAP",  # Communication - Social media, high volume
    "PENN",  # Consumer - Gaming and entertainment
    "ZNGA",  # Technology - Gaming sector
    "SPWR",  # Energy - Solar energy, lower price
    "AMCX",  # Communication - Media, moderate volume
    "TWTR",  # Communication - Social media, high volume
    "MU",  # Technology - Memory chips, high volume
    "T",  # Communication - Telecom, lower price
    "BB",  # Technology - Cybersecurity, moderate price
    "X",  # Industrial - Steel, lower price
    "NCLH"  # Consumer - Cruise line, travel sector
]

# List of top 250 S&P 500 companies tickers
symbol_list_total = ['AAPL', 'MSFT', 'GOOG', 'GOOGL', 'AMZN', 'TSLA', 'BRK.B', 'META',
                     'NVDA', 'UNH', 'JNJ', 'V', 'WMT', 'JPM', 'PG', 'XOM', 'MA', 'CVX', 'HD', 'BAC',
                     'PFE', 'ABBV', 'LLY', 'KO', 'COST', 'DIS', 'AVGO', 'PEP', 'TMO', 'CSCO', 'VZ',
                     'ACN', 'MRK', 'ABT', 'ORCL', 'CMCSA', 'DHR', 'ADBE', 'NKE', 'CRM', 'INTC', 'MCD',
                     'WFC', 'T', 'BMY', 'NEE', 'TMUS', 'UPS', 'AMD', 'LIN', 'TXN', 'NFLX', 'PM',
                     'QCOM', 'SCHW', 'UNP', 'MDT', 'MS', 'RTX', 'SPGI', 'CVS', 'AXP', 'LOW', 'AMGN',
                     'COP', 'INTU', 'ANTM', 'HON', 'PYPL', 'DE', 'PLD', 'LMT', 'AMT', 'CAT', 'IBM',
                     'BLK', 'GS', 'TGT', 'CHTR', 'AMAT', 'ISRG', 'BA', 'NOW', 'SYK', 'C', 'ADP', 'GE',
                     'MO', 'EL', 'ZTS', 'SBUX', 'CB', 'BKNG', 'DUK', 'MDLZ', 'CME', 'MMC', 'CCI',
                     'MMM', 'ADI', 'CI', 'SO', 'MU', 'BDX', 'HCA', 'GILD', 'REGN', 'USB', 'PNC', 'EW',
                     'CSX', 'EOG', 'AON', 'ICE', 'TJX', 'NOC', 'PSA', 'D', 'VRTX', 'TFC', 'FCX',
                     'EQIX', 'PGR', 'SHW', 'LRCX', 'WM', 'CL', 'GD', 'NSC', 'FISV', 'NEM', 'MRNA',
                     'BSX', 'MCO', 'ITW', 'ATVI', 'FIS', 'PXD', 'SLB', 'F', 'MET', 'HUM', 'ETN', 'OXY',
                     'GM', 'ILMN', 'EMR', 'DG', 'APD', 'COF', 'FTNT', 'MAR', 'SRE', 'ADM', 'ECL',
                     'FDX', 'AEP', 'CNC', 'KLAC', 'ROP', 'AIG', 'PAYX', 'KHC', 'LHX', 'DXCM', 'EXC',
                     'SNPS', 'ORLY', 'MCK', 'MPC', 'IQV', 'CTSH', 'HSY', 'STZ', 'IDXX', 'DOW', 'JCI',
                     'TRV', 'KR', 'KMI', 'WELL', 'NXPI', 'ADSK', 'CTAS', 'APH', 'PRU', 'SYY', 'CDNS',
                     'AZO', 'CTVA', 'CMG', 'MNST', 'O', 'RSG', 'AFL', 'DLR', 'KMB', 'VLO', 'GIS',
                     'SPG', 'WMB', 'DVN', 'MSCI', 'XEL', 'TEL', 'HPQ', 'HLT', 'PSX', 'NUE', 'A', 'ANET',
                     'SBAC', 'BAX', 'MSI', 'ALL', 'WBA', 'BK', 'BKR', 'AJG', 'GPN', 'X', 'CARR',
                     'MCHP', 'DLTR', 'RMD', 'PEG', 'HAL', 'TDG', 'VRSK', 'DD', 'PH', 'TT', 'HES',
                     'AVB', 'EA', 'ED', 'ABC', 'EQR', 'YUM', 'ROST', 'TSN', 'LYB', 'TROW', 'FAST',
                     'ALGN', 'ARE', 'WEC', 'OTIS', 'AMP']
