## Summary of the tutorial rounds

Across the tutorial rounds, the product design has usually followed a familiar pattern: one relatively stationary asset and one more dynamic asset.
Examples include:

- **IMC 3 / IMC 4:** one stationary product and one dynamic product
- **IMC 2 / IMC 1:** a similar structure appears, though less explicitly

In general, the stationary asset is best handled with straightforward market making and fair-value trading, while the dynamic asset usually requires some combination of trend, mean reversion, spread, or arbitrage logic.

## Round 1

**Core pattern**

Round 1 typically introduces a simple market structure: one stable product and one directional or more volatile product.

### IMC 3

Round 1 introduced Rainforest Resin, Kelp, and Squid Ink.

Rainforest Resin behaved like a highly stable asset with fair value near 10,000. The strategy was simple: market take when quotes were clearly mispriced relative to fair value, and otherwise market make inside the spread. Standing orders at fair value were also useful for inventory management.
Kelp showed mild drift and modest volatility. A persistent market maker’s mid-price served as a good proxy for fair value, so the same style of market making and taking worked well here too.
Squid Ink was much more volatile, with large short-term swings and little obvious structure at first. Standard indicators such as z-scores, breakout logic, and MACD did not provide a reliable edge. The eventual adjustment was to reduce position sizing and introduce a spike-detection rule based on rolling standard deviation, trading against unusually large moves. This significantly stabilized PnL.

### IMC 2

Round 1 introduced AMETHYSTS and STARFRUIT.

AMETHYSTS behaved as the stable asset, with trading centered around fair value and order-book mispricings.
STARFRUIT was the dynamic asset, requiring more adaptive estimation of fair value.
The core framework combined market making under normal conditions with market taking when quotes were clearly favorable.
Inventory control mattered heavily, and the team experimented with theoretical execution models, though simpler approaches ultimately worked just as well.

### IMC 1

Round 1 featured PEARLS and BANANAS.

PEARLS were essentially stationary around 10,000, making them well suited for simple market making and market taking around a fixed fair value.
BANANAS were more directional, and short-horizon linear regression on recent prices was used to predict near-term movement.
The result was a classic split: stationary asset traded around fair value, dynamic asset traded with predictive signals.


## Round 2
Core pattern

Round 2 generally expands beyond a single dynamic asset and introduces either cross-asset relationships, location arbitrage, or basket structures.

### IMC 3

Round 2 introduced Croissants, Jams, Djembes, and two baskets: PICNIC_BASKET1 and PICNIC_BASKET2.

The main opportunity came from trading the difference between basket prices and their synthetic values from constituents.
The strongest signal was mean reversion in the basket premium, rather than forecasting the underlying products directly.
The final strategy relied on simple, robust threshold trading, with light parameter tuning and some signal adjustment using known trader behavior.
Position limits prevented perfect hedging, so capital allocation across the two baskets and leftover market making became important.

### IMC 2

Round 2 introduced ORCHIDS plus environmental and transport variables.

While there appeared to be many predictive features, they mostly turned out to be distractions.
The real edge came from understanding the market mechanism: profitable cross-island arbitrage between the local and South Archipelago markets.
Execution quality and quote placement mattered more than forecasting.

### IMC 1

Round 2 introduced pair trading opportunities such as COCONUTS and PINA_COLADAS.

The core idea was spread trading between related products.
Momentum approaches were considered, but relative-value trading proved stronger and more reliable.

## Round 3
Core pattern

Round 3 often introduces derivatives or more structured relative-value products.

### IMC 3

Round 3 introduced Volcanic Rock and five Volcanic Rock Vouchers, effectively options.

The strongest edge came from modeling the volatility smile and identifying implied-volatility mispricings.
This supported an IV scalping strategy using fair values derived from Black-Scholes.
A separate mean-reversion signal existed in the underlying, but it was noisier and less reliable.
The final approach combined strong options-theory-based trading with limited mean-reversion exposure for diversification and relative-risk control.

### IMC 2

Round 3 introduced GIFT_BASKET, CHOCOLATE, STRAWBERRIES, and ROSES.

The main opportunity was again the basket premium, defined as basket price minus synthetic price.
The spread appeared to mean revert around a stable premium, making threshold or modified z-score trading effective.
The team prioritized robust spread trading over full constituent hedging to keep implementation simple and reduce costs.

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
