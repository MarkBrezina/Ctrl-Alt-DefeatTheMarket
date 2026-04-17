
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

I cocked this up quite significantly on my own submission, going back over my code I not only reversed my Z-score entry and exit. \
But also force my market making to return negative orders for some timestamps, leading to random orderbook crosses at will. \
I knew that my inventory adjustments were suboptimal, but simply had to load in.

The optimal strategy I was going for was a combination of market-making, market-taking on mispricings, mean reversion and a bit of drift.
The goal than becomes finding the proper quoting mixes of this. Talking with several people on the discord, we all struggled to find this
ideal combination and that is what I suspect gets the difference between all of us.


My specific algo was.
1. Market making, best_bid +1 with best_ask_volume, best_ask -1 with -best_bid_volume.
2. Passive market making, best_bid with 3, best_ask with -3.
3. Market taking on Z-score on price. I now suspect this is suboptimal too.

A set of my errors here was to simply flat subtract 3 on both side, causing my market making for empty timestamps to cross and short. Which is an absolutely idiotic move, I did simply to experiment with my market-making inventory. \
with no adjustment for max of (0, bid/ask_quote).

A set of notes for improvements I have considered were the following.
1. correcting for moments with no bid, ask or mid price.
2. correcting for noisy mid pricing, to develop a memory and timeseries of denoised mid prices.
3. correcting for microtrend following into the mean reversion set up.
4. adding passive quotes in the book.





# Manual Challenge
This is an optimisation problem between profit and cost. Once again I will not be participating in this part, someone else is working on this and I will not share the solution until the round is over.





