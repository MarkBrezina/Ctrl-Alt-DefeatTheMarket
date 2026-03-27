In order to gain/dig/find and whatever you want to call it, alpha.
We must go away from the idea that alpha is a little nice recipe from grandmama's cooking book, where adding 2 tablespoons of salt and 300 grams of flour turns into profit.
If it was that easy, we would all be millionaires by now.

We instead need to consider the dynamics(behaviours) of assets and implement behaviours that benefit or extract value.
The simplest idea is "buy low, sell high". The actual idea mostly used is "implement dynamic with positive expected value".
Because a short is "borrow high, return at low", and pairs trading is "borrow the low one, sell the high one -> reverse on return to correlation".
Those are all representations of a returns distribution, not a "price is low.... ohhh what now". We are looking at expected returns, not prices.


Here are some generic key words to post into chatgpt to get it to tell you everything about the topics.
Relevant trading types to go over

- **Pairs Trading**, Trade two historically related assets when their spread diverges, expecting convergence.
- **Trend Following**, Trade in the direction of short-, medium-, or long-term price momentum.
- **Mean Reversion**, Trade the idea that price, spread, or another signal has moved too far from a short-term or long-term average and is likely to revert back.
- **Price Discrepancy / Statistical Arbitrage**, Exploit temporary mispricings versus a model, fair value, or related instrument.
- **Basket Arbitrage**, Trade a group of related assets against an index, ETF, or synthetic basket when pricing deviates.
- **Exchange Arbitrage**, Exploit price differences for the same asset across different exchanges or venues.
- **Volatility Trading**, Trade expected vs. realized volatility, often through options or volatility-sensitive structures.

If you want to make it a bit more complete for HFT specifically, I’d add:

- **Market Making**, Provide bids and offers, earn spread, and manage inventory/adverse selection.
- **Order Flow / Microstructure Trading**, Use order book imbalance, queue position, and short-term flow signals.
- **Cross-Asset Arbitrage**, Trade relationships across futures, spot, ETFs, options, or correlated assets.

A neat grouping would be:

**Relative value:** Pairs trading, basket arbitrage, exchange arbitrage, cross-asset arbitrage \
**Directional:** Trend following, mean reversion \
**Volatility:** Volatility trading \
**Microstructure / HFT:** Market making, latency arbitrage, order flow trading \
**Model-based mispricing:** Price discrepancy / statistical arbitrage


Watching previous guys work [The road to winning prosperity IMC Prosperity 3 winners](https://www.youtube.com/watch?v=aH1aaS4mtj4)






## Pairs Trading
Pairs trading: https://hudsonthames.org/definitive-guide-to-pairs-trading/ \
Pairs trading: https://palomar.home.ece.ust.hk/MAFS5310_lectures/slides_pairs_trading.pdf \
Portfolio optimization with Pairs Trading https://portfoliooptimizationbook.com/slides/slides-pairs-trading.pdf \
QuantConnect on Pairs Trading: https://github.com/QuantConnect/Research/blob/master/Analysis/02%20Kalman%20Filter%20Based%20Pairs%20Trading.ipynb \
AJeanis on Pairs Trading: https://github.com/AJeanis/Pairs-Trading \
Ozenc Gungor's repo on Pairs trading: https://github.com/ozencgungor/Pairs_Trading_Kalman \
KidQuant on Pairs trading: https://github.com/KidQuant/Pairs-Trading-With-Python/blob/master/PairsTrading.ipynb \
Awdneyk: https://github.com/Awdneyk/stat-arb-pair-selection

## Market Making.
Original Avellaneda Stoikov paper: https://people.orie.cornell.edu/sfs33/LimitOrderBook.pdf \
HFT with inventoru constraints and directional bets: https://arxiv.org/abs/1206.4810 \
Avellaneda Stoikov in Python: https://github.com/fedecaccia/avellaneda-stoikov \
Alvaro Cartea and Yixuan Wang: https://ora.ox.ac.uk/objects/uuid%3Ac2ba6656-8eab-4b2e-a24a-e9e842d1378f/files/s41687h481 \
Optimal Market making: https://arxiv.org/abs/1605.01862 \
Optimal High frequency market making: https://stanford.edu/class/msande448/2018/Final/Reports/gr5.pdf \
Ready trader go Keanekwa: https://github.com/keanekwa/Optiver-Ready-Trader-Go \
ESkripichnikov: https://github.com/ESkripichnikov/market-making \
QuantBeckman: https://www.quantbeckman.com/p/can-you-manage-inventoryor-is-it 

## Trend
Dual moving average crossover: https://github.com/rbhatia46/Dual-Moving-Average-Crossover-Python

