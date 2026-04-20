**Note:** Out of respect for the moderators’ request, I will not share specific code or substantial spoilers while rounds are active. Instead, I will provide high-level descriptions of the assets until each round has concluded.

## Round 3: Notes

We do not yet know what the assets for Rounds 3, 4, and 5 will be, and at present we also do not have data for them. However, based on previous years, we can start forming some reasonable hypotheses.

## Commodities and external factors

From previous years, commodities were products Orchids or Diving gear.
Where orchids apparently was influenced by "sunlight index" and diving gear was influenced by DOLPHIN_SIGHTINGS, another data set provided by IMC. The latter may serve as a feature for predicting the price of DIVING_GEAR.

Our approach dynamically adapts to market conditions based on the "sunlight index" observation:

In normal sunlight regime: We execute two-way arbitrage, buying locally and selling abroad when local prices are lower than foreign prices (after accounting for fees), and vice versa.
In low sunlight regime: We switch to an accumulation strategy, aggressively building up long positions while avoiding exports, capitalizing on the favorable conditions for holding inventory.
The strategy also includes market making elements, placing competitive bids and asks to provide liquidity while skewing order sizes based on our current position to maintain balance.

We couldn't get a working macarons strategy by the end of this round, and we decided to disable trading volcanic rock until we could get a proper strategy. Luckily enough for us, we remained 2nd in the world, while almost every other team in the top 30 dropped.


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

Description
ORCHIDS are very delicate and their value is dependent on all sorts of observable factors like hours of sun light, humidity, shipping costs, in- & export tariffs and suitable storage space.

Strategy
We couldn't find strong connections between ORCHIDS and the various factors. So we didn't do directional bets or price prediction.

Initially, we considered market making due to the wide bid-ask spread of ORCHIDS, but found it impossible because bids lower than the fair price and asks higher than the fair price did not fill well.

Instead, ORCHIDS were also tradable on the exchange of the south archipelago. Therefore, we implemented arbitrage between the two exchanges. We placed orders that maximizes expected profit per trade (= (enter price on this island - exit price on the south archipelago - shipping cost - import tariff) * execution probability). We estimated the execution probability through our own experiment.




## ETF / basket arbitrage

From previous years we had PICNIC_BASKET, UKULELE, DIP, and BAGUETTE. We have been informed that one PICNIC_BASKET consists of one UKULELE, two BAGUETTEs, and four DIPs.
WE also had Gift baskets, chocolate, roses, and strawberries were introduced in Round 3. Each gift basket consisted of 4 chocolate bars, 6 strawberries, and 1 rose. Our main focus in this round was spread trading, where we defined the spread as:
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

Algo
Round 2 introduced new products: CROISSANTS, JAMS, DJEMBES, PICNIC_BASKET1, and PICNIC_BASKET2.
PICNIC_BASKET1 contained 6 Croissants, 3 Jams, and 1 Djembe.

PICNIC_BASKET2 contained 4 Croissants and 2 Jams.

We recognized the structure from previous years and analyzed the price difference between each basket and its components. The basket premiums appeared mean-reverting, so we hard-coded the mean from bottle data, used a short rolling window for standard deviation, and calculated rolling z-scores:

When z-score > 20, we shorted the basket and longed the constituents.

When z-score < -20, we did the opposite.

This hedging isolated and traded the basket premium directly.



We ran into a problem with this though. The position limits prevented fully hedging both baskets simultaneously. To fix this, we did a few things

We focused on the difference in basket premiums between Basket 1 and Basket 2.

Used the z-score (Basket1 premium - Basket2 premium) as entry and exits, using the same 20 and -20 scores for entry/exits, then hedging accordingly.

Using this strategy used the following of our position limits:

100% of Basket 1’s position limit,

60% of Basket 2’s limit.

We did z-score trading with the remaining 40% of position limit on Basket 2, but had to limit it to 32% because we couldn't perfectly hedge due to position limits on the constituents. The remaining 8% of Basket 2’s position limit was unused — so we deployed it by market making (taking advantage of ~7–10 seashell spreads).

Overall, this strategy allowed us to fully utilize 100% of allowed position limits while minimizing unhedged risk. Market making with the leftover 8% added ~5k seashells/day in backtests with very low volatility.

Chris also spotted suspicious trade quantity 15 patterns at highs/lows for Squid Ink and Croissants — hinting at potential price signals. However, it was too late to build a reliable strategy around them, so we planned to revisit this idea in Round 5.

Description
The GIFT_BASKET is now available as a tradable good. This lovely basket contains three things:

Four CHOCOLATE bars
Six STRAWBERRIES
A single ROSES
All four of the above products can now also be traded on the island exchange. Are the gift baskets a bit expensive for your taste?

Strategy
The price of GIFT_BASKET oscillated based on the underlying index, so we only traded GIFT_BASKET. We did not trade the underlying assets to reduce transaction costs. Although trading the underlying assets could have made the portfolio more stable despite some transaction costs, our goal was to maximize expected returns, so we chose not to do so.

We optimized the trading strategy by augmenting data using Monte Carlo simulation. This helps us avoid overfitting to past data.

When trading GIFT_BASKET, we placed market orders deep into the order book, accepting slippage to seize trading opportunities immediately.

Since our limit orders were rarely filled, we did not performed market making.


ound 2: ETF Statistical Arbitrage
Picnic Baskets
In Round 2, three new individual products — Croissants, Jams, and Djembes — were introduced alongside two new baskets: PICNIC_BASKET1 (6x Croissants, 3x Jams, 1x Djembes) and PICNIC_BASKET2 (4x Croissants, 2x Jams). Each basket represented a combination of different quantities of the three products, but crucially, it was not possible to directly convert baskets into their underlying constituents. This setup clearly simulated a basic ETF (Exchange-Traded Fund) structure: linked assets that normally move together, but which might temporarily deviate, creating statistical arbitrage opportunities. In quantitative trading, finding and exploiting such linkages — when the synthetic price of a basket diverges from the sum of its parts — is a classic technique.

