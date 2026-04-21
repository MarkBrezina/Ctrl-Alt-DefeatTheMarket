
**Note:** Out of respect for the moderators' request, I will not share specific code or substantial spoilers while rounds are active. Instead, I will provide high-level descriptions of the assets until the conclusion of each round.

## Round 2: The interian Expansion
Welcome to the second trading round on Intara. This is your final opportunity to reach the threshold of **200,000 XIRECs** before the leaderboard resets for Phase 2. These first two rounds serve as the primary qualifiers for the final mission.

Since your arrival, trading activity has accelerated. The market for **Ash-Coated Osmium** and **Intarian Pepper Root** is increasingly competitive, requiring more than just a basic algorithm to stay ahead.

**New Mechanics: Market Access & Budgets**
In this round, two new strategic layers have been introduced:

1. **Market Access Fee (MAF):** You can now bid for **25% more order book volume**. This is a "blind auction"—only the **top 50% of bidders** will secure the extra flow.
   - Success: You pay your bid price and get 25% more quotes to trade against.
   - Failure: You pay nothing and continue with the standard 80% volume allocation.

2. **Growth Pillars:** XIREN has provided a **50,000 XIRECs investment budget.** You must distribute this across three growth pillars to optimize your outpost’s performance.

**Implementing the Bid:**
To participate in the MAF auction, incorporate the bid() function into your Trader class. Note that this function is unique to Round 2; it is ignored in all other rounds and during the manual "Test Run" phase.

**Game Theory Tip:** You don't need to be the highest bidder to win; you just need to be in the top half. Placing an excessively high bid guarantees access but eats into your final PnL. The goal is to find the "Goldilocks" bid that clears the median without overpaying.

# Algorithmic challenge
The 2nd round continues the 1st round, with the same assets, but with a new mechanism, the bid mechanism that was left in on the standard trader function.
We are now posed with the problem

""You may include a Market Access Fee (MAF) in your Python program to gain access to an additional 25% of quotes. Only the top 50% of total MAFs will secure the contract, pay the MAF, and access this additional 25%. Others will not have to pay their MAF and will continue trading with the original volume allocation.""

This year, **@Tomas** and the team introduced some interesting variations to the asset classes.

From the previous round I can share the following.

## Intarian Pepper Root
Instead of the perfectly stationary "straight-line" behavior seen with **EMERALDS** in the tutorial, we have **Intarian Pepper Root**. This asset follows a similar logic but is adjusted for a **linear trend.**
- **Observation:** I found that running a linear regression on the `mid_price` using a window of roughly 100 timesteps yielded a fairly decent predictive result.
- **Strategy:** While the "ideal" strategy appeared to be **Buy and Hold**, a naive "buy as fast as possible" approach proved suboptimal due to high transaction costs.
- **Pro Tip:** As **@oats(April)** pointed out, there were also significant opportunities to capture value by analyzing and reacting to the increasing spread.

![Pepper Root](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/utils/pepper_root.png)

## Ash-covered Osmium
Similar to **TOMATOES** from the tutorial, **Osmium** is a "drifting" asset. The goal here was to adapt a drift-adjusted mean reversion strategy.
- **Optimal Approach:** The winning play likely involved a sophisticated blend of **market-making, market-taking on mispricings**, and **mean reversion**—all while accounting for the underlying drift. Finding the perfect "quoting mix" for these factors was the main challenge discussed by the community on Discord.

![Osmium](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/utils/osmium.png)

**Notes on research:** I went over an exercise on denoising the price of Osmium, in order to improve my own signal quality on mean reversion, there was significant benefit in backfilling mid_prices on empty orderbook moments and on using full orderbook volume adjusted mid prices, as well as backfilling for prices with significnat orderflow and imbalance.

![denoised](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/utils/denoised.png)

## Research & Denoising: Finding the Signal
I spent considerable time denoising the price of **Osmium** to improve my signal quality for mean reversion. There was a significant advantage in:
- **Backfilling** `mid_prices` during empty order book moments.
- Utilizing **volume-weighted mid-prices** across the full order book.
- Adjusting for prices during periods of significant **order flow imbalance.**

**Post-Mortem: Where it Went Sideways**
To be blunt, I fumbled my own submission quite significantly. After a post-round review of my code, I discovered a comedy of errors:

1. **Directional Logic:** I managed to completely reverse my $Z$-score entry and exit signals.

2. **Order Execution:** I inadvertently forced my market-making logic to return negative orders for certain timestamps, leading the algorithm to "cross the spread" and trade against itself at will.

3. **Suboptimal Inventory:** I knew my inventory adjustments were flawed, but I was forced to ship the code as-is due to the deadline.

## The "Ideal" Strategy vs. Reality
The goal was a sophisticated blend of **Market Making (MM)**, **Market Taking (MT)** on mispricings, **Mean Reversion**, and a slight **Drift adjustment.**

