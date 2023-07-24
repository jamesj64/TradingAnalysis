# TradingAnalysis

### Overview

This repository currently serves to display technical indicators that I've implemented in Python/Jupyter,
and trading strategies such as SMA crossover, simple momentum/contrarian, and mean reversion.

In terms of the technical implementation, I defined an Instrument class that downloads past financial data from Yahoo
Finance provided a ticker symbol, a start date, and an end date. The currently implemented strategy backtesters are
implemented with vectorized operations on Pandas dataframes.

Below you'll find some images with performance analysis for these strategies on historical data and their performance
relative to the simple buy and hold strategy. (Some of the below performance analyses include average trading cost. This
is only for the EUR/USD instrument).

Some of the libraries currently used include Jupyter, Pandas, Matplotlib, sci-kit, yfinance and NumPy.

### Technical Indicators

##### Bollinger Bands
![image](https://github.com/jamesj64/TradingAnalysis/assets/102470405/ce8ecada-4ec7-4ace-bbe4-8b5d714bc7d1)


##### SMA
![image](https://github.com/jamesj64/TradingAnalysis/assets/102470405/2bbe1be4-496e-473d-be74-389d37bb68eb)


### Strategy performance

##### Mean Reversion
![image](https://github.com/jamesj64/TradingAnalysis/assets/102470405/d2158f8b-3019-4c1a-9fb8-ddc6c8cac6ae)


##### SMA Crossover
![image](https://github.com/jamesj64/TradingAnalysis/assets/102470405/a1f27f38-2dd5-4112-adee-bedf975e4426)


##### Momentum
![image](https://github.com/jamesj64/TradingAnalysis/assets/102470405/761aa8c1-9800-491c-bdf7-9d3f7f9e092a)