A deeper look revealed two main spread opportunities: first, trading the spread between the two baskets adjusted by Djembes (ETF1 - 1.5*ETF2 - Djembes), and second, trading each basket relative to its synthetic value based on the underlying products (ETF - Constituents). While both avenues were possible, we quickly identified that comparing baskets directly to their constituent sums was the stronger and more reliable path.

Figure 4: Basket Spreads over Time
Basket spread plot
This plot shows the spreads (basket price minus synthetic value) for both Picnic Baskets over time, revealing short-term mean reversion patterns.
When approaching this kind of structure, it's crucial not to blindly apply textbook strategies but to first ask a fundamental question: How could the market data have been generated? The most natural generation process seemed to be that the three constituents' prices were independently randomized, and a mean-reverting noise sequence was then added on top to produce the basket price. If that's true — and our early testing supported it — then the baskets were mean-reverting relative to their synthetic value, while the constituents themselves were not responding to the baskets. Thus, it made sense to treat baskets as drifting toward their synthetic value, not the other way around. Furthermore, while "hedging" by taking opposite positions in constituents could reduce variance, it would actually lower expected value slightly, especially when accounting for spread costs.

This understanding had important implications for strategy design. Many teams might have rushed into using moving average crossovers or z-scores for trading signals — but applying such methods without a clear theoretical justification is dangerous. For instance, a moving average crossover only makes sense if you believe there is a short-term trend overlaying a longer-term mean, which was not suggested by the structure here. Similarly, using a z-score normalizes the spread by recent volatility, but unless volatility is known to vary meaningfully over time (which we did not observe here), this introduces unnecessary complexity and risk of overfitting. It's easy to fall into the trap of throwing fancy techniques at the problem after a few hours of backtesting — but if you can't explain why a strategy should work from first principles, then any "outperformance" in historical data is probably noise. From the beginning, we placed the highest value on building a deep structural understanding and keeping strategies simple, minimizing parameters whenever possible to maximize robustness.

Final Strategy
Based on that philosophy, our final strategy was built around a fixed threshold model. We entered long positions on the basket when the spread fell below a certain negative threshold, and short positions when it rose above a positive threshold. Instead of dynamically scaling signals or chasing moving averages, we relied on fixed levels tuned through light grid search, focusing on robustness rather than maximizing historical PnL. We further enhanced this base strategy by integrating an informed signal: having already detected Olivia's trading behavior on Croissants (similar to Ink Squid), we used her inferred long/short position to bias our basket spread thresholds dynamically. For example, if our base threshold was ±50, detecting Olivia as short would shift the long entry to -80 and the short entry to +20, dynamically tilting our bias in the favorable direction. This cross-product adjustment allowed us to intelligently exploit correlations between Croissants and the baskets without overcomplicating the system.

Figure 5: Optimal Parameter Search Grid
Optimal parameter grid search
These plots show the backtested basket PnLs across different parameter combinations. The left plot corresponds to Basket 1, and the right plot to Basket 2. num_param_1 represents the base threshold values, while num_param_2 controls the informed threshold adjustments based on Olivia's position.
During parameter selection, we always prioritized landscape stability over pure performance peaks. Rather than picking the best parameter set based on maximum backtested profit, we chose combinations that showed consistent, flat regions of good performance, reducing sensitivity to slight shifts and avoiding overfit disasters. Additionally, because we noticed that the basket prices carried a slight persistent premium (the mean of the spread was not zero), we subtracted an estimated running premium from the spread during live trading, continuously updating it to prevent bias.

Also, for the final round, we were uncertain whether or not to fully hedge our basket exposure with the constituents. Recognizing that any trading strategy can be viewed as a linear combination of two other strategies — in this case, fully hedged and fully unhedged — we decided to hedge 50% of our exposure as a balanced compromise. Additionally, we adjusted our execution logic: instead of waiting for spreads to fully revert and cross opposite thresholds, we neutralized positions immediately upon spreads crossing zero (adjusted for the informed signal). This change aimed to reduce variance and lock in profits more consistently, while maintaining approximately zero expected value under the assumption that spreads did not exhibit momentum when crossing zero. It is important to note that here, "zero" still referred to the base threshold after incorporating informed adjustments.

Anyone thinking carefully about the problem — starting from generation assumptions, doing proper exploratory data analysis, and resisting the temptation to blindly overfit — could have arrived at a similar approach. Concepts like synthetic replication, mean-reversion modeling (e.g., Ornstein-Uhlenbeck processes), and cross-product signal integration are core ideas in quantitative finance. With the dynamic informed adjustment based on Croissants, our strategy made about 40,000–60,000 SeaShells per round on baskets, plus another 20,000 SeaShells per round directly from trading Croissants individually.




# Location arbitrage
**Note**:
From previous years assets like Magnificent Macarons were implemented on multiple exchanges across islands, such that we could trade on multiple exchanges to to optimise for best value.
We do however know that no conversion will be needed this year, and can by that aspect assume it is less likely that Location Arbitrage will be used. Seeing as we are flying in space between planets, it is fair to guess it will be difficult to trade across planets.

From previous years.

Strategy: For Magnificent Macarons, we implemented a cross-market arbitrage strategy that considers trading with a foreign island through the conversion mechanism. The strategy analyzes the bid/ask spreads in both local and foreign markets, accounting for transportation fees, import/export tariffs, and other conversion costs to identify profitable arbitrage opportunities.

This round introduced a new product called Magnificent Macrons. Magnificent Macrons could be bought or sold on the local island and then converted on the Pristine Island (think buying BTC from one crypto exchange and selling it on another — same exact concept). However, when converting your position, you paid several fees: a transport cost, an export tariff (if converting a long position — like exporting from the main island), or an import tariff (if importing to the main island). On top of that, you paid a storage fee of 0.1 seashells per timestamp per Macron held, heavily encouraging players not to hold long positions.

