
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

Watching previous guys work [The road to winning prosperity IMC Prosperity 3 winners](https://www.youtube.com/watch?v=aH1aaS4mtj4)

## Diagram
A simple visual goal is to illustrate **when to buy and when to sell**. \
![diagram](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/utils/alpha.png)

<br>

## Formula or concept
A very simple strategy to present is the notorious mean reversion cross.

```
Buy when the 20-tick Moving average crosses above the 40-tick Moving average.
MA20 > MA40

Sell when the 20-tick Moving average crosses below the 40-tick Moving average.
MA20 <= MA40
```

## Code snippet
I'll write down a simple code that has the above mean reversion strategy.



## Common mistakes
Many players assume that finding a good alpha, must necessarily mean that they've hit a one-hit goldmine, where nothing other than buy 1 at buy signal, sell 1 at sell signal is necessary.
But in reality there will always be false positives and false negatives. Along with that, there is noise, random events and more.
Most of the time alpha is good, but you will need inventory adjustments, signal strength, risk adjustments, signal combinations. Because multiple alphas may signal simultaenously. 


## Where to go next
In more advanced terms than "buy low, sell high", we should like to express what @maxazv presented on the discord.
IN order to always be on the right side of the above statement, you actually want the following mathematical idea.

$$
E[r_t | s_t] > r_m
$$ 

This reads:

**The expected return of your strategy, given the current market state, is greater than the market return.**

Where:

- $r_t$ is your return at time $t$
- $s_t$ is the market state at time $t$
- $r_m$ is the market return

That is a much better framing of alpha.

In general, most quant pipelines look something like this:

```
market data
-> features
-> signals
-> signal combination
-> target inventory
-> quote placement
-> fills
-> risk adjustment
-> PnL / Sharpe
```
To find alpha, we need to move away from the idea that alpha is some magical recipe from a cookbook, where adding two tablespoons of salt and 300 grams of flour somehow turns into profit.

If it were that easy, everyone would be rich already.

Instead, we need to think in terms of **market dynamics** and build behaviours that can systematically extract value from them.

The simplest expression is still **buy low, sell high.**
But the more accurate formulation is:

**Implement a dynamic with positive expected value.**

That distinction matters.

A short position, for example, is not “buy low, sell high.” It is closer to:

**borrow high, return low.**

Pairs trading is not just “one is low and one is high.” It is:

**trade the divergence in a relationship, then reverse when that relationship normalises.**

These are all expressions of **expected return distributions**, not just reactions to raw prices.

In other words, we are not really looking at prices in isolation.
We are looking at **expected returns conditional on structure, state, and behaviour.**


## General summary of Alphas

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

## Specific alpha walk-throughs.

### Market making.
Market making is different from the strategies above because it is less about taking a strong view on direction and more about **providing liquidity.**

A market maker posts both:

- a bid to buy
- an ask to sell

and tries to earn the spread between them.

The ideal cycle is:

- buy slightly below fair value
- sell slightly above fair value
- repeat many times

But market making is not free money. The main risks are:

- adverse selection, where informed traders trade against your stale quotes
- inventory risk, where you accumulate too much long or short position
- sudden volatility, which can move price before you rebalance

So real market making is:

**earn spread while managing inventory and avoiding being run over**

In plain English:

A market maker is like a shopkeeper.
You continuously offer to buy and sell, trying to make a small margin on lots of trades while controlling risk.

**Here are some additional resources for Market-making**
Original Avellaneda Stoikov paper: https://people.orie.cornell.edu/sfs33/LimitOrderBook.pdf \
HFT with inventory constraints and directional bets: https://arxiv.org/abs/1206.4810 \
Avellaneda Stoikov in Python: https://github.com/fedecaccia/avellaneda-stoikov \
Alvaro Cartea and Yixuan Wang: https://ora.ox.ac.uk/objects/uuid%3Ac2ba6656-8eab-4b2e-a24a-e9e842d1378f/files/s41687h481 \
Optimal Market making: https://arxiv.org/abs/1605.01862 \
Optimal High frequency market making: https://stanford.edu/class/msande448/2018/Final/Reports/gr5.pdf \
Ready trader go Keanekwa: https://github.com/keanekwa/Optiver-Ready-Trader-Go \
ESkripichnikov: https://github.com/ESkripichnikov/market-making \
QuantBeckman: https://www.quantbeckman.com/p/can-you-manage-inventoryor-is-it 

### Arbitrage

Arbitrage is the cleanest concept in theory.

It means exploiting a pricing inconsistency between two equivalent or closely related things.

The basic idea is:

- buy where something is cheap
- sell where the same thing, or nearly the same thing, is expensive
- lock in the difference

Classic forms include:

- the same asset priced differently on two exchanges
- an ETF mispriced relative to its components
- an option mispriced relative to the underlying and other options
- a futures contract inconsistent with spot and carry costs

True arbitrage in the pure sense is rare and usually disappears quickly.

In practice, many “arbitrage” strategies are really **near-arbitrage** or **statistical arbitrage,** where the relationship is not perfectly guaranteed but is strong enough to trade.

In plain English:

Arbitrage is about **pricing inconsistencies.**
You are not mainly forecasting the future. You are exploiting something that does not add up properly right now.


### Geneneral statistical patterns
General statistical patterns

This is the broadest category.

The idea is to look for **repeatable behaviours in data** that are not obvious from a single price chart. Instead of saying, “this asset feels cheap,” you are saying, “historically, when these conditions appear, a certain outcome tends to happen more often than chance.”

These patterns can come from:
- price behaviour
- volatility behaviour
- seasonality
- order flow
- cross-asset relationships
- reactions after news or events
- intraday timing effects

So general statistical trading is really about:

**find a pattern -> test whether it is real -> trade it if the expected value is positive**

Examples:

- prices tend to bounce after extreme short-term moves
- volatility clusters after shocks
- one asset tends to react a few seconds after another
- a spread between related assets tends to close after widening

This is often the foundation under many other strategies.

### Pairs Trading
Pairs trading is a form of **relative value trading.**

Instead of asking whether one asset is cheap on its own, you ask whether **two related assets are mispriced relative to each other.**

The idea is:

- find two assets that usually move together
- wait for them to diverge
- buy the relatively cheap one
- sell the relatively rich one
- profit if the relationship normalises

So you are not necessarily betting that both will rise or both will fall.
You are betting that their **spread or relationship** will revert.

Example:

If two supermarket stocks usually trade in a stable relationship, but one suddenly becomes much more expensive relative to the other, you might short the expensive one and buy the cheap one.

In plain English:

Pairs trading is **trading the gap between related assets,** rather than trading one asset alone.

**Here are some resources to go over.**
Pairs trading: https://hudsonthames.org/definitive-guide-to-pairs-trading/ \
Pairs trading: https://palomar.home.ece.ust.hk/MAFS5310_lectures/slides_pairs_trading.pdf \
Portfolio optimization with Pairs Trading https://portfoliooptimizationbook.com/slides/slides-pairs-trading.pdf \
QuantConnect on Pairs Trading: https://github.com/QuantConnect/Research/blob/master/Analysis/02%20Kalman%20Filter%20Based%20Pairs%20Trading.ipynb \
AJeanis on Pairs Trading: https://github.com/AJeanis/Pairs-Trading \
Ozenc Gungor's repo on Pairs trading: https://github.com/ozencgungor/Pairs_Trading_Kalman \
KidQuant on Pairs trading: https://github.com/KidQuant/Pairs-Trading-With-Python/blob/master/PairsTrading.ipynb \
Awdneyk: https://github.com/Awdneyk/stat-arb-pair-selection


### Momentum trading

Momentum trading is almost the opposite of mean reversion.

Instead of assuming a move has gone too far, momentum assumes:

**a move may continue because strength tends to attract further strength**

The trader looks for evidence that something is already moving with force, and then joins that move.

Examples:

- buying assets breaking upward with strong participation
- selling assets in persistent downtrends
- following medium-term strength across sectors or futures

Momentum can exist over many horizons:

- seconds or minutes in microstructure
- days or weeks in swing trading
- months in medium-term trend following

In plain English:

Momentum trading means **buying strength and selling weakness,** because trends often persist longer than expected.

### Mean reversion trading

Mean reversion trading is based on the idea that price, spread, or some signal can move too far away from its normal level and then come back.

The core belief is:

**extreme moves often partially reverse**

So the trader looks for:

- price far above average
- price far below average
- spread unusually wide or narrow
- short-term imbalance likely to fade

Then the trader positions for a move back toward the mean.

Examples:

- selling after an unusually strong short-term spike
- buying after a temporary overshoot downward
- trading a spread back toward its historical average

In plain English:

Mean reversion is the idea that **what moved too far may snap back.**

It works best when there really is a stable anchor, equilibrium, or repeated pullback behaviour.

### Volatility trading

Volatility trading is not mainly about predicting whether price goes up or down.

It is about predicting **how much price will move.**

A trader in volatility asks questions like:

- Will the market be calmer or wilder than people expect?
- Is implied volatility too high or too low compared with realised volatility?
- Are options overpriced or underpriced relative to expected future movement?

The key point is:

- **directional trading cares about where price goes**
- **volatility trading cares about how much price moves**

Examples:

- buying options when you think future movement will be bigger than the market expects
- selling options when you think implied volatility is overpriced
- trading volatility spreads across strikes, maturities, or related assets

In plain English:

Volatility trading is a bet on **movement intensity**, not just direction.


## Other notes for alpha
Because some of you seem completely convinced **that alpha is the key to godhood**, rather than something that has to coexist with inventory management, I have decided to put together a YouTube playlist and expand this page further.

[IMC Inspirational videos on YouTube](https://www.youtube.com/playlist?list=PLjBE3SzJV9A3ahXCKrEXwG8uKa5fQkDMC)

# Other useful youtube playlists
[Algorithmic game theory](https://www.youtube.com/playlist?list=PLEGCF-WLh2RJBqmxvZ0_ie-mleCFhi2N4)
[EC 2022 talks](https://www.youtube.com/watch?v=OXj5X7kRFwQ&list=PLI0o-KVQWwQ_NOW1JQNU88BzGbxR4yksM)

