**Note:** Out of respect for the moderators’ request, I will not share specific code or substantial spoilers while rounds are active. Instead, I will provide high-level descriptions of the assets until each round has concluded.

## Round 3: Notes

We do not yet know what the assets for Rounds 3, 4, and 5 will be, and at present we also do not have data for them. However, based on previous years, we can start forming some reasonable hypotheses.

## Commodities and external factors

From previous years, commodity-style products included Orchids and Diving Gear. Orchids appeared to be linked to a sunlight index, while Diving Gear was influenced by DOLPHIN_SIGHTINGS, another external dataset provided by IMC. In principle, these observations suggested that external variables might be useful predictive features.

For Orchids, our first line of inquiry was therefore a feature-driven directional strategy. We tested whether variables such as sunlight, humidity, tariffs, and shipping costs could be used to predict future Orchid prices. This included simple correlations, lagged and contemporaneous regressions, and various rounds of feature engineering. Although some early patterns looked promising, none of them proved robust enough to support a reliable predictive trading strategy. As a result, we decided against running directional bets based on these environmental observations.

Instead, our implemented strategy focused on cross-exchange arbitrage. Orchids could be traded both on our local island and through the South Archipelago exchange, with the foreign market quote translating into an implied local fair value after adjusting for transport fees and import/export tariffs. In practice, this made Orchids less of a forecasting problem and more of an execution and market-structure problem.

The key discovery was that the local Orchid market contained a large persistent buyer of local sell orders. Through experimentation, we found that sell orders placed slightly above the best local bid were often filled immediately and in full size. This created a profitable arbitrage loop: we could sell locally at an advantageous price while simultaneously sourcing inventory through the South Archipelago at a lower implied cost. Once we identified this behaviour, our Orchid strategy became primarily an exercise in maximizing the value of that arbitrage.

The strategy itself had three layers.

First, we implemented pure arbitrage taking. At every step, we computed the implied foreign bid and ask after accounting for shipping costs and tariffs. If the local market offered prices sufficiently better than those implied foreign levels, we immediately traded against them. This allowed us to capture direct mispricings whenever they appeared.

Second, we added an arbitrage market-making layer. Rather than only taking obvious opportunities, we also posted local quotes designed to earn spread while still remaining profitable after conversion. In practice, this meant placing bids and asks only when the quoted level still implied positive expected value relative to the South Archipelago. Since execution was uncertain, profitability depended not only on raw edge, but also on the probability of being filled. So the effective objective became maximizing:

expected profit per trade = edge × execution probability

where the edge was defined net of local execution price, foreign unwind price, shipping, and tariffs.

Third, we built an adaptive quoting mechanism. A fixed quote level worked well in backtests—particularly selling around foreign ask minus 2—but we were concerned that such a rule might stop filling when market conditions changed. To address this, we monitored realized fill volume over time and adjusted the quoted edge dynamically. If average fills dropped below a threshold, the algorithm would search for a more competitive level, sacrificing a small amount of edge in exchange for better execution. This made the strategy more robust than a single hard-coded quote.

We also considered whether environmental conditions such as sunlight could justify a regime-based inventory strategy, for example switching between two-way arbitrage in normal conditions and outright accumulation in low-sunlight regimes. Conceptually, this would have allowed us to combine arbitrage with selective inventory holding. However, because we never found sufficiently strong predictive power in the external factors, our final live approach remained centered on arbitrage and execution rather than on directional inventory bets.

In summary, our Orchid trading was driven by market structure rather than prediction. We did not find reliable alpha in sunlight, humidity, or the other observable variables, so we avoided forecasting-based trades. Instead, we implemented a strategy built around:

cross-exchange arbitrage between the local market and the South Archipelago,
selective taking of clear mispricings,
passive quoting when expected value remained positive after conversion costs,
and adaptive edge adjustment based on realized execution.

This was ultimately the core of our Round 2 implementation. The approach worked well, but once the same arbitrage became widely known, competition compressed the edge and rankings became highly sensitive to execution quality and small implementation differences.

### ORCHIDS Strategy

ORCHIDS came with a rich set of observable external variables—sunlight, humidity, shipping costs, and tariffs—which initially suggested the possibility of a predictive strategy. We explored this route through correlations, regressions, and feature engineering, but failed to uncover a sufficiently robust signal. As a result, we did not trade ORCHIDS directionally.