While Macron prices were strongly correlated with sugarPrice and sunlightIndex, we decided to completely ignore these factors, since simply arbitraging across islands was far more profitable than trying to predict Macron price movements using a model.

Because import tariffs were negative, we were effectively paid to sell on the local island and convert on the Pristine Island. To calculate the break-even price for selling a Macron, we used the formula: 
sell local break even price
=
conversion ask
+
import tariff
+
transport fee

We also noticed there was a bot aggressively taking orders on the local island near the mid-price of the Pristine Island. We used this to our advantage by placing sell orders near the mid-price (if it was above our break-even price) and immediately converting them after they filled. We would pocket the difference between our sell price and the break-even price, multiplied by 10 (since we could convert 10 Macrons at a time).

In backtests, Chris estimated a potential profit of up to 100k seashells from Macrons over the course of the day, depending on how negative the import tariffs were. We were happy with that, submitted, and went to bed.

Macarons
In Round 4, Magnificent Macarons was introduced. Their fictional value was described as depending on external factors like hours of sunlight, sugar prices, shipping costs, tariffs, and storage capacity. Macarons could be traded on the local island exchange via a standard order book, or externally at fixed bid and ask prices, adjusted for im-/export and transportation fees. The position limit for Macarons was 75 units, with a conversion limit of 10 units per timestep. This setup opened up both straightforward arbitrage opportunities and, for those who studied the environment carefully, access to a much deeper hidden edge.

At first glance, the standard arbitrage logic applied: whenever the local bid exceeded the external ask (after fees), or the local ask was lower than the external bid, profitable conversions were possible. However, there was a critical hidden detail: a taker bot existed that aggressively filled orders offered at attractive prices relative to a hidden "fair value." Through experimentation, we discovered that offers priced at about int(externalBid + 0.5) would often get filled, even when no visible orderbook participants were present. This taker bot executed approximately 60% of eligible trades, meaning that — in expectation — you could sell locally for a price about 3 SeaShells higher than the naive local best bid. Over the course of 10,000 timesteps with a 10-unit conversion limit, this small price improvement could theoretically yield up to 300,000 SeaShells. Of course, those conditions were not always present and realistic optimal profits were around 160,000 and 130,000 SeaShells across the two rounds. Still, the magnitude of this hidden edge made Macarons a very lucrative product of the competition.

Figure 9a: Macarons Microstructure
Macarons microstructure plot
This plot shows approximately 60% of fills occurring at prices better than the local best bid. The orange indicator represents the external ask after costs (i.e., the conversion price for negative inventory). It also illustrates that straightforward local best bid to external ask arbitrage was not profitable during this period.
Figure 9b: Macarons Microstructure (Normalized)
Normalized Macarons microstructure plot
This plot shows the same data as Figure 9a, but normalized by the external ask after costs (orange indicator). It clearly demonstrates the achievable price improvement versus the local best bid: while the local best bid was about -1 SeaShell unprofitable in this snippet, fills often occurred at +2 SeaShell profitable levels.
Machine Learning Approach
Last year, there was a similar round involving a sunlight and humidity index. As far as we know, nobody was able to extract any useful information from these indices, and they were largely considered a false lead. This year, we expected the same outcome, but we still felt it was worth checking, just in case there was something hidden there (especially since an admin in the Discord channel had hinted at it). Our model was a logistic regression, with a target of a trade being profitable in x timestamps.

Features:
Feature	Coefficient	P-value	Explanation
sunlight_diff	-2.0517	0.0000	Change in sunlight over the last 5 timestamps
sunlight_critical	0.4737	0.0000	Binary, if sunlight is below a threshold, set to 45
sunlight_critical_time	-0.0014	0.0096	Binary, if sunlight has been critical for more than 30 timestamps
sunlight_diff_critical	-0.0020	0.0000	Change in sunlight if sunlight has been critical as defined in sunlight_critical_time
sunlight_critical_time_2	0.0001	0.0020	sunlight_critical_time^1.3
All variables produced highly significant p-values and plausible coefficients. These are only a subset of the tested features, and had we employed this strategy, the features would have faced greater scrutiny. We also tested having a lagged price as a feature, which introduced trading small spikes and mean reversion to our model, but decided against it as this was highly volatile.

We then do the following based on the ouput of the logisitc regession y:

If ( y = 0 ): Sell
If ( y = 1 ): Buy
If ( y ) is between 0.49 and 0.51: Hold
The thresholds of 0.49 and 0.51 were set through testing.

Figure 10: Logistic Regression Trades
Logistic Regression Trades
This approach generated solid historic returns of ~25k per day. However, this approach had multiple issues:

Although we employed train-test splits, we lacked confidence in the generalization of the model.
Implementation challenges arose, particularly as longer lags required storing more past data, which significantly slowed down the trader. The serialization of trading data took considerable time, and correctly implementing the logistic regression model introduced numerous potential sources of error.
Compatibility with export/import arbitrage posed a problem. Since positions can only be converted by reducing them, when the model indicates a long position and we wish to import, we first need to sell our entire inventory plus 10 units.
Final Strategy
Our final strategy focused on reliably exploiting this hidden arbitrage. Each timestep, we placed limit sell orders for Macarons at precisely int(externalBid + 0.5), the maximum price that could still trigger fills from the taker bot. We quoted only 10 units per timestep (the conversion limit), which meant we captured approximately 60% of the theoretical maximum profits, in line with the taker's acceptance probability. In hindsight, quoting larger sizes (e.g., 20–30 units) would have allowed us to profitably convert surplus inventory even on non-fills, squeezing out closer to full optimal performance. Nevertheless, even with conservative sizing, this strategy provided consistent, high-value returns with minimal risk.

