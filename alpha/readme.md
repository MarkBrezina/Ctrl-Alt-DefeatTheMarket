In order to gain/dig/find and whatever you want to call it, alpha.
We must go away from the idea that alpha is a little nice recipe from grandmama's cooking book, where adding 2 tablespoons of salt and 300 grams of flour turns into profit.
If it was that easy, we would all be millionaires by now.

We instead need to consider the dynamics(behaviours) of assets and implement behaviours that benefit or extract value.
The simplest idea is "buy low, sell high". The actual idea mostly used is "implement dynamic with positive expected value".
Because a short is "borrow high, return at low", and pairs trading is "borrow the low one, sell the high one -> reverse on return to correlation".
Those are all representations of a returns distribution, not a "price is low.... ohhh what now". We are looking at expected returns, not prices.


Here are some generic key words to post into chatgpt to get it to tell you everything about the topics.
Relevant trading types to go over

- Pairs Trading, Trade two historically related assets when their spread diverges, expecting convergence.
- Trend Following, Trade in the direction of short-, medium-, or long-term price momentum.
- Mean Reversion, Trade the idea that price, spread, or another signal has moved too far from a short-term or long-term average and is likely to revert back.
- Price Discrepancy / Statistical Arbitrage, Exploit temporary mispricings versus a model, fair value, or related instrument.
- Basket Arbitrage, Trade a group of related assets against an index, ETF, or synthetic basket when pricing deviates.
- Exchange Arbitrage, Exploit price differences for the same asset across different exchanges or venues.
- Volatility Trading, Trade expected vs. realized volatility, often through options or volatility-sensitive structures.

If you want to make it a bit more complete for HFT specifically, I’d add:

- Market Making, Provide bids and offers, earn spread, and manage inventory/adverse selection.
- Order Flow / Microstructure Trading, Use order book imbalance, queue position, and short-term flow signals.
- Cross-Asset Arbitrage, Trade relationships across futures, spot, ETFs, options, or correlated assets.

A neat grouping would be:

**Relative value:** Pairs trading, basket arbitrage, exchange arbitrage, cross-asset arbitrage \
**Directional:** Trend following, mean reversion \
**Volatility:** Volatility trading \
**Microstructure / HFT:** Market making, latency arbitrage, order flow trading \
**Model-based mispricing:** Price discrepancy / statistical arbitrage
