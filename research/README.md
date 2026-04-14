# IMC 4

This year @tomas apparently had a hand in mixing up the assets.

Instead of our reliable stationary straight line asset (EMERALDS in the tutorial round), we now have "INTARIAN_PEPPER_ROOT", which is simply the same idea, but adjusted for a linear regression.

We once again have the drifting asset (TOMATOES in the tutorial round), we now have that called "ASH_COATED_OSMIUM", which is the same idea as previous years.

![Pepper Root](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/utils/pepper_root.png)
![Osmium](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/utils/osmium.png)





## Summary of previous tutorial rounds

Across the tutorial rounds, the product design has usually followed a familiar pattern: one relatively stationary asset and one more dynamic asset.
Examples include:

- **IMC 3 / IMC 4:** one stationary product and one dynamic product
- **IMC 2 / IMC 1:** a similar structure appears, though less explicitly

In general, the stationary asset is best handled with straightforward market making and fair-value trading, while the dynamic asset usually requires some combination of trend, mean reversion, spread, or arbitrage logic.

## Round 1

**Core pattern**

Round 1 typically introduces a simple market structure: one stable product and one directional or more volatile product.

### IMC 3

Round 1 introduced **Rainforest Resin, Kelp,** and **Squid Ink.**

- **Rainforest Resin** behaved like a highly stable asset with fair value near 10,000. The strategy was simple: market take when quotes were clearly mispriced relative to fair value, and otherwise market make inside the spread. Standing orders at fair value were also useful for inventory management.
- **Kelp** showed mild drift and modest volatility. A persistent market maker’s mid-price served as a good proxy for fair value, so the same style of market making and taking worked well here too.
- **Squid Ink** was much more volatile, with large short-term swings and little obvious structure at first. Standard indicators such as z-scores, breakout logic, and MACD did not provide a reliable edge. The eventual adjustment was to reduce position sizing and introduce a spike-detection rule based on rolling standard deviation, trading against unusually large moves. This significantly stabilized PnL.

### IMC 2

Round 1 introduced **AMETHYSTS** and **STARFRUIT.**

- **AMETHYSTS** behaved as the stable asset, with trading centered around fair value and order-book mispricings.
- **STARFRUIT** was the dynamic asset, requiring more adaptive estimation of fair value.
- The core framework combined **market making** under normal conditions with **market taking** when quotes were clearly favorable.
- Inventory control mattered heavily, and the teams experimented with theoretical execution models, though simpler approaches ultimately worked just as well.

### IMC 1

Round 1 featured **PEARLS** and **BANANAS.**

- **PEARLS** were essentially stationary around 10,000, making them well suited for simple market making and market taking around a fixed fair value.
- **BANANAS** were more directional, and short-horizon linear regression on recent prices was used to predict near-term movement.
- The result was a classic split: stationary asset traded around fair value, dynamic asset traded with predictive signals.


## Round 2
**Core pattern**

Round 2 generally expands beyond a single dynamic asset and introduces either **cross-asset relationships**, **location arbitrage**, or **basket structures**.

### IMC 3

Round 2 introduced **Croissants, Jams, Djembes,** and two baskets: **PICNIC_BASKET1** and **PICNIC_BASKET2.**
- The main opportunity came from trading the difference between **basket prices** and their **synthetic values** from constituents.
- The strongest signal was mean reversion in the basket premium, rather than forecasting the underlying products directly.
- The final strategy relied on **simple, robust threshold trading**, with light parameter tuning and some signal adjustment using known trader behavior.
- Position limits prevented perfect hedging, so capital allocation across the two baskets and leftover market making became important.

### IMC 2

Round 2 introduced **ORCHIDS** plus environmental and transport variables.
- While there appeared to be many predictive features, they mostly turned out to be distractions.
- The real edge came from understanding the market mechanism: profitable **cross-island arbitrage** between the local and South Archipelago markets.
- Execution quality and quote placement mattered more than forecasting.

### IMC 1

Round 2 introduced **pair trading** opportunities such as **COCONUTS** and **PINA_COLADAS**.
- The core idea was spread trading between related products.
- Momentum approaches were considered, but relative-value trading proved stronger and more reliable.

## Round 3
**Core pattern**

Round 3 often introduces **derivatives** or more structured relative-value products.

### IMC 3

Round 3 introduced **Volcanic Rock** and five **Volcanic Rock Vouchers**, effectively options.

- The strongest edge came from modeling the **volatility smile** and identifying implied-volatility mispricings.
- This supported an **IV scalping** strategy using fair values derived from Black-Scholes.
- A separate mean-reversion signal existed in the underlying, but it was noisier and less reliable.
- The final approach combined strong options-theory-based trading with limited mean-reversion exposure for diversification and relative-risk control.

### IMC 2

Round 3 introduced **GIFT_BASKET, CHOCOLATE, STRAWBERRIES,** and **ROSES.**

- The main opportunity was again the **basket premium**, defined as basket price minus synthetic price.
- The spread appeared to mean revert around a stable premium, making threshold or modified z-score trading effective.
- The team prioritized robust spread trading over full constituent hedging to keep implementation simple and reduce costs.

### IMC 1

Round 3 included products like **BERRIES** and **DIVING_GEAR.**
- These were more signal-driven and less purely structural.
- Timing-based and event-response logic performed well.

