import importlib

import MeanRevBacktester

importlib.reload(MeanRevBacktester)

mean_rev = MeanRevBacktester.MeanRevBacktester("EURUSD=X", "2015-01-01", "2023-01-01", 30, 2, 0.00007)

print(mean_rev.test_strategy())

mean_rev.plot_results()