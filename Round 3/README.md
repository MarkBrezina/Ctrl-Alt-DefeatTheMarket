# Round 3 **- “Gloves Off”**

Welcome to Solvenar! A prosperous and highly developed planet known for technological innovation, a robust economy, and thriving cultural sectors.

This awe-inspiring society will be the stage for the ***Great Orbital Ascension Trials*** (GOAT). In this Great Galactic Trade-Off, you will face other trading crews head-on as you compete for the coveted title of Trading Champion of the Galaxy. This trading round marks the start of GOAT, where ***all teams begin with zero PnL and the leaderboard is reset***.

You will develop a new Python program and incorporate your strategy for trading ***Hydrogel Packs*** (`HYDROGEL_PACK`), ***Velvetfruit Extract*** (`VELVETFRUIT_EXTRACT`), and ***10 Velvetfruit Extract Vouchers*** (`VELVETFRUIT_EXTRACT_VOUCHER`). These vouchers give you the right to buy Velvetfruit Extract at a later point for a specific strike price.

To kick off GOAT, the Celestial Gardeners’ Guild is making a rare appearance, offering you the opportunity to buy ***Ornamental Bio-Pods*** from them. You may submit two offers and trade with as many of the so-called “Guardeners” as aligns with your strategy for maximum profitability. Secure those Bio-Pods, and they will be automatically converted into profit before the next trading round begins.

Be aware that ***trading rounds on Solvenar (Solvenarian days) last only 48 hours***. Be decisive, thorough, and fast, and make this first step toward the ultimate title count.

# **Round Objective**

