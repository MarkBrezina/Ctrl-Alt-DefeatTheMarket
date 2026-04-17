
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
- **Aggressive MM:** Quoted at $best\_bid + 1$ (with $best\_ask$ volume) and $best\_ask - 1$ (with $-best\_bid$ volume).
- **Passive MM:** Placed small orders (volume of 3) exactly at the $best\_bid$ and $best\_ask$.
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





