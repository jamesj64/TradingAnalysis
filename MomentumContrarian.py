import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Instrument import Instrument

plt.style.use("seaborn-v0_8")


class MomentumBacktester:
    """ Class for the vectorized backtesting of simple Momentum trading strategies. """

    def __init__(self, symbol, start, end, tc, is_contrarian=False):
        """
        Parameters
        ----------
        symbol: str
            ticker symbol (instrument) to be backtested
        start: str
            start date for data import
        end: str
            end date for data import
        tc: float
            proportional transaction/trading costs per trade
        is_contrarian: bool
            whether the strategy is contrarian
        """
        self.results_overview = None
        self.window = None
        self.tc = tc
        self.results = None
        self._is_contrarian = is_contrarian
        self._instrument = Instrument(symbol, start, end)
        self._data = self._instrument.get_data()

    @classmethod
    def from_instrument(cls, instrument, tc, is_contrarian=False):
        return cls(instrument.get_ticker(), instrument.get_start(), instrument.get_end(), tc, is_contrarian)

    def __repr__(self):
        return "MomentumBacktester(symbol={}, start={}, end={})".format(self._instrument.get_ticker(),
                                                                        self._instrument.get_start(),
                                                                        self._instrument.get_end())

    def test_strategy(self, window=1):
        """ Backtests the simple Momentum trading strategy.
        
        Parameters
        ----------
        window: int
            time window (number of bars) to be considered for the strategy.
        """
        self.window = window
        data = self._data.copy().dropna()
        data["log_returns"] = np.log(data.price / data.price.shift(1))
        data["position"] = np.sign(data["log_returns"].rolling(self.window).mean()).mul(-1 if self._is_contrarian else 1
                                                                                        )
        data["strategy"] = data["position"].shift(1) * data["log_returns"]
        data.dropna(inplace=True)

        # determine the number of trades in each bar
        data["trades"] = data.position.diff().fillna(0).abs()

        # subtract transaction/trading costs from pre-cost return
        data.strategy = data.strategy - data.trades * self.tc

        data["creturns"] = data["log_returns"].cumsum().apply(np.exp)
        data["cstrategy"] = data["strategy"].cumsum().apply(np.exp)
        self.results = data

        perf = data["cstrategy"].iloc[-1]  # absolute performance of the strategy
        outperf = perf - data["creturns"].iloc[-1]  # out-/underperformance of strategy

        return round(perf, 6), round(outperf, 6)

    def plot_results(self):
        """ Plots the performance of the trading strategy and compares to "buy and hold".
        """
        if self.results is None:
            print("Run test_strategy() first.")
        else:
            title = "{} | Window = {} | TC = {}".format(self._instrument.get_ticker(), self.window, self.tc)
            self.results[["creturns", "cstrategy"]].plot(title=title, figsize=(12, 8))

    def optimize_parameter(self, window_range):
        """ Finds the optimal strategy (global maximum) given the window parameter range.

        Parameters
        ----------
        window_range: tuple
            tuples of the form (start, end, step size)
        """

        windows = range(*window_range)

        results = []
        for window in windows:
            results.append(self.test_strategy(window)[0])

        best_perf = np.max(results)  # best performance
        opt = windows[np.argmax(results)]  # optimal parameter

        # run/set the optimal strategy
        self.test_strategy(opt)

        # create a df with many results
        many_results = pd.DataFrame(data={"window": windows, "performance": results})
        self.results_overview = many_results

        return opt, best_perf