The real challenge—and what likely separated the top of the leaderboard from the rest of us—is finding the perfect "quoting mix" for these strategies. In discussions on Discord, it’s clear that balancing these weights was a universal struggle.

**My Specific (and Flawed) Algo:**
- **Aggressive MM:** Quoted at $best bid + 1$ (with $best ask$ volume) and $best ask - 1$ (with $-best bid$ volume).
- **Passive MM:** Placed small orders (volume of 3) exactly at the $best bid$ and $best ask$.
- **Market Taking:** Executed based on a $Z$-score on price (which, in hindsight, was likely suboptimal).

**The "Idiotic" Move:** A major error was simply subtracting a flat volume of 3 from both sides without a `max(0, quote)` check. For empty timestamps, this caused the algorithm to cross its own orders and short aggressively—an "experiment" in inventory management that proved to be a disaster.

## Roadmap for Improvements
Moving forward, I’m focusing on these four pillars to stabilize the algorithm:
1. **Handling Gaps:** Implementing robust logic for moments with no bids, asks, or mid-prices.
2. **Memory & Denoising:** Developing a time-series "memory" of denoised mid-prices to filter out temporary noise.
3. **Trend Integration:** Adding micro-trend following to better time the entries for the mean reversion setup.
4. **Passive Liquidity:** Refining the placement of passive quotes within the book to capture spread without getting "run over."

# Manual Challenge
This is an optimisation problem between profit and cost. Once again I will not be participating in this part, someone else is working on this and I will not share the solution until the round is over.



Post-Mortem: Where My Submission Broke Down

In hindsight, the biggest gap between the strategy I wanted to run and the strategy I actually submitted was implementation quality.

After reviewing the code post-round, I found several major issues:

Reversed directional logic:
I accidentally inverted my $Z$-score entry and exit logic, which meant I was often leaning the wrong way on the very signal I intended to trade.
Broken order handling:
At certain timestamps, my market-making logic produced negative order quantities where it should not have. In practice, this sometimes caused the strategy to cross the spread and trade against its own intended logic.
Weak inventory control:
I already knew my inventory adjustments were underdeveloped, but I ran out of time and had to ship the strategy as-is. That left the system much more exposed than I would have liked.

So while the high-level idea was reasonable, the actual submission suffered from several avoidable execution errors. In a round where edge came from small but repeatable microstructure signals, those implementation mistakes mattered a lot.

Missed Alpha and What I Underestimated

One of the main lessons from this round is that I initially dismissed several useful microstructure signals as “noise.”

Coming from a more medium-frequency / portfolio-management mindset, I’m used to filtering out very short-horizon effects unless they survive transaction costs and capacity constraints. In this environment, though, some of those short-lived effects were not noise at all — they were a meaningful source of edge.

Here are the main patterns I think mattered most:

1. Pepper Root: trend was the obvious first-order signal

Intarian Pepper Root showed a fairly clean upward linear trend. The first and most important conclusion was simple: the asset wanted to go up.
In that sense, a buy-and-hold style bias was likely the correct baseline view, and I assume most participants picked up on that quickly.

The harder part was not identifying the trend, but executing around it efficiently. A naive “buy immediately and as aggressively as possible” approach leaves too much value on the table through spread costs and poor timing. The better version was likely some combination of:

directional accumulation,
passive buying where possible,
and spread-aware execution.
2. Osmium: classic mean reversion, but with structure

Ash-Coated Osmium behaved much more like a mean-reverting asset, closer to the kind of short-horizon reversion you see in real markets.

The key was not just “buy low, sell high,” but understanding which deviations were worth fading:

deviations in a denoised price,
deviations driven by temporary order-book imbalance,
and short-term dislocations caused by one-sided flow.

In other words, the real edge likely came from combining:

mean reversion,
market making,
selective market taking,
and a light drift adjustment when needed.
3. Order-flow and microprice dislocations were more valuable than I gave them credit for

This was probably my biggest conceptual miss.

Short-horizon price pressure often appeared to overshoot in the direction of recent order flow, creating small reversion opportunities. In practical terms:

When order flow was strongly negative, that often coincided with a short-term push downward that could subsequently mean revert.
When order flow was strongly positive, the opposite setup often appeared.

These were not massive directional bets, but they looked like exactly the kind of repeatable micro-alpha that matters in a low-latency market-making setting.

4. Single-sided and empty order books created unusual opportunities

Another feature I underestimated was how informative thin books could be.

If the book became single-sided, or nearly empty, price discovery effectively became much less competitive. In those moments:

if you were the only meaningful buyer or seller,
or one of the only participants quoting,

you had a temporary opportunity to shape the available price.

That does not mean you can quote anything you want forever, but in a sparse market it clearly matters who is willing to show liquidity first. These moments seemed especially valuable for:

setting favorable passive quotes,
harvesting spread,
and anchoring price when competition temporarily disappeared.
5. The main lesson: microstructure edge compounds

None of these signals in isolation looked huge. But together, they likely formed a meaningful edge:

