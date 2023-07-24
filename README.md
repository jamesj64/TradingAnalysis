# TradingAnalysis

This repository currently serves to display technical indicators that I've implemented in Python/Jupyter,
and trading strategies such as SMA crossover, simple momentum/contrarian, and mean reversion.

Below you'll find some images with performance analysis for these strategies on historical data and their performance
relative to the simple buy and hold strategy. (Some of the below performance analyses include average trading cost. This
is only for the EUR/USD instrument).

In terms of the technical implementation, I defined an Instrument class that downloads past financial data from Yahoo
Finance provided a ticker symbol, a start date, and an end date. The currently implemented strategy backtesters are
implemented with vectorized operations on Pandas dataframes.

Some of the libraries currently used include Jupyter, Pandas, Matplotlib, sci-kit, yfinance and NumPy.

### Technical Indicators

##### Bollinger Bands
![image](https://github.com/jamesj64/TradingAnalysis/assets/102470405/4766b776-3ac7-4e0d-a6e2-57b7b9bc26ae)


### Strategy performance

##### Mean Reversion
![image](https://github.com/jamesj64/TradingAnalysis/assets/102470405/3ba1a758-3ff3-4230-9290-a5d0951cfd84)