Our implemented strategy instead focused on cross-exchange arbitrage. Because ORCHIDS could also be traded through the South Archipelago, we used foreign quotes plus tariffs and transport costs to compute implied fair values on our island. We then traded whenever local prices deviated enough from those implied values to create positive expected value.

In practice, the strongest opportunity came from a persistent buyer in the local market: sell orders placed slightly above the best bid were often filled immediately. This allowed us to repeatedly sell locally and buy abroad, locking in arbitrage profits. We extended this with a market-making layer, posting quotes only when they remained profitable after conversion costs, and with an adaptive edge algorithm that adjusted quote aggressiveness based on realized fill rates.

Overall, the Orchid strategy was not a predictive model on environmental variables, but rather a market-structure and execution-driven arbitrage system.



## ETF / basket arbitrage
From previous years, we were already familiar with basket-style products such as PICNIC_BASKET, composed of UKULELE, BAGUETTE, and DIP. In this year’s competition, the same structural idea reappeared in several forms. In Round 3, for example, GIFT_BASKET was introduced alongside its constituents: 4 CHOCOLATE, 6 STRAWBERRIES, and 1 ROSE. Similarly, in another basket round we saw PICNIC_BASKET1 and PICNIC_BASKET2, each defined as fixed linear combinations of underlying products.

This type of setup naturally suggests a basket-versus-synthetic arbitrage problem. For any quoted basket, one can construct a corresponding synthetic basket price by summing the prices of the constituents in the correct proportions. The central object we traded was therefore the basket premium or spread, defined as:

spread = quoted basket price − synthetic basket price

If markets were perfectly efficient and frictionless, this spread would be close to zero or at least stable around a trivial constant. In practice, however, the basket often traded persistently rich or cheap relative to its synthetic value, and this deviation exhibited clear short-horizon mean reversion. That made the problem less about directional prediction and more about relative value trading.

### Core hypothesis

At the start, we considered two broad possibilities.

The first was a lead-lag hypothesis: perhaps the constituents moved first and the basket followed, or vice versa. If true, this would allow us to forecast short-term price moves using one side of the structure as a predictor for the other.

The second was a mean-reversion hypothesis: perhaps neither side truly led, but instead the spread itself oscillated around a stable equilibrium or premium level. In that case, the profitable strategy would be to buy the spread when it became too cheap and sell it when it became too rich.

After plotting the time series and analyzing historical behaviour, the second interpretation proved much more convincing. The spread was not centered exactly at zero; rather, it fluctuated around a stable non-zero mean. For the gift basket round, this level was roughly 370 across the available historical data. That strongly suggested that the market was pricing baskets with a persistent premium, but that deviations around this premium were mean reverting.

### Structural interpretation

This mattered because it shaped how we thought about execution. Our working model was that the constituents were the more fundamental objects, while the quoted basket price was effectively the constituent value plus a noisy, mean-reverting premium. Under that interpretation, the constituents were not “following” the basket. Instead, the basket was temporarily drifting away from and then back toward its synthetic value.

This implied that the cleanest source of alpha was the premium itself, not trend following on the basket and not prediction of the underlying components. It also meant we should be careful about adding unnecessary complexity. Techniques like moving-average crossovers or heavily parameterized forecasting rules might fit the data, but without a clear structural rationale they would be much more vulnerable to overfitting.

So our strategy centered on a simple principle:

when the basket premium is too high, the basket is expensive relative to the synthetic, so we sell the basket spread;
when the basket premium is too low, the basket is cheap relative to the synthetic, so we buy the basket spread.

In portfolio terms, that means going long basket / short synthetic when the spread is low, and short basket / long synthetic when the spread is high.

### First implementation: fixed-threshold spread trading

Our first implementation used a fixed-threshold model. We estimated the average premium from the historical data and entered trades only when the spread moved sufficiently far away from that baseline. This was robust and easy to reason about. If the spread was rich by more than some threshold, we sold; if it was cheap by more than some threshold, we bought.

The advantage of this approach was that it respected the structural picture and avoided overfitting. The disadvantage was that it could miss profitable reversions. If the spread reversed before reaching the threshold, we earned nothing. Tightening the threshold helped capture more moves, but also caused us to enter too early and give up edge before the spread reached a local extreme.

Even so, this simple threshold model worked reasonably well and projected solid profits in backtests.

