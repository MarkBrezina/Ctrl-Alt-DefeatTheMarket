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
Options / volatility trading

This round introduced a classic options-style structure. In one version, we traded Coconuts and a Coconut Coupon, which was effectively a near-the-money 10,000-strike call option on coconuts with substantial time remaining until expiry. In another version, the market included Volcanic Rock and several Volcanic Rock vouchers with strikes ranging from 9500 to 10500, effectively creating a small option surface across multiple strikes. In both cases, the core problem was the same: identify whether the options were mispriced relative to the underlying, and decide how much risk to take in hedging that exposure.

Our starting point was standard options theory. We used the Black-Scholes model to translate observed option prices into implied volatilities, and then studied the behaviour of those implied volatilities through time. For the Coconut Coupon, the main observation was that implied volatility appeared to oscillate around a relatively stable level of roughly 16%. That immediately suggested a mean-reversion strategy in implied volatility: when the market priced the coupon at an unusually high implied vol, we would look to sell vol; when it priced the coupon at an unusually low implied vol, we would look to buy vol.

For the voucher setup, the analysis extended naturally from a single implied volatility to a volatility smile. Using the hint provided on the website, we plotted implied volatility against moneyness, defined as a strike-relative transformation of the underlying price and time to expiry. Fitting a quadratic curve to this relationship gave us a smoothed estimate of “fair” implied volatility for each strike at each point in time. This let us distinguish between ordinary cross-strike structure and true mispricing. Rather than reacting to raw voucher prices alone, we compared each observed voucher price to the price implied by Black-Scholes using the fitted smile. That turned the problem into one of relative value trading in implied volatility space.

The main strategy we implemented was therefore IV scalping / volatility mean reversion. Once we had a fair implied volatility estimate—either a stable scalar level in the Coconut Coupon case or a strike-dependent smile in the voucher case—we converted that back into a theoretical option price. We then compared theoretical and observed prices and traded when deviations became large enough to overcome execution costs. In practice, this often behaved like a short-horizon mean-reversion signal in option prices: overpriced options were sold, underpriced options were bought, and positions were unwound as prices reverted toward model value.

A crucial part of the strategy was delta management. Since an option embeds directional exposure to the underlying, trading implied volatility cleanly requires controlling that delta. So after trading the options, we computed the option delta and hedged with the underlying. The goal was not to express a directional view on coconuts or volcanic rock, but to isolate mispricing in the option itself. In backtests, this produced the most stable PnL profile: a relatively smooth curve consistent with capturing repeated small pricing inefficiencies rather than relying on one large move in the underlying.

That said, the hedge was not always perfect. For the Coconut Coupon, delta was around 0.53, while the position limits were 300 for coconuts and 600 for coupons. This meant that a full-sized coupon position could not be fully hedged: 600 coupons implied roughly 318 delta, but the underlying position cap was only 300. As a result, even after hedging as much as possible, we were left with some unavoidable directional exposure. Because the option still had a long time to expiry, gamma was relatively modest, so we accepted this residual delta risk in exchange for maintaining large exposure to what looked like a positive-EV volatility trade. In effect, we knowingly chose a higher-variance version of the strategy because the backtests were attractive.

For the voucher version, we dealt with this problem more conservatively. Since we could hold 400 units of the underlying but only 200 of any individual voucher, there was a temptation to take larger option positions across multiple strikes and then patch together a global hedge. Under time pressure, however, we chose to simplify. We capped voucher positions at a smaller size so that they could always be fully hedged cleanly with the underlying. This almost certainly sacrificed some upside, but it made the live implementation far less error-prone and preserved the core advantage of the strategy: keeping exposure focused on option mispricing rather than accidental delta bets.

We also evaluated two related sources of edge.

The first was gamma scalping. Because the options were not near expiry in the early rounds, time decay was real but not overwhelming, and there were periods where buying options and dynamically rehedging the delta appeared to have positive expected value. The intuition was that realized moves in the underlying could generate enough rehedging profit to offset theta. In backtests, this was generally a stable but modest contributor: profitable, but not spectacular.

The second was mean reversion in the underlying itself. In the Volcanic Rock round especially, return dynamics showed signs of short-term negative autocorrelation, somewhat reminiscent of earlier mean-reverting assets. We therefore tested a lightweight mean-reversion model on the underlying, based on a fast EMA and fixed trading thresholds. Importantly, this was kept separate from the core options model. The options strategy was grounded in pricing theory and relative mispricing; the underlying mean-reversion overlay was more statistical and therefore more fragile.

In the end, we deployed a hybrid strategy. The core of the book was still IV scalping: estimate fair implied volatility, identify overpriced and underpriced options, trade them aggressively, and hedge the resulting delta. Around that, we ran a smaller and more cautious underlying mean-reversion overlay. This was not intended as a pure alpha engine on its own, but rather as a complementary source of return and a hedge against scenarios in which the underlying exhibited stronger-than-expected short-term reversion. In other words, the hybrid was designed not just to maximize raw expected value, but to reduce regret across different possible market regimes.

In backtests, this approach looked excellent. The PnL curve from the options component was particularly encouraging because it was smooth and nearly linear on many days, which is often a sign that the strategy is capturing many independent small edges rather than overfitting a small number of large historical trades. We estimated that the options component alone could generate on the order of 80k–150k seashells, depending on the specific product set and round, with additional contribution from other products and overlays.

Live trading, however, was harsher. In the Coconut Coupon round, the residual unhedged delta hurt us materially. What had looked like a sensible trade-off in backtesting—accepting slightly more directional risk in exchange for more volatility exposure—turned out to be too aggressive in the realized path. The strategy still made money, about 145k seashells, but it underperformed our expectations and cost us a significant amount of ranking position. In hindsight, this was less a modeling failure than a risk-allocation failure. We were already near the top of the leaderboard, so preserving rank by lowering variance may have been the better decision.

The broader lesson from this round was that options edge can come from several distinct sources, and they need to be separated carefully:

implied volatility mean reversion, where the market over- or underprices vol relative to a stable level;
cross-strike relative value, where one option is rich or cheap relative to the fitted smile;
gamma scalping, where rehedging converts realized movement into profit;
and underlying mean reversion, which is directional and conceptually different from options mispricing.

Our strongest results came from keeping these components conceptually distinct and making the pricing-theoretic strategy the center of the book. The more we drifted into accepting unhedged directional exposure, the more fragile the results became.

### Strategy summary

For the options round, our implementation was built around the following logic:

Treat the coupon or voucher as a call option on the underlying.
Use Black-Scholes to back out implied volatility from observed market prices.
For multi-strike products, fit a volatility smile as a function of moneyness to estimate fair IV across strikes.
Reprice each option using the fitted or average IV estimate.
Trade when the market price deviates sufficiently from theoretical value.
Delta hedge with the underlying to isolate volatility exposure as cleanly as possible.
Keep position sizing conservative when hedge constraints or position limits make full hedging difficult.
Add only a small and controlled overlay of underlying mean reversion rather than letting the book become dominated by directional bets.

That was the intellectual core of the strategy: not forecasting the underlying directly, but pricing volatility more accurately than the market and managing the hedge well enough to capture that edge.