## Round 4
Core pattern

Round 4 tends to revolve around **conversion mechanics, location arbitrage,** or more advanced derivative pricing.

### IMC 3

Round 4 introduced **Macarons,** tradable locally and externally.
- Naive arbitrage was profitable, but the real edge came from identifying a **hidden taker bot** that would fill favorable local quotes.
- This meant the optimal strategy was not just conversion arbitrage, but conversion arbitrage with improved local execution.
- Environmental variables were tested but ultimately ignored in favor of the much stronger structural edge.

### IMC 2

Round 4 introduced **COCONUTS** and **COCONUT_COUPONS.**

- This was an options problem centered on implied volatility.
- The team modeled fair option value with **Black-Scholes,** traded deviations in implied volatility, and hedged with the underlying when practical.
- Imperfect delta hedging introduced variance, which hurt realized performance despite strong backtests.

### IMC 1

Round 4 again leaned into **basket/pair structures**, with stronger backtesting and more systematic evaluation.

## Round 5
### Core pattern
Round 5 usually does not introduce new products, but instead adds **trader identity information**, turning market behavior itself into a source of alpha.

### IMC 3
- Public trader IDs made it possible to directly follow profitable bots such as Olivia.
- This improved earlier inference-based signals and reduced false positives.
- In some products, bot-following was weaker than existing market making; in others, it became the dominant signal.
- The round became a balance between exploiting revealed behavioral signals and limiting risk to protect leaderboard position.

### IMC 2
- With all products in play, the team searched for deeper predictive relationships and eventually discovered extremely strong mappings between prior-year data and current-year products.
- This enabled a much more aggressive forecasting and optimization framework, including dynamic programming to maximize execution under position and volume constraints.

### IMC 1
- Trader identities again helped refine signals, especially in products where certain bots consistently traded near turning points.

## Short overall conclusion

Across all years, the tutorial and competition rounds repeatedly reduce to a handful of recurring structures:

- **Stable assets** → trade around fixed fair value with market making and selective market taking
- **Dynamic assets** → use trend, regression, mean reversion, or volatility-based signals
- **Basket products** → trade basket premium versus synthetic value
- **Location arbitrage products** → focus on conversion mechanics and execution quality
- **Options/derivatives** → price implied volatility and hedge exposure carefully
- **Trader ID rounds** → exploit revealed behavioral signals from specific counterparties

The main lesson is that the best strategies usually came not from throwing complex indicators at the data, but from first understanding **how the market was likely generated** and then building the simplest strategy that matched that structure.



### A more general market view

So, you have reached the end of your rope and want to know what to write in your trader without actually doing the work.

Well, I am not going to do that until the round is over.

What I *will* do is keep giving you the same model until you are properly confused.

Markets

### Markets

Let **A** be a market with assets:
- A₁
- A₂
- A₃
- ...
- Aₙ

Each asset may have different properties and behave differently.

We also allow related derivatives and structures:

Let **A₁*** be a derivative of **A₁**, where **A₁** is the underlying asset.
Let **A₂*** be a basket containing **A₂** and some other asset **Aᵢ**.
These constructions can be repeated and do not need to be unique.

### Traders

Let B be a group of traders operating on an exchange **$\alpha$**, associated with market **A**.

The exchange acts as a matching engine for the traders in **B.**

The objective of each trader **b ∈ B** is to optimise a reward function while controlling a loss function.

You already know what this is in practice:

**PnL.**

But the important part is this:

Your profit and loss should not be optimised for a single lucky outcome. They should be optimised for **expected value.**

One or two good trades can make a pony look like a unicorn.

Capturing good trades consistently is what turns the pony into a **legendary quantitative unicorn.**

### Dynamics

We now understand the universe in a broad and admittedly superficial way.

The next goal is to understand the rules governing:

- the market,
- the assets,
- and the competition.

Because we do not only want to profit.

We want to profit **the most**.

This becomes a game of understanding how each asset behaves, and then capturing the safest and most repeatable profits possible.

That is how we uncover **all** the good trades.

Reducing losses — or even reducing the *possibility* of losses — is even better.

So what we really want is the method that yields:

- the **highest expected reward**
- the **lowest expected loss**

A general model of price movement can be useful here. These dynamics may be aggregate in nature, or they may appear as components inside a broader model.

For example:
```
Market state[t+1] \
= immediate order-book matching at t \
\+ order-flow imbalance at t \
\+ drift / trend at t \
\+ mean reversion at t \
\+ diffusion / noise at t \
\+ volatility dynamics at t \
\+ liquidity / market-impact effects at t \
\+ jump or shock components at t \
\+ regime behaviour at t \
\+ cross-asset or exogenous drivers at t
```
One could also map it like this

```
Market state[t+1]\
= microstructure effect\
\+ directional component\
\+ corrective component\
\+ stochastic component\
\+ volatility component\
\+ liquidity / impact component\
\+ jump component\
\+ regime component\
\+ exogenous component
```

This is, of course, a very general model of market prices.

The next question is how to earn from it.

Could we adjust our inventory based on this model?
Could we estimate which asset has the highest probability of a positive return?
Could this framework be applied across many different assets?

Those are the kinds of questions worth exploring.




