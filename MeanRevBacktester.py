import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product

from Instrument import Instrument

plt.style.use("seaborn-v0_8")


class MeanRevBacktester:

    def __init__(self, symbol, start, end, window, dev, tc):
        """
        Parameters
        ----------
        symbol: str
            ticker symbol to be backtested
        start: str
            start date for data import
        end: str
            end date for data import
        window: int
            moving window in bars (e.g. days) for shorter SMA
        dev: int
            Number of standard deviations above or below SMA to go short/long (Neutral when crossing the SMA)
        tc: float
            trading cost
        """
        self._window = window
        self._dev = dev

        self._tc = tc

        self._instrument = Instrument(symbol, start, end)
        self._data = self._instrument.get_data()

        self._results = None
        self._results_overview = None

        self.prepare_data()

    @classmethod
    def from_instrument(cls, instrument, window, dev):
        return cls(instrument.get_ticker(), instrument.get_start(), instrument.get_end(), window, dev)

    def prepare_data(self):
        """ Prepares the data for strategy backtesting (strategy-specific). """
        data = self._data.copy()
        data["log_returns"] = np.log(data.price / data.price.shift(1))
        data["SMA"] = data["price"].rolling(self._window).mean()
        data["Upper"] = data["SMA"] + self._dev * data["price"].rolling(self._window).std()
        data["Lower"] = data["SMA"] - self._dev * data["price"].rolling(self._window).std()
        data["distance"] = data.price - data.SMA
        self._data = data
        data.drop(columns=["log_returns", "distance"]).loc["2022"].plot(title="Bollinger Bands Indicator")

    def test_strategy(self):
        """ Backtests the trading strategy. """
        data = self._data.copy().dropna()

        data["position"] = np.where(data.price > data.Upper, -1, np.nan)
        data["position"] = np.where(data.price < data.Lower, 1, data["position"])
        data["position"] = np.where(data.distance * data.distance.shift(1) < 0, 0, data["position"])
        data.position = data.position.ffill().fillna(0)

        data["trades"] = data.position.diff().fillna(0).abs()

        data["strategy"] = data["position"].shift(1) * data["log_returns"] - data.trades * self._tc

        data.dropna(inplace=True)
        data["creturns"] = data["log_returns"].cumsum().apply(np.exp)
        data["cstrategy"] = data["strategy"].cumsum().apply(np.exp)
        self._results = data

        perf = data["cstrategy"].iloc[-1]  # absolute performance of the strategy
        outperf = perf - data["creturns"].iloc[-1]  # out-/underperformance of strategy
        return round(perf, 6), round(outperf, 6)

    def plot_results(self):
        """ Plots the performance of the trading strategy and compares to "buy and hold".
        """
        if self._results is None:
            print("Run test_strategy() first.")
        else:
            title = "{} | Window = {} | TC = {}".format(self._instrument.get_ticker(), self._window, self._tc)
            self._results[["creturns", "cstrategy"]].plot(title=title, figsize=(12, 8))