trend capture in Pepper Root,
mean reversion in Osmium,
spread capture through passive liquidity,
order-flow reversion,
imbalance-based fades,
and opportunistic quoting during empty-book states.

That is also what made implementation quality so important. When your edge comes from many small improvements, even minor mistakes in quoting, sizing, or inventory logic can wipe out the benefit.

Roadmap for Improvements

If I were to rebuild this round from scratch, I would focus on four things:

Robust handling of sparse data:
Better logic for timestamps with missing bids, asks, or mid-prices.
Denoised state estimation:
A cleaner internal fair-value process using backfilled and volume-adjusted prices.
Microstructure-aware signal layering:
Combining trend, reversion, imbalance, and order-flow information in a more structured way.
Safer quote construction:
Stronger inventory controls and stricter safeguards to prevent invalid or self-defeating order placement.
Diagram ideas: what to use for each concept

If you want to showcase the alphas clearly, I would not try to cram everything into one figure. The cleanest approach is a small set of focused charts, each with one job.

Recommended diagram set
1. Pepper Root trend chart

Purpose: Show the linear upward trend and why buy-and-hold was the baseline.

Use:

Line chart of mid_price over time
Overlay rolling linear regression trend line
Optionally mark “passive accumulation” zones

Why it works:
This makes the first-order signal immediately obvious.

Good caption:
“Pepper Root exhibited a persistent upward drift, making directional accumulation the natural baseline strategy.”

2. Osmium raw vs denoised price chart

Purpose: Show why denoising matters for mean reversion.

Use:

Two lines on the same chart:
raw mid-price
denoised / backfilled / volume-adjusted price
Optional shaded bands for mean-reversion thresholds or Z-score bands

Why it works:
It visually explains that the tradable signal is cleaner than the raw tape.

Good caption:
“Denoising reduced microstructure noise and made short-horizon reversion signals easier to identify.”

3. Spread capture / market-making schematic

Purpose: Explain how passive quoting captures edge.

Best format:
A simple order book ladder diagram or a quote placement diagram, not a time series.

Show:

best bid
best ask
your passive quotes
fill arrows
realized spread

Why it works:
Spread capture is easier to understand as a book snapshot than as a noisy time-series plot.

Good caption:
“Passive liquidity provision monetizes the spread when quotes are placed ahead of adverse selection.”

4. Order imbalance vs future return

Purpose: Show mean reversion conditioned on imbalance.

Best format:
A bucketed bar chart or decile plot.

X-axis: order imbalance buckets (very negative to very positive)
Y-axis: average next-period return

If the alpha is reversionary, you should see:

strongly negative imbalance → positive next return
strongly positive imbalance → negative next return

Why it works:
This is probably the cleanest way to present the relationship statistically.

Good caption:
“Extreme order-book imbalance tended to be followed by short-term reversal rather than continuation.”

5. Order flow shock event study

Purpose: Show order-flow reversion.

Best format:
An event study chart.

X-axis: time relative to event (t-10 to t+20)
Y-axis: cumulative return or average mid-price change

Split into two panels or two lines:

positive order-flow shocks
negative order-flow shocks

Why it works:
It shows whether order-flow bursts tend to overshoot and reverse afterward.

Good caption:
“Short-term directional order-flow shocks often reverted over the following few observations.”

6. Empty / single-sided book opportunity chart

Purpose: Show the alpha from sparse books.

You have two good options:

Option A: Event-study style
Detect moments where the order book is empty or single-sided
Plot average return / spread / fill opportunity around those events
Option B: Example snapshots
Show 3–4 small order-book snapshots:
normal book
thin book
single-sided book
empty book
Annotate what opportunity exists in each case

Why it works:
This concept is structural, so examples are often better than pure statistics.

Good caption:
“When the book became sparse or one-sided, the first participant willing to show liquidity gained disproportionate price-setting influence.”


Intarian Pepper Root: Time-Phase Momentum
My strategy here is strictly temporal. I treat the product differently based on the round's progress to maximize volume early and safety late:
Early Game (<15% progress): I focus on Aggressive Accumulation. I’m sweeping the entire ask book and placing passive orders 1 tick above the best ask to dominate the queue and hit my inventory limits immediately.
End Game (>99.9% progress): I trigger an Optimized Exit, where I sweep the top of the bid book to liquidate my entire position and lock in PnL before the timestamp hits the limit.
Ash Coated Osmium: Dynamic Mean Reversion
For this one, I’m running a Market Making strategy centered on price improvement and inventory-weighted pivots:
Robust Fair Value: I use a rolling 10-period median mid-price to filter out outliers and establish a stable fair value.
Inventory Skew: I calculate an internal_pivot that shifts based on my current position. If I’m long, the pivot moves down to make my sell orders more competitive, effectively "leaning" into the spread to manage risk.
Liquidity Sniping: I’ve added a "safety valve" that snipes the entire boat if the market price deviates more than 12 ticks from my pivot, capturing massive mispricings while using passive market making (15-unit chunks) for standard flow.