### Adaptive version: modified z-score strategy

To improve timing, we moved from fixed spread thresholds to a more adaptive modified z-score framework.

The basic idea was to treat the premium mean as relatively stable, but allow the volatility of the spread to change through time. Rather than normalize the spread using a long and slow estimate of volatility, we used a short rolling standard deviation window. This caused the z-score to become more sensitive exactly when the spread began compressing or volatility dropped, which often coincided with turning points.

Formally, we used:

z-score = (spread − long-run premium mean) / rolling spread standard deviation

We then traded this z-score directly:

if the z-score rose above a positive threshold, we sold the spread;
if the z-score fell below a negative threshold, we bought the spread.

This improved the strategy in two ways. First, it made entries more responsive to the actual local regime rather than forcing all deviations to be interpreted in raw price units. Second, because the denominator was short-window volatility, the signal often sharpened near local maxima and minima, allowing us to enter closer to the turning point rather than simply waiting for a large absolute deviation.

This was still fundamentally a mean-reversion strategy, but it was a more adaptive one. The z-score did not replace the structural model; it refined the entry rule.

### Hedged versus unhedged implementation

A key design question was whether to trade the basket premium in a fully hedged way or to trade only the basket itself.

The fully hedged version is the textbook statistical arbitrage implementation: take the basket position and offset it with the underlying constituents in the exact weights needed to isolate the premium. This reduces directional exposure and makes the trade much purer in theory.

However, there were practical trade-offs:

trading more legs means paying more spread and crossing costs;
execution becomes more complex and less certain;
constituent liquidity and basket liquidity were not always symmetric;
in some rounds, position limits made a perfectly hedged implementation impossible at scale.

Because of these trade-offs, our implementation varied by round.

For Gift Basket, we often found that the quoted basket itself carried the signal most cleanly, and we were willing to trade the basket more aggressively rather than always fully replicating or hedging every constituent leg. This reduced transaction costs and simplified execution, at the cost of carrying some extra exposure.

In other basket rounds, especially where synthetic construction was more executable, we leaned more directly into the hedged spread trade, using the constituents to isolate the basket premium.

Conceptually, we viewed this as a continuum rather than a binary choice. A strategy can be seen as a linear combination of fully hedged and fully unhedged exposure. In some cases, we deliberately chose a partial hedge, for example hedging 50% of exposure as a compromise between lower variance and higher expected return.

### Position-limit-aware basket allocation

One of the more difficult problems emerged when multiple baskets shared the same constituents and position limits prevented us from hedging everything simultaneously.

This was particularly important in the dual-basket setup with PICNIC_BASKET1 and PICNIC_BASKET2. Each basket had its own premium relative to its synthetic value, but both baskets also competed for the same constituent inventory and the same position limits. In practice, this meant we could not simply max out both independent basket-versus-synthetic trades at the same time.

To solve this, we decomposed the opportunity into two layers.

The first layer was the relative premium spread between Basket 1 and Basket 2. Instead of only asking whether each basket was rich or cheap relative to its own synthetic, we also examined whether Basket 1’s premium was rich relative to Basket 2’s premium, or vice versa. That gave us a higher-level spread:

premium spread = Basket 1 premium − Basket 2 premium

We then z-scored this difference and traded it as a relative-value signal. This was attractive because it used capital efficiently and reduced some of the shared constituent exposure problem.

The second layer was then to allocate the remaining available risk budget to the stronger standalone basket-premium trades. We effectively treated the total book as a constrained optimization problem: first deploy capacity where the spread opportunity was strongest and most hedge-efficient, then use remaining inventory room for secondary opportunities.

In practical terms, this meant:

using 100% of Basket 1 capacity where justified;
using only part of Basket 2 capacity when constituent limits prevented a full hedge;
scaling down positions when exact synthetic replication became impossible;
and reserving leftover unused capacity for other low-risk strategies.

### Using leftover capacity: residual market making

When position limits prevented perfect deployment into basket arbitrage, we did not want capital to sit idle if it could be used safely. In some rounds, a small residual portion of basket capacity remained after all hedge-feasible statistical arbitrage had been allocated.

We used that leftover capacity for light market making, especially when quoted basket spreads were consistently wide. This was not the main source of profit, but it was a useful secondary overlay. The logic was straightforward: if we could not deploy the last few units into a hedged premium trade, we could still earn from passive liquidity provision with tight inventory control.

