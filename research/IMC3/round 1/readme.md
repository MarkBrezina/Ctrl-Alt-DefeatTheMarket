## Detailed Round 1 Summary

Round 1 introduced three products — **Rainforest Resin, Kelp,** and **Squid Ink** — and although all three traded through the same order-book mechanics, they behaved very differently. As a result, teams often ended up using different combinations of **fair-value estimation, market taking, market making, and inventory management** depending on the product.

A broad lesson from the round was that success did not come from complexity for its own sake. The strongest approaches usually began by understanding the market structure properly: how orders were matched, how long orders remained in the book, how positions constrained future trading, and how fair value could best be approximated from the visible order book. Once those mechanics were understood, the product-specific strategy became much clearer.

## 1. Rainforest Resin

Rainforest Resin was by far the simplest product of the round and served as the clearest demonstration of basic market-making principles.

Its true or fair value was effectively fixed at 10,000 and did not drift in any meaningful way. That meant there was no real forecasting problem. There was no need to estimate trend, predict next-step movement, or identify hidden dynamics. The only thing that mattered was whether the currently available prices in the market were favourable relative to this known fair value.

That naturally split trading into two simple activities:

### Market taking

- If an ask appeared below **10,000**, it was profitable to buy it.
- If a bid appeared above **10,000**, it was profitable to sell into it.

These trades were essentially direct arbitrage relative to the known true price. Since the product itself was stable, capturing these mispricings was low risk and mechanically attractive.

### Market making

Because obvious mispricings did not happen at every moment, teams also made markets around 10,000 by posting passive bids below fair value and passive asks above fair value. The key question here became how far away from fair value to quote.

That gave rise to the classic market-making tradeoff:

- quoting closer to fair increased fill probability,
- quoting further away increased profit per fill.

This distance from fair was the **edge**, and much of the optimization for Rainforest Resin was simply about finding the best edge. Many teams used backtests, visual dashboards, and grid search to determine which quoting distance produced the best overall PnL.

### Inventory management

Even though the product itself was simple, inventory management still mattered a great deal. A recurring issue was that traders could get stuck at the position limit, meaning they could no longer take profitable opportunities on one side of the market.

To solve that, many teams added some form of **position-clearing or liquidation** logic. The idea was to sometimes trade at **zero edge** or near-zero edge — for example, at exactly 10,000 — not because the individual trade was especially profitable, but because it reduced inventory and restored the ability to capture future profitable trades. This often improved performance materially.

### Overall role in the round

Rainforest Resin became the cleanest and most reliable source of profits. It rewarded a basic but well-executed strategy:

- take obvious mispricings,
- make markets around fair value,
- clear inventory when necessary.

For many strong teams, Rainforest Resin was one of the largest and most stable contributors to round PnL.

## 2. Kelp

Kelp looked similar to Rainforest Resin at first glance, but it introduced one important complication: **its fair value was not fixed.** Instead, it moved slowly over time, roughly like a mild random walk.

That meant Kelp still behaved like a market-making product, but unlike Rainforest Resin, it required some estimate of the current fair value before trading could be done well.

### Basic character of the product

Kelp was not wildly directional and did not usually display extreme or persistent trends. Its movement was small enough that many teams concluded the product was still best handled with a largely market-making approach, not with heavy directional speculation.

The main problem was therefore not “where will Kelp go over the next long horizon?” but rather:

> what is the best current estimate of fair value, given that the visible order book is noisy?

### Fair-value estimation

This became the central challenge of Kelp.

Some natural first attempts included:

- the raw mid-price,
- a rolling average of the mid-price,
- local smoothing or moving averages,
- microprice or volume-weighted fair values.

However, many teams found that the visible mid-price was noisy because smaller participants often placed orders at odd levels that distorted the best bid and best ask. So while the simple midpoint was available, it was not always the cleanest representation of the real consensus price.

This led stronger teams to look deeper into the order book structure. Several better proxies emerged:

- the midpoint of **large standing bid and ask quotes,**
- the midpoint of the **popular bid and ask prices,**
- the midpoint of a consistent market maker’s quotes,
- filtered order-book levels that ignored small noisy orders.

In other words, instead of trusting the top of the book blindly, teams tried to identify the more meaningful liquidity providers and use their quotes as the fair-value anchor.

Some teams even verified this empirically by comparing their own backtests with the platform’s PnL marking, concluding that the “real” internal fair used by the game was closer to this large-quote midpoint than to the naive visible mid.

### Execution strategy

Once a robust fair-value estimate had been chosen, the strategy for Kelp looked much like Rainforest Resin:

- take obvious favourable quotes relative to fair,
- place passive quotes around fair,
- improve existing quotes by one tick when attractive,
- and manage inventory conservatively.

Because Kelp’s spread was typically tighter than Resin’s, the total profit opportunity was smaller. This meant accurate fair-value estimation mattered more, and there was less room for sloppy quoting.

### Predictability

An important realization for many teams was that there was not much exploitable directional predictability in Kelp. Although the price moved, it did not do so in a consistently forecastable way. The best practical assumption was often that the **current filtered fair value is the best estimate of the next fair value.**

Some minor effects were observed, such as tiny mean-reverting tendencies from integer rounding versus underlying floating-point fair values, but these were usually too small to drive the whole strategy.

### Overall role in the round

Kelp was basically a more subtle version of Rainforest Resin:

- still spread-driven,
- still suitable for market making,
- but much more dependent on choosing the right fair-value proxy.

The teams that did best on Kelp were often those that realized the raw mid-price was too noisy and that the structure of liquidity itself offered a cleaner signal.

## 3. Squid Ink

Squid Ink was the most difficult and most controversial product of the round.

Compared with Rainforest Resin and Kelp, it was much more volatile, had tighter spreads relative to its price movement, and experienced frequent sharp jumps or reversals. This made ordinary market making much less comfortable.

### Basic character of the product

The main difference with Squid Ink was not necessarily that it always had a directional trend, but that its short-term moves were large enough to create a lot more **variance** in realized PnL.

Even if there was no classic adverse selection in every case, being filled passively in Squid Ink could be much riskier because the product might move sharply soon after the trade. So while market making was still possible, it was less stable and less forgiving than for the other two products.

### Mean-reversion interpretations

The product was often described as having some mean-reverting behaviour, and many teams naturally tried to exploit that through:

- rolling z-score reversions,
- moving average deviations,
- volatility spike fades,
- breakout reversal logic,
- pressure-based top-of-book signals,
- SMA or MACD-like indicators.

In some cases this produced reasonable results, but for many teams these signals were inconsistent. Squid Ink often looked chaotic enough that purely statistical short-term signals were hard to trust.

### Divergence in team approaches

This is where team strategies differed the most.

**Approach A: standard mean reversion**

Some teams treated Squid Ink as a high-volatility mean-reverting asset. They would:

- estimate a short rolling mean,
- detect moves several standard deviations away from that mean,
- and trade in the opposite direction, expecting reversion.

This could work in some environments, but it was also risky because Squid Ink’s moves were large and could persist or overshoot enough to cause pain before any reversion happened.

**Approach B: reuse market making logic**

Some teams, unable to find a strong directional signal, simply reused their Resin/Kelp-style market making logic. They would still estimate fair value and quote around it, perhaps with more caution.

This sometimes worked, but usually produced much more volatile outcomes because Squid Ink had less forgiving price action.

**Approach C: behaviour-based signal detection**

The most interesting and arguably strongest edge described in the text came from identifying a **predictable participant pattern** rather than from modelling Squid Ink price directly.

One anonymous trader repeatedly appeared to:

- buy 15 lots at the daily low,
- and sell 15 lots at the daily high.

This was an unusually strong behavioural regularity. Once detected, it gave a far more robust signal than abstract technical indicators. By tracking the running daily minima and maxima, and flagging trades that matched the expected direction and size at these extremes, a team could infer when this trader had likely acted and position accordingly.

Later, when IDs were briefly visible, this trader was identified as Olivia, confirming the pattern.

This transformed Squid Ink from a difficult statistical forecasting problem into a participant-behaviour detection problem.

### Why this mattered

This was a very different style of edge from the other two products.

For Rainforest Resin and Kelp, the edge mainly came from:

- estimating fair value,
- placing good quotes,
- and managing inventory.

For Squid Ink, at least in the strongest account, the edge came from:

- detecting another trader’s systematic behaviour,
- reacting to that behaviour,
- and invalidating signals when the pattern broke.

That made the strategy much more selective and less reliant on direct price forecasting.

### Overall role in the round

Squid Ink was the most difficult product to trade well and often the least uniform across teams. Some teams struggled to find consistent alpha from conventional signals. Others used volatility-based mean reversion. The strongest reported approach was based on behavioural pattern recognition rather than raw time-series modelling.

## Cross-product strategic themes

Across all three products, several common principles kept appearing.

### A. Fair value was central

Every product required some notion of fair value:

- fixed at 10,000 for Rainforest Resin,
- filtered dynamic fair for Kelp,
- more uncertain, strategy-dependent fair or behavioural trigger for Squid Ink.

The quality of fair-value estimation often determined how well a team could separate profitable trades from noise.

### B. Market taking and market making worked together

Strong strategies were rarely only takers or only makers.

They usually:

- took obvious profitable quotes immediately,
- then placed passive orders around fair value to capture spread.

This combination was especially effective in stable or semi-stable products like Rainforest Resin and Kelp.

### C. Inventory management was crucial

Position limits were not just a mechanical rule — they materially affected profitability.

When inventory became too skewed:

- future profitable trades could no longer be taken,
- market-making flexibility dropped,
- risk increased.

So many teams added:

- soft liquidation,
- hard liquidation,
- position-clearing at fair,
- more aggressive quoting to rebalance.

This often improved results significantly.

### D. The order book contained more information than raw price alone

Especially for Kelp, teams found that the visible raw mid-price was often less useful than:

- large quote levels,
- most popular price levels,
- filtered depth,
- stable market-maker quotes.

The order book was not just execution infrastructure; it was also part of the signal.

### E. Simplicity often beat overfitting

A recurring theme in the text is that many sophisticated ideas were tried:

- regression,
- z-scores,
- MACD,
- volatility models,
- OU processes,
- signal engineering.

But the best practical approaches often remained relatively simple:

- fixed or filtered fair value,
- opportunistic taking,
- passive quoting,
- inventory management,
- and in Squid Ink, possibly a very specific behavioural detector.

## Comparison of the three products

### Rainforest Resin
- easiest product
- fixed fair value
- pure market-making / market-taking environment
- no real forecasting required
- very strong and reliable PnL source

### Kelp
- similar structure to Resin
- fair value moved slowly
- main challenge was filtering noise from the order book
- market making remained strong once fair was estimated properly
- tighter spreads reduced total PnL opportunity


### Squid Ink
- much more volatile
- ordinary market making became riskier
- many statistical signals were attempted
- strongest edge may have come from trader-behaviour detection rather than raw price modelling
- more variance and less consensus across teams



Absolutely — here is a **cleaned, structured, and more professional version** of your text, while keeping your ideas and technical meaning intact.

---

## Codes

### Strategy Logic and What Is Worth Keeping

#### RAINFOREST_RESIN

The fair value of **10,000** appears to be universally accepted. The cleanest and most reliable pattern across the larger codebases is:

* Aggressively take any **ask below 10,000** or **bid above 10,000**
* Use **zero-EV clearing**:

  * if long and **10,000** is available in the book, sell there
  * if short, buy there
* Market make at **9,999 / 10,001**

The `StaticTrader` overbid/underbid logic — quoting one tick inside the best away-from-mid order — is clever for improving queue priority, but it is probably more complex than necessary here given that fair value is known almost exactly.

---

#### KELP

The strongest idea across all codebases is the **market-maker mid-price filter**: ignore orders below a volume threshold of roughly **15–20 units** to remove noise and estimate the “real” market-making quote. The exact threshold varies slightly across implementations, so both 15 and 20 are worth testing.

The **mean-reversion beta** — around **-0.229 to -0.293** across codebases — is surprisingly consistent, which suggests it captures a genuine feature of the data. The third codebase, which uses PCA on volume features and predicts future market-maker returns with **beta = -0.2933**, is the most statistically grounded approach. However, it depends on a historical DataFrame being stored correctly and currently suffers from the unbounded-growth bug mentioned earlier.

The `KelpStrategy` deflection mechanism from the large codebase — temporarily avoiding liquidity provision on one side after a sharp move — is also a good idea, as it may reduce adverse selection. That said, the current `deflection_threshold = 0.5` likely needs tuning.

---

#### SQUID_INK

There is strong agreement across codebases that **Olivia is an informed trader worth following**. The cleanest implementation is `SignalSnoopers.get_olivia_signal` from the large codebase: it checks both `market_trades` and `own_trades` and returns `+1`, `-1`, or `0`. When Olivia is active, the most effective response is to go immediately to the position limit at market.

When Olivia is absent, the most robust fallback appears to be the **smoothed z-score** approach from the first codebase:

```python
score = (
    ((hist - hist.rolling(zscore_period).mean()) / hist.rolling(zscore_period).std())
    .rolling(smoothing_period)
    .mean()
    .iloc[-1]
)
```

Using a rolling z-score smoothed over `smoothing_period = 100` substantially reduces noise relative to a raw z-score. The `z_trigger = 3.75` used in the second codebase seems too conservative and would likely produce very few trades. Thresholds closer to the third codebase’s `edge_0 = 2` or the first codebase’s `threshold = 1` seem more practical starting points.

The pressure signal in the fourth codebase — based on tracking market-maker bid and ask level changes over 50 ticks — is an interesting idea, but its construction is fragile. For example, a single large order disappearing from the book can register as strong negative pressure even if price has not actually moved.

---

## Recommended Combination

Based on the above, the strongest combination would be:

| Product              | Fair Value                                |                                  Take |                            Clear |                                Make | Signal                       |
| -------------------- | ----------------------------------------- | ------------------------------------: | -------------------------------: | ----------------------------------: | ---------------------------- |
| **RAINFOREST_RESIN** | Hardcoded at 10,000                       |        Aggressively at 9,999 / 10,001 |                Zero-EV at 10,000 |                      9,999 / 10,001 | None needed                  |
| **KELP**             | Market-maker mid + reversion beta ≈ -0.23 |                            ±1.5 ticks |                        Near fair |     Inside best away-from-mid order | Deflection on sharp moves    |
| **SQUID_INK**        | Smoothed z-score (e.g. 150/100)           | Follow Olivia immediately when active | Mean reversion threshold ≈ 1.5–2 | Avoid making during high volatility | Olivia first, z-score second |

The `Strategy` base class and `StatefulStrategy` pattern from the first codebase provide the cleanest overall architectural foundation. The save/load-by-symbol structure is well designed and avoids a common mistake: failing to persist part of the strategy state.

The `InteractionBlocks` separation in the large codebase is also useful for reuse, although the volcanic-rock hedge routing should be fixed before reusing the option strategies.

One structural improvement worth standardising is the handling of **insufficient history**. Different codebases currently behave differently: some return empty output, some emit neutral signals, and some skip only market making. It would be better to adopt a single convention throughout the framework so that partially initialised models do not accidentally trade.

---

# 1. Architecture and Design

## Strategy abstraction layer

You have built a modular strategy engine with a clear separation of concerns:

* `Strategy` → base execution class
* `StatefulStrategy` → persistence through `traderData`
* `SignalStrategy` → directional strategies (`LONG`, `SHORT`, `NEUTRAL`)
* `MarketMakingStrategy` → fair-value-based quoting

This is a strong design because it separates:

* signal generation
* execution
* state management

## Trader orchestration

The `Trader` class:

* holds one strategy per product
* loads and saves state per product
* runs each strategy independently

This is effectively a **multi-agent trading system**.

## Two overlapping frameworks

The file actually contains two partially overlapping frameworks:

* a clean abstract OOP framework
* a more manual procedural trading system

This reflects an evolution from a cleaner academic design toward more practical trading heuristics.

---

# 2. Core Trading Logic

At the highest level, the system combines three core behaviours:

* **market making**
* **opportunistic taking** for alpha capture
* **inventory clearing / risk management**

## Standard per-product loop

At each timestep, the strategy typically:

1. estimates fair value
2. takes mispriced liquidity
3. clears inventory if needed
4. provides liquidity through market making

This is a classic hybrid of:

**market making + alpha taking + inventory control**

---

# 3. Per-Product Strategy Ideas

## RAINFOREST_RESIN — Stable Asset

### Idea

Fair value is hardcoded at roughly **10,000** and price only deviates meaningfully when the market moves outside a narrow band.

### Strategy

* pure market making
* minor adaptive quoting
* controlled spread placement

### Interpretation

This is your **EMERALDS-style stationary asset**.

* no alpha signal is really needed
* spread capture dominates
* stable PnL is the objective

---

## KELP — Mean-Reverting / Microstructure-Driven

### Idea

Fair value is derived from a **filtered order-book mid**, using:

* volume filtering to ignore small orders
* last price memory
* a reversion beta

### Model

```python
predicted_return = last_return * reversion_beta
fair = mid + mid * predicted_return
```

### Strategy

* trade around predicted mean reversion
* ignore weak liquidity
* use a filtered microstructure-based fair value

### Interpretation

This is a **microstructure-informed short-term mean reversion strategy**.

It:

* filters fake or weak liquidity
* models short-term reversal
* adjusts fair value using recent returns

Its main limitation is that it assumes constant behaviour and does not explicitly distinguish between trend, noise, and volatility spikes.

---

## SQUID_INK — Hybrid Regime Strategy

This is the most advanced strategy in the system.

### Core idea

Market behaviour changes over time, so strategy should adapt to:

* volatility
* trend
* liquidity conditions

### Regime detection

The strategy switches between:

#### 1. High volatility → Mean Reversion

If volatility exceeds a threshold, it trades against deviations from a moving average.

#### 2. Low volatility → Market Making

If volatility remains below the threshold, it reverts to fair-value-based market making.

### Signal components

The strategy combines several elements:

1. **SMA + volatility**
   Detects overextension and drives mean reversion entries.

2. **Market-maker mid-price**
   Uses larger orders to infer “real” price.

3. **Dynamic reversion beta**
   Based on the rolling slope of recent mid-prices, normalised to approximately `[0.02, 0.3]`.

4. **Spread modelling**
   Tracks minimum, maximum, and average spread levels in order to avoid providing liquidity in unstable conditions.

### Interpretation

This is a **state-dependent hybrid strategy** where:

* volatility determines regime
* slope shapes behaviour
* spread controls participation

---

# 4. Execution Logic

## Take logic

The strategy aggressively hits orders when:

* `best_ask <= fair - width`
* `best_bid >= fair + width`

This is classic **value-based taking**.

## Clear logic

Inventory is reduced when price returns near fair value.

This helps prevent:

* inventory drift
* unwanted directional exposure

## Market making

The strategy places symmetric quotes around fair value:

* `bid = fair - edge`
* `ask = fair + edge`

These quotes are then adjusted based on:

* current book levels
* whether to join or step ahead
* spread conditions

## SQUID_INK-specific execution logic

In unstable spread conditions, the strategy disables market making:

```python
if current_max_spread > avg_max_spread + 2:
    skip_mm = True
```

That is a strong practical safeguard against providing liquidity in bad market conditions.

---

# 5. Key Quantitative Ideas Embedded in the Code

This code contains several genuinely interesting ideas:

### 1. Market microstructure filtering

Small orders are ignored so that fair value is based on more meaningful liquidity.

### 2. Short-term return modelling

Recent returns are mapped into expected next-period returns using a reversion beta.

### 3. Dynamic parameter adaptation

Reversion strength depends on trend, and spread conditions affect participation.

### 4. Regime switching

Volatility determines whether the strategy should revert or provide liquidity.

### 5. Inventory-aware trading

All trading is constrained by the position limit and adjusted using current inventory.

### 6. Execution-aware design

The code does not stop at signal generation; it explicitly models interaction with the book, order removal, and fill volumes.

---

# 6. What Is Actually Interesting and Unique

## 1. Separation of fair value and execution

You estimate fair value first, then run:

* take
* clear
* make

That is close to how real prop trading systems are structured.

## 2. “Real liquidity” filtering

Using `abs(volume) >= threshold` is effectively a way of distinguishing meaningful liquidity from noise.

## 3. Dynamic reversion beta

Rather than assuming constant reversion, the strategy adapts reversion strength based on recent slope.

## 4. Spread-based participation filter

The system monitors spread stability and steps away when conditions deteriorate.

## 5. Hybrid strategy layering

SQUID_INK is effectively:

* directional in volatile regimes
* liquidity-providing in calm regimes

That is highly realistic.

---

# High-Level Difference: KELP vs SQUID_INK

| Feature     | KELP                      | SQUID_INK                            |
| ----------- | ------------------------- | ------------------------------------ |
| Core idea   | Mean-reverting fair value | Regime-switching hybrid              |
| Signal type | Continuous                | Discrete + adaptive                  |
| Behaviour   | Always trades around fair | Switches between MM and alpha        |
| Complexity  | Medium                    | High                                 |
| Adaptivity  | Fixed reversion           | Dynamic reversion + regime awareness |

---

## KELP — What It Is Really Doing

KELP is fundamentally saying:

**“The market moves, but tends to revert. Let us estimate that reversion.”**

It:

1. filters for real liquidity
2. computes a market-maker mid-price
3. applies a mean-reversion adjustment

This makes KELP a **microstructure-aware short-term mean-reversion strategy**.

It is simple, consistent, and effective, but not regime aware.

---

## SQUID_INK — What It Is Really Doing

SQUID_INK is saying:

**“The market changes behaviour, so strategy should adapt.”**

It:

1. identifies regime using volatility
2. chooses between mean reversion and market making
3. adjusts fair value using filtered liquidity and dynamic slope
4. monitors spread stability before participating

This makes SQUID_INK a **state-based adaptive strategy**, rather than just a fixed model.

---

# The Deepest Difference

### KELP

**Model-based trading**

You estimate fair value and trade around it.

### SQUID_INK

**State-based trading**

You identify the market condition, choose the right behaviour, and then execute accordingly.

---

# If You Want to Push This Further

The next step would be to replace hard thresholds with smoother, more continuous logic:

* use probabilities instead of binary regime switches
* learn regimes using HMMs or clustering
* replace single-slope trend logic with multi-timescale trend estimates

---

# Improvements

Your framework is already strong structurally. The main improvements now are in:

1. signal quality
2. execution edge
3. state clarity
4. capital allocation

---

## 1. Biggest weakness right now

At the moment, the code still mixes:

* signal generation
* fair value estimation
* execution

inside the same decision logic.

This makes it harder to tell where edge is really coming from and increases the risk of noisy behaviour or overfitting.

### High-impact fix

Split the system into three layers:

1. **Signal layer**
   trend, reversion, volatility, microstructure

2. **Target layer**
   `target_inventory = f(signals)`

3. **Execution layer**
   take, make, clear

That would give every strategy a consistent structure.

---

## 2. KELP — How to Improve It

### Current limitation

KELP relies mostly on a single signal:

* recent return → expected reversion

This assumes behaviour is constant.

### Improvements

* make reversion strength conditional on the size of the move
* combine price reversal with order-book imbalance
* add multi-timescale returns
* incorporate position into signal construction

For example:

```python
signal = -return + 0.5 * imbalance - k * position
```

That would turn KELP into a **flow + price + position-aware mean reversion strategy**.

---

## 3. SQUID_INK — How to Improve It

### Current limitation

SQUID_INK is already adaptive, but still quite threshold-heavy and rule-based.

### Improvements

* smooth regime switching instead of using binary thresholds
* replace SMA triggers with z-scores
* use multi-timescale trend estimation
* make execution spread-aware rather than simply turning MM off
* add directional skew to market making
* most importantly, introduce an explicit **target inventory**

For example:

```python
target = clip(signal * 20, -50, 50)
```

Execution would then work to move current inventory toward this target.

This would make SQUID_INK a **continuous adaptive control system** rather than a threshold-driven heuristic.

---

## 4. Execution Layer Improvements

These apply to both KELP and SQUID_INK:

### Better separation of intent

* **taker** = alpha capture
* **maker** = inventory management

### Smarter taking

Size trades based on edge, not just fixed thresholds.

### Queue-priority awareness

Decide deliberately whether to join or step ahead.

### Dynamic order sizing

Size should depend on signal strength and inventory state.

---

## 5. The Biggest Upgrade

If you make only one structural change, it should be this:

### Move to:

**signals → target inventory → execution**

For example:

```python
signal = w1 * zscore + w2 * imbalance + w3 * trend
target_inventory = clip(signal * scale, -limit, limit)
```

Then execution becomes:

* if target > position → buy
* if target < position → sell

This would unify:

* KELP
* SQUID_INK
* future strategies

under the same framework.

---

## 6. What Would Likely Improve PnL Most

### Highest impact

* target-inventory framework
* combining z-score and imbalance
* execution sizing based on edge

### Medium impact

* multi-timescale trend
* spread-aware quoting
* replacing hard thresholds with smooth transitions

### Lower impact

* minor fair value tweaks
* overly complicated slope logic

---

# Final Takeaway

### KELP should evolve into:

A clean mean-reversion strategy with signal combination and explicit inventory targeting.

### SQUID_INK should evolve into:

A continuous, regime-weighted adaptive strategy with smarter execution.

### The overall system should become:

A unified control framework in which **signals determine desired position**, and **execution moves the portfolio there efficiently**.

---

# Additional Cleaned Notes

## Core Code Structure

The file is structured to separate configuration from execution logic.

### Configuration layer

The `Product` class and the `PARAMS` / `LIMITS` dictionaries define the characteristics of each product. This lets the same execution framework handle both stable and trending assets simply by changing parameters.

### Data processing

The `run` method acts as the entry point and iterates through each `OrderDepth` to calculate the current market state.

### State management

The strategy keeps track of current positions so that it never exceeds the hard inventory limit of 80 units.

---

## Implemented Trading Strategies

The script uses a two-layer market interaction model:

### Passive strategy: quoting / making

The strategy places limit orders around fair value in order to capture spread.

#### Fair value calculation

Fair value is estimated using `fair_value_window`.

#### Inventory skewing

Inventory is incorporated through:

[
P_{\text{skewed}} = P_{\text{fair}} - (\text{inventory} \cdot \text{inventory_skew})
]

If inventory is long, the strategy lowers quoted prices to encourage selling and discourage further buying.

#### Order sizing

The strategy uses `base_make_size` while ensuring that orders never breach `LIMITS`.

### Aggressive strategy: sniping / taking

If the market offers sufficient edge, the strategy switches from making to taking.

* if a quote is sufficiently mispriced relative to fair value, it is immediately hit
* `target_clip_ratio` controls how much liquidity is taken in one go

---

## Product-Specific Logic

| Feature        | Emeralds / Stationary | Tomatoes / Drift                          |
| -------------- | --------------------- | ----------------------------------------- |
| Logic type     | Mean reversion        | Trend-following                           |
| Inventory risk | Lower sensitivity     | Higher sensitivity + trend inventory bias |
| Aggression     | Conservative          | Higher trade size and clip ratio          |

---

## Further Improvements

### 1. Micro-price for better fair value

Rather than using simple mid-price:

[
P_{\text{mid}} = \frac{P_{\text{bid}} + P_{\text{ask}}}{2}
]

consider using the **micro-price**:

[
P_{\text{micro}} = \frac{V_{\text{bid}} \cdot P_{\text{ask}} + V_{\text{ask}} \cdot P_{\text{bid}}}{V_{\text{bid}} + V_{\text{ask}}}
]

This uses volume information and may improve fair-value estimation.

### 2. More sophisticated inventory management

Instead of linear skew, use:

* exponential skew near the position limit
* asymmetric order sizing depending on whether a side increases or reduces risk

### 3. Order-book imbalance

For drifting assets, use:

[
I = \frac{V_{\text{bid}} - V_{\text{ask}}}{V_{\text{bid}} + V_{\text{ask}}}
]

This can be used alongside z-score signals to confirm directional pressure.

### 4. Toxic-flow protection

Monitor fill patterns. If fills become one-sided, widen quoting edges to reduce adverse selection.

### 5. Product correlation / lead-lag

If one product reliably moves before another, use it as a lead signal when estimating fair value.











## Codes


### Strategy Logic & What's Worth Keeping
RAINFOREST_RESIN
The true value of 10000 is universally agreed on. The cleanest pattern (from the last big codebase and fourth) is:

Take any ask < 10000 or bid > 10000 aggressively
Zero-EV clear: if long and 10000 is in the book, sell there; if short, buy there
Market make at 9999 / 10001