Teams who prepared carefully had a clear advantage this round. Similar hidden taker behavior had already appeared in Orchids during Prosperity 2, and public write-ups from top teams like Jasper and Linear Utility had discussed included it already. Additionally, even without past experience, attentive teams could have detected the pattern by analyzing historical data: best asks occasionally priced close to best bid consistently getting filled was a clear signal. Moreover, similar smart-taker behavior had appeared in assets like Rainforest Resin, providing further hints. Thus, strong preparation, deep intuition about the Prosperity simulation, and diligent empirical observation were all key factors in unlocking the full potential of Macarons. Although, we only made about 80,000 - 100,000 instead of theoretical optimum of 130,000 and 160,000 those who recognized and optimally exploited the hidden taker bot captured some of the highest single-product profits available in the entire competition.




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


Algo
This round introduced six new products: Volcanic Rocks and five different Volcanic Rock vouchers with strike prices of 9500, 9750, 10000, 10250, and 10500. These products closely resembled European option contracts and were set to expire in 7 in-game trading days.

Chris handled the analysis for this round. Using a hint provided on the website, he modeled the volatility smile by plotting the moneyness 
m
t
 against the implied volatility 
v
t
. Moneyness was calculated using the formula: 
m
t
=
l
o
g
(
K
/
S
t
)
/
(
T
T
E
)
 where 
K
 is the voucher strike price, 
S
t
 is the price of the underlying at some time 
t
, and 
T
T
E
 being the time to expiration in years.



Fitting a quadtratic to this we found parameters 
a
,
b
,
c
 for the equation 
v
t
=
a
⋅
m
t
2
+
b
⋅
m
t
+
c
 allowed us to predict a "fair" implied volatility for any given 
m
t
. After coding this up, we found the best way to exploit this was to build a market maker based on the fitted implied volatility. It was an extremely aggressive market maker and would often cross with existing market makers in the order book. We also added functionality to automatically hedge our positions after every timestamp, ensuring we were only exposed to the implied volatility of a contract.

Our backtesting PNL curve was a straight line on most days, indicating we had found a reasonable direction-neutral strategy with true edge. We hypothesized that this was because we were modeling the true IV of the vouchers more accurately. From our backtests, we expected to make around ~80k from all voucher products and ~100k from other products.

A few other things we considered for algo trading this round:

We analyzed how much we were losing in long voucher positions due to theta decay. Chris found that the vouchers had a maximum annualized theta decay of 800 seashells, meaning that holding a voucher for a year — assuming no changes to the underlying or voucher structure — would result in an 800 seashell loss. He estimated that if we were fully long 200 vouchers, the daily loss due to theta would be approximately 430 seashells: 
800
 
seashells per year
365
 
days per year
×
1
 
day
×
200
 
vouchers
≈
430
 
seashells per day
 This loss was negligible compared to the 80k we were making in backtests.

Since we could hold up to 400 Volcanic Rocks and 200 of any voucher, if we went long two different vouchers, we could at best fully hedge two of them assuming each had a delta of 1. To keep things manageable and avoid messy edge cases, we capped all voucher positions at 80. This guaranteed that we could always fully hedge, greatly simplifying our delta hedging logic and making the delta-neutral strategy easy to implement. There was probably a better way to optimize this, but given the time constraints of the challenge, we felt this was a favorable trade-off.


Options
In Round 3, the competition introduced a new class of assets: Volcanic Rock Vouchers — effectively call options on a new underlying product, Volcanic Rock (VR). There were five vouchers available, each with a distinct strike price — 9500, 9750, 10000, 10250, and 10500 — while the underlying Volcanic Rock itself traded around 10,000. Each voucher granted the right (but not the obligation) to buy Volcanic Rock at the specified strike at expiry. Importantly, options had limited time to live: starting with seven days until expiry in the first round, decreasing to just two days by the final round. Without basic familiarity with options theory, particularly concepts like implied volatility and option pricing models, it would have been difficult to design strong strategies for this product.

IV Scalping
Our first major insight came from following hints dropped in the competition wiki, suggesting the construction of a volatility smile: plotting implied volatility (IV) against moneyness. By fitting a parabola to the observed IVs across strikes and then detrending (subtracting the fitted curve from observed values), we could isolate IV deviations that were no longer dependent on moneyness.

Figure 6a: Volatility Smile
Volatility smile scatter plot
This scatter plot visualizes implied volatility (vt) versus moneyness (mt) across different strikes. A fitted parabola is shown to filter out noise, producing v̂t — the "fair" implied volatility given mt. Outliers at the bottom left were disregarded, as they corresponded to historical points where extrinsic value was too low.
Figure 6b: IV Deviations over Time
IV deviations plot
This plot shows the time series of implied volatility deviations (vt - v̂t) derived from Figure 6a, highlighting short-term patterns in relative option mispricing.
To convert these into actionable trading signals, we input the volatility-smile-implied IV into a Black-Scholes model to calculate a theoretical fair price, then compared it to the actual market price to find price deviations. Plots of these price deviations — especially for the 10,000 strike call early on — revealed sharp short-term fluctuations, indicating scalping opportunities.

Figure 6c: Price Deviations over Time
Price deviations plot
This plot shows the same implied volatility deviations from Figure 6b, but transformed into price space using the Black-Scholes model, providing a more intuitive view of relative mispricings over time.
We initially focused on the 10,000 strike, but dynamically expanded to include other strikes as the underlying shifted and expiry approached, tracking profitability thresholds in real time to decide when to activate scalping on new options. Statistical analysis, specifically testing for 1-lag negative autocorrelation in returns, strongly supported the existence of exploitable short-term inefficiencies across several strikes, further validating this approach.