Because this residual market-making layer was small and used only leftover exposure room, it contributed incremental PnL with low additional variance.

### Signal refinement and informed bias

We also explored whether other products could help refine basket entries. In some cases, suspicious recurring order patterns or participant behaviour in related products suggested that certain names might contain informational signals relevant to the baskets.

For example, if a related constituent appeared to be systematically bought or sold by an informed participant, we could use that inferred directional bias to tilt our spread thresholds. Instead of entering symmetrically, we would shift the long-entry and short-entry levels to favour the side supported by the cross-product signal.

This did not replace the basket-premium framework. Rather, it acted as a bias term layered on top of the base mean-reversion model. The philosophy here was important: we wanted to keep the core structural strategy simple, and only use external signals to adjust thresholds, not to completely redefine the trade.

### Execution philosophy

Execution mattered almost as much as signal generation.

In these basket products, passive quoting was often unreliable. Basket signals could appear and disappear quickly, and if the position limit was small relative to the available opportunity, waiting passively for fills was often more costly than crossing the spread. As a result, when the premium moved far enough away from equilibrium, we frequently chose to cross the market and trade immediately, sometimes even deeper into the order book, accepting slippage in exchange for securing the position.

This reflected a deliberate prioritization: if the expected reversion was strong enough, missing the trade entirely was more expensive than paying some execution cost upfront.

At the same time, we were careful on exits. Rather than always requiring the spread to travel all the way to the opposite threshold, we often neutralized once it had reverted sufficiently close to fair value or crossed the adjusted equilibrium level. This helped reduce variance and lock in profits more consistently.

### Strategy summary

Overall, our basket strategy was built on a relatively simple but robust insight: the baskets traded with a persistent premium over their synthetic value, and deviations from that premium tended to mean revert.

Everything else followed from that:

compute the synthetic value from the constituents,
define the basket premium as basket minus synthetic,
estimate a stable long-run premium mean,
normalize deviations using either fixed thresholds or a short-window rolling z-score,
buy the spread when the basket becomes too cheap,
sell the spread when it becomes too rich,
hedge fully, partially, or not at all depending on transaction costs, liquidity, and position limits,
allocate capacity across multiple baskets with awareness of shared constituent constraints,
and use any remaining unused capacity for small residual market making.

The key point is that this was never a purely mechanical z-score strategy. It was a structural relative-value strategy grounded in how baskets and constituents were likely generated, with the z-score serving only as a practical entry-timing device. That kept the model interpretable, limited overfitting, and made it much easier to adapt across different versions of the basket products introduced in different rounds.




# Location arbitrage
Note:
In previous years, products such as Magnificent Macarons were tradable across multiple islands, creating opportunities for location arbitrage through a conversion mechanism. This allowed traders to buy on one exchange, convert inventory, and sell on another when price differences more than covered fees and tariffs.

This year, however, we have been told that no conversion mechanism will be available. That makes classic location arbitrage much less likely to matter. Thematically, this also makes sense: if trading now takes place across planets rather than nearby islands, direct cross-venue conversion is probably less plausible as a game mechanic.

Still, location arbitrage has been an important strategy in prior competitions, so it is worth understanding how it worked and what kinds of opportunities it created.

### Previous-year example: Magnificent Macarons

In Round 4 of the previous competition, Magnificent Macarons were introduced. Macarons could be traded on the local island exchange through the visible order book, but they could also be converted through a second market on Pristine Island. In effect, this created a two-venue trading problem: a trader could transact locally, convert inventory externally, and arbitrage differences between the two markets.

The product came with several frictions:

transport fees for conversion,
an export tariff when exporting from the main island,
an import tariff when importing back,
and a storage cost of 0.1 seashells per timestamp per Macron held.

The storage fee strongly discouraged holding long inventory for extended periods, which meant the best implementations focused on rapid turnover and low inventory duration.

At first glance, Macarons also appeared to invite a predictive strategy. Their fictional value was linked to variables such as sunlight, sugar prices, shipping conditions, and tariffs. We did investigate this path, but ultimately decided not to rely on it. While the external variables showed some statistical relationships, the much stronger edge came from market structure and cross-market execution, not from forecasting price moves.

### Base arbitrage logic