The StaticTrader overbid/underbid logic (quoting one tick inside the best away-from-mid order) is smart for queue priority but is more complex than necessary here since the fair value is known precisely.
KELP
The strongest element across all codebases is the mmbot mid-price filter: ignore orders below a volume threshold (15–20 units) to strip out noise traders and get the "real" market maker quote. There's slight disagreement on the threshold — 15 and 20 both appear — worth testing.
The mean reversion beta (~-0.229 to -0.293 across codebases) is remarkably consistent, suggesting this is a real feature of the data. The third codebase (PCA on volume features + future mmbot return prediction with beta=-0.2933) is the most statistically grounded, but it requires the DataFrame history to persist correctly — which has the unbounded growth bug mentioned above.
The KelpStrategy deflection mechanism (skip making on one side when price moves sharply) in the last big codebase is a good idea to prevent adverse selection, though deflection_threshold=0.5 may need tuning.
SQUID_INK
There's strong consensus across codebases that Olivia is an informed trader worth following. The cleanest implementation is SignalSnoopers.get_olivia_signal from the last big codebase — it checks both market_trades and own_trades, returns +1/-1/0. When she's active, go fully to the limit at market.
For when Olivia is absent, the first codebase's smoothed z-score approach is the most robust:
pythonscore = (
    ((hist - hist.rolling(zscore_period).mean()) / hist.rolling(zscore_period).std())
    .rolling(smoothing_period)
    .mean()
    .iloc[-1]
)
Rolling a z-score over smoothing_period=100 reduces noise significantly versus raw z-score. The z_trigger=3.75 in the second codebase seems too conservative — you'll rarely trade. The third codebase's edge_0=2 and the first's threshold=1 are more reasonable entry points.
The pressure signal in the fourth codebase (tracking mmbot bid/ask level changes over 50 ticks) is an interesting idea but the signal construction is fragile — a single large order disappearing from the book registers as negative pressure even if price hasn't moved.

Recommended Combination
Based on all of this, here's what I'd suggest pulling together:
ProductFair valueTakeClearMakeSignalRESIN10000 (hardcoded)aggressively at 9999/10001zero-EV at 100009999/10001none neededKELPmmbot mid + reversion_beta ≈ -0.23±1.5 ticks±0inside best away-from-mid orderdeflection on sharp movesSQUIDsmoothed z-score (period 150/100)follow Olivia immediately when she tradesz-score mean reversion threshold ≈ 1.5–2skip making during high volatilityOlivia first, z-score second
The Strategy base class and StatefulStrategy pattern from the first codebase is the cleanest architectural foundation — the save/load per-symbol pattern is well-structured and avoids the common bug of forgetting to persist some piece of state.
The InteractionBlocks separation from the last big codebase is good for reuse, but fix the volcanic rock hedge routing before using the option strategies.
One structural thing worth standardizing: every codebase handles the "not enough history yet" case differently (some return empty, some return neutral signal, some skip making). Pick one convention and apply it consistently so you don't accidentally trade with a half-initialized model.



## 1) Architecture / Design
🔹 Strategy abstraction layer

You built a modular strategy engine:

Strategy → base execution class
StatefulStrategy → persistence via traderData
SignalStrategy → directional strategies (LONG / SHORT / NEUTRAL)
MarketMakingStrategy → fair-value based quoting

👉 This is very clean separation of concerns:

signal generation
execution
state management
🔹 Trader orchestration

The Trader class:

Holds one strategy per product
Loads/saves state per product
Runs each independently

→ This is basically a multi-agent trading system

🔹 Two layers exist in the file

You actually have two frameworks overlapping:

Abstract OOP framework (clean)
Manual procedural trading system (more complex)

This shows evolution:

from clean academic design
to practical trading heuristics
2) Core Trading Logic

At the highest level, your system combines:

🧠 Three core behaviours
Market making
Opportunistic taking (alpha capture)
Inventory clearing / risk management
🔁 Standard loop per product

Each timestep:

Estimate fair value
Take mispriced liquidity
Clear inventory if needed
Provide liquidity (market make)

This is a classic:

MM + alpha-taking + inventory control hybrid

3) Per-Product Strategy Ideas
🌳 RAINFOREST_RESIN (Stable Asset)
Idea:
Hard-coded fair value ≈ 10,000
Only deviates if market moves outside ±5
Strategy:
Pure market making
Slight adaptive quoting:
Push quotes away if too close
Maintain spread control
Interpretation:

This is your “EMERALDS-style” stationary asset

✔ No alpha needed
✔ Pure spread capture
✔ Stable PnL maximisation

🌊 KELP (Mean-Reverting / Microstructure Driven)
Idea:
Fair value = filtered order book mid
Uses:
volume filtering (ignore small orders)
last price memory
reversion beta
Key model:
predicted_return = last_return * reversion_beta
fair = mid + mid * predicted_return
Strategy:
Trade around predicted reversion
Ignore weak liquidity (noise filtering)
Interpretation:

This is microstructure-informed mean reversion

✔ Filters fake liquidity
✔ Uses short-term return reversal
✔ Memory-based adjustment

🦑 SQUID_INK (Hybrid Regime Strategy)

This is the most advanced part of your system.

🧠 Regime detection

You switch between:

1. High volatility → Mean Reversion
if volatility > threshold:
    trade against deviation from SMA
2. Low volatility → Market Making
else:
    run MM + fair value + execution engine
📊 Signal components
1. SMA + volatility
Detects overextension
Triggers mean reversion trades
2. Market maker mid-price
Filters for large players
Uses only “real liquidity”
3. Dynamic reversion beta
Based on rolling slope of mid prices
Normalised into range ~[0.02, 0.3]
trend ↑ → positive beta
trend ↓ → negative beta

👉 This is very interesting:

You adapt reversion strength based on trend

📉 Spread modelling

Tracks:

min spread
max spread
averages

Used to:

avoid trading in unstable spread conditions
skip MM if spread too wide
Interpretation:

This is a state-dependent hybrid system:

volatility → regime
slope → behaviour
spread → participation filter
4) Execution Logic (Very Important)
🔴 Take logic (alpha capture)

You:

Hit orders when:
best_ask <= fair - width
best_bid >= fair + width

✔ Classic value-based taking

🟡 Clear logic (inventory control)

You:

Reduce inventory when:
price returns near fair

✔ This prevents:

inventory drift
adverse exposure
🟢 Market making

You:

Post symmetric quotes:
bid = fair - edge
ask = fair + edge

BUT adjust for:

existing book levels
join vs step ahead logic
spread conditions
🧠 Special logic (SQUID_INK)

You disable MM when spread is unstable:

if current_max_spread > avg_max_spread + 2:
    skip MM

👉 This is very strong practical intuition

5) Key Quantitative Ideas Embedded

This file actually encodes a lot of deep ideas:

📌 1. Market microstructure filtering
Ignore small orders → reduce noise
Use “real liquidity” as signal
📌 2. Short-term return modelling
return_t → return_{t+1} via beta
📌 3. Dynamic parameter adaptation
Reversion strength depends on trend
Spread affects participation
📌 4. Regime switching
volatility → mean reversion
calm → market making
📌 5. Inventory-aware trading

Everything is constrained by:

position_limit

and adjusted via:

to_buy = limit - position
to_sell = limit + position
📌 6. Execution-aware design

You don’t just generate signals—you:

simulate order book interaction
remove liquidity from book
track volumes
6) What’s Actually Interesting / Unique

This is where your thinking stands out:

⭐ 1. Separation of fair value vs execution

You:

estimate fair value
then run three layers:
take
clear
make

👉 This is very close to real prop trading systems

⭐ 2. “Real liquidity” filtering

Using:

abs(volume) >= threshold

This is essentially:

detecting informed vs noise orders

⭐ 3. Dynamic reversion beta

This is subtle and powerful:

You don’t assume constant mean reversion
You learn it from recent slope

👉 This is halfway to:

adaptive models
regime-aware signals
⭐ 4. Spread-based participation filter

You:

measure spread stability
avoid trading in bad conditions

👉 This is very realistic microstructure behaviour

⭐ 5. Hybrid strategy layering

SQUID_INK is effectively:

if volatile → trade signal
else → provide liquidity

👉 This is exactly what good HFT systems do.

🟢 High-level difference
Feature	KELP	SQUID_INK
Core idea	Mean-reverting fair value	Regime-switching hybrid
Signal type	Continuous (returns → fair)	Discrete (volatility + SMA + slope)
Behaviour	Always trading around fair	Switches between MM and alpha
Complexity	Medium	High
Adaptivity	Fixed reversion	Dynamic reversion + regime
🌊 KELP — What it is really doing
🧠 Core idea:

“The market moves, but tends to revert — let’s estimate that reversion.”

1) Fair value construction

KELP does NOT just use mid price.

It builds:

Step 1 — Filter “real liquidity”
filtered_ask = prices with volume >= adverse_volume
filtered_bid = prices with volume >= adverse_volume

👉 Meaning:

Ignore small orders (noise)
Only trust large participants
Step 2 — Compute "market maker mid"
mmmid_price = (mm_ask + mm_bid) / 2

Fallback:

If no large orders → use last price or simple mid
Step 3 — Apply mean reversion
last_returns = (current_mid - last_mid) / last_mid
pred_returns = last_returns * reversion_beta
fair = current_mid + current_mid * pred_returns

👉 Interpretation:

If price went up → expect it to go down (negative beta)
If price went down → expect bounce
🔁 Behaviour
Always doing:
Mean reversion trading
Around dynamically adjusted fair value
📈 What strategy this is

KELP is basically:

Microstructure-aware short-term mean reversion

✔ Uses:

order book filtering
last return
linear reversion

❌ Does NOT:

detect regimes
adapt behaviour
⚠️ Key limitation
Assumes constant behaviour
No distinction between:
trend
noise
volatility spikes
🦑 SQUID_INK — What it is really doing

This is MUCH more advanced.

🧠 Core idea:

“Market behaviour changes — adapt strategy depending on volatility, trend, and liquidity.”

1) First layer: REGIME DETECTION
Volatility-based switch
if volatility > threshold:
    → mean reversion
else:
    → market making
🟥 High volatility → Mean Reversion

You compute:

SMA of price
deviation from SMA
volatility

Then:

if price >> SMA → short
if price << SMA → long

👉 This is classic:

Stat arb / mean reversion in volatile regimes

🟩 Low volatility → Market Making

You switch to:

fair value model
take / clear / make

👉 This is:

Liquidity provision in stable regime

2) Fair value model (more advanced than KELP)
Step 1 — Same filtering idea
Ignore small orders
Use large orders → “real price”
Step 2 — Track spreads

You store:

min_spread
max_spread
avg_min_spread
avg_max_spread

👉 This lets you:

detect unstable markets
avoid bad conditions
Step 3 — Dynamic trend detection

You compute slope of recent mid prices:

slope = linear regression over last ~3-4 points

Then normalize it:

norm_slope ∈ [0.02, 0.3] with sign
Step 4 — Dynamic reversion
pred_returns = last_returns * norm_slope

👉 Key idea:

Trend	Behaviour
Strong trend	weak reversion (or trend-following bias)
Weak trend	stronger reversion
3) Spread-based participation filter

This is BIG:

if current_max_spread > avg_max_spread + 2:
    skip market making

👉 Meaning:

If market becomes unstable → step out
4) Execution stack (same structure, smarter inputs)

In low vol regime:

Take mispricing
Clear inventory
Market make

BUT:

Quotes depend on spread
Participation depends on stability
Fair value depends on trend
🔁 Behaviour

SQUID_INK behaves like:

🟥 Volatile regime:
directional trades (mean reversion)
aggressive entries
🟩 Calm regime:
passive liquidity provision
spread capture
⚠️ Unstable spread:
reduce / stop trading
🔥 Key Differences (Deep View)
1. Static vs Dynamic model
KELP:
fair = mid + β * return
β is constant
Always same logic
SQUID_INK:
β = function(trend)
strategy = function(volatility)
participation = function(spread)

👉 Much more adaptive

2. Single-mode vs Multi-mode
KELP:
Always mean reversion
SQUID_INK:
Mean reversion (high vol)
Market making (low vol)
No trading (bad spread)
3. Signal richness
KELP uses:
last return
filtered mid
SQUID_INK uses:
volatility
SMA deviation
trend (slope)
spread structure
filtered mid
memory
4. Risk management
KELP:
implicit (via fair value)
SQUID_INK:
explicit:
volatility filter
spread filter
position limits
safe_order()
5. Market understanding
KELP assumes:

“Market is mean reverting”

SQUID_INK assumes:

“Market has regimes:

noisy → revert
calm → provide liquidity
unstable → step away”
🧠 Intuition Summary
🌊 KELP

Think:

“The market wobbles — I fade it.”

Simple
consistent
predictable
🦑 SQUID_INK

Think:

“The market changes behaviour — I adapt.”

detect regime
choose strategy
adjust aggressiveness
🚨 The most important conceptual difference
KELP:

Model-based trading

You estimate a fair value and trade around it.

SQUID_INK:

State-based trading

You:

Identify market condition
Choose strategy
Execute differently
If you want to push this further

The next level would be:

Replace hard thresholds with probabilities
Learn regimes via:
HMM
clustering
Replace slope → multi-timescale trend

I’ll be direct:
Your framework is already strong structurally. The improvements now are about:

(1) signal quality, (2) execution edge, (3) state clarity, (4) capital allocation

🧠 1. Biggest weakness right now
You are mixing:
signal generation
fair value
execution

👉 inside the same logic

This creates:

noisy signals
overfitting behaviour
unclear edge attribution
🔧 Fix (high impact)

Split everything into three clean layers:

1) Signal layer
trend
reversion
volatility
microstructure
2) Target layer
target_inventory = f(signals)
3) Execution layer
take / make / clear

👉 Right now:

KELP = mostly signal → execution directly
SQUID = partially separated

You want:

all strategies → target inventory → execution

🌊 2. KELP — How to improve it
❌ Current limitation
Single signal:
return → mean reversion
Assumes constant behaviour
✅ Improvement 1: Add state awareness

Even simple:

if abs(return) > threshold:
    reversion_strength ↑
else:
    reversion_strength ↓

👉 Makes reversion conditional

✅ Improvement 2: Add imbalance

You already compute this elsewhere — plug it in:

signal = 
    - return_component
    + imbalance_component

Example:

imbalance = (bid_vol - ask_vol) / (bid_vol + ask_vol)

signal = -return + 0.5 * imbalance

👉 Now you combine:

flow (who is pushing)
price (what happened)
✅ Improvement 3: Multi-timescale reversion

Right now:

last_return → prediction

Better:

short_return + medium_return

Example:

r1 = return_1
r5 = return_5

signal = -0.7*r1 - 0.3*r5
✅ Improvement 4: Position-aware reversion

Right now:

KELP ignores inventory when generating signal

Fix:

adjusted_signal = signal - k * position

👉 Prevents:

over-accumulation
runaway exposure
🧠 Result

KELP becomes:

Flow + price + position-aware mean reversion

🦑 3. SQUID_INK — How to improve it
❌ Current limitation

You already have:

regime switching
slope
volatility
spread

BUT:

👉 It is still:

rule-based
threshold-heavy
slightly inconsistent
✅ Improvement 1: Smooth regime switching

Right now:

if vol > threshold:
    mean reversion
else:
    market making

This is too binary.

Replace with:
alpha = sigmoid(volatility)

strategy_weight = alpha * reversion + (1 - alpha) * market_making

👉 You blend instead of switch

✅ Improvement 2: Replace SMA with Z-score

You already do this elsewhere — unify it:

z = (price - mean) / std

Then:

signal = -z

👉 Much cleaner than:

SMA + trigger + threshold
✅ Improvement 3: Better trend modelling

Right now:

slope over ~3–4 points → noisy
Replace with:
trend = weighted combination of:
    slope_50
    slope_100
    slope_200

👉 You already started this idea earlier — this is where it belongs.

✅ Improvement 4: Spread-aware execution (not just filter)

Right now:

if spread too large → skip

Better:

spread_factor = current_spread / avg_spread

edge = base_edge * spread_factor

👉 Wider spread → quote wider, not stop

✅ Improvement 5: Directional MM skew

Right now:

MM is symmetric
Add:
if signal > 0:
    bid more aggressive
    ask more passive

Example:

bid = fair - edge + skew
ask = fair + edge + skew
✅ Improvement 6: Inventory target (CRITICAL)

Right now:

SQUID_INK trades opportunistically

Better:

target_inventory = f(signal)

Example:

target = clip(signal * 20, -50, 50)

Then execution tries to move toward target.

🧠 Result

SQUID_INK becomes:

Continuous adaptive system instead of threshold system

🔁 4. Execution layer improvements (applies to BOTH)
✅ Improvement 1: Separate maker vs taker intent

Right now:

both mixed
Define:
Taker → alpha capture
Maker → inventory management
✅ Improvement 2: Smarter taking

Instead of:

if price <= fair - width:
    buy

Use:

edge = fair - price

size = f(edge)

Example:

size = min(max_size, k * edge)
✅ Improvement 3: Queue priority awareness

Right now:

you just place orders

Better:

if joining → match price
if stepping → improve by 1 tick
✅ Improvement 4: Dynamic order sizing

Instead of constant size:

size = base_size * signal_strength
🧠 5. The BIG upgrade (if you do one thing)
Move to:
signals → target_inventory → execution
Example pipeline
signal =
    w1 * zscore
  + w2 * imbalance
  + w3 * trend

target_inventory = clip(signal * scale, -limit, limit)

Then:

delta = target - position
if delta > 0 → buy
if delta < 0 → sell

👉 This unifies EVERYTHING:

KELP
SQUID
future strategies
🚀 6. What actually improves PnL most

If I had to rank:

🥇 Highest impact
Target inventory framework
Signal combination (imbalance + z-score)
Execution sizing based on edge
🥈 Medium impact
Multi-timescale trend
Spread-aware quoting
Removing hard thresholds
🥉 Lower impact
Fancy fair value tweaks
Overcomplicated slope logic
🔚 Final takeaway
🌊 KELP → evolve into:

Clean mean-reversion signal + inventory targeting

🦑 SQUID_INK → evolve into:

Continuous regime-weighted system with adaptive execution

🧠 Your system overall should become:

A unified control system where
signals determine desired position,
and execution moves you there optimally.




1. Core Code StructureThe file is structured to separate configuration (parameters) from execution logic (the Trader class).Configuration Layer: The Product class and PARAMS/LIMITS dictionaries define the "personality" of each product. This allows the same logic to handle a stable asset (Emeralds) and a trending asset (Tomatoes) simply by swapping values.Data Processing: The run method (the entry point) iterates through the OrderDepth for each product, calculating the current market state.State Management: The algorithm tracks its own positions for every product to ensure it never exceeds the hard limit of 80 units.2. Implemented Trading StrategiesThe script utilizes a dual-layered approach to interact with the market:Passive Strategy: Quoting (Making)The primary goal is to provide liquidity. The algorithm places Limit Orders on both sides of the "fair value" to capture the spread.Fair Value Calculation: It determines the mid-price based on the fair_value_window.Price Skewing: This is the "brain" of the risk management. It calculates a skewed price based on current inventory:$$P_{skewed} = P_{fair} - (\text{inventory} \cdot \text{inventory\_skew})$$If the algorithm is "long" (holds positive inventory), it lowers its prices to encourage selling and discourage further buying.Order Sizing: It uses base_make_size to determine how many units to offer, ensuring the total doesn't breach the LIMITS.Aggressive Strategy: Sniping (Taking)If the market price moves beyond a certain threshold, the algorithm switches from "making" to "taking".The Edge: If an existing order in the book provides a profit greater than the take_width or default_edge, the algorithm will immediately "hit" that order using a Market Order.Volume Control: The target_clip_ratio dictates how much of the available volume the algorithm is willing to "take" in a single trade (e.g., 80% for Tomatoes vs. 35% for Emeralds).3. Product-Specific LogicThe code differentiates its behavior based on the style parameter:FeatureEmeralds (Stationary)Tomatoes (Drift)Logic TypeMean-ReversionTrend-FollowingInventory RiskLower sensitivity (3.0); assumes price returns to center.Higher sensitivity (4.0) plus trend_inventory_sensitivity (35.0).AggressionConservative; smaller trade sizes and lower clip ratios.High; larger sizes and 80% clip ratio to catch moving trends.4. Key Logic Flow (Pseudocode)For every market update:Update Position: Check current holdings from the previous state.Calculate Fair Price: Look at the best bid/ask to find the mid-point.Aggressive Check: Can we "take" any existing orders for an immediate profit? If yes, append orders.Passive Check: Where should we "make" new orders? Calculate the skewed_price based on inventory and place limit orders at the join_edge or default_edge.Limit Check: Ensure orders + current_position $\leq 80$.



## improvements

1. Kelp Strategy: The Filtered Mean-ReverterThe Kelp strategy is a specialized market maker that ignores "noise" in the order book. It operates under the assumption that the price will consistently revert to a mean determined by larger, more stable market participants.Adverse Volume Filtering: Kelp doesn't calculate its fair value based on the top of the book. Instead, it scans for orders with a volume of at least 15. This filters out small retail trades and focuses on where "institutional-sized" orders are sitting.Static Mean Reversion: It uses a fixed reversion_beta of $-0.229$. This means if the price moves up by 1%, the algorithm predicts it will drop by $0.229\%$ in the next interval, adjusting its quotes downward to stay ahead of the curve.Predictive Logic: It calculates "returns" between the current filtered mid-price and the last recorded price to forecast the "true" fair value for the next tick.2. Squid Ink Strategy: The Adaptive Regime-SwitcherSquid Ink is a much more complex "regime-aware" strategy. It switches its behavior based on market conditions, making it more robust during chaotic price movements.Regime Switching (Volatility Filter): The code implements a volatility threshold (set to 3).In Low Volatility: It acts as a market maker using a dynamic fair value.In High Volatility: It switches to a Mean-Reversion strategy based on a Simple Moving Average (SMA) calculated over a 350-period window.Dynamic Regression: Unlike Kelp’s static beta, Squid Ink calculates a linear regression slope of the last four mid-prices. It uses this slope to create a dynamic_reversion_beta (normalized between $0.02$ and $0.3$), allowing the strategy to become more or less aggressive based on how fast the trend is moving.Z-Score Signal: In its alternative implementation, it uses a Z-score (period 150) to identify "oversold" or "overbought" conditions. If the Z-score exceeds 1.0, it enters a directional trade (Long or Short) rather than just market making.3. Key Technical DifferencesFeatureKelpSquid InkPrimary LogicFixed Mean-ReversionAdaptive Regime-SwitchingHistory Window1 (Last Price)4 (Regression) to 350 (SMA)Volume Filter$\geq 15$ units$\geq 18$ unitsBeta CalculationStatic ($-0.229$)Dynamic (based on slope)Volatility Aware?NoYes (Threshold = 3)Take Width1.55.0 (Higher "edge" required)Summary of BehaviorKelp behaves like a stubborn anchor; it assumes big orders are right and expects the market to keep returning to them.Squid Ink behaves like a tactical scout; it watches the trend, calculates the speed of the market (slope), and changes its entire trading style if things get too volatile.Does the dynamic regression logic in the Squid Ink strategy make sense, or would you like to see how it calculates that norm_slope variable in the code?

1. Price Discovery: The "Micro-price"Currently, your strategies mostly use the mid-price: $\frac{\text{Best Bid} + \text{Best Ask}}{2}$. However, the mid-price ignores the volume available at those prices. If there are 100 units at the bid and only 1 unit at the ask, the price is likely about to move up.Improvement: Implement the Micro-price. It weights the price by opposite volume:$$P_{micro} = \frac{V_{bid} \cdot P_{ask} + V_{ask} \cdot P_{bid}}{V_{bid} + V_{ask}}$$Using this as your "true value" in Kelp or RainforestResin will let you adjust your quotes before the mid-price even moves.2. Sophisticated Inventory ManagementBoth untitled0.py and untitled1.py use a fairly linear inventory skew. The problem with linear skew is that it treats the first 10 units of risk the same as the last 10 units before you hit your LIMIT.Improvement: Exponential Skewing.As you approach your limit (80), you should increase your "aggression" exponentially to get back to neutral.Asymmetric Offsets: Instead of just moving your price, you can also shrink your make_size on the side that increases your risk and increase it on the side that reduces it.3. Order Book Imbalance (OBI)This is a powerful signal for "drifting" products like Tomatoes. It measures the "pressure" in the book.Improvement: Calculate the imbalance ratio:$$I = \frac{V_{bid} - V_{ask}}{V_{bid} + V_{ask}}$$If $I > 0.4$, the market is heavily weighted toward buyers. You should move your "fair value" up immediately.You can use this to improve Squid Ink’s get_signal method by combining the Z-score with an Imbalance check to confirm the move isn't a "fake-out."4. Protecting Against "Toxic Flow" (Adverse Selection)In Kelp, you have an adverse_volume filter. This is a good start, but it’s static. If a high-frequency trader starts "snipping" your orders, you’ll get "run over" (filled right before the price crashes).Improvement: Dynamic Spread Widening.Monitor the frequency of your fills.If you get filled on the bid and ask within a few milliseconds, the market is volatile but stable (good for profit).If you get filled only on the bid 5 times in a row, you are likely being picked off by a trend.The Fix: Automatically widen your default_edge or take_width when you notice "one-sided" fill activity.5. Product Correlation (Lead-Lag)In untitled1.py, you trade multiple products. Markets rarely move in isolation.Improvement: Look for correlations. If RAINFOREST_RESIN consistently moves 2 seconds before KELP, you can use the Resin price as a "lead" signal for your Kelp fair value calculation.Check if one product’s slope (from your Squid Ink logic) can predict the other's direction.Summary of Recommended UpgradesStrategy ComponentCurrent StateImproved StateFair ValueMid-priceMicro-price (Volume-weighted)InventoryLinear SkewExponential Skew + Asymmetric SizingSignal ConfirmationZ-Score / SMAZ-Score + Order Book ImbalanceRisk ControlHard LimitsDynamic Edge (Widening during toxic flow)



class Strategy[T: JSON]:
    def __init__(self, symbol: str, limit: int) -> None:
        self.symbol = symbol
        self.limit = limit

    @abstractmethod
    def act(self, state: TradingState) -> None:
        raise NotImplementedError()

    def run(self, state: TradingState) -> tuple[list[Order], int]:
        self.orders = list[Order]()
        self.conversions = 0

        self.act(state)

        return self.orders, self.conversions

    def buy(self, price: int, quantity: int) -> None:
        self.orders.append(Order(self.symbol, price, quantity))

    def sell(self, price: int, quantity: int) -> None:
        self.orders.append(Order(self.symbol, price, -quantity))

    def convert(self, amount: int) -> None:
        self.conversions += amount

    def get_mid_price(self, state: TradingState, symbol: str) -> float:
        order_depth = state.order_depths[symbol]
        buy_orders = sorted(order_depth.buy_orders.items(), reverse=True)
        sell_orders = sorted(order_depth.sell_orders.items())

        popular_buy_price = max(buy_orders, key=lambda tup: tup[1])[0]
        popular_sell_price = min(sell_orders, key=lambda tup: tup[1])[0]

        return (popular_buy_price + popular_sell_price) / 2


class StatefulStrategy[T: JSON](Strategy):
    @abstractmethod
    def save(self) -> T:
        raise NotImplementedError()

    @abstractmethod
    def load(self, data: T) -> None:
        raise NotImplementedError()


class Signal(IntEnum):
    NEUTRAL = 0
    SHORT = 1
    LONG = 2


class SignalStrategy(StatefulStrategy[int]):
    def __init__(self, symbol: Symbol, limit: int) -> None:
        super().__init__(symbol, limit)

        self.signal = Signal.NEUTRAL

    @abstractmethod
    def get_signal(self, state: TradingState) -> Signal | None:
        raise NotImplementedError()

    def act(self, state: TradingState) -> None:
        new_signal = self.get_signal(state)
        if new_signal is not None:
            self.signal = new_signal

        position = state.position.get(self.symbol, 0)
        order_depth = state.order_depths[self.symbol]

        if self.signal == Signal.NEUTRAL:
            if position < 0:
                self.buy(self.get_buy_price(order_depth), -position)
            elif position > 0:
                self.sell(self.get_sell_price(order_depth), position)
        elif self.signal == Signal.SHORT:
            self.sell(self.get_sell_price(order_depth), self.limit + position)
        elif self.signal == Signal.LONG:
            self.buy(self.get_buy_price(order_depth), self.limit - position)

    def get_buy_price(self, order_depth: OrderDepth) -> int:
        return min(order_depth.sell_orders.keys())

    def get_sell_price(self, order_depth: OrderDepth) -> int:
        return max(order_depth.buy_orders.keys())

    def save(self) -> int:
        return self.signal.value

    def load(self, data: int) -> None:
        self.signal = Signal(data)


class MarketMakingStrategy(Strategy):
    def __init__(self, symbol: Symbol, limit: int) -> None:
        super().__init__(symbol, limit)

    @abstractmethod
    def get_true_value(self, state: TradingState) -> float:
        raise NotImplementedError()

    def act(self, state: TradingState) -> None:
        true_value = self.get_true_value(state)

        order_depth = state.order_depths[self.symbol]
        buy_orders = sorted(order_depth.buy_orders.items(), reverse=True)
        sell_orders = sorted(order_depth.sell_orders.items())

        position = state.position.get(self.symbol, 0)
        to_buy = self.limit - position
        to_sell = self.limit + position

        max_buy_price = int(true_value) - 1 if true_value % 1 == 0 else floor(true_value)
        min_sell_price = int(true_value) + 1 if true_value % 1 == 0 else ceil(true_value)

        for price, volume in sell_orders:
            if to_buy > 0 and price <= max_buy_price:
                quantity = min(to_buy, -volume)
                self.buy(price, quantity)
                to_buy -= quantity

        if to_buy > 0:
            price = next((price + 1 for price, _ in buy_orders if price < max_buy_price), max_buy_price)
            self.buy(price, to_buy)

        for price, volume in buy_orders:
            if to_sell > 0 and price >= min_sell_price:
                quantity = min(to_sell, volume)
                self.sell(price, quantity)
                to_sell -= quantity

        if to_sell > 0:
            price = next((price - 1 for price, _ in sell_orders if price > min_sell_price), min_sell_price)
            self.sell(price, to_sell)


