**Note:** Out of respect for the moderators’ request, I will not share specific code or substantial spoilers while rounds are active. Instead, I will provide high-level descriptions of the assets until each round has concluded.

## Round 3: Notes

We do not yet know what the assets for Rounds 3, 4, and 5 will be, and at present we also do not have data for them. However, based on previous years, we can start forming some reasonable hypotheses.

## Commodities and external factors

Orchids were introduced in Round 2, along with a range of external variables: sunlight, humidity, import/export tariffs, and shipping costs. The premise was that orchids were grown on a separate island and had to be imported, making them subject to tariffs and transport costs. Their value also deteriorated under poor sunlight and humidity conditions. We were able to trade orchids both in our local market and through imports from the South Archipelago.

From the start, we saw two possible approaches. The first was the obvious one: look for alpha in the available data by testing whether orchid prices could be predicted from sunlight, humidity, tariffs, and so on. The second was to understand the mechanics of orchid trading itself, since the documentation was not especially clear. We split up accordingly: Eric looked for predictive signals in the historical data, while Jerry focused on reverse-engineering the trading environment.

Finding tradable correlations in the historical data turned out to be much harder than expected. Among the things we tried were:

- simple correlations between orchid returns and changes in sunlight, humidity, tariffs, and costs;
- linear regressions from these variables to orchid returns, both contemporaneously and with lags;
- feature engineering on the raw inputs, followed by the same correlation and regression analyses.

Some of the early results looked promising, but in the end none of them produced a convincing trading model. Our conclusion was that much of the data was likely a distraction.

Meanwhile, Jerry was making much better progress. Through experimentation, we discovered that there was a large, persistent taker in the local orchid market. Sell orders—and specifically sell orders—placed slightly above the best bid would often be filled immediately and in full size. Combined with relatively cheap implied asks from the foreign market, this created a straightforward arbitrage: sell locally and simultaneously buy from the South Archipelago.

The first version of this strategy generated roughly 60k seashells over about one-fifth of a day. After a few quick optimizations, our website backtest PnL rose to just over 100k, implying roughly 500k over a full day.

Unfortunately, this same strategy was later leaked in the Discord. From our perspective, that was quite damaging: once many teams could implement essentially the same arbitrage, rankings would come down to small implementation differences and noise. We knew we could easily lose places even if our logic was broadly correct.

As a result, we spent a great deal of time searching for incremental improvements. We tested different local sell levels and found that using `foreign ask price - 2` performed best. Even so, we worried that a fixed quoting level might stop filling reliably if market conditions changed. To address this, we built an “adaptive edge” algorithm. It monitored the average executed volume per iteration—where full size was nominally 100 lots—and if fills dropped below a threshold, it would automatically adjust the sell level in search of a better edge.

Even with those refinements, we were ultimately overtaken by the number of teams running the same arbitrage. We fell to 17th place, with 573,000 seashells in algo profit. That still left us within 20k of second place and about 100k behind the first-place team, Puerto Vallarta, who appeared to have found something this round that no one else had.

```python
# orchids code block here
```

## ETF / basket arbitrage
Gift baskets, chocolate, roses, and strawberries were introduced in Round 3. Each gift basket consisted of 4 chocolate bars, 6 strawberries, and 1 rose. Our main focus in this round was spread trading, where we defined the spread as:
```
basket - synthetic
```
with `synthetic` equal to the total price of the basket components.

Very quickly, we narrowed our thinking to two main hypotheses. The first was that either the synthetic basket would lead the quoted basket, or vice versa, creating a lead-lag relationship we could exploit. The second was that the spread itself might simply be mean reverting.

When we plotted the spread, we found that although it should theoretically be zero, in practice it oscillated around a fairly stable level of roughly 370 across all three days of historical data. That suggested a potentially profitable mean-reversion strategy: buy the spread (long basket, short synthetic) when it was too low, and sell the spread when it was too high.

We explored several ways of parameterizing this trade. Our first pass was a simple threshold strategy: trade only when the spread moved a fixed distance away from its average level. After backtesting a range of hard-coded thresholds, our best version projected roughly 120k in PnL.

However, this approach had an obvious weakness. If the spread reverted before reaching our entry threshold, we would miss the move entirely. Moving the thresholds closer solved that problem only partially, since it also caused us to trade too early and sacrifice edge before the spread reached a local maximum or minimum.

To address this, we developed a more adaptive version based on a modified z-score. We used a hard-coded long-run mean for the spread, but estimated volatility with a relatively short rolling window. The logic was that the mean level likely reflected something structural—such as the basket’s embedded pricing—while the day-to-day volatility was less stable and better handled adaptively.

We then traded based on z-score thresholds: selling the spread when the z-score rose above a certain level, and buying when it fell below a corresponding negative threshold. Because the rolling standard deviation window was short, the z-score would often spike just as volatility compressed, which tended to happen near turning points in the spread. In practice, this helped us enter trades closer to local extrema. This improved our projected backtest PnL from around 120k to roughly 135k.