The natural first step was to calculate the true conversion-adjusted break-even price. A local trade was only worthwhile if the local execution price was better than the external market price after adjusting for all conversion costs.

For local selling, the relevant break-even level was:

local sell break-even = external ask + import tariff + transport fee

This gave us the minimum local sale price required to make a profitable round-trip after conversion.

Symmetrically, for local buying, one could compare the local ask against the external bid adjusted for export costs.

This is the basic location-arbitrage framework: compare the local order book to the external venue after fees, and trade only when the difference is positive.

### The hidden edge: aggressive taker behaviour

What made Macarons especially profitable was not merely the visible arbitrage. The more important discovery was a hidden taker bot in the local market.

Through experimentation, we found that local sell orders placed near a price derived from the external market—roughly around int(externalBid + 0.5)—were frequently filled even when the visible local order book did not obviously justify it. In other words, there was a hidden participant willing to buy aggressively at prices that were attractive relative to some internal notion of fair value.

This meant that the best local executable price was often better than the visible best bid. In practice, this created a much more profitable strategy than naïvely hitting the displayed market. Rather than simply selling into the visible best bid and converting, we could post higher-priced sell orders locally, wait for the taker bot to lift them, and then immediately convert the resulting inventory externally.

This transformed the problem from simple arbitrage into a microstructure-aware arbitrage strategy:

quote at the best price that still triggers hidden taker fills,
get executed above the naïve local market,
and immediately convert to lock in the spread.

The key insight was that even a small improvement in price per unit became very valuable when repeated over thousands of timesteps.

### Why we ignored the predictive features

Although Macron prices were correlated with variables such as sunlight and sugar prices, we chose to deprioritize forecasting models. The reason was straightforward: the execution-based arbitrage edge was much larger, simpler, and more reliable.

We did test a machine-learning approach based on logistic regression. Features included sunlight changes, threshold effects when sunlight became “critical,” and interaction terms capturing the duration of abnormal conditions. The model generated statistically significant coefficients and historically respectable profits, on the order of roughly 25k per day.

However, this approach had several weaknesses:

we were not fully confident in out-of-sample generalization;
the implementation burden was high, especially with lagged features and state storage;
serialization and trader-state overhead made the system slower and more fragile;
and most importantly, the model conflicted awkwardly with the conversion logic, since conversions could only reduce inventory and therefore made directional positioning cumbersome.

So while the predictive model was interesting as a research exercise, it was not the strongest production strategy.

### Final strategy

Our final strategy focused on reliably monetizing the hidden arbitrage.

At each timestep, we placed limit sell orders in the local market at the highest price that still appeared to attract the taker bot—approximately int(externalBid + 0.5). Once filled, we would immediately use the conversion mechanism to unwind the position externally.

This strategy had several advantages:

it exploited a structural market inefficiency rather than a fragile forecast;
it required only simple, robust calculations based on observable prices and fees;
it minimized inventory risk because filled positions were converted quickly;
and it scaled naturally with repeated opportunities across the day.

We initially quoted only 10 units per timestep, matching the conversion limit. This was conservative and reduced operational complexity, but it also meant we captured only part of the full potential opportunity. In hindsight, quoting somewhat larger sizes could have improved results further by allowing excess inventory to be converted gradually, even if not all quotes filled immediately.

Even with conservative sizing, the strategy produced substantial profits with relatively low risk. In practice, this was one of the strongest pure execution-based opportunities in the competition.

### Broader lesson

Macarons illustrated a recurring theme in Prosperity-style competitions: the best strategy is not always the most mathematically elaborate. External variables such as sunlight or sugar prices may look important, but often the dominant edge lies in understanding the trading mechanism itself.

In this case, the winning ingredients were:

correct conversion-adjusted pricing,
recognition of hidden taker behaviour,
disciplined quote placement,
and fast conversion after execution.

Teams that had studied earlier competitions carefully had a meaningful advantage, since similar hidden taker patterns had appeared before in products such as Orchids and other simulated microstructure settings. But even without prior knowledge, the signal was available to anyone who inspected the historical fills closely: repeated executions at prices better than the visible local best bid were a strong clue that something deeper was happening.

Although our own implementation did not fully reach the theoretical optimum, it still captured a large share of the available edge. More importantly, it reinforced a core principle of these rounds: deep understanding of market structure often beats predictive modeling.




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
