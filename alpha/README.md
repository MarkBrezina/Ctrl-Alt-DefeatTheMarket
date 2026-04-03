
## Plain-English explanation
Alpha is in its simplicity a description for "how do we make money in the markets".

A simple way to think about many IMC rounds is as a sequence of increasingly difficult pricing and prediction problems.

For each asset, IMC is effectively presenting a different type of alpha opportunity.

For a stationary asset, the core idea is simple: buy low, sell high.
The price moves around a stable level, so the job is to identify when it is temporarily cheap or expensive relative to that anchor.

For an asset with drift, things become more interesting.
Now the goal is no longer just “buy low, sell high” around a fixed centre. Instead, you want to identify local minima, local maxima, and the direction of movement.

That is the beginning of trend-following.

As the rounds progress, IMC usually increases the complexity in the same direction.

Imagine, for example, that Round 2 introduces an asset correlated with the drifting one. Now you are not just dealing with one moving curve, but with a relationship between multiple assets.

That is the beginning of pairs trading.

Later rounds may introduce basket arbitrage, derivatives, or more complex combinations of assets. These are really just further extensions of the same core question:

What is mispriced, relative to what, and why?

As the products become more complex, the methods used to extract alpha become more complex too.

## Diagram
A simple idea is this, we want to be able to illustrate when to buy and when to sell.

## Formula or concept
A very simple strategy to present is the notorious mean reversion cross.

```
Buy when the 20-tick Moving average crosses above the 40-tick Moving average.
MA20 > MA40

Sell when the 20-tick Moving average crosses below the 40-tick Moving average.
MA20 <= MA40
```


## Code snippet


Plot/example result

## Common mistakes
Where to go next

market data
-> features
-> signals
-> signal combination
-> target inventory
-> quote placement
-> fills
-> risk adjustment
-> PnL / Sharpe



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


## Market making.
What is it, how do we benefit from it?


## Directional
What is it, how do we benefit from it?


## Mean reversion
What is it, how do we benefit from it?


## Pairs Trading
What is it, how do we benefit from it?


## Volatility
What is it, how do we benefit from it?

## General statistical patterns
What is it, how do we benefit from it?


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
HFT with inventory constraints and directional bets: https://arxiv.org/abs/1206.4810 \
Avellaneda Stoikov in Python: https://github.com/fedecaccia/avellaneda-stoikov \
Alvaro Cartea and Yixuan Wang: https://ora.ox.ac.uk/objects/uuid%3Ac2ba6656-8eab-4b2e-a24a-e9e842d1378f/files/s41687h481 \
Optimal Market making: https://arxiv.org/abs/1605.01862 \
Optimal High frequency market making: https://stanford.edu/class/msande448/2018/Final/Reports/gr5.pdf \
Ready trader go Keanekwa: https://github.com/keanekwa/Optiver-Ready-Trader-Go \
ESkripichnikov: https://github.com/ESkripichnikov/market-making \
QuantBeckman: https://www.quantbeckman.com/p/can-you-manage-inventoryor-is-it 

## Trend
Dual moving average crossover: https://github.com/rbhatia46/Dual-Moving-Average-Crossover-Python




Because you're all apparently completely insane and think that ALPHA IS THE KEY TO GODHOOD, not inventory management... I have decided to put together a youtube playlist.
Along with an expansion to this page.

[IMC Inspirational videos on YouTube](https://www.youtube.com/playlist?list=PLjBE3SzJV9A3ahXCKrEXwG8uKa5fQkDMC)

# Other useful youtube playlists
[Algorithmic game theory](https://www.youtube.com/playlist?list=PLEGCF-WLh2RJBqmxvZ0_ie-mleCFhi2N4)
[EC 2022 talks](https://www.youtube.com/watch?v=OXj5X7kRFwQ&list=PLI0o-KVQWwQ_NOW1JQNU88BzGbxR4yksM)