Figure 7a: 10k Call Price Fluctuations
10k call price fluctuations
This plot shows short-term price fluctuations of the 10,000 strike call option. The orange indicator represents the theoretical call price, calculated using the implied volatility from the fitted parabola (v̂t) at the option’s current moneyness.
Figure 7b: 10k Call Price Fluctuations (Normalized)
Normalized 10k call price fluctuations
This plot shows the same 10,000 strike call fluctuations as in Figure 7a, but with prices normalized by the theoretical value (orange indicator) to make deviations more stationary and visually clear.
Gamma Scalping
The expected value from gamma scalping was consistently positive, as the gains from underlying price movements outweighed the losses from time decay. This made buying options and rehedging the resulting deltas from gamma exposure a relatively low-risk way to generate profit. However, while the approach was stable and mostly safe, the absolute returns were limited. It was a reliable source of small gains, but ultimately, we had a higher risk appetite and wanted better returns.

Mean Reversion Trading
Simultaneously, analysis of the underlying Volcanic Rock asset suggested potential mean reversion behavior. Return distributions and price dynamics resembled Squid Ink, which was explicitly designed to mean revert in Round 1. Autocorrelation analysis of Volcanic Rock returns, compared against randomized normal samples, confirmed significant short-term negative autocorrelation at various horizons, although caution was needed given the presence of large jumps and non-normal return distributions. Given the limited historical data available (only three days), and uncertainty about future dynamics, fully committing to mean reversion was considered too risky. Instead, we implemented a lightweight mean reversion model: tracking a fast rolling Exponential Moving Average (EMA) and trading deviations from this EMA using fixed thresholds — without scaling by rolling volatility — to keep the model simple and robust.

Figure 8: Autocorrelation Plot for Volcanic Rock
Autocorrelation plot for Volcanic Rock
Rolling autocorrelation of Volcanic Rock returns compared to autocorrelations from purely random sequences, suggesting statistically significant mean reversion behavior in the underlying.
Final Strategy
In the end, we deployed a hybrid strategy combining both alpha sources. Our core focus remained on IV scalping, dynamically expanding across strikes and adjusting thresholds based on evolving conditions, while simultaneously maintaining a moderate mean reversion position — both in the underlying Volcanic Rock and in the deepest in-the-money call (the highest delta option available). Importantly, this was not a delta hedge in the traditional sense: the delta exposure from scalping was relatively small, and explicit delta hedging would have been prohibitively expensive bid-ask spreads. It was rather a hedge against bad luck. Because this hybrid model was designed to minimize maximum regret across different possible market outcomes: it protected us if strong mean reversion materialized (even if other teams aggressively leveraged mean reversion delta exposure across multiple options and therefore outperforming us in a relative sense), while keeping our core reliance on the more stable, theory-supported scalping opportunities.

Someone could have arrived at a similar strategy without deep prior options expertise by carefully observing the market dynamics. Even without constructing a full volatility smile, simply watching option prices — particularly the 10,000 strike — would reveal clear short-term mean-reversion patterns and negative autocorrelation in returns. On the underlying asset side, basic return autocorrelation analysis and exploratory plotting would hint at mean reversion tendencies. Thus, while a strong theoretical background was helpful, a combination of attentive observation, critical data analysis, and statistical common sense would have led to very similar conclusions.

In terms of results, IV scalping contributed approximately 100,000 - 150,000 SeaShells per round, providing strong and stable profits across all rounds. Mean reversion trading was much more volatile, delivering around 100,000, -50,000, and -10,000 SeaShells across the rounds respectively. Despite the swings, our hybrid approach allowed us to achieve consistently positive net results while keeping downside risks manageable.

Note: After the fourth round, where the mean reversion strategy resulted in a loss of approximately 50,000 SeaShells, we reassessed its validity. Although we no longer found strong empirical evidence to justify continuing with mean reversion purely on standalone expected value grounds, we knew that several top teams were actively only trading mean reversion strategies. So we figured, if they wouldn't find the IV scalping strategy, they might just accept the coinflip and go all in mean reversion because otherwise they would surely get overtaken by everyone. Facing a 200,000 SeaShell lead at that point, we made a calculated decision to maintain some mean reversion exposure — not because we believed it was necessarily positive EV anymore, but to hedge relatively against the teams still pursuing that angle. We estimated the 95% Value at Risk (VaR) of the mean reversion component to be around 50,000 SeaShells — only about 25% of our lead — leaving us with sufficient margin even if the strategy failed again. Under our assumptions, keeping this balanced exposure maximized our likelihood of securing first place by minimizing relative downside risk while preserving our core scalping profits. This turned out to be the right decision. Although, in the last round some random team very unnaturally jumped from 100+ rank to 1st place, we could keep a healthy distance to all teams that were previously close behind us.


Products: Volcanic rock, volcanic rock vouchers

Strategy: For Volcanic Rock and its vouchers, we implemented an options pricing strategy using the Black-Scholes model. We treated vouchers as call options on Volcanic Rock with various strike prices. The strategy calculates implied volatility from market prices, maintains a rolling volatility window, and prices vouchers based on this volatility estimate. We also look for arbitrage opportunities between vouchers with different strike prices, exploiting situations where the price spread between vouchers deviates from their strike price differences.

For Volcanic Rock itself, we implemented a strategy that uses the average implied volatility from all vouchers to determine if the underlying rock is fairly priced. When the rock price significantly deviates from our model's prediction, we take directional positions.

Due to an unexpected bug in our code, we ended up shorting volcanic rock at the max position limit for the entire duration of the trading day. Fortunately for us, this strategy ended up working, bringing our ranking to 2nd in the world!




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


## Insider / competitor

Algo
This round no new products were introduced. Instead, we were told the counterparties that we were trading agaisnt. Specifically, there were 11 other bots trading the same products we were. We started by visualizing all trading activity for all the bots, and plotted products prices and overlayed a scatter plot with the prices bots would trade at. We did this for all bots and all products, and quickly found that one bot, 'Olivia', would buy/sell and the low/high of the day every day on 3 different products.


Chris had correctly guessed that the trades present in round 2 data did indeed have a true signal. Using this information, we planned to update our algorithms to copy Olivia's trades.

After running some quick tests, we found that we were making more just market making and taking on kelp than using Olivia's signal, so we left our Kelp trading alone.