Create a new Python program that algorithmically trades `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, and `VELVETFRUIT_EXTRACT_VOUCHER` on your behalf and generates your first profit in this final phase.

In addition, manually submit two orders to trade Ornamental Bio-Pods with members of the Celestial Gardeners’ Guild, then automatically sell your acquired Bio-Pods to generate additional profit.

# **Algorithmic trading challenge: “Options Require Decisions”**

There are 2 ‘asset classes’ in the three products you trade. The `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT` are “delta 1” products, similar to the products in the tutorial and rounds 1 and 2. The 10 `VELVETFRUIT_EXTRACT_VOUCHER` products (each with a different strike price) are options, and thus follow different dynamics. All products are traded independently, even though the price of `VELVETFRUIT_EXTRACT_VOUCHER` might be related to that of `VELVETFRUIT_EXTRACT` due to the nature of options.

The vouchers are labeled `VEV_4000`, `VEV_4500`, `VEV_5000`, `VEV_5100`, `VEV_5200`, `VEV_5300`, `VEV_5400`, `VEV_5500`, `VEV_6000`, `VEV_6500`, where VEV stands for **V**elvetfruit **E**xtract **V**oucher, and the number represents the strike price. They all have a 7-day expiration deadline starting from round 1, where each round represents 1 day. Thus, the ‘time till expiry’ (TTE) is 7 days at the start of round 1 (TTE=7d), 6 days at the start of round 2, 5 days at the start of round 3, and so on.

The position limits ([see the Position Limits page for extra context and troubleshooting](https://imc-prosperity.notion.site/writing-an-algorithm-in-python#328e8453a09380cfb53edaa112e960a9)) are:

- `HYDROGEL_PACK`: 200
- `VELVETFRUIT_EXTRACT`: 200
- `VELVETFRUIT_EXTRACT_VOUCHER`: 300 for each of the 10 vouchers.

<aside>
📃

**Example**: `VEV_5000` is an option on the underlying VEV with a strike price of 5000 and a position limit of 300. At the start of the final simulation of Round 3, its time to expiry (TTE) is 5 days. In the historical data, the corresponding TTE values are:

- TTE=8d at the start of historical day 0 (coinciding with the tutorial round),
- TTE=7d at the start of historical day 1 (coinciding with Round 1),
- TTE=6d at the start of historical day 2 (coinciding with Round 2).
</aside>

Vouchers cannot be exercised before their expiry, and inventory does not carry over into the next round. Like in previous rounds, any open positions are automatically liquidated against a hidden fair value at the end of the round.




























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

# Additional Notes
Cross-year signal discovery

Our leading hypothesis for Puerto Vallarta’s outsized profits was that they had found some way to predict future price movements. A result on the order of 1.2 million SeaShells looked too large to be explained by ordinary execution improvements alone; it seemed more consistent with a very strong predictive signal spanning multiple products.

We therefore began a broad search for missed structure in the data. First, we ran regressions on both contemporaneous and lagged returns across all symbols and all available days, looking for cross-asset relationships we might have overlooked. A few effects looked mildly interesting—for example, Starfruit appeared to have some lagged predictive power for several other products—but nothing remotely strong enough to explain the sort of edge we were trying to replicate.

As a final attempt, we looked outside the competition year itself. The previous year’s competition, as discussed in the Stanford Cardinal write-up, appeared to share a number of structural similarities with this one, especially in the early rounds where the product set sounded almost identical. That led us to source the previous year’s public data from GitHub and test whether returns in last year’s assets might map onto this year’s products.

The results were absurd, but hard to ignore. Returns in last year’s Diving Gear, scaled by roughly 3, were almost a perfect predictor of Roses, with an R
2
 of about 0.99. Similarly, last year’s Coconuts were an almost perfect predictor of this year’s Coconuts, with a beta of roughly 1.25 and an R
2
 again near 0.99.

These relationships were obviously artificial, but the competition objective was simple: maximize PnL. Since the prior-year data was public, we treated it as fair game. From that point onward, our focus shifted from discovery to extraction: if other teams could find the same relationships, then implementation quality and optimization would matter just as much as the signal itself.

Our first pass was straightforward. We simply bought or sold Coconuts and Roses whenever the predictor implied a sufficiently large future move to overcome the spread. Even this naïve implementation dramatically outperformed almost everything we had built in earlier rounds. But because the historical signal was so strong, we believed even more value could be extracted by optimizing pathwise execution rather than using crude entry thresholds.

That led us to a dynamic programming (DP) approach. Since the predictor effectively gave us a future price path, the real challenge was no longer forecasting direction, but determining the optimal sequence of trades subject to realistic trading constraints. These constraints included:

spread costs,
limited executable size at each timestamp,
and hard position limits.

The need for DP came from the fact that we could not always move directly to the ideal position. The optimal trade at a given timestamp depended not just on the forecasted future prices, but on which intermediate inventory levels were actually reachable under order-book volume constraints.

A simple example illustrates the issue. Suppose prices evolve as:

8 → 7 → 12 → 10

with a position limit of 2.

If enough volume is available at every step, the optimal trade sequence is:

sell 2 → buy 4 → sell 4

for a total PnL of 16.

But if execution is capped at 2 units per step, the optimum changes to:

buy 2 → buy 2 → sell 2

for a total PnL of 14.

This kind of path dependence is exactly what the dynamic program was designed to handle.

The inputs to the DP were the predictor price series, an average spread estimate, and an estimate of executable volume as a fraction of the position limit. Because the predictive relationship was so strong, it was sufficient to generate trades directly from the predictor path. The DP then produced a timestamp-by-timestamp action sequence for each product, deciding whether to buy, sell, or hold in order to maximize total achievable PnL under the constraints.

Using this approach across Roses, Coconuts, and Gift Baskets, we achieved an algo PnL of roughly 2.1 million SeaShells, the highest of any team in that round. That performance was ultimately the main driver behind our rise back up the overall leaderboard.

# dynamic programming code block here
Counterparty analysis and informed flow

In another round, no new products were introduced. Instead, the exchange revealed the identities of the counterparties we were trading against. There were 11 other bots active in the market, and that immediately suggested a different kind of edge: perhaps one of the bots was systematically better informed than the rest.

We began by visualizing the full trade flow of every bot across every product. For each product, we plotted the price series and overlaid the trades of individual bots, which made it possible to visually inspect whether any trader consistently bought near lows or sold near highs. One name stood out almost immediately: Olivia.

Across multiple products, Olivia’s trades appeared suspiciously well timed. She repeatedly bought near local lows and sold near local highs, often across the same products on consecutive days. This confirmed a suspicion we had already formed in earlier rounds from pattern analysis alone: some trades in the data were not random, and at least one trader seemed to possess a strong directional signal.

From there, the question became how best to exploit that information.

Squid Ink

For Squid Ink, we chose a hybrid approach. Before Olivia’s signal appeared, we continued with our existing market-making and liquidity-taking strategy. Once Olivia traded, however, we treated that as a regime shift and followed her direction for the rest of the day. In practice, this meant that Olivia’s signal dominated our directional posture once it appeared, while our earlier strategy monetized the spread and volatility while waiting for it.

Croissants and basket interaction

Croissants were more complicated because they were also one of the main components in our basket trades. Chris reasoned that if Olivia had a true directional edge in Croissants, then we should not continue running basket trades that effectively put us in the opposite direction. Since Croissants represented roughly 50% of the value of the baskets, opposing Olivia through the basket could undo a substantial part of the signal’s value.

This insight pushed us toward a much more aggressive stance. Rather than merely copy Olivia in Croissants with the direct product limit, we realized that we could amplify that exposure indirectly through the baskets. Our direct Croissant position limit was 250, but by going long through both baskets we could reach an effective exposure closer to 1050 Croissants.

This was a much more aggressive strategy than our previous basket-stat-arb implementation, but the upside looked compelling. On weaker days, the difference between the high and low in Croissants was still often around 40 SeaShells, which implied that an extra 800 Croissant-equivalent exposure could add something like 32k in additional PnL even in a relatively poor scenario. On stronger days, when the high-low move was more like 120, the extra upside was enormous.

By comparison, our statistical basket arbitrage often produced around 50k on its best days, whereas “YOLO-ing” into Croissants on Olivia’s signal could produce as much as 120k on strong days. That trade-off made the decision attractive, especially because it was also much simpler to implement cleanly.

To support this structure, we hedged the baskets with the remaining components—Jams and Djembes—as much as position limits allowed, since basket movement still remained substantially correlated with those products. Even after hedging, we ended up with some unavoidable residual exposure, including about 30 Jams. We accepted that risk because it allowed us to take on even more effective Croissant exposure, and the expected gain from the Croissant signal appeared larger than the likely downside in Jams.

Premium risk in baskets

This strategy did leave us exposed to basket premium risk. In a near-worst-case scenario, if we entered a basket position at the top of its premium and exited at the bottom, the premium movement alone could cost roughly 300 SeaShells per basket, or as much as 45,000 SeaShells in aggregate in an extreme case.

We could not find a good way to hedge that premium risk directly. Instead, we relied on a probabilistic argument. Chris found evidence that the change in basket premiums was approximately stationary, with reasonably strong statistical confidence. Under that assumption, premium movements were more like noise than drift, and the probability of systematically entering at the exact worst moment seemed low—provided Olivia’s signal was not itself correlated with premium extrema. In hindsight, that latter assumption should probably have been tested more directly, but at the time we concluded that the expected premium loss was close to zero and that the practical worst-case loss was likely far smaller than the theoretical bound.

That made the risk worth taking.

Final optimization

One final optimization Chris added was to continue market making and taking on both picnic baskets while waiting for Olivia’s first signal to arrive. Since both baskets had wide spreads, this added up to another 10k SeaShells per day depending on how long the wait was before the signal appeared.

By the time trader IDs were formally exposed in the final round, this did not fundamentally change our strategy, since we had already identified Olivia’s behavior earlier. What it did do was simplify and harden the implementation. Instead of inferring Olivia’s actions indirectly from suspicious price patterns and trade locations, we could check the trader ID directly, which reduced false positives, lowered the chance of missing a real signal, and saved a few hundred SeaShells over the round.

Because we entered the final round with a lead of roughly 190k over third place, we also made the overall portfolio more conservative. We half-hedged basket exposure and toned down the mean-reversion sleeve in order to reduce the risk of a catastrophic late-round loss.

Summary of the counterparty strategy

The strategy in this round was not merely “copy Olivia.” It had several layers:

identify which trader had genuine predictive timing;
follow her directly in products where the signal was clearly superior to our own alpha;
stop trading correlated basket structures against her directional information;
increase effective exposure through basket components where risk-reward justified it;
hedge residual basket risk where possible;
and continue harvesting spread income while waiting for the signal to appear.

That combination of signal extraction, structural amplification, and pragmatic execution was one of the most profitable and conceptually satisfying parts of our overall approach.

Pair trading

We also experimented with more classical relative-value trades during the competition. In the Coconuts / Pina Coladas setup, Konstantin implemented a pair-trading strategy based on the spread:

Pina Colada − (15/8) × Coconut

The idea was to exploit deviations from the historical relationship between the two products. We also considered momentum-based alternatives, but pair trading consistently generated stronger results in our tests, so it remained the main approach in that product pair.

This strategy never became the centerpiece of our book, but it was one of several examples where standard statistical-arbitrage logic still produced decent returns when the product design supported it.

Research that did not make it into production

Throughout the competition, we explored a number of ideas that were theoretically interesting but either too fragile, too complex, or too unreliable to deploy live.

Basket mean-reversion modeling

We tried to model the spread between picnic baskets and their synthetic values for standalone mean-reversion trading. The logic was sound, but the implementation became messy, especially once position limits and cross-product dependencies started to matter. Some variants backtested well, but the performance was not consistent enough to justify relying on them as core production strategies.

Volatility surface fitting

For Volcanic Rock vouchers, we experimented with fitting a full volatility surface / smile to implied volatilities as a function of moneyness. In principle this would have given us a more refined options-pricing framework than a single rolling implied vol estimate. In practice, it proved too complex to implement reliably under time pressure, and we were not sufficiently confident in the live robustness of the calibration.

Delta hedging

We also attempted more sophisticated delta-hedged options strategies in Volcanic Rock and its vouchers. Conceptually, this was attractive: isolate implied-volatility mispricing while hedging away directional exposure in the underlying. But in practice, calibration, timing, and position-limit interactions made the live implementation much harder than expected.

Direct basket-component arbitrage

We wrote code to arbitrage directly between picnic baskets and their constituents (Croissants, Jams, Djembes), but ran into implementation bugs and hedge-allocation problems. We never managed to deploy a version we trusted.

Broad price-pattern analysis

We spent a great deal of time modeling almost every product—Squid Ink, Croissants, Jams, Djembes, Volcanic Rock, Macarons, and others—for autocorrelation, seasonality, and cross-asset predictive structure. Some of that effort paid off indirectly by sharpening our intuition, but much of it did not produce live-tradable strategies.

More advanced use of Olivia’s signal

After identifying Olivia as an informed trader, we tried to integrate her signal more subtly into our quoting logic—for example by dynamically shifting bids and asks rather than just following her trades outright. These approaches were elegant in theory, but the added complexity did not translate into sufficiently reliable gains. Direct copy-trading and directional positioning simply worked better.

Round-by-round overview
Round 1

Round 1 introduced the first three products: Rainforest Resin, Kelp, and Squid Ink.

Rainforest Resin

We treated Resin as a stable-value product centered around 10,000. The strategy combined tight market making with controlled inventory management. We placed passive orders slightly inside inefficient book levels and selectively took favorable quotes when the market drifted away from fair value. Additional passive rebalancing orders helped keep inventory under control.

Kelp

Kelp required a more adaptive fair-value model. We first analyzed the frequency of quoted sizes to identify the most reliable order-book levels, and then used those filtered quotes to compute a more platform-aligned estimate of fair value. Around this estimate, we ran a mix of passive market making and opportunistic liquidity taking when spreads widened. Conservative inventory management remained central throughout.

Squid Ink

For Squid Ink, our first implementation used a directional signal based on top-of-book pressure. We tracked changes in best bid/ask levels and volumes, converted those into a pressure score, and then generated buy, sell, or hold signals. Execution used adaptive offsets that adjusted based on recent fill behavior.

Round 2

Round 2 introduced Croissants, Jams, Djembes, Picnic Basket 1, and Picnic Basket 2.

Squid Ink

After poor results in Round 1, we rebuilt the Squid Ink model from scratch. The new version used a runtime-trained logistic regression with a seven-feature vector including z-score, momentum, order-book imbalance, MACD-style signals, and pressure features. Orders were sized and priced based on model confidence, and the model was retrained every 50 timestamps on recent history.

Jams

Jams looked more naturally mean reverting, so we traded them with a rolling z-score framework combined with light trend confirmation. Position sizes were adjusted based on existing exposure.

Croissants and Djembes

We initially chose not to trade Croissants or Djembes individually. Both were volatile, and neither looked like a clean standalone product for market making or directional execution at that stage.

Picnic Basket 1

For Basket 1, we computed its synthetic value from the components:

Synthetic = 6 × Croissants + 3 × Jams + 1 × Djembe

We then traded the basket directionally whenever its quoted price diverged from this synthetic value by more than a threshold. To reduce latency and execution complexity, we avoided trading all legs simultaneously and instead focused on the basket itself.

Picnic Basket 2

We tested the same logic on Basket 2:

Synthetic = 4 × Croissants + 2 × Jams

But Basket 2 proved harder to trade consistently. Correlation with the synthetic was less stable, spreads were tighter, and noise was proportionally larger. Backtests showed significantly worse drawdowns, so we dropped it from the live book in that round.

Round 3

Round 3 introduced Volcanic Rock and five Volcanic Rock vouchers, which effectively behaved as European call options with seven in-game days to expiry.

Squid Ink

Squid Ink once again underperformed, which pushed us toward a simpler mean-reversion model. We replaced the previous logic with a z-score / EMA-based setup and kept position sizes very small to limit further damage.

Picnic Baskets

We made modest improvements to the basket strategies, including using volume-weighted mids and re-tuning thresholds.

Volcanic Rock

For the underlying itself, we ran a position-sensitive dynamic market-making strategy that adjusted quoting aggressiveness based on both inventory and recent execution pressure.

Volcanic Rock Vouchers

We initially focused on the 10,000 and 10,250 strike vouchers, which were the most attractive based on moneyness and liquidity. We priced them using Black-Scholes, inferred implied volatility from market prices, and compared that to a rolling reference level. When deviations were large enough, we traded volatility directionally by buying underpriced premium and selling overpriced premium.

Round 4

Round 4 introduced Magnificent Macarons, a conversion-based product influenced by sunlight, sugar prices, transport fees, tariffs, and storage costs.

Squid Ink

After repeated rewrites and continued losses, we finally gave up on Squid Ink. At that point, it had become a sink of engineering time without delivering reliable PnL.

Picnic Basket 1

We improved Basket 1 by smoothing the synthetic value with an EMA, introducing separate entry and exit thresholds, and layering orders across multiple price levels to improve fill probability.

Picnic Basket 2

We applied the same structural improvements to Basket 2 and tuned the thresholds in our own backtester.

Volcanic Rock and vouchers

We revisited the options sleeve in more depth. We found that the 9500 and 9750 vouchers were now deeply in the money and closely co-moved with the underlying, so we applied a mean-reversion framework similar to the one used for Volcanic Rock. The 10,000 voucher remained close to at-the-money, so we continued using implied-volatility z-score arbitrage. The 10,250 voucher sat in an intermediate region, and we reused the 10,000-strike logic there as well.

Magnificent Macarons

We explored several regression-based fair-value models using sunlight and sugar prices, but the combination of unstable dependencies, strict conversion constraints, and inventory-storage costs made the product far more complex than it looked. With exams approaching and limited time, we chose not to trade Macarons in that round.

Round 5

No new products were introduced in the final round, but the exchange began revealing counterparty identities, which enabled trader-specific signal extraction.

By then we were around 15th globally, and our priority shifted from upside maximization to protecting rank by avoiding large negative PnL.

Volcanic Rock vouchers

We refined our strike selection based on updated volatility analysis. The 10,250 voucher was removed because it appeared likely to remain deeply out of the money. The 10,000 voucher remained active using the same IV-based logic, while the 9500 and 9750 vouchers continued under the mean-reversion approach tied to Volcanic Rock.

Magnificent Macarons

We finally introduced a very conservative, one-sided arbitrage strategy. Whenever the local bid exceeded Pristine Cuisine’s adjusted ask—including transport and import fees—we sold locally and converted from Pristine Cuisine. We disabled the reverse direction because export tariffs made it rarely worthwhile. This created a safe, low-frequency source of alpha with essentially zero directional exposure.

Signal-based trading using trader identities

We performed a broad analysis of all traders, plotting their trades across products and studying their interactions. Olivia once again emerged as the clearest source of predictive information, particularly in:

Squid Ink
Croissants
Kelp

Knowing that many teams would likely have identified the same signal, we focused on execution quality as the differentiator. Rather than simply crossing the best bid or ask when Olivia traded, we placed layered limit orders across multiple price levels, distributing volume according to confidence and historical fill behavior. This turned a widely known signal into a more differentiated source of realized alpha.