After live results were released, we discovered that our actual PnL suffered meaningful slippage relative to the backtest. We made only 111k seashells in the round. Even so, we benefited from the fact that many of the teams ahead of us appeared to have overfit more aggressively, and we finished the round ranked #2 overall.
```
# basket arbitrage code block here
```

# Location arbitrage

[Add this section if you want to cover it separately.]

# Derivatives / underlying
Coconuts / coconut coupon

Coconuts and coconut coupons were introduced in Round 4. The coconut coupon was effectively a 10,000-strike call option on coconuts with 250 days to expiry. Since coconuts traded around 10,000, the option was close to at-the-money.

This round was conceptually straightforward. We used Black-Scholes to compute implied volatility from the observed option price, and once we plotted the resulting time series, it became clear that implied vol oscillated around roughly 16%. From there, we implemented a mean-reversion strategy similar to the one we had used in Round 3.

To isolate volatility exposure, we also computed the option delta at each point in time and hedged with the underlying coconuts. However, there was an important limitation: delta was around 0.53, while the position limits were 300 for coconuts and 600 for coconut coupons. This meant that if we held the full 600-coupon position, we could not fully hedge the delta because the coconut position cap bound first.

In practice, that left us with some unavoidable directional exposure. Since the option was still far from expiry—and therefore gamma mattered less—we accepted the residual delta risk in exchange for higher expected exposure to volatility. In other words, we knowingly ran more variance because it looked positive EV in backtests.

That worked well in simulation, but in the actual round we experienced a meaningful amount of slippage and were hurt by the unhedged delta exposure. In retrospect, this was probably too aggressive. We were already in second place overall, so reducing variance and defending our position may have been the better strategic choice.

Our algorithm made only 145k seashells in this round, which dropped us to a worrying 26th place. At the same time, Puerto Vallarta posted an enormous 1.2 million seashells in profit. That performance convinced us that if we could figure out what they had done, a top-10 finish was still very much within reach.

```
# coconut / option code block here
```









Cross-year signal discovery

Our leading hypothesis for Puerto Vallarta’s outsized profits was that they had found some way to predict future price movements. Profits on the order of 1.2 million seemed consistent with a strong statistical arbitrage signal spanning multiple products.

So we started searching aggressively. We ran linear regressions on lagged and contemporaneous returns across all symbols and all days in our dataset, hoping to uncover cross-asset relationships we had previously missed. We found a few mildly interesting effects—for example, starfruit appeared to have some lagged predictive power for several other symbols—but nothing close to what would explain an extra 1.2 million in profit.

As a final attempt, we remembered that the previous year’s competition—described in an excellent Stanford Cardinal write-up—shared a number of structural similarities with this one, especially in Round 1, where the product set sounded almost identical. So we sourced last year’s public data from GitHub and ran regressions from last year’s returns into this year’s symbols.

The results were absurd, but undeniable. Returns in last year’s diving gear, scaled by roughly 3, were almost a perfect predictor of roses, with an R² of 0.99. Likewise, last year’s coconuts were an almost perfect predictor of this year’s coconuts, with a beta of 1.25 and an R² of 0.99.

These relationships were ridiculous, but our objective in the competition was simple: maximize PnL. Since last year’s data was publicly available, we considered it fair game.

From that point onward, most of our work focused on extracting as much value as possible from these discovered relationships. We also assumed that other teams might uncover them, so optimization was critical.

Our first pass was simple: buy or sell coconuts and roses whenever the predicted future price moved beyond a threshold large enough to cover the spread. Even that worked dramatically better than anything we had built in the earlier rounds. But we believed there was still more value to extract. Since last year’s data effectively gave us the locations of future local maxima and minima, in principle we could time trades almost perfectly.

To do that in a systematic way across the three products we wanted to trade—roses, coconuts, and gift baskets—we developed a dynamic programming algorithm. The DP accounted for several practical constraints simultaneously: spread costs, executable volume at each iteration, and hard position limits.

The complexity came from the fact that we could not always move immediately to our ideal position. At any given step, the optimal strategy depended not only on the forecasted price path, but also on which intermediate positions were actually reachable under the available order book volume.

A simple example illustrates this. Suppose prices move as:

8 → 7 → 12 → 10

and the position limit is 2. If enough volume is available at every step, the optimal strategy is:

sell 2 → buy 4 → sell 4

for a total PnL of 16.

But if execution is capped at 2 units per step, the optimum changes:

buy 2 → buy 2 → sell 2

for a total PnL of 14.

This is exactly the kind of path dependency our DP was designed to handle.

The inputs to the algorithm were the predictor price series, an average spread estimate, and an estimate of executable volume as a fraction of the position limit. Because the predictive correlation was so high, generating trades directly from the predictor time series was sufficient. The DP then produced an action sequence for each product, using 'b' and 's' at each timestamp to indicate buys and sells.

Using this approach, we achieved an algo PnL of 2.1 million seashells—the highest of any team in that round. That performance lifted us to second place overall in the final standings.
```
# dynamic programming code block here
```