For Squid Ink, we decided to market make and take with maximum position sizing until Olivia's signal, and then just follow it for the rest of the day.

Croissants was slightly more complicated because we were using it as a hedge in our basket trades. Because we had a true signal on croissants, Chris reasoned that we shouldn't take trades on baskets in the opposite direction of Olivia's signal, as the price of Croissants accounted for ~50% of the price of the baskets.

Building off this, we decided to YOLO into Croissants. Our maximum position size for Croissants was 250, but if we went long on both baskets, we could effectively be long 1050 Croissants. We estimated that on a bad trading day for this signal, the difference between the high and low on Croissants is 40 seashells, so a lower bound on our croissants PNL was 40x our position size. Going long an extra 800 Croissants on this bad day will give us an extra 32k Seashells.

Our statistical basket arbitrage was hitting 50k on it's best days, while YOLOing croissaints on Olivia's signal was getting up to 120k on its best day (difference of about ~120 between the high and low). We decided this was the best idea. Convenient that it was also very simple to implement.

We hedged the baskets by going opposite on Jams and Djembes, as the movement of the basket was still about 50% correlated with these products. Our final position ended up being exposed to 30 Jams due to position limits. By taking on the extra 30 jams, we were able to go long another 60 croissants. We found that Jams would move on average 50 on their most volatile day, so the upside of the 60 Croissants was higher than the potential downside on Jams leading us to believe that this was a risk worth taking.

We also realized we were exposed to the premium of the basket, and that in a near worst-case scenario, we could lose up to 300 seashells per basket we were holding if we bought at the top of premium then sold at the bottom or vice versa, meaning a total potential loss of up to 45,000 seashells due to premium movement against us while in our trade. We could not think of a way to reduce this risk.

Chris found that with 90% confidence the difference in basket 2 premiums from one timestep to the next was stationary, and with 95% confidence for basket 1, so we reasoned that it's a coinflip that premium will move agaisnt us, and the probability of us buying right as the series is mean reverting is incredibly low (assuming Olivia's signal is not correlated with the top/bottom of premiums, something that in hindsight we should have tested for). Because of this, we reasoned that our potential loss is most likely not 45,000 and more realistically 20,000 at most, and that in expectation our loss is 0. Based on this line of reasoning, we ultimately decided that this risk was worth taking.

One final optimization Chris made was that while waiting for Olivia's signal, we would market make and take on both picnic baskets since they both had large spreads. This made us up to an extra 10k seashells per day depending on how long we had to wait before Olivia's signal.

Round 5: Trader IDs
In Round 5, no new products were introduced. The main change was that historical trader IDs were made public, allowing teams to directly identify which trades were executed by specific bots. For us, this did not fundamentally alter our strategies, as we had already identified Olivia’s behavior early in the competition. However, we took this opportunity to update our detection logic: instead of inferring Olivia’s trades indirectly by tracking running minimums and maximums, we now simply checked the trader ID directly. This adjustment helped eliminate false positives, reduced the risk of missing genuine Olivia trades, and saved a few hundred SeaShells over the course of the round. As with every previous round, we also re-optimized all relevant parameters based on the latest available data to ensure robustness going into the final evaluation. This was the last round, and we had a sizeable lead to place 2 (~190k), so we decided to play it save, incase ETF spreads don't converge, by half-hedging the baskets. We also limited our mean reversion strategy to minimze risk.

New Change: Counterparties are revealed

Strategy: When counterparties were revealed, we suspected there might be an insider trader with an information advantage in the marketplace. To systematically identify this trader, we implemented a data-driven approach. We calculated the percentage of "good trades" (buying at low prices and selling at high prices relative to future price movements) for each trader over rolling windows. By filtering traders who consistently executed advantageous trades at a rate significantly above chance, we were able to narrow down potential insiders. We then visualized these traders' buy and sell orders relative to the mid-price of each asset and observed that a trader named "Olivia" was suspiciously precise in her timing—buying just before price increases and selling just before price drops across multiple products. This confirmed our hypothesis that she was indeed an insider with advance knowledge of price movements.

With counterparties revealed, we implemented a copy trading strategy specifically for Squid Ink and Croissants by tracking trades made by "Olivia". When Olivia bought one of these products, we interpreted this as a bullish signal and also bought; when she sold, we took this as a bearish signal and sold alongside her. This approach helped us establish market regimes (bullish or bearish) based on insider behavior.

We did not actively trade Jams or Djembes in this round, focusing instead on the copy trading strategy for Croissants and Squid Ink, where we could leverage Olivia's insider information.

For the Magnificent Macarons, we made a quick fix to our regime modeling strategy by ignoring the sunlight index completely. Instead, we focused solely on statistical arbitrage throughout the entire trading day, as we weren't confident whether our sunlight threshold was overfit to previous data or not.

For other products, we maintained our existing strategies:

Market making for Kelp and Rainforest Resin
Statistical arbitrage for Picnic Baskets
Black-Scholes model for Volcanic Rock Vouchers
We also implemented a position management system that scales order sizes based on current inventory to avoid overexposure, and added features to close positions for inactive products to reduce risk.

Unfortunately our luck ran dry, and we were not able to make up the ground from the previous two rounds, and ended up being surpassed by a few teams. We ended at 9th in the world and 2nd in the USA, behind CMU Physics. Overall, we're very thankful to have had the opportunity to compete in this competition, and we are pleased with the results for this being many of our first times competing in a trading competition.

## Pair trading

Unfortunately, both me and Konstantin were travelling/very busy during the next couple of rounds, so it was a bit harder to try things in Rounds 2-4. For the Coconuts/Pina Coladas, Konstantin wrote up code to perform pair-trading (arbitraging pina colada - 15/8 * coconut); something else we tried was momentum-based trading, but this didn't give a PnL as high as pair-trading, so we mostly submitted the first code we came up with.