class RainforestResinStrategy(MarketMakingStrategy):
    def get_true_value(self, state: TradingState) -> float:
        expected_true_value = 10_000
        max_delta = 5

        mid_price = self.get_mid_price(state, self.symbol)
        if (expected_true_value - max_delta) <= mid_price <= (expected_true_value + max_delta):
            return expected_true_value

        return mid_price


class KelpStrategy(MarketMakingStrategy):
    def get_true_value(self, state: TradingState) -> float:
        return self.get_mid_price(state, self.symbol)


class SquidInkStrategy(SignalStrategy, StatefulStrategy[dict[str, Any]]):
    def __init__(self, symbol: Symbol, limit: int) -> None:
        super().__init__(symbol, limit)

        self.history: list[float] = []

    def get_signal(self, state: TradingState) -> Signal | None:
        self.history.append(self.get_mid_price(state, self.symbol))

        zscore_period = 150  # opt: int(50, 300, step=50)
        smoothing_period = 100  # opt: int(50, 300, step=50)
        threshold = 1  # opt: float(1, 3, step=0.25)

        required_history = zscore_period + smoothing_period
        if len(self.history) < required_history:
            return
        if len(self.history) > required_history:
            self.history.pop(0)

        hist = pd.Series(self.history)
        score = (
            ((hist - hist.rolling(zscore_period).mean()) / hist.rolling(zscore_period).std())
            .rolling(smoothing_period)
            .mean()
            .iloc[-1]
        )

        if score < -threshold:
            return Signal.LONG

        if score > threshold:
            return Signal.SHORT

    def save(self) -> dict[str, Any]:
        return {"signal": SignalStrategy.save(self), "history": self.history}

    def load(self, data: dict[str, Any]) -> None:
        SignalStrategy.load(self, data["signal"])
        self.history = data["history"]


class Trader:
    def __init__(self) -> None:
        limits = {
            "RAINFOREST_RESIN": 50,
            "KELP": 50,
            "SQUID_INK": 50,
        }

        self.strategies: dict[Symbol, Strategy] = {
            symbol: clazz(symbol, limits[symbol])
            for symbol, clazz in {
                "RAINFOREST_RESIN": RainforestResinStrategy,
                "KELP": KelpStrategy,
                "SQUID_INK": SquidInkStrategy,
            }.items()
        }

    def run(self, state: TradingState) -> tuple[dict[Symbol, list[Order]], int, str]:
        orders = {}
        conversions = 0

        old_trader_data = json.loads(state.traderData) if state.traderData != "" else {}
        new_trader_data = {}

        for symbol, strategy in self.strategies.items():
            if isinstance(strategy, StatefulStrategy) and symbol in old_trader_data:
                strategy.load(old_trader_data[symbol])

            if (
                symbol in state.order_depths
                and len(state.order_depths[symbol].buy_orders) > 0
                and len(state.order_depths[symbol].sell_orders) > 0
            ):
                strategy_orders, strategy_conversions = strategy.run(state)
                orders[symbol] = strategy_orders
                conversions += strategy_conversions

            if isinstance(strategy, StatefulStrategy):
                new_trader_data[symbol] = strategy.save()

        trader_data = json.dumps(new_trader_data, separators=(",", ":"))

        logger.flush(state, orders, conversions, trader_data)
        return orders, conversions, trader_data

class Product:
    CROISSANTS = "CROISSANTS"
    JAMS = "JAMS"
    DJEMBES = "DJEMBES"
    PICNIC_BASKET1 = "PICNIC_BASKET1"
    PICNIC_BASKET2 = "PICNIC_BASKET2"
    RAINFOREST_RESIN = "RAINFOREST_RESIN"
    KELP = "KELP"
    SQUID_INK = "SQUID_INK" 

PARAMS = {
    Product.RAINFOREST_RESIN: {
        "fair_value": 10000,
        "take_width": 1,
        "clear_width": 0.5,
        "volume_limit": 0
    },
    Product.KELP: {
        "take_width": 1.5,          # 1         # 2
        "clear_width": 0,
        "prevent_adverse": True,
        "adverse_volume": 15,       # 15        # 20
        "reversion_beta": -0.229,   # -0.0229   # -0.25
        "disregard_edge": 1,        # 1         # 2
        "join_edge": 0,
        "default_edge": 1,
    },
    Product.SQUID_INK: {
        "fair_value" : 2000,
        "averaging_length" : 350,
        "trigger_price" : 10,
        "take_width": 5, #5
        "clear_width": 1, #1
        "prevent_adverse": False, #False
        "adverse_volume": 18, #16
        "reversion_beta":-0.3, #-0.3
        "disregard_edge": 1, #1
        "join_edge": 1, #1
        "default_edge": 1, #1
        "max_order_quantity": 35,
        "volatility_threshold": 3,
        "z_trigger" : 3.75
    },
}

