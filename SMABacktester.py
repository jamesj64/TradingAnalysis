import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product

from Instrument import Instrument

plt.style.use("seaborn-v0_8")


class SMABacktester:
    """ Vectorized backtesting for SMA crossover trading strategies """

    def __init__(self, symbol, start, end, sma_s, sma_l):
        """
        Parameters
        ----------
        symbol: str
            ticker symbol to be backtested
        start: str
            start date for data import
        end: str
            end date for data import
        SMA_S: int
            moving window in bars (e.g. days) for shorter SMA
        SMA_L: int
            moving window in bars (e.g. days) for longer SMA
        """
        self._SMA_S = sma_s
        self._SMA_L = sma_l

        self._instrument = Instrument(symbol, start, end)
        self._data = self._instrument.get_data()

        self._results = None
        self._results_overview = None

        self.prepare_data()

    @classmethod
    def from_instrument(cls, instrument, sma_s, sma_l):
        return cls(instrument.get_ticker(), instrument.get_start(), instrument.get_end(), sma_s, sma_l)

    def __repr__(self):
        return "SMABacktester(symbol={}, start={}, end={}, SMA_S={}, SMA_L={})".format(self._instrument.get_ticker(),
                                                                                       self._instrument.get_start(),
                                                                                       self._instrument.get_end(),
                                                                                       self._SMA_S,
                                                                                       self._SMA_L)

    def get_instrument(self):
        return self._instrument

    def prepare_data(self):
        """ Prepares the data for strategy backtesting (strategy-specific). """
        data = self._data.copy()
        data["log_returns"] = np.log(data.price / data.price.shift(1))
        data["SMA_S"] = data["price"].rolling(self._SMA_S).mean()
        data["SMA_L"] = data["price"].rolling(self._SMA_L).mean()
        self._data = data

    def set_sma_s(self, sma_s):
        self._SMA_S = sma_s
        self._data["SMA_S"] = self._data["price"].rolling(self._SMA_S).mean()

    def set_sma_l(self, sma_l):
        self._SMA_L = sma_l
        self._data["SMA_L"] = self._data["price"].rolling(self._SMA_L).mean()

    def test_strategy(self):
        """ Backtests the SMA-based trading strategy. """
        data = self._data.copy().dropna()
        data["position"] = np.where(data["SMA_S"] > data["SMA_L"], 1, -1)
        data["strategy"] = data["position"].shift(1) * data["log_returns"]
        data.dropna(inplace=True)
        data["creturns"] = data["log_returns"].cumsum().apply(np.exp)
        data["cstrategy"] = data["strategy"].cumsum().apply(np.exp)
        self._results = data

        perf = data["cstrategy"].iloc[-1]  # absolute performance of the strategy
        outperf = perf - data["creturns"].iloc[-1]  # out-/underperformance of strategy
        return round(perf, 6), round(outperf, 6)

    def plot_results(self):
        """ Plots the performance of the trading strategy and compares to "buy and hold". """
        if self._results is None:
            print("Run test_strategy() first.")
        else:
            title = "{} | SMA_S = {} | SMA_L = {}".format(self._instrument.get_ticker(), self._SMA_S, self._SMA_L)
            self._results[["creturns", "cstrategy"]].plot(title=title, figsize=(12, 8))

    def get_results(self):
        return self._results

    def get_results_overview(self):
        return self._results_overview.copy()

    def optimize_parameters(self, sma_s_range, sma_l_range):
        """ Finds the optimal strategy (global maximum) given the SMA parameter ranges.

        Parameters
        ----------
        sma_s_range, sma_l_range: tuple
            tuples of the form (start, end, step size)
        """

        combinations = list(product(range(*sma_s_range), range(*sma_l_range)))

        # test all combinations
        results = []
        for comb in combinations:
            self.set_sma_s(comb[0])
            self.set_sma_l(comb[1])
            results.append(self.test_strategy()[0])

        best_perf = np.max(results)  # best performance
        opt = combinations[np.argmax(results)]  # optimal parameters

        # run/set the optimal strategy
        self.set_sma_s(opt[0])
        self.set_sma_l(opt[1])
        self.test_strategy()

        # create a df with many results
        many_results = pd.DataFrame(data=combinations, columns=["SMA_S", "SMA_L"])
        many_results["performance"] = results
        self._results_overview = many_results

        return opt, best_perf