Throughout the competition, we experimented with several approaches that ultimately didn't make it into our final strategy:

Basket Mean-Reversion Modeling: We attempted to model the spread between picnic baskets and their synthetic prices (based on component values) for mean-reversion trading. While theoretically sound, this approach faced implementation challenges and didn't yield consistent results.

Volatility Surface Fitting: For volcanic rock vouchers, we tried fitting a volatility surface (smile) to the implied volatility versus moneyness from the call options. This would have given us a more sophisticated options pricing model, but it proved too complex to implement reliably given the competition's time constraints.

Delta Hedging: We attempted to implement delta hedging with volcanic rock positions to create market-neutral strategies, but struggled with proper calibration and execution within the position limits.

Component-Basket Arbitrage: While we developed code for direct arbitrage between picnic baskets and their component products (Croissants, Jams, Djembes), we never successfully traded the components due to implementation bugs and position limit challenges.

Price Pattern Analysis: We spent considerable time modeling the price movements of virtually every product (squid ink, croissants, jams, djembes, volcanic rock, macarons, etc.) to find correlations, seasonality, or other patterns in the data. Despite extensive analysis, many of these efforts didn't yield actionable strategies.

Insider Signal Integration: After identifying Olivia as an insider trader, we attempted to use her directional hints as a regime indicator to adjust our bids/asks dynamically, rather than just copying her trades. This proved more complicated than direct copy trading and didn't provide sufficiently reliable signals to justify the added complexity.


Round 1️⃣
Round 1 introduced the first three products: Rainforest Resin, Kelp, and Squid Ink. Resin remained stable around a known historical price. Kelp moved up and down without a clear trend, while Squid Ink was highly volatile.

🌳 Rainforest Resin
We treated Resin as a static-value product centred at 10,000. The strategy combined tight market making with controlled position management. We placed passive bids and asks slightly inside inefficient book levels, while selectively taking favourable quotes when prices deviated from the fair value to capture mispricing. We used additional passive orders outside the spread to gently rebalance positions to minimise exposure.

🪸 Kelp
Kelp required a more adaptive strategy. We first plotted volume frequency distributions to identify the most reliable quoted sizes on each side of the book. These filtered quotes were then used to compute a more platform-aligned fair price. Around this price, we deployed a mix of passive market making and aggressive liquidity-taking if spreads widened. We also used conservative passive orders to manage position buildup.

🦑 Squid Ink
For Squid Ink, we implemented a directional signal based on top-of-book pressure. We computed a running pressure score by analysing changes in the best bid and ask levels and their volumes. Based on the signal (buy/sell/hold), we placed limit orders with self-adjusting price offsets that adapted based on recent fill volumes.

Round 2️⃣
This round introduced two composite products — Picnic Basket 1 and Picnic Basket 2 — which bundled together Croissants, Jams, and Djembes in fixed proportions. These components were also made individually tradable.

🦑 Squid Ink
We had to rework our strategy after a negative P&L in Round 1, focusing on better signal generation and execution logic. We transitioned from a heuristic pressure-based strategy to a logistic regression model trained during runtime. The model used a 7-feature vector — including Z-score, price momentum, order book imbalance, MACD, and pressure signals — to generate probabilistic buy/sell decisions. Orders were sized and priced based on signal confidence, and the model was retrained every 50 timestamps using recent price history.

🍓 Jams
Jams exhibited mean-reverting behaviour with frequent short-term overextensions. We implemented a simple statistical strategy using the Z-score of mid-prices over a rolling window, with trend confirmation based on recent averages. Long positions were entered when Z-scores dropped sharply in an uptrend, while short positions were taken in overbought conditions with negative momentum. Position sizing was adjusted based on current exposure to control risk.

🥐 Croissants & 🪘 Djembes
We chose not to trade Croissants or Djembes individually. Both products were highly volatile, making them unreliable and poor candidates for market making or directional execution.

🧺 Picnic Basket 1
We ran a directional index arbitrage strategy on Basket 1 by computing its synthetic value in real time using the mid-prices of its components: Synthetic Price = 6 × Croissants + 3 × Jams + 1 × Djembe

We compared this synthetic price to the quoted market price of Basket 1. If the spread between them exceeded a pre-defined threshold, we placed directional trades on the basket — buying when undervalued and selling when overvalued. We deliberately avoided executing on the individual legs to reduce slippage and latency risks.

🧺 Picnic Basket 2
We initially applied the same arbitrage logic to Basket 2, using a synthetic price computed as: Synthetic Price = 4 × Croissants + 2 × Jams

However, this model showed high drawdowns in backtests due to inconsistent pricing and unstable correlation between Basket 2 and its components. The smaller size of the basket and tighter spreads amplified noise, and execution risk was significantly higher. Given these challenges and limited time to tune the model further, we dropped trading Basket 2 in this round.

Round 3️⃣
In Round 3, a new product — Volcanic Rock — was introduced, along with five associated Volcanic Rock Vouchers, each acting as a European-style call option with an expiration of 7 in-game days.

🦑 Squid Ink
Squid Ink again gave a negative P&L, and we decided to come up with an altogether different strategy. This mean reverting strategy using z-score based signals. When the current price deviated significantly from the EMA, we entered trades in the direction of expected mean reversion, limiting our position to 6 for limited exposure to the market.

🧺 Picnic Basket 1 & 2
We made some minor changes in the last round strategy by using volume-weighted mids for better estimation of mid prices, and also tuned the thresholds for better performance.

🪨 Volcanic Rock
We ran a dynamic market-making strategy that adjusted quoting aggressiveness based on both position and recent execution pressure. Spread placement and size were adjusted using a position-sensitive logic, quoting tighter when flat and backing off when near limits.

🎟️ Volcanic Rock Vouchers
We selected two vouchers (10250 and 10000 strike) for active trading based on their moneyness and relative liquidity. For each, we computed a theoretical value using the Black-Scholes model, taking into account:

Current Volcanic Rock mid-price (spot),
Strike price,
Time to expiry (adjusted daily),
Estimated volatility (inferred from Rock’s price history).
We then back-calculated the implied volatility from the voucher’s market price and compared it against a rolling average of historical implied vols. If the deviation exceeded a threshold, we traded directionally — buying underpriced volatility and selling overpriced premium.

Round 4️⃣
The luxury product Magnificent Macarons was introduced. Macarons could only be traded via conversion requests through Pristine Cuisine, subject to transport fees, tariffs, and a per-timestamp storage cost on long positions. The product's pricing was influenced by multiple external signals like sunlight, sugar price, and tariffs.

🦑 Squid Ink
Despite multiple rounds of tuning and complete rewrites of the logic, Squid Ink continued to underperform, once again closing the round with negative P&L. After significant sunk time across three rounds, we decided not to trade the product and allocate our engineering effort to other products.

🧺 Picnic Basket 1
We made targeted improvements to our Basket 1 strategy this round. After analysing noise in our spread signals, we made three key changes:

Instead of using the raw synthetic price, we applied an EMA to smooth it and reduce short-term noise.
We added an exit threshold to our Z-score logic, allowing us to gradually exit when the spread converged to the mean, rather than waiting for a full reversal.
We improved order placement by splitting orders across multiple price levels. Analysis showed that baskets often got filled near the optimal level, so we placed layered orders with varying sizes based on confidence in fill probability.
These changes led to more stable performance and improved fill consistency.

🧺 Picnic Basket 2
We extended the same improvements to Basket 2. EMA smoothing, Z-score thresholds (entry + exit), and layered fills were applied similarly. The thresholds were tuned using our own backtester and some other optimisations.

(We plan to release cleaned-up versions of our Jupyter notebooks used in tuning once we have time to format and comment them.)

🪨 Volcanic Rock & 🎟️ Vouchers
After Round 3, we did a deeper analysis on Rock and the 9500 and 9750 vouchers, which we hadn’t actively traded before.

We confirmed that Volcanic Rock exhibited mean-reverting behaviour, so we implemented a Z-score-based mean reversion strategy with conservative sizing and exit logic.
For 9500 and 9750 vouchers, thanks to the hint released about the volatility smile, we realised that they were (and would remain) deeply ITM and strongly co-moved with Rock. We applied the same mean-reverting model used for Rock, with threshold tuning to adjust for the different option premiums.
10000 voucher remained ATM, so we continued with the implied volatility Z-score arbitrage strategy from Round 3.
10250 voucher had moved slightly OTM, but we anticipated it would hover around the ATM region. So we reused the 10000 strategy, betting on premium fluctuations and short-term mispricings.
This combined approach allowed us to trade both volatility and direction depending on each voucher’s moneyness and market structure.

🍬 Magnificent Macarons
We explored several strategies for Macarons, including regression-based fair value estimation using external inputs (sunlight and sugar prices). However, due to:

Complex and unstable input dependencies,
Strict conversion limits (10 units),
Continuous storage cost on long positions,
We could not design a strategy we trusted under simulation.
With end-semester exams approaching for all of us, we chose to skip trading Macarons and focus on improving proven models instead.

Round 5️⃣
No new products were introduced in the final round, but a key feature was unlocked: the exchange began exposing the counterparty identity for each executed trade. This enabled detailed adversarial analysis and reactive strategies based on flow from known participants.

By this point, we were ranked 15 globally, so our goal was to preserve our standing by avoiding any negative P&L, especially from Squid Ink and Macarons, which we had previously skipped. With limited time and increasing risk, we shifted our focus toward signal-driven trading, prioritising safe and high-confidence setups.

🎟️ Volcanic Rock Vouchers
We refined our voucher selection based on updated volatility analysis:

10250 voucher showed persistent signs of staying deeply OTM, so we fully removed it from our portfolio.
10000 voucher appeared to be drifting towards OTM as well, but our analysis suggested a high-confidence profit window of 15–20k Seashells as it approached the ATM region. We kept it active using the same IV-based Z-score strategy from earlier rounds.
For 9500 and 9750, we continued using the mean-reversion strategy synced with the Volcanic Rock movement.
🍬 Magnificent Macarons
We chose to include a very conservative arbitrage strategy in this round. We only executed a single-leg conversion strategy:

When the local market bid exceeded Pristine Cuisine's adjusted ask (including transport + import fees), we sold Macarons locally and converted them from Pristine Cuisine.
This trade had zero directional exposure and was triggered only when the arbitrage edge was obvious.
We disabled the reverse leg (buy local, sell to Pristine) due to high export tariffs, which rarely made the flow profitable. This strategy acted as a safe, low-frequency alpha component that aligned with our risk-averse approach in this round.

🧠 Signal-Based Trading (Using Bot Names)
After implementing our core voucher and Macaron changes, we shifted focus to exploring the newly introduced bot identities. We performed an exhaustive analysis of all bots, plotting the trades each bot made across different products and analysing bot-pair interactions to identify patterns in flow and reaction.

Shoutout to Aniruddhh and Shresth for leading this research, helping us uncover that Olivia’s trades showed strong, consistent short-term predictiveness, especially on:

Squid Ink
Croissants
Kelp
The signal was clear, and much like in Prosperity 2, we realised that many teams likely picked up on it. To gain an edge, we knew that execution quality had to be the differentiator.

We initially spent time experimenting with dynamic level selection using fill probability modelling. While that approach didn’t improve profits much, it helped us discover that many assets consistently filled at multiple levels near the top of the book.

So, when a signal was detected from Olivia’s trade:

We went all-in on the predicted direction, placing layered limit orders across multiple levels instead of just hitting the best bid/ask.
We distributed volume across levels proportional to confidence and historical fill behaviour.
This aggressive and breadth-aware execution strategy significantly boosted our realised profits, turning a widely known signal into a differentiated alpha source through tactical precision.
