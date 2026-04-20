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