class Trader:
    def __init__(self, params=None):
        if params is None:
            params = PARAMS
        self.params = params
        self.LIMIT = {
            Product.RAINFOREST_RESIN: 50,
            Product.KELP: 50,
            Product.SQUID_INK: 50
        }
        # Store mid-price history for RAINFOREST_RESIN if desired
        self.resin_price_history = {Product.RAINFOREST_RESIN: []}

    def get_midprice(self, order_depth: OrderDepth) -> Optional[float]:
        """Compute the mid-price from an order depth (used for RAINFOREST_RESIN only)."""
        if not order_depth or (not order_depth.buy_orders) or (not order_depth.sell_orders):
            return None
        best_bid = max(order_depth.buy_orders.keys())
        best_ask = min(order_depth.sell_orders.keys())
        return (best_bid + best_ask) / 2.0

    def take_best_orders(
            self,
            product: str,
            fair_value: int,
            take_width: float,
            orders: List[Order],
            order_depth: OrderDepth,
            position: int,
            buy_order_volume: int,
            sell_order_volume: int,
            prevent_adverse: bool = False,
            adverse_volume: int = 0
    ) -> (int, int):
        position_limit = self.LIMIT[product]

        # Sell side
        if len(order_depth.sell_orders) != 0:
            best_ask = min(order_depth.sell_orders.keys())
            best_ask_amount = -1 * order_depth.sell_orders[best_ask]
            if best_ask <= fair_value - take_width:
                quantity = min(best_ask_amount, position_limit - position)
                if quantity > 0:
                    orders.append(Order(product, best_ask, quantity))
                    buy_order_volume += quantity
                    order_depth.sell_orders[best_ask] += quantity
                    if order_depth.sell_orders[best_ask] == 0:
                        del order_depth.sell_orders[best_ask]

        # Buy side
        if len(order_depth.buy_orders) != 0:
            best_bid = max(order_depth.buy_orders.keys())
            best_bid_amount = order_depth.buy_orders[best_bid]
            if best_bid >= fair_value + take_width:
                quantity = min(best_bid_amount, position_limit + position)
                if quantity > 0:
                    orders.append(Order(product, best_bid, -1 * quantity))
                    sell_order_volume += quantity
                    order_depth.buy_orders[best_bid] -= quantity
                    if order_depth.buy_orders[best_bid] == 0:
                        del order_depth.buy_orders[best_bid]

        return buy_order_volume, sell_order_volume

    def market_make(
        self,
        product: str,
        orders: List[Order],
        bid: int,
        ask: int,
        position: int,
        buy_order_volume: int,
        sell_order_volume: int,
    ) -> (int, int):
        """(Unchanged) Symmetrical market making. Works for all products."""
        buy_quantity = self.LIMIT[product] - (position + buy_order_volume)
        if buy_quantity > 0:
            orders.append(Order(product, round(bid), buy_quantity))  # Buy order

        sell_quantity = self.LIMIT[product] + (position - sell_order_volume)
        if sell_quantity > 0:
            orders.append(Order(product, round(ask), -sell_quantity))  # Sell order

        return buy_order_volume, sell_order_volume

    def clear_position_order(
        self,
        product: str,
        fair_value: float,
        width: int,
        orders: List[Order],
        order_depth: OrderDepth,
        position: int,
        buy_order_volume: int,
        sell_order_volume: int,
    ) -> (int,int):
        """(Unchanged) For KELP/SQUID_INK. RAINFOREST_RESIN calls different code below."""
        position_after_take = position + buy_order_volume - sell_order_volume
        fair_for_bid = round(fair_value - width)
        fair_for_ask = round(fair_value + width)

        buy_quantity = self.LIMIT[product] - (position + buy_order_volume)
        sell_quantity = self.LIMIT[product] + (position - sell_order_volume)

        if position_after_take > 0:
            clear_quantity = sum(
                volume
                for price, volume in order_depth.buy_orders.items()
                if price >= fair_for_ask
            )
            clear_quantity = min(clear_quantity, position_after_take)
            sent_quantity = min(sell_quantity, clear_quantity)
            if sent_quantity > 0:
                orders.append(Order(product, fair_for_ask, -abs(sent_quantity)))
                sell_order_volume += abs(sent_quantity)

        if position_after_take < 0:
            clear_quantity = sum(
                abs(volume)
                for price, volume in order_depth.sell_orders.items()
                if price <= fair_for_bid
            )
            clear_quantity = min(clear_quantity, abs(position_after_take))
            sent_quantity = min(buy_quantity, clear_quantity)
            if sent_quantity > 0:
                orders.append(Order(product, fair_for_bid, abs(sent_quantity)))
                buy_order_volume += abs(sent_quantity)

        return buy_order_volume, sell_order_volume

    def kelp_fair_value(self, order_depth: OrderDepth, traderObject) -> float:
        if len(order_depth.sell_orders) != 0 and len(order_depth.buy_orders) != 0:
            best_ask = min(order_depth.sell_orders.keys())
            best_bid = max(order_depth.buy_orders.keys())

            # Filter out orders that do not meet the 'adverse_volume' threshold
            filtered_ask = [
                price for price in order_depth.sell_orders.keys()
                if abs(order_depth.sell_orders[price]) >= self.params[Product.KELP]["adverse_volume"]
            ]
            filtered_bid = [
                price for price in order_depth.buy_orders.keys()
                if abs(order_depth.buy_orders[price]) >= self.params[Product.KELP]["adverse_volume"]
            ]

            mm_ask = min(filtered_ask) if len(filtered_ask) > 0 else None
            mm_bid = max(filtered_bid) if len(filtered_bid) > 0 else None

            # If we can't find both a "meaningful" ask and bid, fallback
            if mm_ask is None or mm_bid is None:
                if traderObject.get("kelp_last_price", None) is None:
                    mmmid_price = (best_ask + best_bid) / 2
                else:
                    mmmid_price = traderObject["kelp_last_price"]
            else:
                mmmid_price = (mm_ask + mm_bid) / 2

            # Incorporate reversion logic if we have a previous price
            if traderObject.get("kelp_last_price", None) is not None:
                last_price = traderObject["kelp_last_price"]
                last_returns = (mmmid_price - last_price) / last_price
                pred_returns = last_returns * self.params[Product.KELP]["reversion_beta"]
                fair = mmmid_price + (mmmid_price * pred_returns)
            else:
                fair = mmmid_price

            traderObject["kelp_last_price"] = mmmid_price
            return fair
        return None
        
    def squid_ink_fair_value(self, order_depth: OrderDepth, traderObject) -> float:
        if 'squid_ink_mm_midprices' not in traderObject:
            traderObject['squid_ink_mm_midprices'] = []
        if 'squid_ink_min_spreads' not in traderObject:
            traderObject['squid_ink_min_spreads'] = []
        if 'squid_ink_max_spreads' not in traderObject:
            traderObject['squid_ink_max_spreads'] = []
        
        # Calculate current market maker mid price
        if len(order_depth.sell_orders) != 0 and len(order_depth.buy_orders) != 0:
            best_ask = min(order_depth.sell_orders.keys())
            best_bid = max(order_depth.buy_orders.keys())
            min_spread = best_ask - best_bid
            
            # Calculate max spread (widest spread in the book)
            max_ask = max(order_depth.sell_orders.keys())
            min_bid = min(order_depth.buy_orders.keys())
            max_spread = max_ask - min_bid
            
            # Filter for large orders (potential market makers)
            filtered_ask = [
                price
                for price in order_depth.sell_orders.keys()
                if abs(order_depth.sell_orders[price])
                >= self.params[Product.SQUID_INK]["adverse_volume"]
            ]
            filtered_bid = [
                price
                for price in order_depth.buy_orders.keys()
                if abs(order_depth.buy_orders[price])
                >= self.params[Product.SQUID_INK]["adverse_volume"]
            ]
            mm_ask = min(filtered_ask) if len(filtered_ask) > 0 else None
            mm_bid = max(filtered_bid) if len(filtered_bid) > 0 else None
            if mm_ask is None or mm_bid is None:
                if traderObject.get("squid_ink_last_price", None) is None:
                    mmmid_price = (best_ask + best_bid-1) // 2 
                else:
                    mmmid_price = traderObject["squid_ink_last_price"]
            else:
                mmmid_price = (mm_ask + mm_bid-1) // 2
            
            # Store spreads
            traderObject['squid_ink_min_spreads'].append(min_spread)
            traderObject['squid_ink_max_spreads'].append(max_spread)
            
            # Keep only last 15 values
            if len(traderObject['squid_ink_min_spreads']) > 4:
                traderObject['squid_ink_min_spreads'] = traderObject['squid_ink_min_spreads'][-4:]
            if len(traderObject['squid_ink_max_spreads']) > 4:
                traderObject['squid_ink_max_spreads'] = traderObject['squid_ink_max_spreads'][-4:]
            
            # Store mm mid price
            traderObject['squid_ink_mm_midprices'].append(mmmid_price)
            if len(traderObject['squid_ink_mm_midprices']) > 4:
                traderObject['squid_ink_mm_midprices'] = traderObject['squid_ink_mm_midprices'][-4:]
            
            # Calculate average spreads
            avg_min_spread = sum(traderObject['squid_ink_min_spreads']) / len(traderObject['squid_ink_min_spreads'])
            avg_max_spread = sum(traderObject['squid_ink_max_spreads']) / len(traderObject['squid_ink_max_spreads'])
            traderObject['avg_min_spread'] = avg_min_spread
            traderObject['avg_max_spread'] = avg_max_spread
            if len(traderObject['squid_ink_mm_midprices']) >= 3:
                x = list(range(len(traderObject['squid_ink_mm_midprices'])))
                y = traderObject['squid_ink_mm_midprices']
                x_mean = sum(x) / len(x)
                y_mean = sum(y) / len(y)
                numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(len(x)))
                denominator = sum((x[i] - x_mean) ** 2 for i in range(len(x)))
                
                if denominator != 0:
                    slope = numerator / denominator
                else:
                    slope = 0
                
                # Update normalization to allow for both positive and negative slopes
                # Keep the sign of the slope, but normalize its magnitude
                slope_sign = 1 if slope > 0 else -1
                slope_magnitude = abs(slope)
                # Scale magnitude to a reasonable range (0.02 to 0.3)
                normalized_magnitude = min(0.3, max(0.02, 0.1 * (slope_magnitude / 100)))
                # Apply the original sign to the normalized magnitude
                norm_slope = slope_sign * normalized_magnitude
                
                traderObject['dynamic_reversion_beta'] = norm_slope
                if traderObject.get("squid_ink_last_price", None) is not None:
                    last_price = traderObject["squid_ink_last_price"]
                    last_returns = (mmmid_price - last_price) / last_price if last_price > 0 else 0
                    pred_returns = last_returns * norm_slope
                    fair = mmmid_price + (mmmid_price * pred_returns)
                else:
                    fair = mmmid_price
            else:
                if traderObject.get("squid_ink_last_price", None) is not None:
                    last_price = traderObject["squid_ink_last_price"]
                    last_returns = (mmmid_price - last_price) / last_price if last_price > 0 else 0
                    pred_returns = last_returns * -0.1
                    fair = mmmid_price + (mmmid_price * pred_returns)
                else:
                    fair = mmmid_price
                    
            # Store last price for next iteration
            traderObject["squid_ink_last_price"] = mmmid_price
            return fair

    def sma(self, order_depth: OrderDepth, traderObject, position: int):
        orders: List[Order] = []
        product = Product.SQUID_INK
        position_limit = self.LIMIT[product]

        if not order_depth.sell_orders or not order_depth.buy_orders:
            return orders

        best_ask = min(order_depth.sell_orders.keys())
        best_bid = max(order_depth.buy_orders.keys())
        mid_price = (best_ask + best_bid) / 2

        params = self.params[product]
        take_width = params["take_width"]
        av_len = params["averaging_length"]
        trigger_price = params["trigger_price"]
        max_quantity = params["max_order_quantity"]
        volatility_threshold = params["volatility_threshold"]

        if "squid_prices" not in traderObject:
            traderObject["squid_prices"] = []
        traderObject["squid_prices"].append(mid_price)
        if len(traderObject["squid_prices"]) > av_len:
            traderObject["squid_prices"].pop(0)

        if len(traderObject["squid_prices"]) < 3:
            return orders

        mean_price = sum(traderObject["squid_prices"]) / len(traderObject["squid_prices"])
        squared_diffs = [(p - mean_price) ** 2 for p in traderObject["squid_prices"]]
        volatility = (sum(squared_diffs) / len(traderObject["squid_prices"])) ** 0.5

        bid_volume = abs(order_depth.buy_orders[best_bid])
        ask_volume = abs(order_depth.sell_orders[best_ask])
        avg_volume = (bid_volume + ask_volume) / 2
        quantity = min(int(avg_volume), max_quantity)

        def safe_order(price, qty):
            new_position = position + sum(order.quantity for order in orders) + qty
            if abs(new_position) > position_limit:
                allowed_qty = position_limit - abs(position) if qty > 0 else -(position + sum(o.quantity for o in orders))
                qty = max(min(qty, allowed_qty), -allowed_qty)
            if qty != 0:
                orders.append(Order(product, price, qty))

        # Mean-Reversion if volatility is high
        if volatility > volatility_threshold:
            sma_val = mean_price
            diff = mid_price - sma_val
            if diff >= trigger_price and position > -position_limit:
                safe_order(best_bid - take_width, -quantity)
            elif diff <= -trigger_price and position < position_limit:
                safe_order(best_ask + take_width, quantity)

        else:
            # Market making
            print("MARKETMAKING")
            squid_ink_fair_value = self.squid_ink_fair_value(order_depth, traderObject)
            take_orders, buy_order_volume, sell_order_volume = self.take_orders(
                Product.SQUID_INK,
                order_depth,
                squid_ink_fair_value,
                self.params[Product.SQUID_INK]["take_width"],
                position,
                self.params[Product.SQUID_INK]["prevent_adverse"],
                self.params[Product.SQUID_INK]["adverse_volume"],
            )
            clear_orders, buy_order_volume, sell_order_volume = self.clear_orders(
                Product.SQUID_INK,
                order_depth,
                squid_ink_fair_value,
                self.params[Product.SQUID_INK]["clear_width"],
                position,
                buy_order_volume,
                sell_order_volume,
            )
            make_orders, _, _ = self.make_orders(
                Product.SQUID_INK,
                order_depth,
                squid_ink_fair_value,
                position,
                buy_order_volume,
                sell_order_volume,
                self.params[Product.SQUID_INK]["disregard_edge"],
                self.params[Product.SQUID_INK]["join_edge"],
                self.params[Product.SQUID_INK]["default_edge"],
                traderObject=traderObject
            )
            for o in take_orders + clear_orders + make_orders:
                safe_order(o.price, o.quantity)

        return orders

    def take_orders(
        self,
        product: str,
        order_depth: OrderDepth,
        fair_value: float,
        take_width: float,
        position: int,
        prevent_adverse: bool = False,
        adverse_volume: int = 0,
    ) -> (List[Order], int, int):

        if product == Product.RAINFOREST_RESIN:
            orders = []
            buy_order_volume = 0
            sell_order_volume = 0

            # Attempt to buy if best ask is significantly below fair_value
            if order_depth.sell_orders:
                best_ask = min(order_depth.sell_orders.keys())
                best_ask_amount = -order_depth.sell_orders[best_ask]
                if best_ask <= fair_value - take_width:
                    quantity = min(best_ask_amount, self.LIMIT[product] - position)
                    if quantity > 0:
                        orders.append(Order(product, best_ask, quantity))
                        buy_order_volume += quantity

            # Attempt to sell if best bid is significantly above fair_value
            if order_depth.buy_orders:
                best_bid = max(order_depth.buy_orders.keys())
                best_bid_amount = order_depth.buy_orders[best_bid]
                if best_bid >= fair_value + take_width:
                    quantity = min(best_bid_amount, self.LIMIT[product] + position)
                    if quantity > 0:
                        orders.append(Order(product, best_bid, -quantity))
                        sell_order_volume += quantity

            return orders, buy_order_volume, sell_order_volume

        else:
            orders: List[Order] = []
            buy_order_volume = 0
            sell_order_volume = 0

            buy_order_volume, sell_order_volume = self.take_best_orders(
                product,
                fair_value,
                take_width,
                orders,
                order_depth,
                position,
                buy_order_volume,
                sell_order_volume,
                prevent_adverse,
                adverse_volume,
            )
            return orders, buy_order_volume, sell_order_volume

    def clear_orders(
        self,
        product: str,
        order_depth: OrderDepth,
        fair_value: float,
        clear_width: float,
        position: int,
        buy_order_volume: int,
        sell_order_volume: int,
    ) -> (List[Order], int, int):

        if product == Product.RAINFOREST_RESIN:
            orders = []
            position_after_take = position + buy_order_volume - sell_order_volume
            buy_quantity = self.LIMIT[product] - (position + buy_order_volume)
            sell_quantity = self.LIMIT[product] + (position - sell_order_volume)

            if position_after_take > 0:
                # net long => see if we can sell near fair_value
                bids_to_hit = {
                    price: vol for price, vol in order_depth.buy_orders.items()
                    if price >= fair_value - clear_width
                }
                if bids_to_hit:
                    best_clear_bid = max(bids_to_hit.keys())
                    available_volume = abs(bids_to_hit[best_clear_bid])
                    qty_to_clear = min(abs(position_after_take), available_volume)
                    sent_quantity = min(sell_quantity, qty_to_clear)
                    if sent_quantity > 0:
                        orders.append(Order(product, best_clear_bid, -sent_quantity))
                        sell_order_volume += sent_quantity

            if position_after_take < 0:
                # net short => see if we can buy near fair_value
                asks_to_hit = {
                    price: vol for price, vol in order_depth.sell_orders.items()
                    if price <= fair_value
                }
                if asks_to_hit:
                    best_clear_ask = min(asks_to_hit.keys())
                    available_volume = abs(asks_to_hit[best_clear_ask])
                    qty_to_clear = min(abs(position_after_take), available_volume)
                    sent_quantity = min(buy_quantity, qty_to_clear)
                    if sent_quantity > 0:
                        orders.append(Order(product, best_clear_ask, sent_quantity))
                        buy_order_volume += sent_quantity

            return orders, buy_order_volume, sell_order_volume

        else:
            orders: List[Order] = []
            buy_order_volume, sell_order_volume = self.clear_position_order(
                product,
                fair_value,
                int(clear_width),
                orders,
                order_depth,
                position,
                buy_order_volume,
                sell_order_volume,
            )
            return orders, buy_order_volume, sell_order_volume

    def make_orders(
        self,
        product,
        order_depth: OrderDepth,
        fair_value: float,
        position: int,
        buy_order_volume: int,
        sell_order_volume: int,
        disregard_edge: float,  
        join_edge: float,       
        default_edge: float,    
        manage_position: bool = False,
        soft_position_limit: int = 0,
        traderObject: dict = None,
    ) -> (List[Order], int, int):
        """
        For RAINFOREST_RESIN: new "market-making" approach from your updated code.
        For KELP/SQUID_INK: original approach from your old code.
        """
        if product == Product.RAINFOREST_RESIN:
            orders = []
            volume_limit = self.params[product]["volume_limit"]

            # best ask above fair_value+1
            asks_above = [
                price for price in order_depth.sell_orders.keys()
                if price > fair_value + 1
            ]
            best_ask_above_fair = min(asks_above) if asks_above else (fair_value + 1)

            # best bid below fair_value-1
            bids_below = [
                price for price in order_depth.buy_orders.keys()
                if price < fair_value - 1
            ]
            best_bid_below_fair = max(bids_below) if bids_below else (fair_value - 1)

            # If best ask is too close, push higher (if position within limit)
            if best_ask_above_fair <= fair_value + 2:
                if position <= volume_limit:
                    best_ask_above_fair = fair_value + 3

            # If best bid is too close, push lower (if position within limit)
            if best_bid_below_fair >= fair_value - 2:
                if position >= -volume_limit:
                    best_bid_below_fair = fair_value - 3

            # We use your usual 'market_make' for symmetrical orders:
            bid_price = best_bid_below_fair + 1
            ask_price = best_ask_above_fair - 1
            buy_order_volume, sell_order_volume = self.market_make(
                product,
                orders,
                bid_price,
                ask_price,
                position,
                buy_order_volume,
                sell_order_volume,
            )
            return orders, buy_order_volume, sell_order_volume

        else:
            orders: List[Order] = []

            # For SQUID_INK, check max_spread condition and adjust bid/ask based on slope sign
            if product == Product.SQUID_INK and traderObject is not None:
                # Get current max_spread and average max_spread
                current_max_spread = traderObject.get('squid_ink_max_spreads', [])[-1] if traderObject.get('squid_ink_max_spreads', []) else 0
                avg_max_spread = traderObject.get('avg_max_spread', 0)
                
                # Get current min_spread
                current_min_spread = traderObject.get('squid_ink_min_spreads', [])[-1] if traderObject.get('squid_ink_min_spreads', []) else 0
                
                # Get slope sign
                slope = traderObject.get('dynamic_reversion_beta', 0)
                positive_slope = slope > 0
                
                # Skip market making if max_spread is too large compared to average
                if current_max_spread > avg_max_spread + 2:
                    return [], buy_order_volume, sell_order_volume

            asks_above_fair = [
                price
                for price in order_depth.sell_orders.keys()
                if price > fair_value + disregard_edge
            ]
            bids_below_fair = [
                price
                for price in order_depth.buy_orders.keys()
                if price < fair_value - disregard_edge
            ]

            best_ask_above_fair = min(asks_above_fair) if len(asks_above_fair) > 0 else None
            best_bid_below_fair = max(bids_below_fair) if len(bids_below_fair) > 0 else None

            ask = round(fair_value + default_edge)
            if best_ask_above_fair is not None:
                if abs(best_ask_above_fair - fair_value) <= join_edge:
                    ask = best_ask_above_fair
                else:
                    ask = best_ask_above_fair - 1

            bid = round(fair_value - default_edge)
            if best_bid_below_fair is not None:
                if abs(fair_value - best_bid_below_fair) <= join_edge:
                    bid = best_bid_below_fair
                else:
                    bid = best_bid_below_fair + 1

            # SQUID_INK additional check
            if product == Product.SQUID_INK and traderObject is not None and best_bid_below_fair is not None and best_ask_above_fair is not None:
                current_min_spread = traderObject.get('squid_ink_min_spreads', [])[-1] if traderObject.get('squid_ink_min_spreads', []) else 0
                slope = traderObject.get('dynamic_reversion_beta', 0)
                
                if current_min_spread >= 2:
                    if slope > 0:  # Positive slope
                        if abs(best_ask_above_fair - fair_value) <= join_edge:
                            ask = best_ask_above_fair
                        else:
                            ask = best_ask_above_fair
                        if abs(fair_value - best_bid_below_fair) <= join_edge:
                            bid = best_bid_below_fair
                        else:
                            bid = best_bid_below_fair + 1
                    elif slope < 0:  # Negative slope
                        if abs(best_ask_above_fair - fair_value) <= join_edge:
                            ask = best_ask_above_fair
                        else:
                            ask = best_ask_above_fair -1
                        if abs(fair_value - best_bid_below_fair) <= join_edge:
                            bid = best_bid_below_fair
                        else:
                            bid = best_bid_below_fair 
                else:
                    return [], buy_order_volume, sell_order_volume


            if manage_position:
                if position > soft_position_limit:
                    ask -= 1
                elif position < -1 * soft_position_limit:
                    bid += 1

            buy_order_volume, sell_order_volume = self.market_make(
                product,
                orders,
                bid,
                ask,
                position,
                buy_order_volume,
                sell_order_volume,
            )
            return orders, buy_order_volume, sell_order_volume

    def squid_ink_orders(self, order_depth: OrderDepth, traderObject, position: int) -> List[Order]:
        orders: List[Order] = []
        product = Product.SQUID_INK
        params = PARAMS[product]
        position_limit = self.LIMIT[product]

        if not order_depth.sell_orders or not order_depth.buy_orders:
            return orders

        # --- Market Data ---
        best_ask = min(order_depth.sell_orders)
        best_bid = max(order_depth.buy_orders)
        mid_price = (best_ask + best_bid) / 2
        fair_value = params["fair_value"]

        # --- Parameters ---
        take_width = params["take_width"]
        av_len = params["averaging_length"]
        max_quantity = params["max_order_quantity"]
        volatility_threshold = params["volatility_threshold"]
        z_trigger = params["z_trigger"]
        min_quantity = max(1, max_quantity // 4)

        # --- Historical Tracking ---
        if "squid_prices" not in traderObject:
            traderObject["squid_prices"] = []

        prices = traderObject["squid_prices"]
        prices.append(mid_price)
        if len(prices) > av_len:
            prices.pop(0)
        if len(prices) < av_len:
            return orders
        

        # --- Volatility & Z-Score ---
        mean_price = sum(prices) / len(prices)
        variance = sum((p - mean_price) ** 2 for p in prices) / len(prices)
        volatility = variance ** 0.5
        zscore = (mid_price - mean_price) / volatility if volatility else 0

        # --- Volume Estimation ---
        bid_volume = abs(order_depth.buy_orders[best_bid])
        ask_volume = abs(order_depth.sell_orders[best_ask])
        avg_volume = (bid_volume + ask_volume) / 2
        base_quantity = min(int(avg_volume), max_quantity)

        # --- Adaptive Position Control ---
        distance_from_anchor = abs(mid_price - fair_value)
        anchor_proximity = max(0, 1 - (distance_from_anchor / 100))  # Closer to 1 near 2000
        adjusted_limit = int(position_limit * anchor_proximity)
        adjusted_limit = max(adjusted_limit, 10)  # Always allow small trades

        # --- Helper: Clamped Order ---
        def safe_order(price: float, qty: int):
            new_position = position + sum(o.quantity for o in orders) + qty
            if abs(new_position) > position_limit:
                allowed_qty = position_limit - abs(position) if qty > 0 else -(position + sum(o.quantity for o in orders))
                qty = max(min(qty, allowed_qty), -allowed_qty)
            if qty != 0:
                orders.append(Order(product, price, qty))

        # --- Mean Reversion Trading ---
        if  abs(zscore) >= z_trigger:
            print("MEAN REVERSION")
            scale = min(abs(zscore), 3)
            dynamic_qty = max(min(int(scale * min(base_quantity, adjusted_limit)), max_quantity), min_quantity)
            price_offset = round(take_width * scale)

            if zscore > 0 and position > -adjusted_limit:
                safe_order(best_bid - price_offset, -dynamic_qty)
            elif zscore < 0 and position < adjusted_limit:
                safe_order(best_ask + price_offset, dynamic_qty)

        # --- Low-Volatility: Market Making Mode ---
        else:
            print("MARKETMAKING")
            fv = self.squid_ink_fair_value(order_depth, traderObject)

            take_orders, bvol, svol = self.take_orders(
                product, order_depth, fv,
                self.params[product]["take_width"], position,
                self.params[product]["prevent_adverse"],
                self.params[product]["adverse_volume"]
            )
            clear_orders, bvol, svol = self.clear_orders(
                product, order_depth, fv,
                self.params[product]["clear_width"], position,
                bvol, svol
            )
            make_orders, _, _ = self.make_orders(
                product, order_depth, fv, position, bvol, svol,
                self.params[product]["disregard_edge"],
                self.params[product]["join_edge"],
                self.params[product]["default_edge"],
                traderObject=traderObject
            )
            orders +=  take_orders + clear_orders + make_orders
        return orders

    ##########################################################################
    # Finally, the run method: same overall structure, new RAINFOREST_RESIN logic
    ##########################################################################
    def run(self, state: TradingState):
        traderObject = {}
        if state.traderData != None and state.traderData != "":
            traderObject = jsonpickle.decode(state.traderData)

        result = {}

        # RAINFOREST RESIN
        
        if Product.RAINFOREST_RESIN in self.params and Product.RAINFOREST_RESIN in state.order_depths:
            rainforest_position = state.position.get(Product.RAINFOREST_RESIN, 0)
            order_depth = state.order_depths[Product.RAINFOREST_RESIN]
            # Store mid-price if available
            mid_price = self.get_midprice(order_depth)
            if mid_price is not None:
                self.resin_price_history[Product.RAINFOREST_RESIN].append(mid_price)

            # 1) Take orders
            rainforest_take_orders, buy_order_volume, sell_order_volume = self.take_orders(
                Product.RAINFOREST_RESIN,
                order_depth,
                self.params[Product.RAINFOREST_RESIN]["fair_value"],
                self.params[Product.RAINFOREST_RESIN]["take_width"],
                rainforest_position,
            )
            # 2) Clear orders
            rainforest_clear_orders, buy_order_volume, sell_order_volume = self.clear_orders(
                Product.RAINFOREST_RESIN,
                order_depth,
                self.params[Product.RAINFOREST_RESIN]["fair_value"],
                self.params[Product.RAINFOREST_RESIN]["clear_width"],
                rainforest_position,
                buy_order_volume,
                sell_order_volume,
            )
            # 3) Market-making
            rainforest_make_orders, buy_order_volume, sell_order_volume = self.make_orders(
                Product.RAINFOREST_RESIN,
                order_depth,
                self.params[Product.RAINFOREST_RESIN]["fair_value"],
                rainforest_position,
                buy_order_volume,
                sell_order_volume,
                # We pass these but they aren't used in the new logic:
                disregard_edge=0,  
                join_edge=0,
                default_edge=0,
            )
            result[Product.RAINFOREST_RESIN] = (
                rainforest_take_orders + rainforest_clear_orders + rainforest_make_orders
            )

        # KELP

        if Product.KELP in self.params and Product.KELP in state.order_depths:
            kelp_position = state.position.get(Product.KELP, 0)
            kelp_fair_value = self.kelp_fair_value(state.order_depths[Product.KELP], traderObject)

            kelp_take_orders, buy_order_volume, sell_order_volume = self.take_orders(
                Product.KELP,
                state.order_depths[Product.KELP],
                kelp_fair_value,
                self.params[Product.KELP]["take_width"],
                kelp_position,
                self.params[Product.KELP]["prevent_adverse"],
                self.params[Product.KELP]["adverse_volume"],
            )
            kelp_clear_orders, buy_order_volume, sell_order_volume = self.clear_orders(
                Product.KELP,
                state.order_depths[Product.KELP],
                kelp_fair_value,
                self.params[Product.KELP]["clear_width"],
                kelp_position,
                buy_order_volume,
                sell_order_volume,
            )
            kelp_make_orders, _, _ = self.make_orders(
                Product.KELP,
                state.order_depths[Product.KELP],
                kelp_fair_value,
                kelp_position,
                buy_order_volume,
                sell_order_volume,
                self.params[Product.KELP]["disregard_edge"],
                self.params[Product.KELP]["join_edge"],
                self.params[Product.KELP]["default_edge"],
            )
            result[Product.KELP] = kelp_take_orders + kelp_clear_orders + kelp_make_orders


        # SQUID INK

        if Product.SQUID_INK in self.params and Product.SQUID_INK in state.order_depths:
        # SQUID INK
            squid_position = (
                    state.position[Product.SQUID_INK]
                    if Product.SQUID_INK in state.position
                    else 0
                )
            result[Product.SQUID_INK] = self.squid_ink_orders(state.order_depths[Product.SQUID_INK], traderObject, squid_position)

        traderData = jsonpickle.encode(traderObject)
        conversions = 1  # same as your original
        logger.flush(state, result, conversions, traderData)
        return result, conversions, traderData

from datamodel import OrderDepth, UserId, TradingState, Order
import pandas as pd
import numpy as np


class Trader:
    kelp_df = pd.DataFrame(
        columns=[
            "timestamp",
            "product",
            "bid_price_1",
            "bid_volume_1",
            "bid_price_2",
            "bid_volume_2",
            "bid_price_3",
            "bid_volume_3",
            "ask_price_1",
            "ask_volume_1",
            "ask_price_2",
            "ask_volume_2",
            "ask_price_3",
            "ask_volume_3",
            "mid_price",
            "profit_and_loss",
            "mmbot_bid",
            "mmbot_ask",
            "mmbot_midprice",
        ]
    )

    squink_df = pd.DataFrame(
        columns=[
            "timestamp",
            "product",
            "bid_price_1",
            "bid_volume_1",
            "bid_price_2",
            "bid_volume_2",
            "bid_price_3",
            "bid_volume_3",
            "ask_price_1",
            "ask_volume_1",
            "ask_price_2",
            "ask_volume_2",
            "ask_price_3",
            "ask_volume_3",
            "mid_price",
            "profit_and_loss",
        ]
    )

    # not used?
    # resin_df = pd.DataFrame(columns=[
    #     "timestamp", "product",
    #     "bid_price_1", "bid_volume_1", "bid_price_2", "bid_volume_2", "bid_price_3", "bid_volume_3",
    #     "ask_price_1", "ask_volume_1", "ask_price_2", "ask_volume_2", "ask_price_3", "ask_volume_3",
    #     "mid_price", "profit_and_loss", 'mmbot_bid', 'mmbot_ask', 'mmbot_midprice'
    # ])
    # “If none of the bots trade on an outstanding player quote, the quote is automatically cancelled at the end of the iteration.”

    # HARDCODED PARAMETERS
    def __init__(self):
        # config
        self.position_limit = {"RAINFOREST_RESIN": 50}
        self.resinsymbol = "RAINFOREST_RESIN"

        # PARAMETERS - RESIN
        self.sk1 = 0.00
        self.sk2 = 0.00
        self.sk3 = 1.0
        self.sk4 = 0.0
        self.sk5 = 0.00
        self.bk1 = 0.00
        self.bk2 = 0.00
        self.bk3 = 0.75
        self.bk4 = 0.25
        self.bk5 = 0.00

        # PARAMETERS - KELP
        self.retreat_per_lot = 0.012
        self.edge_per_lot = 0.015
        self.edge0 = 0.02

        # runtime
        self.resin_max_position = 0
        self.resin_min_position = 0
        pass

    def SQUINK_update_df(df, product, state, orders, order_depth):
        buy_orders = sorted(order_depth.buy_orders.items(), key=lambda x: -x[0])
        sell_orders = sorted(order_depth.sell_orders.items(), key=lambda x: x[0])

        bid_levels = buy_orders[:3] + [(None, None)] * (3 - len(buy_orders))
        ask_levels = sell_orders[:3] + [(None, None)] * (3 - len(sell_orders))

        if bid_levels[0][0] is not None and ask_levels[0][0] is not None:
            mid_price = (bid_levels[0][0] + ask_levels[0][0]) / 2
        else:
            mid_price = None

        row = {
            "timestamp": state.timestamp,
            "product": product,
            "bid_price_1": bid_levels[0][0],
            "bid_volume_1": bid_levels[0][1],
            "bid_price_2": bid_levels[1][0],
            "bid_volume_2": bid_levels[1][1],
            "bid_price_3": bid_levels[2][0],
            "bid_volume_3": bid_levels[2][1],
            "ask_price_1": ask_levels[0][0],
            "ask_volume_1": ask_levels[0][1],
            "ask_price_2": ask_levels[1][0],
            "ask_volume_2": ask_levels[1][1],
            "ask_price_3": ask_levels[2][0],
            "ask_volume_3": ask_levels[2][1],
            "mid_price": mid_price,
        }

        df.loc[len(df)] = row

    def KELP_update_df(df, product, state, orders, order_depth):
        buy_orders = sorted(order_depth.buy_orders.items(), key=lambda x: -x[0])
        sell_orders = sorted(order_depth.sell_orders.items(), key=lambda x: x[0])

        bid_levels = buy_orders[:3] + [(None, None)] * (3 - len(buy_orders))
        ask_levels = sell_orders[:3] + [(None, None)] * (3 - len(sell_orders))

        if bid_levels[0][0] is not None and ask_levels[0][0] is not None:
            mid_price = (bid_levels[0][0] + ask_levels[0][0]) / 2
        else:
            mid_price = None

        row = {
            "timestamp": state.timestamp,
            "product": product,
            "bid_price_1": bid_levels[0][0],
            "bid_volume_1": bid_levels[0][1] or 0,  # If bid_volume_1 is None, set it to 0
            "bid_price_2": bid_levels[1][0],
            "bid_volume_2": bid_levels[1][1] or 0,  # If bid_volume_2 is None, set it to 0
            "bid_price_3": bid_levels[2][0],
            "bid_volume_3": bid_levels[2][1] or 0,  # If bid_volume_3 is None, set it to 0
            "ask_price_1": ask_levels[0][0],
            "ask_volume_1": ask_levels[0][1] or 0,  # If ask_volume_1 is None, set it to 0
            "ask_price_2": ask_levels[1][0],
            "ask_volume_2": ask_levels[1][1] or 0,  # If ask_volume_2 is None, set it to 0
            "ask_price_3": ask_levels[2][0],
            "ask_volume_3": ask_levels[2][1] or 0,  # If ask_volume_3 is None, set it to 0
            "mid_price": mid_price,
        }

        if row["bid_volume_1"] >= 15:  # Adverse volume set to 15. #mm_bot_bid will just become the top level if there is no adverse volume.
            mm_bot_bid = row["bid_price_1"]
        elif row["bid_volume_2"] >= 15:
            mm_bot_bid = row["bid_price_2"]
        elif row["bid_volume_3"] >= 15:
            mm_bot_bid = row["bid_price_3"]
        else:
            mm_bot_bid = row["bid_price_1"]

        if row["ask_volume_1"] >= 15:  # Adverse volume set to 15. mm_bot_ask will just become the top level if there is no adverse volume.
            mm_bot_ask = row["ask_price_1"]
        elif row["ask_volume_2"] >= 15:
            mm_bot_ask = row["ask_price_2"]
        elif row["ask_volume_3"] >= 15:
            mm_bot_ask = row["ask_price_3"]
        else:
            mm_bot_ask = row["ask_price_1"]

        row["mmbot_bid"] = mm_bot_bid
        row["mmbot_ask"] = mm_bot_ask
        row["mmbot_midprice"] = (mm_bot_bid + mm_bot_ask) / 2

        df.loc[len(df)] = row

    # takes +ev orders from the orderbook.
    def RESIN_take_best_orders(self, state: TradingState, orderbook: OrderDepth) -> list[Order]:
        orders: list[Order] = []

        max_buy_amount = self.position_limit[self.resinsymbol] - self.resin_max_position
        max_sell_amount = abs(-self.position_limit[self.resinsymbol] - self.resin_min_position)

        if len(orderbook.buy_orders) != 0:
            best_bid_price = max(orderbook.buy_orders.keys())
            best_bid_volume = orderbook.buy_orders[best_bid_price]

            if best_bid_price > 10000:
                fill_quantity = min(max_sell_amount, best_bid_volume)

                if fill_quantity > 0:
                    orders.append(Order(self.resinsymbol, best_bid_price, -fill_quantity))
                    del orderbook.buy_orders[best_bid_price]

        if len(orderbook.sell_orders) != 0:
            best_ask_price = min(orderbook.sell_orders.keys())
            best_ask_volume = abs(orderbook.sell_orders[best_ask_price])

            if best_ask_price < 10000:
                fill_quantity = min(max_buy_amount, best_ask_volume)

                if fill_quantity > 0:
                    orders.append(Order(self.resinsymbol, best_ask_price, fill_quantity))
                    del orderbook.sell_orders[best_ask_price]

        return orders

    # puts in some quoting orders
    def RESIN_add_mm_orders(self, state: TradingState) -> list[Order]:
        orders: list[Order] = []

        max_buy_amount = self.position_limit[self.resinsymbol] - self.resin_max_position
        max_sell_amount = abs(-self.position_limit[self.resinsymbol] - self.resin_min_position)

        portion = max_sell_amount / 5
        sq1 = self.sk1 * portion
        sq2 = self.sk2 * portion
        sq3 = self.sk3 * portion
        sq4 = self.sk4 * portion
        sq5 = self.sk5 * (max_sell_amount - 4 * int(portion))

        portion = max_buy_amount / 5
        bq1 = self.bk1 * portion
        bq2 = self.bk2 * portion
        bq3 = self.bk3 * portion
        bq4 = self.bk4 * portion
        bq5 = self.bk5 * (max_buy_amount - 4 * int(portion))

        orders.append(Order(self.resinsymbol, 10001, -int(sq1)))
        orders.append(Order(self.resinsymbol, 10002, -int(sq2)))
        orders.append(Order(self.resinsymbol, 10003, -int(sq3)))
        orders.append(Order(self.resinsymbol, 10004, -int(sq4)))
        orders.append(Order(self.resinsymbol, 10005, -int(sq5)))

        orders.append(Order(self.resinsymbol, 9999, int(bq1)))
        orders.append(Order(self.resinsymbol, 9998, int(bq2)))
        orders.append(Order(self.resinsymbol, 9997, int(bq3)))
        orders.append(Order(self.resinsymbol, 9996, int(bq4)))
        orders.append(Order(self.resinsymbol, 9995, int(bq5)))

        return orders

    def RESIN_init_runtime_variables(self, state: TradingState):
        self.resin_max_position = state.position[self.resinsymbol] if self.resinsymbol in state.position else 0
        self.resin_min_position = state.position[self.resinsymbol] if self.resinsymbol in state.position else 0

    def run(self, state: TradingState):
        self.RESIN_init_runtime_variables(state)

        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: list[Order] = []

            if product == "RAINFOREST_RESIN":
                took = self.RESIN_take_best_orders(state, state.order_depths[product])

                while len(took) != 0:
                    orders = orders + took

                    for order in took:
                        if order.quantity > 0:
                            self.resin_max_position += order.quantity
                        elif order.quantity < 0:
                            self.resin_min_position -= abs(order.quantity)

                    took = self.RESIN_take_best_orders(state, state.order_depths[product])

                took = self.RESIN_add_mm_orders(state)
                orders = orders + took

                for order in took:
                    if order.quantity > 0:
                        self.resin_max_position += order.quantity
                    elif order.quantity < 0:
                        self.resin_min_position -= abs(order.quantity)
            elif product == "KELP":
                kelp_position = state.position.get(product, 0)
                Trader.KELP_update_df(Trader.kelp_df, product, state, orders, order_depth)

                if len(order_depth.sell_orders) and len(order_depth.buy_orders):
                    if len(self.kelp_df) >= 2:
                        current_row = self.kelp_df.iloc[-1]
                        previous_row = self.kelp_df.iloc[-2]
                        current_midprice = (current_row.bid_price_1 + current_row.ask_price_1) / 2
                        previous_midprice = (previous_row.bid_price_1 + previous_row.ask_price_1) / 2
                        current_log_return = np.log(current_midprice) - np.log(previous_midprice)

                        ask_pca = (
                            -0.67802679 * (current_row.ask_volume_1 or 0)
                            + 0.73468115 * (current_row.ask_volume_2 or 0)
                            + 0.02287503 * (current_row.ask_volume_3 or 0)
                        )
                        bid_pca = (
                            -0.69827525 * (current_row.bid_volume_1 or 0)
                            + 0.71532596 * (current_row.bid_volume_2 or 0)
                            + 0.02684134 * (current_row.bid_volume_3 or 0)
                        )

                        lag_1_bidvol_return_interaction = bid_pca * current_log_return
                        lag_1_askvol_return_interaction = ask_pca * current_log_return
                        future_log_return_prediction = (
                            -0.0000035249
                            + 0.0000070160 * ask_pca
                            + -0.0000069054 * bid_pca
                            + -0.2087831028 * current_log_return
                            + -0.0064021782 * lag_1_askvol_return_interaction
                            + -0.0049996728 * lag_1_bidvol_return_interaction
                        )
                        """
                        future_price_prediction = np.exp(np.log(current_midprice) + future_log_return_prediction)
                        """
                        # What if we just set future price prediction to be equal to the mmbot_ midprice?
                        current_mmbot_log_return = np.log(current_row.mmbot_midprice) - np.log(previous_row.mmbot_midprice)
                        future_mmbot_log_return_prediction = -0.2933 * current_mmbot_log_return
                        future_price_prediction = current_row.mmbot_midprice * np.exp(future_mmbot_log_return_prediction)
                        # print(f"current_mmbt_midprice: {current_row.mmbot_midprice}")
                        # print(f"future_mmbot_log_return_prediction: {future_mmbot_log_return_prediction}")
                        # print(f"future_price_prediction: {future_price_prediction}")
                        theo = future_price_prediction - kelp_position * self.retreat_per_lot
                        bid_ask_spread = current_row.ask_price_1 - current_row.bid_price_1
                        # Maybe implement some sort of "dime check" that checks if we are diming others and have QP?
                        # Try a strategy where we go as wide as possible whilst still having QP, and not being in cross with our theo.
                        """
                        if bid_ask_spread <= 2:
                            my_bid = min(int(np.floor(theo)), current_row.bid_price_1)
                            my_ask = max(int(np.ceil(theo)), current_row.ask_price_1) #Try quoting wider - maybe if ba spread is wider we want to quote wider - if market is 4 wide maybe we quote 2 wide, else we quote 1 wide?
                        if bid_ask_spread >= 3:
                            my_bid = int(np.floor(theo - 0.5))
                            my_ask = int(np.ceil(theo + 0.5))
                        """
                        # Quoting as wide as possible whilst still having QP, and not being through our theo.
                        my_bid = min(int(np.floor(theo)), current_row.bid_price_1 + 1)
                        my_ask = max(int(np.ceil(theo)), current_row.ask_price_1 - 1)
                        bid_edge = theo - my_bid
                        ask_edge = my_ask - theo
                        edge0 = self.edge0

                        bid_volume = int(np.floor((bid_edge - edge0) / self.edge_per_lot)) if bid_edge > edge0 else 0
                        ask_volume = -int(np.floor((ask_edge - edge0) / self.edge_per_lot)) if ask_edge > edge0 else 0
                        # Below makes sure that we dont send orders over position limits.
                        bid_volume = min(bid_volume, 50 - kelp_position)
                        ask_volume = max(ask_volume, -50 - kelp_position)

                        orders.append(Order(product, int(my_ask), int(ask_volume)))
                        orders.append(Order(product, int(my_bid), int(bid_volume)))
            elif product == "SQUID_INK":
                # Check the rolling z score. If it is > 4, we sell,
                squink_position = state.position.get(product, 0)
                Trader.SQUINK_update_df(Trader.squink_df, product, state, orders, order_depth)

                if len(order_depth.sell_orders) != 0 and len(order_depth.buy_orders) != 0:
                    best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                    best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                    mid_price = (best_ask + best_bid) / 2
                    rolling_window = 150
                    if len(self.squink_df) > rolling_window:

                        z_score = (mid_price - self.squink_df.mid_price.rolling(rolling_window).mean().iloc[-1]) / self.squink_df.mid_price.rolling(
                            rolling_window
                        ).std().iloc[-1]
                        # Now that I have the Z-Score, I want to implement an edge model for entry

                        edge_0 = 2

                        if abs(z_score) > edge_0:
                            target_position = min(int((np.abs(z_score) - edge_0) * 10), 30)
                        else:
                            target_position = 0

                        if z_score <= -edge_0:
                            # print("A")
                            target_position = max(target_position, squink_position)
                            size_needed = target_position - squink_position
                            if size_needed < 0:
                                pass
                            else:
                                orders.append(Order(product, int(best_ask), int(size_needed)))
                            # orders.append(Order(product, best_bid+1, size_needed))

                        elif z_score >= edge_0:
                            # print("C")
                            target_position = min(-target_position, squink_position)
                            size_needed = target_position - squink_position
                            if size_needed > 0:
                                pass
                            else:
                                orders.append(Order(product, int(best_bid), int(size_needed)))
                                # orders.append(Order(product, best_ask - 1, size_needed))
                        # Now what if it is between?

                        else:
                            if squink_position > 0:
                                if z_score > 0:
                                    target_position = 0
                                    size_needed = target_position - squink_position
                                    orders.append(Order(product, int(best_bid), int(size_needed)))
                                    # orders.append(Order(product, best_ask - 1, size_needed))

                                else:
                                    exit_position = min(squink_position, int(-15 * z_score))
                                    trades_needed = exit_position - squink_position
                                    orders.append(Order(product, int(best_bid), int(trades_needed)))
                                    # orders.append(Order(product, best_ask-1, trades_needed))

                            if squink_position < 0:
                                if z_score < 0:
                                    target_position = 0
                                    size_needed = target_position - squink_position
                                    orders.append(Order(product, int(best_ask), int(size_needed)))
                                    # orders.append(Order(product, best_bid + 1, size_needed))
                                else:
                                    exit_position = min(squink_position, int(15 * z_score))
                                    trades_needed = exit_position - squink_position
                                    orders.append(Order(product, int(best_ask), int(trades_needed)))
                                    # orders.append(Order(product, best_bid + 1, trades_needed))

                        # Entry Attempt to fix sizing scheme above
                        """
                        if z_score < 0:
                            if z_score <= -edge_0:
                                print("A")
                                target_position = max(target_position, squink_position)
                                size_needed = target_position - squink_position
                                if size_needed < 0:
                                    pass
                                else:
                                    orders.append(Order(product, best_ask, size_needed))
                                    
                            elif z_score > -2 and z_score <= 0 and squink_position > 0:
                                print("B")
                                exit_position = min(squink_position, int(-15*z_score))
                                trades_needed = exit_position - squink_position
                                orders.append(Order(product, best_bid, -trades_needed))
                                
                        elif z_score > 0:        
                            if z_score >= edge_0:
                                print("C")
                                target_position = min(-target_position, squink_position)
                                size_needed = target_position - squink_position
                                if size_needed > 0:
                                    pass
                                else:
                                    orders.append(Order(product, best_bid, size_needed))

                            if z_score < 2 and z_score >=0 and squink_position < 0:
                                print("D")
                                exit_position = min(squink_position, int(15*z_score))
                                trades_needed = exit_position - squink_position
                                orders.append(Order(product, best_ask, trades_needed)) 
                            """

            result[product] = orders
        traderData = "SAMPLE"  # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.

        conversions = 1
        return result, conversions, traderData

class Product:
    KELP = "KELP"
    SQUID_INK = "SQUID_INK"
    RAINFOREST_RESIN = "RAINFOREST_RESIN"

class Trader:
    def __init__(self):
        self.kelp_prices = []
        self.kelp_vwap = []
        
        self.traderData = {}
        self.squid_mid_history = []

        self.POSITION_LIMITS = {
            Product.KELP: 50,
            Product.SQUID_INK: 50,
            Product.RAINFOREST_RESIN: 50,
        }

    def resin_orders(self, order_depth: OrderDepth, fair_value: int, position: int, position_limit: int) -> List[Order]:
        orders: List[Order] = []

        buy_order_volume = 0
        sell_order_volume = 0
        
        sell_prices_above = [price for price in order_depth.sell_orders.keys() if price > fair_value + 1]
        if sell_prices_above:
            baaf = min(sell_prices_above)
        else:
            baaf = fair_value + 2

        buy_prices_below = [price for price in order_depth.buy_orders.keys() if price < fair_value - 1]
        if buy_prices_below:
            bbbf = max(buy_prices_below)
        else:
            bbbf = fair_value - 2

        if len(order_depth.sell_orders) != 0:
            best_ask = min(order_depth.sell_orders.keys())
            best_ask_amount = -1 * order_depth.sell_orders[best_ask]
            if best_ask < fair_value:
                quantity = min(best_ask_amount, position_limit - position)  
                if quantity > 0:
                    orders.append(Order(Product.RAINFOREST_RESIN, int(round(best_ask)), quantity))
                    buy_order_volume += quantity

        if len(order_depth.buy_orders) != 0:
            best_bid = max(order_depth.buy_orders.keys())
            best_bid_amount = order_depth.buy_orders[best_bid]
            if best_bid > fair_value:
                quantity = min(best_bid_amount, position_limit + position)  
                if quantity > 0:
                    orders.append(Order(Product.RAINFOREST_RESIN, int(round(best_bid)), -1 * quantity))
                    sell_order_volume += quantity
        
        buy_order_volume, sell_order_volume = self.clear_position_order(
            orders, order_depth, position, position_limit, Product.RAINFOREST_RESIN,
            buy_order_volume, sell_order_volume, fair_value, 1)

        buy_quantity = position_limit - (position + buy_order_volume)
        if buy_quantity > 0:
            orders.append(Order(Product.RAINFOREST_RESIN, int(round(bbbf + 1)), buy_quantity))  

        sell_quantity = position_limit + (position - sell_order_volume)
        if sell_quantity > 0:
            orders.append(Order(Product.RAINFOREST_RESIN, int(round(baaf - 1)), -sell_quantity))  

        return orders
    
    def clear_position_order(
        self, orders: List[Order], order_depth: OrderDepth, position: int, position_limit: int,
        product: str, buy_order_volume: int, sell_order_volume: int, fair_value: float, width: int
    ) -> List[Order]:
        
        position_after_take = position + buy_order_volume - sell_order_volume
        fair = round(fair_value)
        fair_for_bid = math.floor(fair_value)
        fair_for_ask = math.ceil(fair_value)

        buy_quantity = position_limit - (position + buy_order_volume)
        sell_quantity = position_limit + (position - sell_order_volume)

        if position_after_take > 0:
            if fair_for_ask in order_depth.buy_orders.keys():
                clear_quantity = min(order_depth.buy_orders[fair_for_ask], position_after_take)
                sent_quantity = min(sell_quantity, clear_quantity)
                orders.append(Order(product, int(fair_for_ask), -abs(sent_quantity)))
                sell_order_volume += abs(sent_quantity)

        if position_after_take < 0:
            if fair_for_bid in order_depth.sell_orders.keys():
                clear_quantity = min(abs(order_depth.sell_orders[fair_for_bid]), abs(position_after_take))
                sent_quantity = min(buy_quantity, clear_quantity)
                orders.append(Order(product, int(fair_for_bid), abs(sent_quantity)))
                buy_order_volume += abs(sent_quantity)
    
        return buy_order_volume, sell_order_volume

    def kelp_orders(self, order_depth: OrderDepth, timespan: int, kelp_take_width: float, position: int, position_limit: int) -> List[Order]:
        orders: List[Order] = []

        buy_order_volume = 0
        sell_order_volume = 0

        if len(order_depth.sell_orders) != 0 and len(order_depth.buy_orders) != 0:    
            best_ask = min(order_depth.sell_orders.keys())
            best_bid = max(order_depth.buy_orders.keys())
            filtered_ask = [price for price in order_depth.sell_orders.keys() if abs(order_depth.sell_orders[price]) >= 21]  
            filtered_bid = [price for price in order_depth.buy_orders.keys() if abs(order_depth.buy_orders[price]) >= 15]
            mm_ask = min(filtered_ask) if len(filtered_ask) > 0 else best_ask
            mm_bid = max(filtered_bid) if len(filtered_bid) > 0 else best_bid
            
            mmmid_price = (mm_ask + mm_bid) / 2    
            self.kelp_prices.append(mmmid_price)

            volume = -1 * order_depth.sell_orders[best_ask] + order_depth.buy_orders[best_bid]
            vwap = (best_bid * (-1) * order_depth.sell_orders[best_ask] + best_ask * order_depth.buy_orders[best_bid]) / volume
            self.kelp_vwap.append({"vol": volume, "vwap": vwap})
            
            if len(self.kelp_vwap) > timespan:
                self.kelp_vwap.pop(0)
            
            if len(self.kelp_prices) > timespan:
                self.kelp_prices.pop(0)
        
            fair_value = mmmid_price

            if best_ask <= fair_value - kelp_take_width:
                ask_amount = -1 * order_depth.sell_orders[best_ask]
                if ask_amount <= 20:
                    quantity = min(ask_amount, position_limit - position)
                    if quantity > 0:
                        orders.append(Order(Product.KELP, int(round(best_ask)), quantity))
                        buy_order_volume += quantity
            if best_bid >= fair_value + kelp_take_width:
                bid_amount = order_depth.buy_orders[best_bid]
                if bid_amount <= 20:
                    quantity = min(bid_amount, position_limit + position)
                    if quantity > 0:
                        orders.append(Order(Product.KELP, int(round(best_bid)), -1 * quantity))
                        sell_order_volume += quantity

            buy_order_volume, sell_order_volume = self.clear_position_order(
                orders, order_depth, position, position_limit, Product.KELP,
                buy_order_volume, sell_order_volume, fair_value, 2)
            
            aaf = [price for price in order_depth.sell_orders.keys() if price > fair_value + 1]
            bbf = [price for price in order_depth.buy_orders.keys() if price < fair_value - 1]
            baaf = min(aaf) if len(aaf) > 0 else fair_value + 2
            bbbf = max(bbf) if len(bbf) > 0 else fair_value - 2
           
            buy_quantity = position_limit - (position + buy_order_volume)
            if buy_quantity > 0:
                orders.append(Order(Product.KELP, int(round(bbbf + 1)), buy_quantity))  

            sell_quantity = position_limit + (position - sell_order_volume)
            if sell_quantity > 0:
                orders.append(Order(Product.KELP, int(round(baaf - 1)), -sell_quantity))  

        return orders

    def get_running_pressure(self, order_depth: OrderDepth, trader_data: dict) -> float:
        if "last_best_bid" not in trader_data:
            trader_data["last_best_bid"] = None
        if "last_best_ask" not in trader_data:
            trader_data["last_best_ask"] = None
        if "last_best_bid_volume" not in trader_data:
            trader_data["last_best_bid_volume"] = 0
        if "last_best_ask_volume" not in trader_data:
            trader_data["last_best_ask_volume"] = 0
        if "pressure_history" not in trader_data:
            trader_data["pressure_history"] = []

        best_bid = None
        best_ask = None
        best_bid_volume = 0
        best_ask_volume = 0

        for bid, volume in order_depth.buy_orders.items():
            if volume >= 15:
                if best_bid is None or bid > best_bid:
                    best_bid = bid
                    best_bid_volume = volume

        for ask, volume in order_depth.sell_orders.items():
            if abs(volume) >= 15:
                if best_ask is None or ask < best_ask:
                    best_ask = ask
                    best_ask_volume = abs(volume)

        if best_bid is None or best_ask is None:
            return 0.0

        buy_pressure = 0
        sell_pressure = 0

        if best_bid is not None and trader_data["last_best_bid"] is not None:
            if best_bid > trader_data["last_best_bid"]:
                buy_pressure = best_bid_volume
            elif best_bid == trader_data["last_best_bid"]:
                buy_pressure = best_bid_volume - trader_data["last_best_bid_volume"]
            else:
                buy_pressure = -trader_data["last_best_bid_volume"]

        if best_ask is not None and trader_data["last_best_ask"] is not None:
            if best_ask < trader_data["last_best_ask"]:
                sell_pressure = best_ask_volume
            elif best_ask == trader_data["last_best_ask"]:
                sell_pressure = best_ask_volume - trader_data["last_best_ask_volume"]
            else:
                sell_pressure = -trader_data["last_best_ask_volume"]

        pressure_difference = buy_pressure - sell_pressure
        trader_data["pressure_history"].append(pressure_difference)
        if len(trader_data["pressure_history"]) > 50:
            trader_data["pressure_history"].pop(0)

        running_pressure = sum(trader_data["pressure_history"]) if len(trader_data["pressure_history"]) == 50 else 0

        trader_data["last_best_bid"] = best_bid
        trader_data["last_best_ask"] = best_ask
        trader_data["last_best_bid_volume"] = best_bid_volume
        trader_data["last_best_ask_volume"] = best_ask_volume

        return running_pressure
    
    def squid_ink_orders(self, position: int, timestamp: int, signal: str, fair_value: float) -> List[Order]:
        if Product.SQUID_INK not in self.traderData:
            self.traderData[Product.SQUID_INK] = {
                "upper_edge": 3,   
                "lower_edge": 3,    
                "volume_history": [],  
                "last_position": 0,   
                "optimized": False,    
                "last_signal": None     
            }
        
        available_volume = self.POSITION_LIMITS[Product.SQUID_INK] - abs(position)
        if available_volume <= 0:
            return []  
        
        orders = []
        state_data = self.traderData[Product.SQUID_INK]
        filled_volume = abs(position - state_data["last_position"])
        state_data["last_position"] = position

        if timestamp > 0:
            state_data["volume_history"].append(filled_volume)
            if len(state_data["volume_history"]) > 5:
                state_data["volume_history"].pop(0)
            
            if state_data["last_signal"] != signal:
                state_data["optimized"] = False
                state_data["volume_history"] = []
            
            if len(state_data["volume_history"]) >= 3 and not state_data["optimized"]:
                volume_avg = sum(state_data["volume_history"]) / len(state_data["volume_history"])
                volume_bar = 1  
                
                if signal == "b":
                    curr_edge = state_data["lower_edge"]
                    if volume_avg > volume_bar:
                        state_data["lower_edge"] = min(curr_edge + 1, 5)
                        state_data["volume_history"] = []
                    elif volume_avg < volume_bar * 0.7:
                        state_data["lower_edge"] = max(curr_edge - 1, -5)
                        state_data["volume_history"] = []
                else: 
                    curr_edge = state_data["upper_edge"]
                    if volume_avg > volume_bar:
                        state_data["upper_edge"] = min(curr_edge + 1, 5)
                        state_data["volume_history"] = []
                    elif volume_avg < volume_bar * 0.7:
                        state_data["upper_edge"] = max(curr_edge - 1, -5)
                        state_data["volume_history"] = []
        
        state_data["last_signal"] = signal
        upper_edge = state_data["upper_edge"]
        lower_edge = state_data["lower_edge"]
        
        if signal == "b":
            target_volume = self.POSITION_LIMITS[Product.SQUID_INK] - position
            if target_volume > 0:
                return [Order(Product.SQUID_INK, fair_value - lower_edge, int(round(target_volume)))]
            else:
                return []
        elif signal == "s":
            target_volume = -self.POSITION_LIMITS[Product.SQUID_INK] - position
            if target_volume < 0:
                return [Order(Product.SQUID_INK, fair_value + upper_edge, int(round(target_volume)))]
            else:
                return []
        else:
            return []

    def squid_orders(self, state: TradingState) -> List[Order]:
        squid_position = state.position.get(Product.SQUID_INK, 0)
        order_depth = state.order_depths[Product.SQUID_INK]

        best_ask = min(order_depth.sell_orders.keys())
        best_bid = max(order_depth.buy_orders.keys())
        filtered_ask = [price for price in order_depth.sell_orders.keys() if abs(order_depth.sell_orders[price]) >= 20]
        filtered_bid = [price for price in order_depth.buy_orders.keys() if abs(order_depth.buy_orders[price]) >= 20]
        mm_ask = min(filtered_ask) if len(filtered_ask) > 0 else best_ask
        mm_bid = max(filtered_bid) if len(filtered_bid) > 0 else best_bid
        mmmid_price = (mm_ask + mm_bid) / 2
        self.squid_mid_history.append(mmmid_price)
        self.squid_mid_history = self.squid_mid_history[-4:]
        if len(self.squid_mid_history) >= 2:
            fair_value = round((self.squid_mid_history[-1] + self.squid_mid_history[-2]) / 2)
        else:
            fair_value = mmmid_price

        running_pressure = self.get_running_pressure(order_depth, self.traderData)
        if (running_pressure > 0 and running_pressure < 30) or (running_pressure < -30):
            signal = "b"
        elif (running_pressure < 0 and running_pressure > -30) or (running_pressure > 30):
            signal = "s"
        else:
            signal = "h"

        return self.squid_ink_orders(squid_position, state.timestamp, signal, fair_value)
    
    def run(self, state: TradingState):
        result = {}

        if Product.RAINFOREST_RESIN in state.order_depths:
            resin_position = state.position.get(Product.RAINFOREST_RESIN, 0)
            resin_orders_list = self.resin_orders(
                state.order_depths[Product.RAINFOREST_RESIN], 10000,
                resin_position, self.POSITION_LIMITS[Product.RAINFOREST_RESIN]
            )
            result[Product.RAINFOREST_RESIN] = resin_orders_list

        if Product.KELP in state.order_depths:
            kelp_position = state.position.get(Product.KELP, 0)
            kelp_orders_list = self.kelp_orders(state.order_depths[Product.KELP], 10, 1, kelp_position, self.POSITION_LIMITS[Product.KELP])
            result[Product.KELP] = kelp_orders_list

        if Product.SQUID_INK in state.order_depths:
            result[Product.SQUID_INK] = self.squid_orders(state)

        traderData = jsonpickle.encode({
            "kelp_prices": self.kelp_prices, 
            "kelp_vwap": self.kelp_vwap,
            "squid_mid_history": self.squid_mid_history,
            "traderData": self.traderData
        })

        conversions = 0
        logger.flush(state, result, conversions, "")
        return result, conversions, traderData


class Trader:
    def __init__(self):
        self.kelp_prices = []
        self.resin_prices = []
        self.squid_ink_prices = []
        self.croissants_prices = []
        self.jams_prices = []
        self.djembes_prices = []
        self.kelp_vwap = []
        self.resin_vwap = []
        self.squid_ink_vwap = []
        self.croissants_vwap = []
        self.jams_vwap = []
        self.djembes_vwap = []
        self.insider_id = "Olivia"
        self.insider_tracked_products = ["SQUID_INK", "CROISSANTS"]

        self.insider_regimes = {
            "SQUID_INK": None,  # Can be "bullish", "bearish", or None
            "CROISSANTS": None  # Can be "bullish", "bearish", or None
        }
        self.insider_last_trades = {
            "SQUID_INK": [],
            "CROISSANTS": []
        }

        # Basket statistical arbitrage constants
        self.pb1_intercept = 2023.97
        self.pb1_croissants_coef = 6.87
        self.pb1_jams_coef = 2.02
        self.pb1_djembes_coef = 1.06
        
        self.pb2_intercept = 4684.05
        self.pb2_croissants_coef = 3.14
        self.pb2_jams_coef = 1.85

        # Basket equation constants
        self.pb1_intercept = -57.71 # calculated from R1-3
        self.pb1_croissants_coef = 6
        self.pb1_jams_coef = 3
        self.pb1_djembes_coef = 1

        self.pb2_intercept = -22.59 # calculated from R1-3
        self.pb2_croissants_coef = 4
        self.pb2_jams_coef = 2
        
        # Define basket components for convert operations
        self.basket_components = {
            "PICNIC_BASKET1": {"CROISSANTS": 6, "JAMS": 3, "DJEMBES": 1},
            "PICNIC_BASKET2": {"CROISSANTS": 4, "JAMS": 2}
        }

        self.active_products = {
            "KELP": True,
            "RAINFOREST_RESIN": True,
            "SQUID_INK": True,
            "CROISSANTS": True,
            "JAMS": True,
            "DJEMBES": True,
            "PICNIC_BASKET1": True,
            "PICNIC_BASKET2": False,
            "VOLCANIC_ROCK": False,
            "VOLCANIC_ROCK_VOUCHER_9500": False,
            "VOLCANIC_ROCK_VOUCHER_9750": True,
            "VOLCANIC_ROCK_VOUCHER_10000": True,
            "VOLCANIC_ROCK_VOUCHER_10250": False,
            "VOLCANIC_ROCK_VOUCHER_10500": False,
            "MAGNIFICENT_MACARONS": True,
        }
        self.config: Dict[str, float] = {
            "CSI_THRESHOLD": 0,          # sunlight index cut‑off
            "MAX_CONVERSION_LIMIT": 10,  # contractual daily cap
            "NORMAL_EDGE": 1.0,          # base edge (ticks) in normal regime
        }
        self.position_limits = {
            "KELP": 50,
            "RAINFOREST_RESIN": 50,
            "SQUID_INK": 50,
            "CROISSANTS": 250,
            "JAMS": 350,
            "DJEMBES": 60,
            "PICNIC_BASKET1": 60,
            "PICNIC_BASKET2": 100,
            "VOLCANIC_ROCK_VOUCHER_9500": 200,
            "VOLCANIC_ROCK_VOUCHER_9750": 200,
            "VOLCANIC_ROCK_VOUCHER_10000": 200,
            "VOLCANIC_ROCK_VOUCHER_10250": 200,
            "VOLCANIC_ROCK_VOUCHER_10500": 200,
            "VOLCANIC_ROCK": 400,
            "MAGNIFICENT_MACARONS": 75,
        }
        self.timespan = 20
        self.make_width = {
            "KELP": 8.0,
            "RAINFOREST_RESIN": 3.0,
            "SQUID_INK": 5.0,
            "CROISSANTS": 1.0,
            "JAMS": 2.0,
            "DJEMBES": 2.0,
        }
        self.take_width = {
            "KELP": 1.0,
            "RAINFOREST_RESIN": 0.3,
            "SQUID_INK": 0.7,
            "CROISSANTS": 0.5,
            "JAMS": 0.5,
            "DJEMBES": 0.5,
        }
        self.squid_ink_volatility_threshold = 3.0
        self.squid_ink_momentum_period = 10
        self.squid_ink_mean_window = 30
        self.squid_ink_deviation_threshold = 0.05
        self.squid_ink_max_position_time = 5
        self.squid_ink_position_start_time = 0
        self.squid_ink_last_position = 0
        self.voucher_strikes = {
            "VOLCANIC_ROCK_VOUCHER_9500": 9500,
            "VOLCANIC_ROCK_VOUCHER_9750": 9750,
            "VOLCANIC_ROCK_VOUCHER_10000": 10000,
            "VOLCANIC_ROCK_VOUCHER_10250": 10250,
            "VOLCANIC_ROCK_VOUCHER_10500": 10500,
        }
        self.days_to_expiry = 7
        self.mean_volatility = 0.18
        self.volatility_window = 30
        self.zscore_threshold = 1.8
        self.past_volatilities = {}
        self.arbitrage_threshold = 0.001
        self.max_arbitrage_size = 50
        self.risk_free_rate = 0.0
        self.stop_loss_multiplier = 1.2
        self.profit_target_multiplier = 2.5
        self.max_stop_loss_hits = 1
        self.stop_loss_hits = 0
        self.positions = {}
        self.daily_pnl = 0
        self.current_day = 0
        self.max_daily_loss = 50000
        self.profit_target = 20000
        self.position_scale = 1.0
        self.max_volatility_history = 30
        self.cache = {}
        self.last_tick_time = 0
        self.adaptive_edge = 1.0
        self.macaron_edge = 1.0
        self.macaron_target_vol = 10
        self.macaron_fill_history: list[int] = []
        self.low_sun_regime = False
        self.timespan = 20
        self.cache: dict[str, float] = {}

    def calculate_fair_value(self, order_depth: OrderDepth) -> float:
        try:
            if not order_depth.buy_orders or not order_depth.sell_orders:
                return None
            best_bid = max(order_depth.buy_orders.keys())
            best_ask = min(order_depth.sell_orders.keys())
            return (best_bid + best_ask) / 2
        except Exception as e:
            logger.print(f"Error calculating fair value: {e}")
            return None

    def clear_position_order(
        self,
        orders: list[Order],
        order_depth: OrderDepth,
        position: int,
        position_limit: int,
        product: str,
        buy_order_volume: int,
        sell_order_volume: int,
        fair_value: float,
        width: int,
    ) -> tuple[int, int]:
        position_after_take = position + buy_order_volume - sell_order_volume
        fair_for_bid = int(math.floor(fair_value))
        fair_for_ask = int(math.ceil(fair_value))
        buy_quantity = position_limit - (position + buy_order_volume)
        sell_quantity = position_limit + (position - sell_order_volume)
        if position_after_take > 0:
            if fair_for_ask in order_depth.buy_orders.keys():
                clear_quantity = min(
                    order_depth.buy_orders[fair_for_ask], position_after_take
                )
                sent_quantity = min(sell_quantity, clear_quantity)
                if sent_quantity > 0:
                    orders.append(Order(product, fair_for_ask, -abs(sent_quantity)))
                    sell_order_volume += abs(sent_quantity)
        if position_after_take < 0:
            if fair_for_bid in order_depth.sell_orders.keys():
                clear_quantity = min(
                    abs(order_depth.sell_orders[fair_for_bid]), abs(position_after_take)
                )
                sent_quantity = min(buy_quantity, clear_quantity)
                if sent_quantity > 0:
                    orders.append(Order(product, fair_for_bid, abs(sent_quantity)))
                    buy_order_volume += abs(sent_quantity)
        return buy_order_volume, sell_order_volume

    def product_orders(
        self, product: str, order_depth: OrderDepth, position: int
    ) -> list[Order]:
        orders = []
        position_limit = self.position_limits[product]
        buy_order_volume = 0
        sell_order_volume = 0
        if len(order_depth.sell_orders) == 0 or len(order_depth.buy_orders) == 0:
            return orders
        best_ask = min(order_depth.sell_orders.keys())
        best_bid = max(order_depth.buy_orders.keys())
        filtered_asks = [
            p
            for p in order_depth.sell_orders.keys()
            if abs(order_depth.sell_orders[p]) >= 10
        ]
        filtered_bids = [
            p
            for p in order_depth.buy_orders.keys()
            if abs(order_depth.buy_orders[p]) >= 10
        ]
        mm_ask = min(filtered_asks) if filtered_asks else best_ask
        mm_bid = max(filtered_bids) if filtered_bids else best_bid
        mm_mid_price = (mm_ask + mm_bid) / 2
        if product == "KELP":
            self.kelp_prices.append(mm_mid_price)
            if len(self.kelp_prices) > self.timespan:
                self.kelp_prices.pop(0)
            volume = (
                -1 * order_depth.sell_orders[best_ask]
                + order_depth.buy_orders[best_bid]
            )
            vwap = (
                best_bid * (-1) * order_depth.sell_orders[best_ask]
                + best_ask * order_depth.buy_orders[best_bid]
            ) / volume
            self.kelp_vwap.append({"vol": volume, "vwap": vwap})
            if len(self.kelp_vwap) > self.timespan:
                self.kelp_vwap.pop(0)
            if len(self.kelp_vwap) > 0:
                total_vol = sum(x["vol"] for x in self.kelp_vwap)
                fair_value = (
                    (sum(x["vwap"] * x["vol"] for x in self.kelp_vwap) / total_vol)
                    if total_vol > 0
                    else mm_mid_price
                )
            else:
                fair_value = mm_mid_price
        elif product == "RAINFOREST_RESIN":
            self.resin_prices.append(mm_mid_price)
            if len(self.resin_prices) > self.timespan:
                self.resin_prices.pop(0)
            volume = (
                -1 * order_depth.sell_orders[best_ask]
                + order_depth.buy_orders[best_bid]
            )
            vwap = (
                best_bid * (-1) * order_depth.sell_orders[best_ask]
                + best_ask * order_depth.buy_orders[best_bid]
            ) / volume
            self.resin_vwap.append({"vol": volume, "vwap": vwap})
            if len(self.resin_vwap) > self.timespan:
                self.resin_vwap.pop(0)
            if len(self.resin_vwap) > 0:
                total_vol = sum(x["vol"] for x in self.resin_vwap)
                fair_value = (
                    (sum(x["vwap"] * x["vol"] for x in self.resin_vwap) / total_vol)
                    if total_vol > 0
                    else mm_mid_price
                )
            else:
                fair_value = mm_mid_price
        else:
            fair_value = mm_mid_price
        if best_ask <= fair_value - self.take_width.get(product, 0):
            ask_amount = -1 * order_depth.sell_orders[best_ask]
            if ask_amount <= 20:
                quantity = min(ask_amount, position_limit - position)
                if quantity > 0:
                    orders.append(Order(product, best_ask, quantity))
                    buy_order_volume += quantity
        if best_bid >= fair_value + self.take_width.get(product, 0):
            bid_amount = order_depth.buy_orders[best_bid]
            if bid_amount <= 20:
                quantity = min(bid_amount, position_limit + position)
                if quantity > 0:
                    orders.append(Order(product, best_bid, -quantity))
                    sell_order_volume += quantity
        buy_order_volume, sell_order_volume = self.clear_position_order(
            orders,
            order_depth,
            position,
            position_limit,
            product,
            buy_order_volume,
            sell_order_volume,
            fair_value,
            2,
        )
        asks_above_fair = [
            p for p in order_depth.sell_orders.keys() if p > fair_value + 1
        ]
        bids_below_fair = [
            p for p in order_depth.buy_orders.keys() if p < fair_value - 1
        ]
        best_ask_above_fair = (
            min(asks_above_fair) if asks_above_fair else int(fair_value) + 2
        )
        best_bid_below_fair = (
            max(bids_below_fair) if bids_below_fair else int(fair_value) - 2
        )
        buy_quantity = position_limit - (position + buy_order_volume)
        if buy_quantity > 0:
            buy_price = int(best_bid_below_fair + 1)
            orders.append(Order(product, buy_price, buy_quantity))
        sell_quantity = position_limit + (position - sell_order_volume)
        if sell_quantity > 0:
            sell_price = int(best_ask_above_fair - 1)
            orders.append(Order(product, sell_price, -sell_quantity))
        return orders

    def close_position(
        self, product: str, order_depth: OrderDepth, position: int
    ) -> list[Order]:
        orders = []
        if position == 0:
            return orders
        if position > 0:
            if order_depth.buy_orders:
                best_bid = max(order_depth.buy_orders.keys())
                sell_quantity = min(position, order_depth.buy_orders[best_bid])
                if sell_quantity > 0:
                    orders.append(Order(product, best_bid, -sell_quantity))
        else:
            if order_depth.sell_orders:
                best_ask = min(order_depth.sell_orders.keys())
                buy_quantity = min(-position, -order_depth.sell_orders[best_ask])
                if buy_quantity > 0:
                    orders.append(Order(product, best_ask, buy_quantity))
        return orders

    def squid_ink_strategy(
        self, order_depth: OrderDepth, position: int, state_timestamp: int
    ) -> list[Order]:
        orders = []
        position_limit = self.position_limits["SQUID_INK"]
        if not order_depth.sell_orders or not order_depth.buy_orders:
            return orders
        
        best_ask = min(order_depth.sell_orders.keys())
        best_bid = max(order_depth.buy_orders.keys())
        mid_price = (best_ask + best_bid) / 2
        
        self.squid_ink_prices.append(mid_price)
        if len(self.squid_ink_prices) > max(self.timespan, self.squid_ink_mean_window):
            self.squid_ink_prices.pop(0)
            
        if len(self.squid_ink_prices) < 10:
            return orders
            
        recent_window = min(len(self.squid_ink_prices), self.squid_ink_mean_window)
        mean_price = sum(self.squid_ink_prices[-recent_window:]) / recent_window
        
        if len(self.squid_ink_prices) >= 2:
            volatility = statistics.stdev(
                self.squid_ink_prices[-min(10, len(self.squid_ink_prices)) :]
            )
        else:
            volatility = 0
            
        deviation_pct = (
            abs(mid_price - mean_price) / mean_price if mean_price > 0 else 0
        )
        
        # Get the current regime from insider signals
        current_regime = self.insider_regimes["SQUID_INK"]
        
        # Position management based on time in position
        if position != 0 and self.squid_ink_position_start_time > 0:
            time_in_position = state_timestamp - self.squid_ink_position_start_time
            if time_in_position >= self.squid_ink_max_position_time:
                return self.close_position("SQUID_INK", order_depth, position)
        
        # Adjust strategy based on insider regime
        if position == 0:
            # Opening new positions
            if volatility > self.squid_ink_volatility_threshold and deviation_pct > self.squid_ink_deviation_threshold:
                # If price is above mean and regime is bearish, take short position
                if mid_price > mean_price and (current_regime != "bullish"):
                    quantity = min(order_depth.buy_orders[best_bid], position_limit)
                    if quantity > 0:
                        orders.append(Order("SQUID_INK", best_bid, -quantity))
                        self.squid_ink_position_start_time = state_timestamp
                        self.squid_ink_last_position = -quantity
                
                # If price is below mean and regime is bullish, take long position
                elif mid_price < mean_price and (current_regime != "bearish"):
                    quantity = min(-order_depth.sell_orders[best_ask], position_limit)
                    if quantity > 0:
                        orders.append(Order("SQUID_INK", best_ask, quantity))
                        self.squid_ink_position_start_time = state_timestamp
                        self.squid_ink_last_position = quantity
        else:
            # Managing existing positions
            if position > 0:
                # For long positions
                if mid_price >= mean_price or current_regime == "bearish":
                    # Close long position if price is at or above mean or regime turned bearish
                    quantity = min(position, order_depth.buy_orders[best_bid])
                    if quantity > 0:
                        orders.append(Order("SQUID_INK", best_bid, -quantity))
                        if quantity == position:
                            self.squid_ink_position_start_time = 0
                            self.squid_ink_last_position = 0
            elif position < 0:
                # For short positions
                if mid_price <= mean_price or current_regime == "bullish":
                    # Close short position if price is at or below mean or regime turned bullish
                    quantity = min(-position, -order_depth.sell_orders[best_ask])
                    if quantity > 0:
                        orders.append(Order("SQUID_INK", best_ask, quantity))
                        if quantity == -position:
                            self.squid_ink_position_start_time = 0
                            self.squid_ink_last_position = 0
        
        return orders

    def calculate_synthetic_value(self, state: TradingState, basket_type: str) -> float:
        if basket_type == "PICNIC_BASKET1":
            croissant_price = self.calculate_fair_value(
                state.order_depths["CROISSANTS"]
            )
            jams_price = self.calculate_fair_value(state.order_depths["JAMS"])
            djembes_price = self.calculate_fair_value(state.order_depths["DJEMBES"])
            if None in [croissant_price, jams_price, djembes_price]:
                return None
            return (self.pb1_intercept + 
                   self.pb1_croissants_coef * croissant_price + 
                   self.pb1_jams_coef * jams_price + 
                   self.pb1_djembes_coef * djembes_price)
        elif basket_type == "PICNIC_BASKET2":
            croissant_price = self.calculate_fair_value(
                state.order_depths["CROISSANTS"]
            )
            jams_price = self.calculate_fair_value(state.order_depths["JAMS"])
            if None in [croissant_price, jams_price]:
                return None
            return (self.pb2_intercept +
                   self.pb2_croissants_coef * croissant_price +
                   self.pb2_jams_coef * jams_price)
        return None
def norm_cdf(self, x: float) -> float:
        a1 = 0.254829592
        a2 = -0.284496736
        a3 = 1.421413741
        a4 = -1.453152027
        a5 = 1.061405429
        p = 0.3275911
        sign = 1
        if x < 0:
            sign = -1
        x = abs(x) / math.sqrt(2.0)
        t = 1.0 / (1.0 + p * x)
        y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(
            -x * x
        )
        return 0.5 * (1.0 + sign * y)

    def norm_pdf(self, x: float) -> float:
        return (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * x * x)
def find_arbitrage_opportunities(
        self, state: TradingState, rock_order_depth: OrderDepth, rock_mid: float
    ) -> list[Order]:
        orders = []
        tte = self.get_time_to_expiry(state.timestamp)
        voucher_prices = {}
        for voucher_symbol in self.voucher_strikes.keys():
            if voucher_symbol in state.order_depths:
                voucher_mid = self.calculate_fair_value(
                    state.order_depths[voucher_symbol]
                )
                if voucher_mid is not None:
                    voucher_prices[voucher_symbol] = voucher_mid
        for i in range(len(self.voucher_strikes)):
            for j in range(i + 1, len(self.voucher_strikes)):
                strike1 = list(self.voucher_strikes.values())[i]
                strike2 = list(self.voucher_strikes.values())[j]
                symbol1 = list(self.voucher_strikes.keys())[i]
                symbol2 = list(self.voucher_strikes.keys())[j]
                if symbol1 in voucher_prices and symbol2 in voucher_prices:
                    price1 = voucher_prices[symbol1]
                    price2 = voucher_prices[symbol2]
                    spread = abs(price1 - price2)
                    strike_diff = abs(strike1 - strike2)
                    if (
                        abs(spread - strike_diff)
                        > self.arbitrage_threshold * strike_diff
                    ):
                        if spread > strike_diff * (1 + self.arbitrage_threshold):
                            if price1 > price2:
                                orders.append(
                                    Order(
                                        symbol1,
                                        int(
                                            min(
                                                state.order_depths[
                                                    symbol1
                                                ].sell_orders.keys()
                                            )
                                        ),
                                        -self.max_arbitrage_size,
                                    )
                                )
                                orders.append(
                                    Order(
                                        symbol2,
                                        int(
                                            max(
                                                state.order_depths[
                                                    symbol2
                                                ].buy_orders.keys()
                                            )
                                        ),
                                        self.max_arbitrage_size,
                                    )
                                )
                            else:
                                orders.append(
                                    Order(
                                        symbol2,
                                        int(
                                            min(
                                                state.order_depths[
                                                    symbol2
                                                ].sell_orders.keys()
                                            )
                                        ),
                                        -self.max_arbitrage_size,
                                    )
                                )
                                orders.append(
                                    Order(
                                        symbol1,
                                        int(
                                            max(
                                                state.order_depths[
                                                    symbol1
                                                ].buy_orders.keys()
                                            )
                                        ),
                                        self.max_arbitrage_size,
                                    )
                                )
        return orders

def run(self, state: TradingState) -> tuple[dict[str, list[Order]], int, str]:
        try:
            result = {}
            conversions = 0
            trader_data = {}

            # --- 1) Process insider trades and update sunshine regime
            self.process_insider_trades(state)
            obs = state.observations
            self._update_regime(obs)

            current_day = state.timestamp // 1000000
            if current_day != self.current_day:
                self.daily_pnl = 0
                self.current_day = current_day

            # Update days_to_expiry based on current timestamp
            days_remaining = max(0, 7 - current_day)
            self.days_to_expiry = days_remaining

            if state.traderData and state.traderData != "SAMPLE":
                try:
                    trader_data = jsonpickle.decode(state.traderData)
                    if "past_volatilities" in trader_data:
                        self.past_volatilities = trader_data["past_volatilities"]
                    for prod in [
                        "kelp",
                        "resin",
                        "squid_ink",
                        "croissants",
                        "jams",
                        "djembes",
                    ]:
                        if f"{prod}_prices" in trader_data:
                            setattr(
                                self, f"{prod}_prices", trader_data[f"{prod}_prices"]
                            )
                        if f"{prod}_vwap" in trader_data:
                            setattr(self, f"{prod}_vwap", trader_data[f"{prod}_vwap"])

                    # Load insider trading data from trader_data if available
                    if "insider_regimes" in trader_data:
                        self.insider_regimes = trader_data["insider_regimes"]
                    if "insider_last_trades" in trader_data:
                        self.insider_last_trades = trader_data["insider_last_trades"]

                except Exception as e:
                    logger.print(f"Could not parse trader data: {e}")

            # --- 2) Compute macarons conversions based on sunlight and arbitrage
            mac_pos = state.position.get("MAGNIFICENT_MACARONS", 0)
            conversions = self.macaron_arb_clear(mac_pos, obs)

            # --- 3) Macarons take/make orders
            mac_od = state.order_depths.get("MAGNIFICENT_MACARONS")
            if mac_od and self.active_products.get("MAGNIFICENT_MACARONS", False):
                take_orders, buy_vol, sell_vol = self.macaron_arb_take(mac_od, obs, mac_pos)
                make_orders, _, _ = self.macaron_arb_make(mac_od, obs, mac_pos, buy_vol, sell_vol)
                if take_orders or make_orders:
                    result["MAGNIFICENT_MACARONS"] = take_orders + make_orders
            # If product is inactive but we have a position, try to close it
            elif mac_pos != 0:
                close_orders = self.close_position(
                    "MAGNIFICENT_MACARONS", mac_od, mac_pos
                )
                if close_orders:
                    result["MAGNIFICENT_MACARONS"] = close_orders

            handled = set()
            if "MAGNIFICENT_MACARONS" in result:
                handled.add("MAGNIFICENT_MACARONS")
            
            # Special handling for CROISSANTS and SQUID_INK - copy Olivia's trades
            for product in ["CROISSANTS", "SQUID_INK"]:
                if product in state.order_depths and self.active_products.get(product, False):
                    product_orders = self.copy_olivia_trades(state, product)
                    if product_orders:
                        result[product] = product_orders
                    handled.add(product)

            # Handle vouchers and VOLCANIC_ROCK
            if "VOLCANIC_ROCK" in state.order_depths:
                rock_position = state.position.get("VOLCANIC_ROCK", 0)
                rock_order_depth = state.order_depths["VOLCANIC_ROCK"]
                rock_mid = self.calculate_fair_value(rock_order_depth)

                # Always process vouchers
                if rock_mid is not None:
                    voucher_positions = {}
                    voucher_deltas = {}
                    for voucher_symbol in self.voucher_strikes.keys():
                        if voucher_symbol in state.order_depths:
                            try:
                                voucher_position = state.position.get(voucher_symbol, 0)
                                voucher_positions[voucher_symbol] = voucher_position

                                # Only generate orders if the voucher is active
                                if self.active_products.get(voucher_symbol, False):
                                    take_orders, make_orders = (
                                        self.volcanic_rock_voucher_orders(
                                            state,
                                            rock_order_depth,
                                            rock_position,
                                            voucher_symbol,
                                            state.order_depths[voucher_symbol],
                                            voucher_position,
                                            trader_data,
                                        )
                                    )
                                    if take_orders or make_orders:
                                        result.setdefault(voucher_symbol, []).extend(
                                            take_orders + make_orders
                                        )
                                # If inactive but has position, try to close it
                                elif voucher_position != 0:
                                    close_orders = self.close_position(
                                        voucher_symbol,
                                        state.order_depths[voucher_symbol],
                                        voucher_position,
                                    )
                                    if close_orders:
                                        result.setdefault(voucher_symbol, []).extend(
                                            close_orders
                                        )
                            except Exception as e:
                                logger.print(
                                    f"Error processing voucher {voucher_symbol}: {e}"
                                )

                # Only trade VOLCANIC_ROCK if it's active
                if self.active_products.get("VOLCANIC_ROCK", False):
                    if rock_mid is not None:
                        arbitrage_orders = self.find_arbitrage_opportunities(
                            state, rock_order_depth, rock_mid
                        )
                        if arbitrage_orders:
                            for order in arbitrage_orders:
                                result.setdefault(order.symbol, []).append(order)

                    vol_orders = self.volcanic_rock_orders(
                        rock_order_depth, rock_position, state
                    )
                    if vol_orders:
                        result.setdefault("VOLCANIC_ROCK", []).extend(vol_orders)
                # If VOLCANIC_ROCK is not active but we have a position, close it
                elif rock_position != 0:
                    orders = self.close_position(
                        "VOLCANIC_ROCK", rock_order_depth, rock_position
                    )
                    if orders:
                        result["VOLCANIC_ROCK"] = orders

                handled.add("VOLCANIC_ROCK")
                handled.update(self.voucher_strikes.keys())

            # Handle other products
            for product in state.order_depths.keys():
                if product in handled:
                    continue

                position = state.position.get(product, 0)

                if product in ["PICNIC_BASKET1", "PICNIC_BASKET2"]:
                    # Always calculate synthetic values for baskets
                    synthetic_value = self.calculate_synthetic_value(state, product)

                    # Only execute trades if the product is active
                    if self.active_products.get(product, False):
                        # Execute basket arbitrage - don't skip for baskets
                        arbitrage_orders = self.execute_basket_arbitrage(state, product)
                        if not arbitrage_orders or product not in arbitrage_orders:
                            orders = self.trade_basket_divergence(
                                product,
                                state.order_depths[product],
                                position,
                                synthetic_value,
                            )
                            if orders:
                                result[product] = orders
                        else:
                            for p, orders in arbitrage_orders.items():
                                # Only add orders for active products, but skip CROISSANTS and SQUID_INK
                                # (These are traded only through copy_olivia_trades)
                                if self.active_products.get(p, False) and p not in ["CROISSANTS", "SQUID_INK"]:
                                    result.setdefault(p, []).extend(orders)

                elif product in [
                    "KELP",
                    "RAINFOREST_RESIN",
                    "JAMS",
                    "DJEMBES",
                ]:  # Removed CROISSANTS and SQUID_INK from this list
                    # Always perform calculations
                    if product == "KELP":
                        self.kelp_prices.append(
                            self.calculate_fair_value(state.order_depths[product]) or 0
                        )
                        if len(self.kelp_prices) > self.timespan:
                            self.kelp_prices.pop(0)
                    elif product == "RAINFOREST_RESIN":
                        self.resin_prices.append(
                            self.calculate_fair_value(state.order_depths[product]) or 0
                        )
                        if len(self.resin_prices) > self.timespan:
                            self.resin_prices.pop(0)

                    # Only execute trades if the product is active
                    if self.active_products.get(product, False):
                        orders = self.product_orders(
                            product, state.order_depths[product], position
                        )
                        if orders:
                            result[product] = orders

                # Handle vouchers - check separately since they have different names
                elif product.startswith("VOLCANIC_ROCK_VOUCHER_"):
                    # Only execute trades if the product is active
                    if self.active_products.get(product, False):
                        if position != 0:
                            orders = self.close_position(
                                product, state.order_depths[product], position
                            )
                            if orders:
                                result[product] = orders

                elif product in self.active_products and self.active_products[product] and product not in ["CROISSANTS", "SQUID_INK"]:
                    orders = self.product_orders(
                        product, state.order_depths[product], position
                    )
                    if orders:
                        result[product] = orders

                # For inactive products with positions, close the positions
                elif position != 0:
                    orders = self.close_position(
                        product, state.order_depths[product], position
                    )
                    if orders:
                        result[product] = orders

            # Save insider trading data in trader_data
            trader_data["insider_regimes"] = self.insider_regimes
            trader_data["insider_last_trades"] = self.insider_last_trades

            trader_data["past_volatilities"] = self.past_volatilities
            serialized_trader_data = jsonpickle.encode(trader_data)
            if len(self.cache) > 1000:
                self.cache.clear()
            logger.flush(state, result, conversions, serialized_trader_data)
            return result, conversions, serialized_trader_data
        except Exception as e:
            logger.print(f"Error in run method: {e}")
            return {}, 0, "{}"

    def _update_regime(self, obs: Observation) -> None:
        """Compute sunlight regime & emit log on change."""
        if "MAGNIFICENT_MACARONS" not in obs.conversionObservations:
            return
        sun = obs.conversionObservations["MAGNIFICENT_MACARONS"].sunlightIndex
        prev = getattr(self, "low_sun_regime", False)
        self.low_sun_regime = sun < self.config["CSI_THRESHOLD"]
        if self.low_sun_regime != prev:
            regime = "LOW" if self.low_sun_regime else "NORMAL"
            logger.print(f"Regime switch → {regime} (CSI {sun:.1f})")



class MarketUtils:
    """Holds utility functions used across strategies."""

    def safe_best_bid(self, order_depth) -> Optional[int]:
        if not order_depth or not order_depth.buy_orders:
            return None
        return max(order_depth.buy_orders.keys())

    def safe_best_ask(self, order_depth) -> Optional[int]:
        if not order_depth or not order_depth.sell_orders:
            return None
        return min(order_depth.sell_orders.keys())

    def has_liquidity(self, order_depth) -> bool:
        return bool(order_depth and order_depth.buy_orders and order_depth.sell_orders)

    def rolling_mean_std(self, values: List[float], period: int) -> Tuple[float, float]:
        window = values[-period:]
        n = len(window)
        if n == 0:
            return 0.0, 0.0
        m = sum(window) / n
        var = sum((x - m) ** 2 for x in window) / n
        return m, math.sqrt(var)


class InteractionBlocks:
    """Wraps strategy helper functions: mean reversion, taking, making, zero-EV."""

    def __init__(self, utils: MarketUtils):
        self.u = utils

    def mean_reversion_taker(
        self,
        state,  # TradingState
        parent,  # Strategy
        symbol: str,
        limit: int,
        price_array: List[float],
        fair_price: float,
        period: int,
        z_score_threshold: float,
        fixed_threshold: float,
    ) -> None:
        position = state.position.get(symbol, 0)
        order_depth = parent.order_depth_internal

        if len(price_array) < period:
            return

        rolling_mean = sum(price_array[-period:]) / period
        rolling_std = (sum((x - rolling_mean) ** 2 for x in price_array[-period:]) / period) ** 0.5

        if rolling_std == 0:
            return

        deviation = fair_price - rolling_mean
        z_score = deviation / rolling_std

        if z_score < -z_score_threshold and deviation < -fixed_threshold and order_depth.sell_orders:
            best_ask = min(order_depth.sell_orders.keys())
            amount_to_buy = min(
                -order_depth.sell_orders[best_ask],
                limit - position - parent.total_buying_amount,
            )
            if amount_to_buy > 0 and best_ask > 0:
                parent.buy(best_ask, amount_to_buy)
                parent.total_buying_amount += amount_to_buy

        elif z_score > z_score_threshold and deviation > fixed_threshold and order_depth.buy_orders:
            best_bid = max(order_depth.buy_orders.keys())
            amount_to_sell = min(
                order_depth.buy_orders[best_bid],
                limit + position - parent.total_selling_amount,
            )
            if amount_to_sell > 0 and best_bid > 0:
                parent.sell(best_bid, amount_to_sell)
                parent.total_selling_amount += amount_to_sell

    def market_taking_strategy(
        self,
        state,  # TradingState
        parent,  # Strategy
        symbol: str,
        limit: int,
        fair_buying_price: float,
        fair_selling_price: float,
        max_size: int,
    ) -> Tuple[int, int]:
        position = state.position.get(symbol, 0)
        order_depth = parent.order_depth_internal
        sizes = [0, 0]

        # Market taking: selling orders
        max_buy_amount = max_size
        if order_depth.sell_orders:
            asks = sorted(order_depth.sell_orders.keys())
            for best_buying_price in asks:
                if best_buying_price <= fair_buying_price:
                    best_buying_amount = -order_depth.sell_orders[best_buying_price]
                    amount_to_buy = min(
                        best_buying_amount, limit - position - parent.total_buying_amount, max_buy_amount
                    )
                    if amount_to_buy > 0:
                        parent.buy(best_buying_price, amount_to_buy)
                        sizes[0] += amount_to_buy
                        max_buy_amount -= amount_to_buy

        # Market taking: buying orders
        max_sell_amount = max_size
        if order_depth.buy_orders:
            bids = sorted(order_depth.buy_orders.keys(), reverse=True)
            for best_selling_price in bids:
                if best_selling_price >= fair_selling_price:
                    best_selling_amount = order_depth.buy_orders[best_selling_price]
                    amount_to_sell = min(
                        best_selling_amount, limit + position - parent.total_selling_amount, max_sell_amount
                    )
                    if amount_to_sell > 0:
                        parent.sell(best_selling_price, amount_to_sell)
                        sizes[1] += amount_to_sell
                        max_sell_amount -= amount_to_sell

        return sizes[0], sizes[1]

    def market_making_strategy(
        self,
        state,  # TradingState
        parent,  # Strategy
        symbol: str,
        limit: int,
        zero_ev_bid: float,
        zero_ev_ask: float,
        pos_ev_bid: float,
        pos_ev_ask: float,
        max_bid_size: int,
        max_ask_size: int,
    ) -> None:
        position = state.position.get(symbol, 0)
        order_depth = parent.order_depth_internal

        # Market making: buy orders
        remaining_buy_capacity = min(limit - position - parent.total_buying_amount, max_bid_size)
        if remaining_buy_capacity > 0:
            max_buy_price = (
                max(
                    [price for price in order_depth.buy_orders.keys() if price < zero_ev_bid],
                    default=pos_ev_bid,
                )
                + 1
            )
            buy_price = min(max_buy_price, pos_ev_bid)
            parent.buy(buy_price, remaining_buy_capacity)

        # Market making: sell orders
        remaining_sell_capacity = min(limit + position - parent.total_selling_amount, max_ask_size)
        if remaining_sell_capacity > 0:
            min_sell_price = (
                min(
                    [price for price in order_depth.sell_orders.keys() if price > zero_ev_ask],
                    default=pos_ev_ask,
                )
                - 1
            )
            sell_price = max(min_sell_price, pos_ev_ask)
            parent.sell(sell_price, remaining_sell_capacity)

    def zero_ev_trades(
        self,
        state,  # TradingState
        parent,  # Strategy
        symbol: str,
        limit: int,
        fair_buying_price: float,
        fair_selling_price: float,
    ) -> None:
        position = state.position.get(symbol, 0)
        order_depth = parent.order_depth_internal

        # Zero EV sell trades
        if position > 0 and fair_selling_price in order_depth.buy_orders:
            amount_to_sell = min(
                position,
                order_depth.buy_orders[fair_selling_price],
                limit + position - parent.total_selling_amount,
            )
            if amount_to_sell > 0:
                parent.sell(fair_selling_price, amount_to_sell)

        # Zero EV buy trades
        elif position < 0 and fair_buying_price in order_depth.sell_orders:
            amount_to_buy = min(
                -position,
                -order_depth.sell_orders[fair_buying_price],
                limit - position - parent.total_buying_amount,
            )
            if amount_to_buy > 0:
                parent.buy(fair_buying_price, amount_to_buy)


class SignalSnoopers:

    def get_olivia_signal(self, product, state) -> int:
        buy_bots = [t.buyer for t in state.own_trades.get(product, []) + state.market_trades.get(product, [])]
        sell_bots = [t.seller for t in state.own_trades.get(product, []) + state.market_trades.get(product, [])]
        if "Olivia" in buy_bots:
            return 1
        if "Olivia" in sell_bots:
            return -1
        return 0


class Strategy(ABC):
    """Base class unchanged in logic; provides order handling and internal book simulation."""

    def __init__(self, symbol: str, limit: int) -> None:
        self.symbol = symbol
        self.limit = limit
        self.total_buying_amount = 0
        self.total_selling_amount = 0
        self.order_depth_internal = None
        self.orders = []
        self.conversions = 0

    @abstractmethod
    def act(self, state) -> None:
        raise NotImplementedError()

    def run(self, state) -> Tuple[List, int]:
        self.total_buying_amount = 0
        self.total_selling_amount = 0
        self.orders = []
        self.conversions = 0

        self.order_depth_internal = deepcopy(state.order_depths.get(self.symbol, []))

        self.act(state)

        return self.orders, self.conversions

    def popular_price_calculator(self, order_depth) -> float:
        buy_orders = order_depth.buy_orders
        sell_orders = order_depth.sell_orders

        if not buy_orders and not sell_orders:
            return 0
        elif not buy_orders:
            popular_buying_price = min(sell_orders.keys()) - 1
        else:
            popular_buying_price = max(buy_orders.keys())

        if not sell_orders:
            popular_selling_price = max(buy_orders.keys()) + 1
        else:
            popular_selling_price = min(sell_orders.keys())

        popular_price = (popular_buying_price + popular_selling_price) / 2

        return popular_price

    def buy(self, price: int, quantity: int) -> None:
        assert isinstance(price, int)
        assert isinstance(quantity, int)
        assert price > 0
        assert quantity > 0

        self.orders.append(Order(self.symbol, price, quantity))
        self.total_buying_amount += quantity

        remaining_quantity = quantity
        while (
            price >= min(self.order_depth_internal.sell_orders.keys(), default=float("inf")) and remaining_quantity > 0
        ):
            ask_price = min(self.order_depth_internal.sell_orders.keys())
            ask_size = -self.order_depth_internal.sell_orders[ask_price]
            if ask_size > remaining_quantity:
                self.order_depth_internal.sell_orders[ask_price] -= remaining_quantity
                remaining_quantity = 0
            else:
                self.order_depth_internal.sell_orders.pop(ask_price)
                remaining_quantity -= ask_size

    def sell(self, price: int, quantity: int) -> None:
        assert isinstance(price, int)
        assert isinstance(quantity, int)
        assert price > 0
        assert quantity > 0

        self.orders.append(Order(self.symbol, price, -quantity))
        self.total_selling_amount += quantity

        remaining_quantity = quantity
        while (
            price <= max(self.order_depth_internal.buy_orders.keys(), default=float("-inf")) and remaining_quantity > 0
        ):
            bid_price = max(self.order_depth_internal.buy_orders.keys())
            bid_size = self.order_depth_internal.buy_orders[bid_price]
            if bid_size > remaining_quantity:
                self.order_depth_internal.buy_orders[bid_price] -= remaining_quantity
                remaining_quantity = 0
            else:
                self.order_depth_internal.buy_orders.pop(bid_price)
                remaining_quantity -= bid_size

    def convert(self, amount: int) -> None:
        self.conversions += amount

    def save(self) -> JSON:
        return None

    def load(self, data: JSON) -> None:
        pass


class BlackScholes:

    def black_scholes_call(self, spot, strike, time_to_expiry, volatility):
        d1 = (log(spot) - log(strike) + (0.5 * volatility * volatility) * time_to_expiry) / (
            volatility * sqrt(time_to_expiry)
        )
        d2 = d1 - volatility * sqrt(time_to_expiry)
        call_price = spot * NormalDist().cdf(d1) - strike * NormalDist().cdf(d2)
        return call_price

    def delta(self, spot, strike, time_to_expiry, volatility):
        d1 = (log(spot) - log(strike) + (0.5 * volatility * volatility) * time_to_expiry) / (
            volatility * sqrt(time_to_expiry)
        )
        return NormalDist().cdf(d1)

    def implied_volatility(self, call_price, spot, strike, time_to_expiry, max_iterations=200, tolerance=1e-10):
        low_vol = 0.01
        high_vol = 1.0
        volatility = (low_vol + high_vol) / 2.0  # Initial guess as the midpoint
        for _ in range(max_iterations):
            estimated_price = BlackScholes.black_scholes_call(spot, strike, time_to_expiry, volatility)
            diff = estimated_price - call_price
            if abs(diff) < tolerance:
                break
            elif diff > 0:
                high_vol = volatility
            else:
                low_vol = volatility
            volatility = (low_vol + high_vol) / 2.0
        return volatility


class KelpStrategy(Strategy):
    def __init__(self, symbol: str, limit: int, deflection_threshold: float, utils: MarketUtils, blocks: InteractionBlocks):
        super().__init__(symbol, limit)
        self.symbol = symbol
        self.limit = limit
        self.deflection_threshold = deflection_threshold
        self.price_array = []
        self.price_array_max_length = 10
        self.fair_price = 0.0
        self.u = utils
        self.b = blocks

    def act(self, state) -> None:
        order_depth = state.order_depths.get(self.symbol, None)
        if not order_depth:
            return
        if len(order_depth.buy_orders) == 0 or len(order_depth.sell_orders) == 0:
            return

        self.fair_price = self.popular_price_calculator(order_depth)
        zero_ev_bid, zero_ev_ask = math.floor(self.fair_price), math.ceil(self.fair_price)
        pos_ev_bid = zero_ev_bid if zero_ev_bid < self.fair_price else zero_ev_bid - 1
        pos_ev_ask = zero_ev_ask if zero_ev_ask > self.fair_price else zero_ev_ask + 1

        # Deflection mechanism
        if len(self.price_array) > 0:
            change_in_fair = self.fair_price - self.price_array[-1]
            if change_in_fair > self.deflection_threshold:
                # Deduct 100 from pos_ev_bid so that the algo only sells
                pos_ev_bid -= 100
            elif change_in_fair < -self.deflection_threshold:
                # Add 100 to pos_ev_ask so that the algo only buys
                pos_ev_ask += 100

        self.b.zero_ev_trades(state, self, self.symbol, self.limit, zero_ev_bid, zero_ev_ask)
        self.b.market_taking_strategy(state, self, self.symbol, self.limit, pos_ev_bid, pos_ev_ask, self.limit)
        self.b.market_making_strategy(
            state,
            self,
            self.symbol,
            self.limit,
            zero_ev_bid,
            zero_ev_ask,
            pos_ev_bid,
            pos_ev_ask,
            self.limit,
            self.limit,
        )

    def save(self) -> JSON:
        self.price_array.append(self.fair_price)
        if len(self.price_array) > self.price_array_max_length:
            self.price_array.pop(0)
        return jsonpickle.encode(self.price_array)

    def load(self, data) -> None:
        self.price_array = jsonpickle.decode(data)


class SquidInkStrategy(Strategy):
    def __init__(self, symbol: str, limit: int, utils: MarketUtils, blocks: InteractionBlocks, snoop: SignalSnoopers):
        super().__init__(symbol, limit)
        self.symbol = symbol
        self.limit = limit

        self.price_array = []
        self.price_array_max_length = 100
        self.fair_price = 0.0
        self.u = utils
        self.b = blocks
        self.s = snoop

    def act(self, state) -> None:
        order_depth = state.order_depths.get(self.symbol, None)
        if not order_depth:
            return
        if len(order_depth.buy_orders) == 0 or len(order_depth.sell_orders) == 0:
            return

        self.fair_price = self.popular_price_calculator(order_depth)
        olivia_signal = self.s.get_olivia_signal(self.symbol, state)
        if olivia_signal == 1:
            self.b.market_taking_strategy(state, self, self.symbol, self.limit, 99999, 99999, self.limit)
            return
        elif olivia_signal == -1:
            self.b.market_taking_strategy(state, self, self.symbol, self.limit, 1, 1, self.limit)
            return

        self.b.mean_reversion_taker(state, self, self.symbol, self.limit, self.price_array, self.fair_price, 100, 0, 30)

    def save(self) -> JSON:
        self.price_array.append(self.fair_price)
        if len(self.price_array) > self.price_array_max_length:
            self.price_array.pop(0)
        return jsonpickle.encode(self.price_array)

    def load(self, data) -> None:
        self.price_array = jsonpickle.decode(data)


class CroissantStrategy(Strategy):
    def __init__(self, symbol: str, limit: int, snoop: SignalSnoopers, blocks: InteractionBlocks):
        super().__init__(symbol, limit)
        self.symbol = symbol
        self.limit = limit
        self.s = snoop
        self.b = blocks

    def act(self, state) -> None:
        order_depth = state.order_depths.get(self.symbol, None)
        if not order_depth:
            return
        if len(order_depth.buy_orders) == 0 or len(order_depth.sell_orders) == 0:
            return

        olivia_signal = self.s.get_olivia_signal(self.symbol, state)
        if olivia_signal == 1:
            self.b.market_taking_strategy(state, self, self.symbol, self.limit, 99999, 99999, self.limit)
            return
        elif olivia_signal == -1:
            self.b.market_taking_strategy(state, self, self.symbol, self.limit, 1, 1, self.limit)
            return


class RainforestResinStrategy(Strategy):
    def __init__(self, symbol: str, limit: int, blocks: InteractionBlocks):
        super().__init__(symbol, limit)
        self.symbol = symbol
        self.limit = limit
        self.market_taking = None
        self.zero_ev = None
        self.market_making = None
        self.b = blocks

    def act(self, state) -> None:
        order_depth = state.order_depths.get(self.symbol, None)
        if not order_depth:
            return

        zero_ev_bid, zero_ev_ask = 10000, 10000
        pos_ev_bid, pos_ev_ask = 9999, 10001
        self.b.market_taking_strategy(state, self, self.symbol, self.limit, pos_ev_bid, pos_ev_ask, self.limit)
        self.b.zero_ev_trades(state, self, self.symbol, self.limit, zero_ev_bid, zero_ev_ask)
        self.b.market_making_strategy(
            state,
            self,
            self.symbol,
            self.limit,
            zero_ev_bid,
            zero_ev_ask,
            pos_ev_bid,
            pos_ev_ask,
            self.limit,
            self.limit,
        )


class PicnicBasketStrategy(Strategy):
    def __init__(
        self,
        symbol: str,
        limit: int,
        position_threshold: int,
        aggressive_adj: int,
        aggressive_deflection_adj: int,
        normal_deflection_adj: int,
        default_size: int,
        utils: MarketUtils,
        blocks: InteractionBlocks,
    ) -> None:
        super().__init__(symbol, limit)
        self.symbol = symbol
        self.limit = limit
        self.position_threshold = position_threshold
        self.aggressive_adj = aggressive_adj
        self.aggressive_deflection_adj = aggressive_deflection_adj
        self.normal_deflection_adj = normal_deflection_adj
        self.default_size = default_size
        self.u = utils
        self.b = blocks

    def act(self, state) -> None:
        if any(
            symbol not in state.order_depths
            for symbol in ["CROISSANTS", "JAMS", "DJEMBES", "PICNIC_BASKET1", "PICNIC_BASKET2"]
        ):
            return
        if any(
            len(state.order_depths[symbol].buy_orders) == 0 or len(state.order_depths[symbol].sell_orders) == 0
            for symbol in ["CROISSANTS", "JAMS", "DJEMBES", "PICNIC_BASKET1", "PICNIC_BASKET2"]
        ):
            return

        position = state.position.get(self.symbol, 0)

        croissants_mid = self.get_mid(state.order_depths["CROISSANTS"], "impact_weighted_mid_price2")
        jams_mid = self.get_mid(state.order_depths["JAMS"], "weighted_mid_price")
        djembes_mid = self.get_mid(state.order_depths["DJEMBES"], "weighted_mid_price")
        picnic_basket1_mid = self.get_mid(state.order_depths["PICNIC_BASKET1"], "popular_simple_mid_price")
        picnic_basket2_mid = self.get_mid(state.order_depths["PICNIC_BASKET2"], "weighted_mid_price")

        spread_1 = picnic_basket1_mid - (croissants_mid * 6 + jams_mid * 3 + djembes_mid * 1)
        spread_2 = picnic_basket2_mid - (croissants_mid * 4 + jams_mid * 2)
        spread_3 = picnic_basket1_mid - (picnic_basket2_mid * 3 / 2 + djembes_mid)
        desired_position = self.get_desired_position(spread_1, spread_2, spread_3)
        amount_to_buy = max(0, desired_position - position)
        amount_to_sell = max(0, position - desired_position)

        self.fair_price = {"PICNIC_BASKET1": picnic_basket1_mid, "PICNIC_BASKET2": picnic_basket2_mid}[self.symbol]
        zero_ev_bid, zero_ev_ask = math.floor(self.fair_price), math.ceil(self.fair_price)

        if amount_to_buy > 0:
            if amount_to_buy > self.position_threshold:
                bid = zero_ev_bid + self.aggressive_adj
                ask = zero_ev_ask + self.aggressive_deflection_adj
                sent_sizes = self.b.market_taking_strategy(state, self, self.symbol, self.limit, bid, ask, amount_to_buy)
                self.b.market_making_strategy(
                    state,
                    self,
                    self.symbol,
                    self.limit,
                    bid,
                    ask,
                    bid,
                    ask,
                    max(0, amount_to_buy - sent_sizes[0]),
                    self.default_size,
                )
            else:
                bid = zero_ev_bid
                ask = zero_ev_ask + self.normal_deflection_adj
                sent_sizes = self.b.market_taking_strategy(state, self, self.symbol, self.limit, bid, ask, amount_to_buy)
                self.b.market_making_strategy(
                    state,
                    self,
                    self.symbol,
                    self.limit,
                    bid,
                    ask,
                    bid,
                    ask,
                    max(0, amount_to_buy - sent_sizes[0]),
                    self.default_size,
                )

        elif amount_to_sell > 0:
            if amount_to_sell > self.position_threshold:
                bid = zero_ev_bid - self.aggressive_deflection_adj
                ask = zero_ev_ask - self.aggressive_adj
                sent_sizes = self.b.market_taking_strategy(state, self, self.symbol, self.limit, bid, ask, amount_to_sell)
                self.b.market_making_strategy(
                    state,
                    self,
                    self.symbol,
                    self.limit,
                    bid,
                    ask,
                    bid,
                    ask,
                    self.default_size,
                    max(0, amount_to_sell - sent_sizes[1]),
                )
            else:
                bid = zero_ev_bid - self.normal_deflection_adj
                ask = zero_ev_ask
                sent_sizes = self.b.market_taking_strategy(state, self, self.symbol, self.limit, bid, ask, amount_to_sell)
                self.b.market_making_strategy(
                    state,
                    self,
                    self.symbol,
                    self.limit,
                    bid,
                    ask,
                    bid,
                    ask,
                    self.default_size,
                    max(0, amount_to_sell - sent_sizes[1]),
                )

        else:
            bid, ask = zero_ev_bid, zero_ev_ask
            sent_sizes = self.b.market_taking_strategy(state, self, self.symbol, self.limit, bid, ask, self.default_size)
            self.b.market_making_strategy(
                state,
                self,
                self.symbol,
                self.limit,
                bid,
                ask,
                bid,
                ask,
                self.default_size,
                self.default_size,
            )

        logger.print(self.symbol, spread_1, spread_2, desired_position, position, amount_to_buy, amount_to_sell)

    def get_mid(self, order_depth, method: str) -> float:
        bid_prices, ask_prices, bid_volumes, ask_volumes = [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]
        for i, (price, volume) in enumerate(sorted(order_depth.buy_orders.items(), reverse=True)[:3]):
            bid_prices[i] = price
            bid_volumes[i] = volume
        for i, (price, volume) in enumerate(sorted(order_depth.sell_orders.items(), reverse=False)[:3]):
            ask_prices[i] = price
            ask_volumes[i] = -volume

        if method == "impact_weighted_mid_price2":
            total_bid_volume = sum(bid_volumes)
            total_ask_volume = sum(ask_volumes)
            weighted_bid = sum(price * volume for price, volume in zip(bid_prices, bid_volumes)) / total_bid_volume
            weighted_ask = sum(price * volume for price, volume in zip(ask_prices, ask_volumes)) / total_ask_volume
            return (weighted_bid * total_ask_volume + weighted_ask * total_bid_volume) / (
                total_bid_volume + total_ask_volume
            )

        elif method == "weighted_mid_price":
            return (bid_prices[0] * ask_volumes[0] + ask_prices[0] * bid_volumes[0]) / (bid_volumes[0] + ask_volumes[0])

        elif method == "popular_simple_mid_price":
            popular_bid = bid_prices[bid_volumes.index(max(bid_volumes))]
            popular_ask = ask_prices[ask_volumes.index(max(ask_volumes))]
            return (popular_bid + popular_ask) / 2

        else:
            raise Exception()

    def get_desired_position(self, spread1, spread2, spread3):
        if self.symbol == "PICNIC_BASKET1":
            res = -(math.tanh(spread1 / 85) + math.tanh(spread3 / 95))
            res = max(min(res, 1), -1) * self.limit
            return round(res)

        elif self.symbol == "PICNIC_BASKET2":
            res = -(math.tanh(spread2 / 65))
            res = max(min(res, 1), -1) * self.limit
            return round(res)

        else:
            return 0


class OptionStrategy(Strategy):
    def __init__(
        self,
        symbol: str,
        limit: int,
        window: int,
        z_score_threshold: float,
        strike: int,
        utils: MarketUtils,
        blocks: InteractionBlocks,
    ) -> None:
        super().__init__(symbol, limit)
        self.symbol = symbol
        self.limit = limit
        self.window = window
        self.threshold = 0.01
        self.strike = strike
        self.z_score_threshold = z_score_threshold
        self.price_array = []
        self.underlying_current_orders = 0

        self.options_model = BlackScholes()

        self.implied_vols = []
        self.deltas = []

        self.underlying_price_history = []
        self.timestamps_per_year = 365e6
        self.days_left = 3

        # Volatility parameters (coefficients for IV curve fitting)
        self.ask_params = {"a": 0.2878490683651303, "b": -0.0009201058370376721, "c": 0.1499510693474374}
        self.bid_params = {"a": 0.1850111314490967, "b": 0.0008529599232086579, "c": 0.14879176125529844}

        self.u = utils
        self.b = blocks

    def act(self, state) -> None:
        self.underlying_current_orders = 0
        order_depth = state.order_depths.get(self.symbol, None)
        if not order_depth:
            return

        # Update underlying price and calculate implied volatility
        underlying_symbol = "VOLCANIC_ROCK"
        underlying_order_depth = state.order_depths.get(underlying_symbol, None)
        if not underlying_order_depth or not underlying_order_depth.sell_orders or not underlying_order_depth.buy_orders:
            return
        underlying_bid = min(underlying_order_depth.buy_orders.keys())
        underlying_ask = max(underlying_order_depth.sell_orders.keys())
        underlying_price = (underlying_ask + underlying_bid) / 2
        self.underlying_price_history.append(underlying_price)
        self.underlying_price_history = self.underlying_price_history[-5:]
        underlying_price = self.underlying_price_history[-1]
        tte = (self.days_left / 365) - state.timestamp / self.timestamps_per_year
        moneyness = np.log(self.strike / underlying_price) / np.sqrt(tte)

        theoretical_ask_price = None
        theoretical_bid_price = None

        # Checking ask level
        if order_depth.sell_orders:
            best_ask = min(order_depth.sell_orders.keys())
            theoretical_iv_ask = self.ask_params["c"] + self.ask_params["b"] * moneyness + self.ask_params["a"] * moneyness**2
            theoretical_ask_price = self.options_model.black_scholes_call(underlying_price, self.strike, tte, theoretical_iv_ask)

        # Checking bid level
        if order_depth.buy_orders:
            best_bid = max(order_depth.buy_orders.keys())
            theoretical_iv_bid = self.bid_params["c"] + self.bid_params["b"] * moneyness + self.bid_params["a"] * moneyness**2
            theoretical_bid_price = self.options_model.black_scholes_call(underlying_price, self.strike, tte, theoretical_iv_bid)

        # Update price array
        if not order_depth.sell_orders:
            mid_price = best_bid + 1
            theoretical_mid_price = theoretical_bid_price + 1
            theoretical_iv_mid = theoretical_iv_bid
        elif not order_depth.buy_orders:
            mid_price = best_ask - 1
            theoretical_mid_price = theoretical_ask_price - 1
            theoretical_iv_mid = theoretical_iv_ask
        else:
            mid_price = (best_ask + best_bid) / 2
            theoretical_mid_price = (theoretical_ask_price + theoretical_bid_price) / 2
            theoretical_iv_mid = (theoretical_iv_ask + theoretical_iv_bid) / 2
        self.price_array.append(mid_price)
        if len(self.price_array) < self.window:
            return

        self.price_array = self.price_array[-self.window:]
        self.b.mean_reversion_taker(
            state, self, self.symbol, self.limit, self.price_array, theoretical_mid_price, self.window, self.z_score_threshold, 1
        )

        current_position = state.position.get(self.symbol, 0) + self.total_buying_amount - self.total_selling_amount
        delta = self.options_model.delta(underlying_price, self.strike, tte, theoretical_iv_mid)
        total_delta = int(current_position * delta)
        position_to_fill = total_delta - state.position.get(underlying_symbol, 0) - self.underlying_current_orders

        if position_to_fill > 0:
            size = min(position_to_fill, self.limit)
            self.buy_underlying(underlying_ask, size, underlying_order_depth)
        elif position_to_fill < 0:
            size = min(-position_to_fill, self.limit)
            self.sell_underlying(underlying_bid, size, underlying_order_depth)

    def buy_underlying(self, price: int, quantity: int, underlying_order_depth) -> None:
        assert isinstance(price, int)
        assert isinstance(quantity, int)
        assert price > 0
        assert quantity > 0

        self.orders.append(Order("VOLCANIC_ROCK", price, quantity))
        self.underlying_current_orders += quantity

        remaining_quantity = quantity

        while (
            price >= min(underlying_order_depth.sell_orders.keys(), default=float("inf")) and remaining_quantity > 0
        ):
            ask_price = min(underlying_order_depth.sell_orders.keys())
            ask_size = -underlying_order_depth.sell_orders[ask_price]
            if ask_size > remaining_quantity:
                underlying_order_depth.sell_orders[ask_price] -= remaining_quantity
                remaining_quantity = 0
            else:
                underlying_order_depth.sell_orders.pop(ask_price)
                remaining_quantity -= ask_size

    def sell_underlying(self, price: int, quantity: int, underlying_order_depth) -> None:
        assert isinstance(price, int)
        assert isinstance(quantity, int)
        assert price > 0
        assert quantity > 0

        self.orders.append(Order("VOLCANIC_ROCK", price, -quantity))
        self.underlying_current_orders -= quantity

        remaining_quantity = quantity
        while (
            price <= max(underlying_order_depth.buy_orders.keys(), default=float("-inf")) and remaining_quantity > 0
        ):
            bid_price = max(underlying_order_depth.buy_orders.keys())
            bid_size = underlying_order_depth.buy_orders[bid_price]
            if bid_size > remaining_quantity:
                underlying_order_depth.buy_orders[bid_price] -= remaining_quantity
                remaining_quantity = 0
            else:
                underlying_order_depth.buy_orders.pop(bid_price)
                remaining_quantity -= bid_size


class MacaronsStrategy(Strategy):
    def __init__(self, symbol: str, limit: int, conversion_limit: int, sunlight_threshold: float, z_score_threshold: float) -> None:
        super().__init__(symbol, limit)
        self.symbol = symbol
        self.limit = limit
        self.sunlight_threshold = sunlight_threshold
        self.conversion_limit = conversion_limit
        self.previous_sunlight = None
        self.previous_sugar = None
        self.price_array = []
        self.fair_price = 0
        self.current_trend_sunlight = None
        self.current_trend_sugar = None

    def act(self, state) -> None:
        position = state.position.get(self.symbol, 0)

        # Get observations
        obs = state.observations.conversionObservations.get(self.symbol, None)
        if obs is None:
            return
        order_depth = state.order_depths.get(self.symbol, None)
        if order_depth is None:
            return

        # Extract sugar price and sunlight index
        sugar_price = obs.sugarPrice
        sunlight = obs.sunlightIndex

        # Initialize previous values if not set
        if self.previous_sugar is None:
            self.previous_sugar = sugar_price
        if self.previous_sunlight is None:
            self.previous_sunlight = sunlight

        # Update rolling price array and calculate Z-score
        self.price_array.append(sugar_price)
        if len(self.price_array) > 100:  # Keep a rolling window of 100 prices
            self.price_array.pop(0)

        # Calculate fair price
        self.fair_price = self.popular_price_calculator(order_depth)

        # Determine buy/sell amounts based on position limits
        buy_amount = min(self.limit - position, self.conversion_limit)
        sell_amount = min(self.limit + position, self.conversion_limit)

        # Local and foreign price calculations
        foreign_ask = obs.askPrice + obs.transportFees - obs.importTariff
        foreign_bid = obs.bidPrice - obs.transportFees - obs.exportTariff
        local_ask = min(order_depth.sell_orders.keys())
        local_bid = max(order_depth.buy_orders.keys())
        local_ask_volume = abs(order_depth.sell_orders.get(local_ask, 0))
        local_bid_volume = abs(order_depth.buy_orders.get(local_bid, 0))

        # Detect sunlight trend
        sunlight_change = sunlight - self.previous_sunlight
        if sunlight_change > 0:
            self.current_trend_sunlight = 'uptrend'
        elif sunlight_change < 0:
            self.current_trend_sunlight = 'downtrend'
        # If sunlight_change == 0, maintain the current trend

        # Detect sugar price trend
        sugar_change = sugar_price - self.previous_sugar
        if sugar_change > 0:
            self.current_trend_sugar = 'uptrend'
        elif sugar_change < 0:
            self.current_trend_sugar = 'downtrend'
        # If sugar_change == 0, maintain the current trend

        if state.timestamp > 999000:  # Start unwinding positions aggressively near the end of the day
            # Gradually reduce position to zero
            if position > 0:  # If long position, sell to reduce it
                if local_bid > foreign_bid:
                    self.sell(local_bid, sell_amount)
                else:
                    convert_amount = min(abs(position), sell_amount, self.conversion_limit)
                    self.convert(-convert_amount)
                    remaining_amount = sell_amount - convert_amount
                    if remaining_amount > 0:
                        self.sell(local_bid, min(remaining_amount, local_bid_volume))
            elif position < 0:  # If short position, buy to reduce it
                if local_ask < foreign_ask:
                    self.buy(local_ask, buy_amount)
                else:
                    convert_amount = min(abs(position), buy_amount, self.conversion_limit)
                    self.convert(convert_amount)
                    remaining_amount = buy_amount - convert_amount
                    if remaining_amount > 0:
                        self.buy(local_ask, min(remaining_amount, local_ask_volume))
            return

        # Act based on trends when sunlight is below the threshold
        elif sunlight <= self.sunlight_threshold:
            if self.current_trend_sunlight == 'uptrend' and sell_amount > 0 and self.current_trend_sugar == 'downtrend':
                # Uptrend in sunlight and downtrend in sugar price: Sell
                if position > 0:
                    if local_bid > foreign_bid:
                        self.sell(local_bid, sell_amount)
                    else:
                        convert_amount = min(abs(position), sell_amount, self.conversion_limit)
                        self.convert(-convert_amount)
                        remaining_amount = sell_amount - convert_amount
                        if remaining_amount > 0:
                            self.sell(local_bid, min(remaining_amount, local_bid_volume))
                else:
                    self.sell(local_bid, sell_amount)

            elif self.current_trend_sunlight == 'downtrend' and buy_amount > 0 and self.current_trend_sugar == 'uptrend':
                # Downtrend in sunlight and uptrend in sugar price: Buy
                if position < 0:
                    if local_ask < foreign_ask:
                        self.buy(local_ask, buy_amount)
                    else:
                        convert_amount = min(abs(position), buy_amount, self.conversion_limit)
                        self.convert(convert_amount)
                        remaining_amount = buy_amount - convert_amount
                        if remaining_amount > 0:
                            self.buy(local_ask, min(remaining_amount, local_ask_volume))
                else:
                    self.buy(local_ask, buy_amount)

        # Update previous values
        self.previous_sunlight = sunlight
        self.previous_sugar = sugar_price


class Trader:

    def __init__(self):
        self.utils = MarketUtils()
        self.blocks = InteractionBlocks(self.utils)
        self.snoop = SignalSnoopers()

        self.limit = {
            "RAINFOREST_RESIN": 50,
            "KELP": 50,
            "SQUID_INK": 50,
            "CROISSANTS": 250,
            "JAMS": 350,
            "DJEMBES": 60,
            "PICNIC_BASKET1": 60,
            "PICNIC_BASKET2": 100,
            "VOLCANIC_ROCK": 400,
            "VOLCANIC_ROCK_VOUCHER_9500": 200,
            "VOLCANIC_ROCK_VOUCHER_9750": 200,
            "VOLCANIC_ROCK_VOUCHER_10000": 200,
            "VOLCANIC_ROCK_VOUCHER_10250": 200,
            "VOLCANIC_ROCK_VOUCHER_10500": 200,
            "MAGNIFICENT_MACARONS": 75,
        }

        self.strategies = {
            "RAINFOREST_RESIN": RainforestResinStrategy(
                symbol="RAINFOREST_RESIN", limit=self.limit["RAINFOREST_RESIN"], blocks=self.blocks
            ),
            "KELP": KelpStrategy(symbol="KELP", limit=self.limit["KELP"], deflection_threshold=0.5, utils=self.utils, blocks=self.blocks),
            "SQUID_INK": SquidInkStrategy(
                symbol="SQUID_INK",
                limit=self.limit["SQUID_INK"],
                utils=self.utils,
                blocks=self.blocks,
                snoop=self.snoop,
            ),
            "CROISSANTS": CroissantStrategy(
                symbol="CROISSANTS",
                limit=self.limit["CROISSANTS"],
                snoop=self.snoop,
                blocks=self.blocks,
            ),
            "PICNIC_BASKET1": PicnicBasketStrategy(
                symbol="PICNIC_BASKET1",
                limit=self.limit["PICNIC_BASKET1"],
                position_threshold=60,
                aggressive_adj=3,
                aggressive_deflection_adj=100,
                normal_deflection_adj=100,
                default_size=3,
                utils=self.utils,
                blocks=self.blocks,
            ),
            "PICNIC_BASKET2": PicnicBasketStrategy(
                symbol="PICNIC_BASKET2",
                limit=self.limit["PICNIC_BASKET2"],
                position_threshold=100,
                aggressive_adj=2,
                aggressive_deflection_adj=100,
                normal_deflection_adj=100,
                default_size=5,
                utils=self.utils,
                blocks=self.blocks,
            ),
            "VOLCANIC_ROCK_VOUCHER_9500": OptionStrategy(
                symbol="VOLCANIC_ROCK_VOUCHER_9500",
                limit=self.limit["VOLCANIC_ROCK_VOUCHER_9500"],
                window=100,
                z_score_threshold=2,
                strike=9500,
                utils=self.utils,
                blocks=self.blocks,
            ),
            "VOLCANIC_ROCK_VOUCHER_9750": OptionStrategy(
                symbol="VOLCANIC_ROCK_VOUCHER_9750",
                limit=self.limit["VOLCANIC_ROCK_VOUCHER_9750"],
                window=100,
                z_score_threshold=2,
                strike=9750,
                utils=self.utils,
                blocks=self.blocks,
            ),
            "VOLCANIC_ROCK_VOUCHER_10000": OptionStrategy(
                symbol="VOLCANIC_ROCK_VOUCHER_10000",
                limit=self.limit["VOLCANIC_ROCK_VOUCHER_10000"],
                window=100,
                z_score_threshold=2,
                strike=10000,
                utils=self.utils,
                blocks=self.blocks,
            ),
            "VOLCANIC_ROCK_VOUCHER_10250": OptionStrategy(
                symbol="VOLCANIC_ROCK_VOUCHER_10250",
                limit=self.limit["VOLCANIC_ROCK_VOUCHER_10250"],
                window=100,
                z_score_threshold=2,
                strike=10250,
                utils=self.utils,
                blocks=self.blocks,
            ),
            "VOLCANIC_ROCK_VOUCHER_10500": OptionStrategy(
                symbol="VOLCANIC_ROCK_VOUCHER_10500",
                limit=self.limit["VOLCANIC_ROCK_VOUCHER_10500"],
                window=100,
                z_score_threshold=2,
                strike=10500,
                utils=self.utils,
                blocks=self.blocks,
            ),
            "MAGNIFICENT_MACARONS": MacaronsStrategy("MAGNIFICENT_MACARONS", self.limit["MAGNIFICENT_MACARONS"], conversion_limit=10, sunlight_threshold=50, z_score_threshold=3),
        }

    def run(self, state) -> Tuple[Dict[str, List], int, str]:
        logger.print(state.position)

        conversions = 0

        old_trader_data = jsonpickle.decode(state.traderData) if state.traderData != "" else {}
        new_trader_data = {}

        orders = {}
        for symbol, strategy in self.strategies.items():
            if symbol in old_trader_data:
                strategy.load(old_trader_data.get(symbol, None))

            if symbol in state.order_depths:
                strategy_orders, strategy_conversions = strategy.run(state)
                orders[symbol] = strategy_orders
                conversions += strategy_conversions
            else:
                orders[symbol] = []

            new_trader_data[symbol] = strategy.save()

        trader_data = jsonpickle.encode(new_trader_data)

        logger.flush(state, orders, conversions, trader_data)

        return orders, conversions, trader_data

class Trader:
    def __init__(self):
        self.volume = 35
        self.spread = 5
        self.position_limit = 50
        self.current_position = 0

        self.bid_price = 9998
        self.ask_price = 10002

    def run(self, state):
        from datamodel import Order

        product = "RAINFOREST_RESIN"
        orders = []

        order_depth = state.order_depths[product]
        self.current_position = state.position.get(product, 0)
        
        if self.current_position < self.position_limit:
            bid_volume = min(self.volume, self.position_limit - self.current_position)
            orders.append(Order(product, self.bid_price, bid_volume))

        if self.current_position > -self.position_limit:
            ask_volume = min(self.volume, self.position_limit + self.current_position)
            orders.append(Order(product, self.ask_price, -ask_volume))

        result = {product: orders}
        conversions = 0
        traderData = ""
        logger.flush(state, result, conversions, traderData)
        return result, conversions, traderData
lass Trader:
    def __init__(self):
        self.product = "SQUID_INK"
        self.position_limit = 50
        self.volume = 2
        self.history = []

        self.window = 30
        self.std_threshold = 1.4
        self.momentum_threshold = 0.5
        self.weak_momentum_threshold = 0.2
        self.slope_threshold = 0.01

        self.entry_price = None
        self.entry_timestamp = None
        self.max_hold_time = 50_000

    def ema(self, prices, span):
        alpha = 2 / (span + 1)
        ema_vals = [prices[0]]
        for price in prices[1:]:
            ema_vals.append(alpha * price + (1 - alpha) * ema_vals[-1])
        return ema_vals[-1]

    def run(self, state: TradingState):
        orders = []
        product = self.product

        if product not in state.order_depths:
            return {}, 0, ""

        order_depth = state.order_depths[product]
        if not order_depth.buy_orders or not order_depth.sell_orders:
            return {}, 0, ""

        best_bid = max(order_depth.buy_orders.keys())
        best_ask = min(order_depth.sell_orders.keys())
        mid_price = (best_bid + best_ask) / 2

        self.history.append(mid_price)
        if len(self.history) <= self.window:
            return {}, 0, ""

        recent = self.history[-self.window:]
        rolling_std = np.std(recent)

        ema_short = self.ema(recent, span=5)
        ema_long = self.ema(recent, span=15)
        momentum = ema_short - ema_long

        x = np.arange(len(recent))
        slope = np.polyfit(x, recent, 1)[0]
        trend_ok = abs(slope) > self.slope_threshold

        pos = state.position.get(product, 0)


        # mysterious shit block
        if pos != 0 and self.entry_timestamp is None:
            self.entry_timestamp = state.timestamp
            self.entry_price = mid_price
        if pos == 0:
            self.entry_price = None
            self.entry_timestamp = None
        if pos != 0 and self.entry_timestamp is not None:
            held_time = state.timestamp - self.entry_timestamp
            if held_time > self.max_hold_time:
                orders.append(Order(product, best_bid if pos > 0 else best_ask, -pos))
        elif trend_ok and momentum < -self.momentum_threshold and pos > 0:
            bid_volume = order_depth.buy_orders.get(best_bid, 0)
            volume = min(self.volume, bid_volume, pos)
            if volume > 0:
                orders.append(Order(product, best_bid, -volume))
        elif trend_ok and momentum > self.momentum_threshold and pos < 0:
            ask_volume = order_depth.sell_orders.get(best_ask, 0)
            volume = min(self.volume, ask_volume, -pos)
            if volume > 0:
                orders.append(Order(product, best_ask, volume))
        elif abs(momentum) < self.weak_momentum_threshold and rolling_std < self.std_threshold / 2:
            if pos > 0:
                bid_volume = order_depth.buy_orders.get(best_bid, 0)
                volume = min(self.volume, bid_volume, pos)
                if volume > 0:
                    orders.append(Order(product, best_bid, -volume))
            elif pos < 0:
                ask_volume = order_depth.sell_orders.get(best_ask, 0)
                volume = min(self.volume, ask_volume, -pos)
                if volume > 0:
                    orders.append(Order(product, best_ask, volume))
                    
        # ema momentum trading
        if trend_ok and rolling_std > self.std_threshold:
            if momentum > self.momentum_threshold and pos < self.position_limit:
                ask_volume = order_depth.sell_orders.get(best_ask, 0)
                volume = min(self.volume, ask_volume, self.position_limit - pos)
                if volume > 0:
                    orders.append(Order(product, best_ask, volume))

            elif momentum < -self.momentum_threshold and pos > -self.position_limit:
                bid_volume = order_depth.buy_orders.get(best_bid, 0)
                volume = min(self.volume, bid_volume, pos + self.position_limit)
                if volume > 0:
                    orders.append(Order(product, best_bid, -volume))

        result = {product: orders}
        conversions = 0
        traderData = ""
        logger.flush(state, result, conversions, traderData)
        return result, conversions, traderData



      class Trader:
    def __init__(self):
        self.product = "SQUID_INK"
        self.position_limit = 50
        self.volume = 2
        self.history = []

        self.window = 30
        self.std_threshold = 1.0
        self.momentum_threshold = 0.8

    def run(self, state: TradingState):
        orders = []
        product = self.product

        if product not in state.order_depths:
            return {}, 0, ""

        order_depth = state.order_depths[product]
        if not order_depth.buy_orders or not order_depth.sell_orders:
            return {}, 0, ""

        best_bid = max(order_depth.buy_orders.keys())
        best_ask = min(order_depth.sell_orders.keys())
        mid_price = (best_bid + best_ask) / 2

        self.history.append(mid_price)
        if len(self.history) <= self.window:
            return {}, 0, ""

        recent = self.history[-self.window:]
        rolling_std = np.std(recent)
        
        momentum = self.history[-1] - self.history[-self.window]

        pos = state.position.get(product, 0)

        if rolling_std > self.std_threshold:
            if momentum > self.momentum_threshold and pos < self.position_limit:
                ask_volume = order_depth.sell_orders[best_ask]
                volume = min(self.volume, ask_volume, self.position_limit - pos)
                if volume > 0:
                    orders.append(Order(product, best_ask, volume))

            elif momentum < -self.momentum_threshold and pos > -self.position_limit:
                bid_volume = order_depth.buy_orders[best_bid]
                volume = min(self.volume, bid_volume, pos + self.position_limit)
                if volume > 0:
                    orders.append(Order(product, best_bid, -volume))
        else:
            pass

        result = {product: orders}
        conversions = 0
        traderData = ""
        logger.flush(state, result, conversions, traderData)
        return result, conversions, traderData
class Trader:
    def __init__(self):
        self.current_position = 0
        self.price_history = []
        self.return_history = []
        self.remaining_time = 0
        self.position_wanted = 0
        self.spread_history = []

        # parameters
        self.position_limit = 50
        self.time_frame = 200
        self.z_score_threshold = 0.5
        self.time_threshold = 100
        self.alpha = 0.1
        self.beta = 1 - self.alpha
        self.position_offset = 0
        self.momentum_threshold = 1

    def encode_trader_data(self):
        data_dict = {
            'price_history': self.price_history,
            'return_history': self.return_history,
            'remaining_time': self.remaining_time,
            'position_wanted': self.position_wanted
        }
        return jsonpickle.encode(data_dict)

    def decode_trader_data(self, data):
        if not data:
            return
        data_dict = jsonpickle.decode(data)
        self.price_history = data_dict['price_history']
        self.return_history = data_dict['return_history']
        self.remaining_time = data_dict['remaining_time']
        self.position_wanted = data_dict['position_wanted']

    def run(self, state: TradingState):
        #self.decode_trader_data(state.traderData)
        result = {}
        product = "KELP"
        orders: List[Order] = []

        order_depth = state.order_depths[product]

        if product in state.position:
            self.current_position = state.position[product]

        if order_depth.buy_orders and order_depth.sell_orders:
            best_bid = max(order_depth.buy_orders.keys())
            best_ask = min(order_depth.sell_orders.keys())
            t_price = (best_bid + best_ask) / 2
            spread = abs(best_ask - best_bid)
        else:
            return {}, 0, ""  # Exit early if no data to trade on

        if self.price_history:
            t_return = (t_price - self.price_history[-1]) * 1000 / self.price_history[-1]
            self.return_history.append(t_return)
        else:
            t_return = 0
            self.return_history.append(0)

        if len(self.return_history) >= 50:
            mean_return = statistics.mean(self.return_history[-self.time_frame:])
            std_return = statistics.stdev(self.return_history[-self.time_frame:])
            z_score = (t_return - mean_return) / std_return if std_return != 0 else 0
        else:
            mean_return = 0
            std_return = 1
            z_score = 0
        if (len(self.price_history) >= 2):
            t_price_change = t_price - self.price_history[-1]
            t_mean_price = statistics.mean(self.price_history[-self.time_frame:])
            momentum = self.alpha * (t_price - t_mean_price) + self.beta * t_price_change
            if(abs(momentum) >= 0.5):
                self.position_offset = int(20 * min(1, momentum / self.momentum_threshold))
            else:
                self.position_offset = 0

        if self.spread_history:
            t_mean_spread = statistics.mean(self.spread_history[-self.time_frame:])
        else:
            t_mean_spread = spread

        logger.print(f"Return: {t_return:.4f}, Z-Score: {z_score:.2f}, Mean Return: {mean_return:.4f}, Std Return: {std_return:.4f}")

        self.remaining_time -= 1

        # if self.current_position > 0 and (z_score >= 0.5):
        #     self.position_wanted = 0
        # elif self.current_position < 0 and (z_score <= -0.5 ):
        #     self.position_wanted = 0
        z_scaled = min(1, abs(z_score) / 5)  # normalize z-score
        position = int(self.position_limit * z_scaled)
        self.position_wanted = position if z_score < 0 else -position
        self.remaining_time = self.time_threshold

        position_diff = self.position_wanted - self.current_position

        if position_diff > 0:
            if self.position_wanted == 0:
                orders.append(Order(product, round(best_ask - t_mean_spread), position_diff))
            else:
                orders.append(Order(product, best_bid + 1, position_diff))
        elif position_diff < 0:
            if self.position_wanted == 0:
                orders.append(Order(product, round(best_bid + t_mean_spread), position_diff))
            else:
                orders.append(Order(product, best_ask - 1, position_diff))

        #self.current_position = self.position_wanted
        self.price_history.append(t_price)
        self.spread_history.append(spread)
        #trader_data = self.encode_trader_data()
        result[product] = orders
        conversions = 0
        trader_data = ""
        logger.flush(state, result, conversions, trader_data)
        return result, conversions, trader_data

class Trader:
    # definite init state
    def __init__(self):

        self.limits = {
            'RAINFOREST_RESIN' : 50,
            'SQUID_INK' : 50,
            'KELP' : 50,
        }

        self.orders = {}
        self.conversions = 0
        self.traderData = "SAMPLE"

        # Resin
        self.resin_buy_orders = 0
        self.resin_sell_orders = 0
        self.resin_position = 0

        # Kelp
        self.kelp_position = 0
        self.kelp_buy_orders = 0
        self.kelp_sell_orders = 0

        # squid
        self.squid_ink_position = 0
        self.squid_ink_buy_orders = 0
        self.squid_ink_sell_orders = 0
        self.squid_ink_prices = []
        self.squid_ink_ema_short = None
        self.squid_ink_ema_long = None
        self.squid_ink_short_window = 600
        self.squid_ink_long_window = 1400 


    # define easier sell and buy order functions
    def send_sell_order(self, product, price, amount, msg=None):
        self.orders[product].append(Order(product, price, amount))

        if msg is not None:
            logger.print(msg)

    def send_buy_order(self, product, price, amount, msg=None):
        self.orders[product].append(Order(product, int(price), amount))

        if msg is not None:
            logger.print(msg)

    def printStuff(self, state):
        logger.print("traderData: " + state.traderData)
        logger.print("Observations: " + str(state.observations))        

    # TODO: UPDATE WHENEVER YOU ADD A NEW PRODUCT
    def get_product_pos(self, state, product):
        if product == 'RAINFOREST_RESIN':
            pos = state.position.get('RAINFOREST_RESIN', 0)
        elif product == 'KELP':
            pos = state.position.get('KELP', 0)
        elif product == 'SQUID_INK':
            pos = state.position.get('SQUID_INK', 0)
        else:
            raise ValueError(f"Unknown product: {product}")

        return pos
                
    def search_buys(self, state, product, acceptable_price, depth=1):
        # Buys things if there are asks below or equal acceptable price
        order_depth = state.order_depths[product]
        if len(order_depth.sell_orders) != 0:
            orders = list(order_depth.sell_orders.items())
            for ask, amount in orders[0:max(len(orders), depth)]: 

                pos = self.get_product_pos(state, product)                    
                if int(ask) < acceptable_price or (abs(ask - acceptable_price) < 1 and (pos < 0 and abs(pos - amount) < abs(pos))):
                    if product == 'RAINFOREST_RESIN':
                        size = min(50-self.resin_position-self.resin_buy_orders, -amount)

                        self.resin_buy_orders += size 
                        self.send_buy_order(product, ask, size, msg=f"TRADE BUY {str(size)} x @ {ask}")

                    elif product == 'KELP':
                        size = min(50-self.kelp_position-self.kelp_buy_orders, -amount)
                        self.kelp_buy_orders += size 
                        self.send_buy_order(product, ask, size, msg=f"TRADE BUY {str(size)} x @ {ask}")
                    
                    elif product == 'SQUID_INK':
                        size = min(50-self.squid_ink_position-self.squid_ink_buy_orders, -amount)
                        self.squid_ink_buy_orders += size 
                        self.send_buy_order(product, ask, size, msg=f"TRADE BUY {str(size)} x @ {ask}")
                    
    def search_sells(self, state, product, acceptable_price, depth=1):   
        order_depth = state.order_depths[product]
        if len(order_depth.buy_orders) != 0:
            orders = list(order_depth.buy_orders.items())
            for bid, amount in orders[0:max(len(orders), depth)]: 
                
                pos = self.get_product_pos(state, product)   
                if int(bid) > acceptable_price or (abs(bid-acceptable_price) < 1 and (pos > 0 and abs(pos - amount) < abs(pos))):
                    if product == 'RAINFOREST_RESIN':
                        size = min(self.resin_position + 50 - self.resin_sell_orders, amount)
                        self.resin_sell_orders += size
                        self.send_sell_order(product, bid, -size, msg=f"TRADE SELL {str(-size)} x @ {bid}")

                    elif product == 'KELP':
                        size = min(self.kelp_position + 50 - self.kelp_sell_orders, amount)
                        self.kelp_sell_orders += size
                        self.send_sell_order(product, bid, -size, msg=f"TRADE SELL {str(-size)} x @ {bid}")
                    
                    elif product == 'SQUID_INK':
                        size = min(self.squid_ink_position + 50 - self.squid_ink_sell_orders, amount)
                        self.squid_ink_sell_orders += size
                        self.send_sell_order(product, bid, -size, msg=f"TRADE SELL {str(-size)} x @ {bid}")

    def get_bid(self, state, product, price):        
        order_depth = state.order_depths[product]
        if len(order_depth.buy_orders) != 0:
            orders = list(order_depth.buy_orders.items())
            for bid, _ in orders: 
                if bid < price: # DONT COPY SHIT MARKETS
                    return bid
        
        return None

    def get_ask(self, state, product, price):      
        order_depth = state.order_depths[product]
        if len(order_depth.sell_orders) != 0:
            orders = list(order_depth.sell_orders.items())
            for ask, _ in orders: 
                if ask > price: # DONT COPY A SHITY MARKET
                    return ask
        
        return None

    def get_second_bid(self, state, product):
        order_depth = state.order_depths[product]
        if len(order_depth.buy_orders) != 0:
            orders = list(order_depth.buy_orders.items())
            if len(orders) < 2:
                return None
            else:
                bid, _ = orders[1]
                return bid
            
        return None
    
    def get_second_ask(self, state, product):
        order_depth = state.order_depths[product]
        if len(order_depth.sell_orders) != 0:
            orders = list(order_depth.sell_orders.items())
            if len(orders) < 2:
                return None
            else:
                ask, _ = orders[1]
                return ask
            
        return None        

    def trade_resin(self, state):
        # Buy anything at a good price
        self.search_buys(state, 'RAINFOREST_RESIN', 10000, depth=3)
        self.search_sells(state, 'RAINFOREST_RESIN', 10000, depth=3)

        # Check if there's another market maker
        best_ask = self.get_ask(state, 'RAINFOREST_RESIN', 10000)
        best_bid =  self.get_bid(state, 'RAINFOREST_RESIN', 10000)

        # our ordinary market
        buy_price = 9996
        sell_price = 10004  

        # update market if someone else is better than us
        if best_ask is not None and best_bid is not None:
            ask = best_ask
            bid = best_bid
            
            sell_price = ask - 1
            buy_price = bid + 1
    
        max_buy =  50 - self.resin_position - self.resin_buy_orders 
        max_sell = self.resin_position + 50 - self.resin_sell_orders

        self.send_sell_order('RAINFOREST_RESIN', sell_price, -max_sell, msg=f"RAINFOREST_RESIN: MARKET MADE Sell {max_sell} @ {sell_price}")
        self.send_buy_order('RAINFOREST_RESIN', buy_price, max_buy, msg=f"RAINFOREST_RESIN: MARKET MADE Buy {max_buy} @ {buy_price}")

    def trade_kelp(self, state):
        # position limits
        low = -50
        high = 50

        position = state.position.get("KELP", 0)

        max_buy = high - position
        max_sell = position - low

        order_book = state.order_depths['KELP']
        sell_orders = order_book.sell_orders
        buy_orders = order_book.buy_orders

        if len(sell_orders) != 0 and len(buy_orders) != 0:
            ask, _ = list(sell_orders.items())[-1] # worst ask
            bid, _ = list(buy_orders.items())[-1]  # worst bid
            
            fair_price = int(math.ceil((ask + bid) / 2))  # try changing this to floor maybe

            decimal_fair_price = (ask + bid) / 2

            logger.print(f"KELP FAIR PRICE: {decimal_fair_price}")
            self.search_buys(state, 'KELP', decimal_fair_price, depth=3)
            self.search_sells(state, 'KELP', decimal_fair_price, depth=3)

            # Check if there's another market maker
            best_ask = self.get_ask(state, 'KELP', fair_price)
            best_bid =  self.get_bid(state, 'KELP', fair_price)

            # our ordinary market
            buy_price = math.floor(decimal_fair_price) - 2
            sell_price = math.ceil(decimal_fair_price) + 2
        
            # update market if someone else is better than us
            if best_ask is not None and best_bid is not None:
                ask = best_ask
                bid = best_bid
                
                sell_price = ask - 1
                buy_price = bid + 1

            max_buy =  50 - self.kelp_position - self.kelp_buy_orders # MAXIMUM SIZE OF MARKET ON BUY SIDE
            max_sell = self.kelp_position + 50 - self.kelp_sell_orders # MAXIMUM SIZE OF MARKET ON SELL SIDE

            self.send_buy_order('KELP', buy_price, max_buy, msg=f"KELP: MARKET MADE Buy {max_buy} @ {buy_price}")
            self.send_sell_order('KELP', sell_price, -max_sell, msg=f"KELP: MARKET MADE Sell {max_sell} @ {sell_price}")

    def trade_squid_ink(self, state):
        symbol = "SQUID_INK"
        order_book = state.order_depths[symbol]
        position = state.position.get(symbol, 0)
        max_pos = self.limits[symbol]

        # Require full book to work
        if not order_book.buy_orders or not order_book.sell_orders:
            logger.print("SQUID_INK: No liquidity")
            return

        best_bid = max(order_book.buy_orders.keys())
        best_ask = min(order_book.sell_orders.keys())
        mid_price = (best_bid + best_ask) / 2

        # Update price history
        self.squid_ink_prices.append(mid_price)
        if len(self.squid_ink_prices) > 3000:
            self.squid_ink_prices = self.squid_ink_prices[-3000:]

        # Only trade once we have enough data
        if len(self.squid_ink_prices) < self.squid_ink_long_window:
            logger.print(f"SQUID_INK: Warming up ({len(self.squid_ink_prices)}/{self.squid_ink_long_window})")
            return

        # Calculate EMA
        alpha = 2 / (self.squid_ink_long_window + 1)
        if self.squid_ink_ema_long is None:
            self.squid_ink_ema_long = np.mean(self.squid_ink_prices[-self.squid_ink_long_window:])
        else:
            self.squid_ink_ema_long = alpha * mid_price + (1 - alpha) * self.squid_ink_ema_long

        ema = self.squid_ink_ema_long
        std_dev = np.std(self.squid_ink_prices[-50:])

        if std_dev == 0:
            return  # No volatility = no signal

        z = (mid_price - ema) / std_dev
        logger.print(f"SQUID_INK - Mid: {mid_price:.1f}, EMA: {ema:.1f}, Z: {z:.2f}, Pos: {position}")

        # Strategy parameters
        entry_z = 1.25  # When to enter trades
        exit_z = 0.3    # When to exit trades
        aggression = int(min(25, abs(z) * max_pos))  # Dynamic size

        # Mean Reversion Entry
        if z > entry_z and position > -max_pos:
            size = min(aggression, max_pos + position)
            self.send_sell_order(symbol, best_bid, -size, msg=f"SQUID: MR SELL {size} @ {best_bid} (Z={z:.2f})")
            self.squid_ink_sell_orders += size

        elif z < -entry_z and position < max_pos:
            size = min(aggression, max_pos - position)
            self.send_buy_order(symbol, best_ask, size, msg=f"SQUID: MR BUY {size} @ {best_ask} (Z={z:.2f})")
            self.squid_ink_buy_orders += size

        # Mean Reversion Exit
        elif abs(z) < exit_z:
            if position > 0:
                self.send_sell_order(symbol, best_bid, -position, msg=f"SQUID: EXIT SELL {position} @ {best_bid}")
                self.squid_ink_sell_orders += position
            elif position < 0:
                self.send_buy_order(symbol, best_ask, -position, msg=f"SQUID: EXIT BUY {-position} @ {best_ask}")
                self.squid_ink_buy_orders += -position



    # TODO: UPDATE WHENEVER YOU ADD A NEW PRODUCT
    def reset_orders(self, state):
        self.orders = {}
        self.conversions = 0

        # reset order counts and positions
        self.resin_position = self.get_product_pos(state, 'RAINFOREST_RESIN')
        self.resin_buy_orders = 0
        self.resin_sell_orders = 0

        self.kelp_position = self.get_product_pos(state, 'KELP')
        self.kelp_buy_orders = 0
        self.kelp_sell_orders = 0

        self.squid_ink_position = self.get_product_pos(state, 'SQUID_INK')
        self.squid_ink_buy_orders = 0
        self.squid_ink_sell_orders = 0

        for product in state.order_depths:
            self.orders[product] = []

    def run(self, state: TradingState):        
        self.reset_orders(state)

        self.trade_resin(state)
        self.trade_kelp(state)
        self.trade_squid_ink(state)

        logger.flush(state, self.orders, self.conversions, self.traderData)
        return self.orders, self.conversions, self.traderData

STATIC_SYMBOL = 'RAINFOREST_RESIN'
DYNAMIC_SYMBOL = 'KELP'
INK_SYMBOL = 'SQUID_INK'

POS_LIMITS = {
    STATIC_SYMBOL: 50, 
    DYNAMIC_SYMBOL: 50,
    INK_SYMBOL: 50,

LONG, NEUTRAL, SHORT = 1, 0, -1

class ProductTrader:

    def __init__(self, name, state, prints, new_trader_data, product_group=None):

        self.orders = []

        self.name = name
        self.state = state
        self.prints = prints
        self.new_trader_data = new_trader_data
        self.product_group = name if product_group is None else product_group

        self.last_traderData = self.get_last_traderData()

        self.position_limit = POS_LIMITS.get(self.name, 0)
        self.initial_position = self.state.position.get(self.name, 0) # position at beginning of round

        self.expected_position = self.initial_position # update this if you expect a certain change in position e.g. to already hedge


        self.mkt_buy_orders, self.mkt_sell_orders = self.get_order_depth()
        self.bid_wall, self.wall_mid, self.ask_wall = self.get_walls()
        self.best_bid, self.best_ask = self.get_best_bid_ask()

        self.max_allowed_buy_volume, self.max_allowed_sell_volume = self.get_max_allowed_volume() # gets updated when order created
        self.total_mkt_buy_volume, self.total_mkt_sell_volume = self.get_total_market_buy_sell_volume()

    def get_last_traderData(self):
                        
        last_traderData = {}
        try:
            if self.state.traderData != '':
                last_traderData = json.loads(self.state.traderData)
        except: self.log("ERROR", 'td')

        return last_traderData


    def get_best_bid_ask(self):

        best_bid = best_ask = None

        try:
            if len(self.mkt_buy_orders) > 0:
                best_bid = max(self.mkt_buy_orders.keys())
            if len(self.mkt_sell_orders) > 0:
                best_ask = min(self.mkt_sell_orders.keys())
        except: pass

        return best_bid, best_ask


    def get_walls(self):

        bid_wall = wall_mid = ask_wall = None

        try: bid_wall = min([x for x,_ in self.mkt_buy_orders.items()])
        except: pass
        
        try: ask_wall = max([x for x,_ in self.mkt_sell_orders.items()])
        except: pass

        try: wall_mid = (bid_wall + ask_wall) / 2
        except: pass

        return bid_wall, wall_mid, ask_wall
    
    def get_total_market_buy_sell_volume(self):

        market_bid_volume = market_ask_volume = 0

        try:
            market_bid_volume = sum([v for p, v in self.mkt_buy_orders.items()])
            market_ask_volume = sum([v for p, v in self.mkt_sell_orders.items()])
        except: pass

        return market_bid_volume, market_ask_volume
    

    def get_max_allowed_volume(self):
        max_allowed_buy_volume = self.position_limit - self.initial_position
        max_allowed_sell_volume = self.position_limit + self.initial_position
        return max_allowed_buy_volume, max_allowed_sell_volume

    def get_order_depth(self):

        order_depth, buy_orders, sell_orders = {}, {}, {}

        try: order_depth: OrderDepth = self.state.order_depths[self.name]
        except: pass
        try: buy_orders = {bp: abs(bv) for bp, bv in sorted(order_depth.buy_orders.items(), key=lambda x: x[0], reverse=True)}
        except: pass
        try: sell_orders = {sp: abs(sv) for sp, sv in sorted(order_depth.sell_orders.items(), key=lambda x: x[0])}
        except: pass

        return buy_orders, sell_orders
    

    def bid(self, price, volume, logging=True):
        abs_volume = min(abs(int(volume)), self.max_allowed_buy_volume)
        order = Order(self.name, int(price), abs_volume)
        if logging: self.log("BUYO", {"p":price, "s":self.name, "v":int(volume)}, product_group='ORDERS')
        self.max_allowed_buy_volume -= abs_volume
        self.orders.append(order)

    def ask(self, price, volume, logging=True):
        abs_volume = min(abs(int(volume)), self.max_allowed_sell_volume)
        order = Order(self.name, int(price), -abs_volume)
        if logging: self.log("SELLO", {"p":price, "s":self.name, "v":int(volume)}, product_group='ORDERS')
        self.max_allowed_sell_volume -= abs_volume
        self.orders.append(order)

    def log(self, kind, message, product_group=None):
        if product_group is None: product_group = self.product_group

        if product_group == 'ORDERS':
            group = self.prints.get(product_group, [])
            group.append({kind: message})
        else:
            group = self.prints.get(product_group, {})
            group[kind] = message

        self.prints[product_group] = group

    def check_for_informed(self):

        informed_direction, informed_bought_ts, informed_sold_ts = NEUTRAL, None, None
        

        informed_bought_ts, informed_sold_ts = self.last_traderData.get(self.name, [None, None])

        trades = self.state.market_trades.get(self.name, []) + self.state.own_trades.get(self.name, [])

        for trade in trades:
            if trade.buyer == INFORMED_TRADER_ID:
                informed_bought_ts = trade.timestamp
            if trade.seller == INFORMED_TRADER_ID: 
                informed_sold_ts = trade.timestamp
            
        self.new_trader_data[self.name] = [informed_bought_ts, informed_sold_ts]

        informed_sold = informed_sold_ts is not None
        informed_bought = informed_bought_ts is not None

        if not informed_bought and not informed_sold:
            informed_direction = NEUTRAL

        elif not informed_bought and informed_sold:
            informed_direction = SHORT

        elif informed_bought and not informed_sold:
            informed_direction = LONG

        elif informed_bought and informed_sold:
            if informed_sold_ts > informed_bought_ts:
                informed_direction = SHORT
            elif informed_sold_ts < informed_bought_ts:
                informed_direction = LONG
            else:
                informed_direction = NEUTRAL

        self.log('TD', self.new_trader_data[self.name])
        self.log('ID', informed_direction)

        return informed_direction, informed_bought_ts, informed_sold_ts


    def get_orders(self):
        # overwrite this in each trader
        return {}


# Rainforest Raisin
class StaticTrader(ProductTrader):
    def __init__(self, state, prints, new_trader_data):
        super().__init__(STATIC_SYMBOL, state, prints, new_trader_data)

    def get_orders(self):

        if self.wall_mid is not None:

            ##########################################################
            ####### 1. TAKING
            ##########################################################
            for sp, sv in self.mkt_sell_orders.items():
                if sp <= self.wall_mid - 1:
                    self.bid(sp, sv, logging=False)
                elif sp <= self.wall_mid and self.initial_position < 0:
                        volume = min(sv,  abs(self.initial_position))
                        self.bid(sp, volume, logging=False)

            for bp, bv in self.mkt_buy_orders.items():
                if bp >= self.wall_mid + 1:
                    self.ask(bp, bv, logging=False)
                elif bp >= self.wall_mid and self.initial_position > 0:
                        volume = min(bv,  self.initial_position)
                        self.ask(bp, volume, logging=False)

            ###########################################################
            ####### 2. MAKING
            ###########################################################
            bid_price = int(self.bid_wall + 1) # base case
            ask_price = int(self.ask_wall - 1) # base case

            # OVERBIDDING: overbid best bid that is still under the mid wall
            for bp, bv in self.mkt_buy_orders.items():
                overbidding_price = bp + 1
                if bv > 1 and overbidding_price < self.wall_mid:
                    bid_price = max(bid_price, overbidding_price)
                    break
                elif bp < self.wall_mid:
                    bid_price = max(bid_price, bp)
                    break

            # UNDERBIDDING: underbid best ask that is still over the mid wall
            for sp, sv in self.mkt_sell_orders.items():
                underbidding_price = sp - 1
                if sv > 1 and underbidding_price > self.wall_mid:
                    ask_price = min(ask_price, underbidding_price)
                    break
                elif sp > self.wall_mid:
                    ask_price = min(ask_price, sp)
                    break

            # POST ORDERS
            self.bid(bid_price, self.max_allowed_buy_volume)
            self.ask(ask_price, self.max_allowed_sell_volume)


        return {self.name: self.orders}


# Kelp
class DynamicTrader(ProductTrader):
    def __init__(self, state, prints, new_trader_data):
        super().__init__(DYNAMIC_SYMBOL, state, prints, new_trader_data)

        self.informed_direction, self.informed_bought_ts, self.informed_sold_ts = self.check_for_informed()


    def get_orders(self):

        if self.wall_mid is not None:

            bid_price = self.bid_wall + 1
            bid_volume = self.max_allowed_buy_volume

            if self.informed_bought_ts is not None and self.informed_bought_ts + 5_00 >= self.state.timestamp:
                if self.initial_position < 40:
                    bid_price = self.ask_wall
                    bid_volume = 40 - self.initial_position

            else:

                if self.wall_mid - bid_price < 1 and (self.informed_direction == SHORT and self.initial_position > -40):
                    bid_price = self.bid_wall

            self.bid(bid_price, bid_volume)


            ask_price = self.ask_wall - 1
            ask_volume = self.max_allowed_sell_volume

            if self.informed_sold_ts is not None and self.informed_sold_ts + 5_00 >= self.state.timestamp:

                if self.initial_position > -40:
                    ask_price = self.bid_wall
                    ask_volume = 40 + self.initial_position

            if ask_price - self.wall_mid < 1 and (self.informed_direction == LONG and self.initial_position < 40):
                ask_price = self.ask_wall

            self.ask(ask_price, ask_volume)


        return {self.name: self.orders}
    



class InkTrader(ProductTrader):
    def __init__(self, state, prints, new_trader_data):
        super().__init__(INK_SYMBOL, state, prints, new_trader_data)

        self.informed_direction, _, _ = self.check_for_informed()


    def get_orders(self):

        expected_position = 0
        if self.informed_direction == LONG:
            expected_position = self.position_limit
        elif self.informed_direction == SHORT:
            expected_position = -self.position_limit

        remaining_volume = expected_position - self.initial_position

        if remaining_volume > 0 and self.ask_wall is not None:
            self.bid(self.ask_wall, remaining_volume)

        elif remaining_volume < 0 and self.bid_wall is not None:
            self.ask(self.bid_wall, -remaining_volume)

        return {self.name: self.orders}
class Trader:

    def run(self, state: TradingState):
        result:dict[str,list[Order]] = {}
        new_trader_data = {}
        prints = {
            "GENERAL": {
                "TIMESTAMP": state.timestamp,
                "POSITIONS": state.position
            },
        }

        def export(prints):
            try: print(json.dumps(prints))
            except: pass


        product_traders = {
            STATIC_SYMBOL: StaticTrader,
            DYNAMIC_SYMBOL: DynamicTrader,
            INK_SYMBOL: InkTrader,
            ETF_BASKET_SYMBOLS[0]: EtfTrader,
            OPTION_UNDERLYING_SYMBOL: OptionTrader,
            COMMODITY_SYMBOL: CommodityTrader,
        }

        result, conversions = {}, 0
        for symbol, product_trader in product_traders.items():
            if symbol in state.order_depths:

                try:
                    trader = product_trader(state, prints, new_trader_data)
                    result.update(trader.get_orders())

                    if symbol == COMMODITY_SYMBOL:
                        conversions = trader.get_conversions()
                except: pass


        try: final_trader_data = json.dumps(new_trader_data)
        except: final_trader_data = ''


        export(prints)
        return result, conversions, final_trader_data






