
**Note:** Out of respect for the moderators' request, I will not be sharing specific code or substantial spoilers while rounds are active. Instead, I will provide high-level descriptions of the assets until the conclusion of each round.

# Algorithmic challenge
This year, **@Tomas** and the team introduced some interesting variations to the asset classes.

## Intarian Pepper Root
Instead of the perfectly stationary "straight-line" behavior seen with **EMERALDS** in the tutorial, we have **Intarian Pepper Root**. This asset follows a similar logic but is adjusted for a **linear trend.**
- **Observation:** I found that running a linear regression on the `mid_price` using a window of roughly 100 timesteps yielded a fairly decent predictive result.
- **Strategy:** While the "ideal" strategy appeared to be **Buy and Hold**, a naive "buy as fast as possible" approach proved suboptimal due to high transaction costs.
- **Pro Tip:** As **@oats(April)** pointed out, there were also significant opportunities to capture value by analyzing and reacting to the increasing spread.

![Pepper Root](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/utils/pepper_root.png)

## Ash-covered Osmium
Similar to **TOMATOES** from the tutorial, **Osmium** is a "drifting" asset. The goal here was to adapt a drift-adjusted mean reversion strategy.
- **The "Post-Mortem":** I'll be honest—I botched the implementation here. Going back through my code, I realized I had accidentally reversed my Z-score entry and exit logic. Furthermore, a bug in my market-making function forced negative orders at certain timestamps, leading to unintended orderbook crosses. While I knew my inventory management was suboptimal, I had to ship the code as-is for the round.
- **Optimal Approach:** The winning play likely involved a sophisticated blend of **market-making, market-taking on mispricings**, and **mean reversion**—all while accounting for the underlying drift. Finding the perfect "quoting mix" for these factors was the main challenge discussed by the community on Discord.

![Osmium](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/utils/osmium.png)

**Note on research:** I went over an exercise on denoising the price of Osmium, in order to improve my own signal quality on mean reversion, there was significant benefit in backfilling mid_prices on empty orderbook moments and on using full orderbook volume adjusted mid prices, as well as backfilling for prices with significnat orderflow and imbalance.

![denoised](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/utils/denoised.png)

# Manual Challenge
The manual challenge required balancing volume against price impact to maximize net profit. Here is the breakdown of my logic:

## DRYLANX_FLAX
- **The Play:** Bid **9999 @ 30.**
- **The Result:** This results in a clearing price of **29**, leading to a full fill of the 9999 order.
- **Profit Calculation:** $9999 \times (30 - 29) = 9999$.
- **Why not more?** Increasing the order size to 10,000 would have pushed the clearing price up to 30, resulting in zero profit. Conversely, bidding lower would either result in no fill or a partial fill (e.g., 5,000 units), both of which yield lower total profit.

## EMBER_MUSHROOM
- **The Play:** Bid **19,999 @ 17.**
- **The Result:** This leads to a clearing price of **16** (matching a volume of 91k).
- **Profit Calculation:** $19,999 \times (19.9 - 16) = 77,996.1$.
  - *Note: 19.9 represents the 20.0 buyback price minus 0.10 in total transaction costs (0.05 for the buy and 0.05 for the sell).*
- **Why not more?** Bidding for 20,000 units would have moved the clearing price to 17, significantly reducing the profit margin per unit.



I cocked this up quite significantly, going back over my code I not only reversed my Z-score entry and exit. \
But also force my market making to return negative orders for some timestamps, leading to random orderbook crosses at will. \
I knew that my inventory adjustments were suboptimal, but simply had to load in.

The optimal strategy I was going for was a combination of market-making, market-taking on mispricings, mean reversion and a bit of drift.
The goal than becomes finding the proper quoting mixes of this. Talking with several people on the discord, we all struggled to find this
ideal combination and that is what I suspect gets the difference between all of us.


My specific algo was.
1. Market making, best_bid +1 with best_ask_volume, best_ask -1 with -best_bid_volume.
2. Passive market making, best_bid with 3, best_ask with -3.

My error here was to simply flat subtract 3 on both side, causing my market making for empty timestamps to cross and short. Which is an absolutely idiotic move, I did simply to experiment with my market-making inventory. \
Yeah, no adjustment for max of (0, bid/ask_quote)
