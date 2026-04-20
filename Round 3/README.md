






**Note:** Out of respect for the moderators' request, I will not share specific code or substantial spoilers while rounds are active. Instead, I will provide high-level descriptions of the assets until the conclusion of each round.




## Round 3: Notes
WE do not yet know what the assets for round 3, 4 and 5 will be and at current we don't have data for those either.
But we can build ourselves some suspecions based on previous years.

## Commodities and external factors
Orchids were introduced in round 2, as well as a bunch of data on sunlight, humidity, import/export tariffs, and shipping costs. The premise was that orchids were grown on a separate island4, and had to be imported–subject to import tariffs and shipping costs, and that they would degrade with suboptimal levels of sunlight and humidity. We were able to trade orchids both in a market on our own island, as well as through importing them from the South archipelago. With this, we had two initial approaches. The obvious approach, to us, was to look for alpha in all the data available, investigating if the price of orchids could be predicted using sunlight, humidity, etc. The other approach involved understanding exactly how the mechanisms for trading orchids worked, as the documentation was fairly unclear. Thus, we split up: Eric looked for alpha in the historical data while Jerry worked on understanding the actual trading environment.

Finding tradable correlations in the historical data was tougher than we initially thought. Some things that we tried were5:

Just trying to find correlations to orchids returns from returns in sunlight, humidity, tarriffs, costs. Initial results from this seemed interesting–but the correlations we found here were likely spurious.
Linear regressions from returns in sunlight, humidity, etc., to returns in orchids. We tried varying timeframes–first predicting orchids returns in the same timeframe as the returns in the predictors, and then predicting using lagged returns–building models that predicted future orchids returns over some timeframe using past returns in each of the predictors.
Feature engineering with the various features given and performing the previous two steps again with the newly constructed features
All of these failed to leave us with a convincing model, leading us to believe that the data given was a bit of a distraction6.

Meanwhile, Jerry was having much better luck. In experimenting around with the trading environment, we realized that there was a massive taker in the local orchids market. Sell orders–and just sell orders–just a bit above the best bids would be instantly taken for full size. This, combined with low implied ask prices from the foreign market, meant that we could simply put large sell orders locally and simultaneously buy from the south archipelago for an arbitrage. As a first pass, our algorithm running this strategy made 60k seashells over over a fifth of a day. From here, some quick further optimization brought our website test pnl to just over 100k seashells, giving us a projected profit of 500k over a full day.

While we figured this out independently, someone in the discord leaked this same strategy–which was quite unfortunate from our standpoint, as we knew that many teams would be able to implement the exact same thing and get the same pnl as us. With some noise from slight differences in implementation, we knew that we very well could end up dropping many places, if other teams with the same strategy simply got a bit luckier. So, we spent lots of time desperately searching for any further optimization on the arbitrage. We tested out different prices for sell orders in the local market, and found that using a price of foreign ask price - 2 worked best. However, with this fixed level for our sell orders, we worried about changes in the market preventing this level from being consistently filled. As such, we came up with an "adaptive edge" algorithm, which looked at how much volume we got at each iteration (with the maximum, nominal volume being 100 lots). If the average volume we received was below some threshold, we'd start moving our sell order level around, automatically searching for a new level to maximize profits.

Even with these optimizations, we still were beat out by the surge of teams who also found the arbitrage. We dropped all the way to 17th place, with a profit of 573,000 seashells from algo trading. We were within 20k of the second place team, and 100k away from the first place team, Puerto Vallarta, who seemed to have figured something out this round that no other teams could find.

```
def orchids_implied_bid_ask(
        self,
        observation: ConversionObservation,
    ) -> (float, float):
        return (
            observation.bidPrice - observation.exportTariff - observation.transportFees,
            observation.askPrice + observation.importTariff + observation.transportFees,
        )

    def orchids_arb_take(
        self,
        order_depth: OrderDepth,
        observation: ConversionObservation,
        position: int,
    ) -> (List[Order], int, int):
        orders: List[Order] = []
        position_limit = self.LIMIT[Product.ORCHIDS]
        buy_order_volume = 0
        sell_order_volume = 0

        implied_bid, implied_ask = self.orchids_implied_bid_ask(observation)

        buy_quantity = position_limit - position
        sell_quantity = position_limit + position

        ask = round(observation.askPrice) - 2

        if ask > implied_ask:
            edge = (ask - implied_ask) * self.params[Product.ORCHIDS][
                "make_probability"
            ]
        else:
            edge = 0

        for price in sorted(list(order_depth.sell_orders.keys())):
            if price > implied_bid - 0.1 - edge:
                break

            if price < implied_bid - 0.1 - edge:
                quantity = min(
                    abs(order_depth.sell_orders[price]), buy_quantity
                )  # max amount to buy
                if quantity > 0:
                    orders.append(Order(Product.ORCHIDS, round(price), quantity))
                    buy_order_volume += quantity

        for price in sorted(list(order_depth.buy_orders.keys()), reverse=True):
            if price < implied_ask + edge:
                break

            if price > implied_ask + edge:
                quantity = min(
                    abs(order_depth.buy_orders[price]), sell_quantity
                )  # max amount to sell
                if quantity > 0:
                    orders.append(Order(Product.ORCHIDS, round(price), -quantity))
                    sell_order_volume += quantity

        return orders, buy_order_volume, sell_order_volume

    def orchids_arb_clear(self, position: int) -> int:
        conversions = -position
        return conversions

    def orchids_arb_make(
        self,
        observation: ConversionObservation,
        position: int,
        buy_order_volume: int,
        sell_order_volume: int,
    ) -> (List[Order], int, int):
        orders: List[Order] = []
        position_limit = self.LIMIT[Product.ORCHIDS]

        # Implied Bid = observation.bidPrice - observation.exportTariff - observation.transportFees - 0.1
        # Implied Ask = observation.askPrice + observation.importTariff + observation.transportFees
        implied_bid, implied_ask = self.orchids_implied_bid_ask(observation)

        aggressive_ask = round(observation.askPrice) - 2
        aggressive_bid = round(observation.bidPrice) + 2

        if aggressive_bid < implied_bid - 0.1:
            bid = aggressive_bid
        else:
            bid = implied_bid - 0.1 - 1

        if aggressive_ask >= implied_ask + 0.5:
            ask = aggressive_ask
        elif aggressive_ask + 1 >= implied_ask + 0.5:
            ask = aggressive_ask + 1
        else:
            ask = implied_ask + 2

        print(f"ALGO_ASK: {round(ask)}")
        print(f"IMPLIED_BID: {implied_bid}")
        print(f"IMPLIED_ASK: {implied_ask}")
        print(f"FOREIGN_ASK: {observation.askPrice}")
        print(f"FOREIGN_BID: {observation.bidPrice}")

        buy_quantity = position_limit - (position + buy_order_volume)
        if buy_quantity > 0:
            orders.append(Order(Product.ORCHIDS, round(bid), buy_quantity))

        sell_quantity = position_limit + (position - sell_order_volume)
        if sell_quantity > 0:
            orders.append(Order(Product.ORCHIDS, round(ask), -sell_quantity))

        return orders, buy_order_volume, sell_order_volume

```

## ETF/Basket arbitrage

Gift baskets 🧺, chocolate 🍫, roses 🌹, and strawberries 🍓 were introduced in round 3, where a gift basket consisted of 4 chocolate bars, 6 strawberries, and a single rose. This round, we mainly traded spreads, which we defined as `basket - synthetic`, with `synthetic` being the sum of the price of all products in a basket.
spread 🧈
In this round, we quickly converged on two hypotheses. The first hypothesis was that the synthetic would be leading baskets or vice versa, where changes in the price of one would lead to later changes in the price of the other. Our second hypothesis was that the spread might simply just be mean reverting. We observed that the price of the spread–which theoretically should be 0–hovered around some fixed value, which we could trade around. We looked into leading/lagging relationships between the synthetic and the basket, but this wasn't very fruitful, so we then investigated the spread price.

newplot (1)

Looking at the spread, we found that the price oscillated around ~370 across all three days of our historical data. Thus, we could profitably trade a mean-reverting strategy, buying spreads (going long baskets and short synthetic) when the spread price was below average, and selling spreads when the price was above. We tried various different ways to parameterize this trade. Due to our position limits, which were relatively small (about 2x the volume on the book at any instant), and the relatively small number of mean-reverting trading opportunities, we realized that timing the trade correctly was critical, and could result in a large amount of additional pnl.

We tried various approaches in parameterizing this trade. A simple, first-pass strategy was just to set hardcoded prices at which to trade–for example, trading only when the spread deviated from the average value by a certain amount. We backtested to optimize these hardcoded thresholds, and our best parameters netted us ~120k in projected pnl7. However, with this strategy, we noticed that we could lose out on a lot of pnl if the spread price reverted before touching our threshold. To remedy this, we could set our thresholds closer, but then we'd also lose pnl from trading before the spread price reached a local max/min.

Therefore, we developed a more adaptive algorithm for spreads. We traded on a modified z-score, using a hardcoded mean and a rolling window standard deviation, with the window set relatively small. The idea behind this was that there should be a fundamental reason behind the mean of spread (think the price of the basket itself), but the volatility each day would be less predictable. Then, we thresholded the z-score, selling spreads when our z-score went above a certain value and buying when the z-score dropped below. By using a small window for our rolling standard deviation, we'd see our z-score spike when the standard deviation drastically dropped–and this would often happen right as the price started reverting, allowing us to trade closer to local minima/maxima. This idea bumped our backtest pnl up to ~135k.

newplot (2)

a plot of spread prices and our modified z-score, as well as z-score thresholds (in green) to trade at

After results from this round were released, we found that our actual pnl had a significant amount of slippage compared to our backtests–we made only 111k seashells from our algo. Nevertheless, we got a bit lucky–all the teams ahead of us in this round seemed to overfit significantly more, as we were ranked #2 overall.

```
def get_synthetic_basket_order_depth(
        self, order_depths: Dict[str, OrderDepth]
    ) -> OrderDepth:
        # Constants
        CHOCOLATE_PER_BASKET = BASKET_WEIGHTS[Product.CHOCOLATE]
        STRAWBERRIES_PER_BASKET = BASKET_WEIGHTS[Product.STRAWBERRIES]
        ROSES_PER_BASKET = BASKET_WEIGHTS[Product.ROSES]

        # Initialize the synthetic basket order depth
        synthetic_order_price = OrderDepth()

        # Calculate the best bid and ask for each component
        chocolate_best_bid = (
            max(order_depths[Product.CHOCOLATE].buy_orders.keys())
            if order_depths[Product.CHOCOLATE].buy_orders
            else 0
        )
        chocolate_best_ask = (
            min(order_depths[Product.CHOCOLATE].sell_orders.keys())
            if order_depths[Product.CHOCOLATE].sell_orders
            else float("inf")
        )
        strawberries_best_bid = (
            max(order_depths[Product.STRAWBERRIES].buy_orders.keys())
            if order_depths[Product.STRAWBERRIES].buy_orders
            else 0
        )
        strawberries_best_ask = (
            min(order_depths[Product.STRAWBERRIES].sell_orders.keys())
            if order_depths[Product.STRAWBERRIES].sell_orders
            else float("inf")
        )
        roses_best_bid = (
            max(order_depths[Product.ROSES].buy_orders.keys())
            if order_depths[Product.ROSES].buy_orders
            else 0
        )
        roses_best_ask = (
            min(order_depths[Product.ROSES].sell_orders.keys())
            if order_depths[Product.ROSES].sell_orders
            else float("inf")
        )

        # Calculate the implied bid and ask for the synthetic basket
        implied_bid = (
            chocolate_best_bid * CHOCOLATE_PER_BASKET
            + strawberries_best_bid * STRAWBERRIES_PER_BASKET
            + roses_best_bid * ROSES_PER_BASKET
        )
        implied_ask = (
            chocolate_best_ask * CHOCOLATE_PER_BASKET
            + strawberries_best_ask * STRAWBERRIES_PER_BASKET
            + roses_best_ask * ROSES_PER_BASKET
        )

        # Calculate the maximum number of synthetic baskets available at the implied bid and ask
        if implied_bid > 0:
            chocolate_bid_volume = (
                order_depths[Product.CHOCOLATE].buy_orders[chocolate_best_bid]
                // CHOCOLATE_PER_BASKET
            )
            strawberries_bid_volume = (
                order_depths[Product.STRAWBERRIES].buy_orders[strawberries_best_bid]
                // STRAWBERRIES_PER_BASKET
            )
            roses_bid_volume = (
                order_depths[Product.ROSES].buy_orders[roses_best_bid]
                // ROSES_PER_BASKET
            )
            implied_bid_volume = min(
                chocolate_bid_volume, strawberries_bid_volume, roses_bid_volume
            )
            synthetic_order_price.buy_orders[implied_bid] = implied_bid_volume

        if implied_ask < float("inf"):
            chocolate_ask_volume = (
                -order_depths[Product.CHOCOLATE].sell_orders[chocolate_best_ask]
                // CHOCOLATE_PER_BASKET
            )
            strawberries_ask_volume = (
                -order_depths[Product.STRAWBERRIES].sell_orders[strawberries_best_ask]
                // STRAWBERRIES_PER_BASKET
            )
            roses_ask_volume = (
                -order_depths[Product.ROSES].sell_orders[roses_best_ask]
                // ROSES_PER_BASKET
            )
            implied_ask_volume = min(
                chocolate_ask_volume, strawberries_ask_volume, roses_ask_volume
            )
            synthetic_order_price.sell_orders[implied_ask] = -implied_ask_volume

        return synthetic_order_price

    def convert_synthetic_basket_orders(
        self, synthetic_orders: List[Order], order_depths: Dict[str, OrderDepth]
    ) -> Dict[str, List[Order]]:
        # Initialize the dictionary to store component orders
        component_orders = {
            Product.CHOCOLATE: [],
            Product.STRAWBERRIES: [],
            Product.ROSES: [],
        }

        # Get the best bid and ask for the synthetic basket
        synthetic_basket_order_depth = self.get_synthetic_basket_order_depth(
            order_depths
        )
        best_bid = (
            max(synthetic_basket_order_depth.buy_orders.keys())
            if synthetic_basket_order_depth.buy_orders
            else 0
        )
        best_ask = (
            min(synthetic_basket_order_depth.sell_orders.keys())
            if synthetic_basket_order_depth.sell_orders
            else float("inf")
        )

        # Iterate through each synthetic basket order
        for order in synthetic_orders:
            # Extract the price and quantity from the synthetic basket order
            price = order.price
            quantity = order.quantity

            # Check if the synthetic basket order aligns with the best bid or ask
            if quantity > 0 and price >= best_ask:
                # Buy order - trade components at their best ask prices
                chocolate_price = min(
                    order_depths[Product.CHOCOLATE].sell_orders.keys()
                )
                strawberries_price = min(
                    order_depths[Product.STRAWBERRIES].sell_orders.keys()
                )
                roses_price = min(order_depths[Product.ROSES].sell_orders.keys())
            elif quantity < 0 and price <= best_bid:
                # Sell order - trade components at their best bid prices
                chocolate_price = max(order_depths[Product.CHOCOLATE].buy_orders.keys())
                strawberries_price = max(
                    order_depths[Product.STRAWBERRIES].buy_orders.keys()
                )
                roses_price = max(order_depths[Product.ROSES].buy_orders.keys())
            else:
                # The synthetic basket order does not align with the best bid or ask
                continue

            # Create orders for each component
            chocolate_order = Order(
                Product.CHOCOLATE,
                chocolate_price,
                quantity * BASKET_WEIGHTS[Product.CHOCOLATE],
            )
            strawberries_order = Order(
                Product.STRAWBERRIES,
                strawberries_price,
                quantity * BASKET_WEIGHTS[Product.STRAWBERRIES],
            )
            roses_order = Order(
                Product.ROSES, roses_price, quantity * BASKET_WEIGHTS[Product.ROSES]
            )

            # Add the component orders to the respective lists
            component_orders[Product.CHOCOLATE].append(chocolate_order)
            component_orders[Product.STRAWBERRIES].append(strawberries_order)
            component_orders[Product.ROSES].append(roses_order)

        return component_orders

    def execute_spread_orders(
        self,
        target_position: int,
        basket_position: int,
        order_depths: Dict[str, OrderDepth],
    ):

        if target_position == basket_position:
            return None

        target_quantity = abs(target_position - basket_position)
        basket_order_depth = order_depths[Product.GIFT_BASKET]
        synthetic_order_depth = self.get_synthetic_basket_order_depth(order_depths)

        if target_position > basket_position:
            basket_ask_price = min(basket_order_depth.sell_orders.keys())
            basket_ask_volume = abs(basket_order_depth.sell_orders[basket_ask_price])

            synthetic_bid_price = max(synthetic_order_depth.buy_orders.keys())
            synthetic_bid_volume = abs(
                synthetic_order_depth.buy_orders[synthetic_bid_price]
            )

            orderbook_volume = min(basket_ask_volume, synthetic_bid_volume)
            execute_volume = min(orderbook_volume, target_quantity)

            basket_orders = [
                Order(Product.GIFT_BASKET, basket_ask_price, execute_volume)
            ]
            synthetic_orders = [
                Order(Product.SYNTHETIC, synthetic_bid_price, -execute_volume)
            ]

            aggregate_orders = self.convert_synthetic_basket_orders(
                synthetic_orders, order_depths
            )
            aggregate_orders[Product.GIFT_BASKET] = basket_orders
            return aggregate_orders

        else:
            basket_bid_price = max(basket_order_depth.buy_orders.keys())
            basket_bid_volume = abs(basket_order_depth.buy_orders[basket_bid_price])

            synthetic_ask_price = min(synthetic_order_depth.sell_orders.keys())
            synthetic_ask_volume = abs(
                synthetic_order_depth.sell_orders[synthetic_ask_price]
            )

            orderbook_volume = min(basket_bid_volume, synthetic_ask_volume)
            execute_volume = min(orderbook_volume, target_quantity)

            basket_orders = [
                Order(Product.GIFT_BASKET, basket_bid_price, -execute_volume)
            ]
            synthetic_orders = [
                Order(Product.SYNTHETIC, synthetic_ask_price, execute_volume)
            ]

            aggregate_orders = self.convert_synthetic_basket_orders(
                synthetic_orders, order_depths
            )
            aggregate_orders[Product.GIFT_BASKET] = basket_orders
            return aggregate_orders

    def spread_orders(
        self,
        order_depths: Dict[str, OrderDepth],
        product: Product,
        basket_position: int,
        spread_data: Dict[str, Any],
    ):
        if Product.GIFT_BASKET not in order_depths.keys():
            return None

        basket_order_depth = order_depths[Product.GIFT_BASKET]
        synthetic_order_depth = self.get_synthetic_basket_order_depth(order_depths)
        basket_swmid = self.get_swmid(basket_order_depth)
        synthetic_swmid = self.get_swmid(synthetic_order_depth)
        spread = basket_swmid - synthetic_swmid
        spread_data["spread_history"].append(spread)

        if (
            len(spread_data["spread_history"])
            < self.params[Product.SPREAD]["spread_std_window"]
        ):
            return None
        elif (
            len(spread_data["spread_history"])
            > self.params[Product.SPREAD]["spread_std_window"]
        ):
            spread_data["spread_history"].pop(0)

        spread_std = np.std(spread_data["spread_history"])

        zscore = (
            spread - self.params[Product.SPREAD]["default_spread_mean"]
        ) / spread_std

        if zscore >= self.params[Product.SPREAD]["zscore_threshold"]:
            if basket_position != -self.params[Product.SPREAD]["target_position"]:
                return self.execute_spread_orders(
                    -self.params[Product.SPREAD]["target_position"],
                    basket_position,
                    order_depths,
                )

        if zscore <= -self.params[Product.SPREAD]["zscore_threshold"]:
            if basket_position != self.params[Product.SPREAD]["target_position"]:
                return self.execute_spread_orders(
                    self.params[Product.SPREAD]["target_position"],
                    basket_position,
                    order_depths,
                )

        spread_data["prev_zscore"] = zscore
        return None
```


## Location arbitrage




## Derivatives/underlying
coconuts/coconut coupon 🥥
Coconuts and coconut coupons were introduced in round 4. Coconut coupons were the 10,000 strike call option on coconuts, with a time to expiry of 250 days. The price of coconuts hovered around 10,000, so this option was near-the-money.

This round was fairly simple. Using Black-Scholes, we calculated the implied volatility of the option, and once we plotted this out, it became clear that the implied vol oscillated around a value of ~16%. We implemented a mean reverting strategy similar to round 3, and calculated the delta of the coconut coupons at each time in order to hedge with coconuts and gain pure exposure to vol. However, the delta was around 0.53 while the position limits for coconuts/coconut coupons were 300/600, respectively. This meant that we couldn't be fully hedged when holding 600 coupons (we would be holding 18 delta). Since the coupon was far away from expiry (thus, gamma didn't matter as much) and holding delta with vega was still positive ev (but higher var), we ran the variance in hopes of making more from our exposure to vol.

newplot (3)

While holding this variance worked out in our backtests, we experienced a fair amount of slippage in our submission–we got unlucky and lost money from our delta exposure. In retrospect, not fully delta hedging might not have been a smart move–we were already second place and thus should've went for lower var to try and keep the lead. Our algorithm in this round made only 145k, dropping us down to a terrifying 26th place. However, in the results of this round, we saw Puerto Vallarta leap ahead with a whopping profit of 1.2 million seashells. We knew we could catch up and end up well within the top 10 if only we could figure out what they did.



```
class BlackScholes:
    @staticmethod
    def black_scholes_call(spot, strike, time_to_expiry, volatility):
        d1 = (
            log(spot) - log(strike) + (0.5 * volatility * volatility) * time_to_expiry
        ) / (volatility * sqrt(time_to_expiry))
        d2 = d1 - volatility * sqrt(time_to_expiry)
        call_price = spot * NormalDist().cdf(d1) - strike * NormalDist().cdf(d2)
        return call_price

    @staticmethod
    def black_scholes_put(spot, strike, time_to_expiry, volatility):
        d1 = (log(spot / strike) + (0.5 * volatility * volatility) * time_to_expiry) / (
            volatility * sqrt(time_to_expiry)
        )
        d2 = d1 - volatility * sqrt(time_to_expiry)
        put_price = strike * NormalDist().cdf(-d2) - spot * NormalDist().cdf(-d1)
        return put_price

    @staticmethod
    def delta(spot, strike, time_to_expiry, volatility):
        d1 = (
            log(spot) - log(strike) + (0.5 * volatility * volatility) * time_to_expiry
        ) / (volatility * sqrt(time_to_expiry))
        return NormalDist().cdf(d1)

    @staticmethod
    def gamma(spot, strike, time_to_expiry, volatility):
        d1 = (
            log(spot) - log(strike) + (0.5 * volatility * volatility) * time_to_expiry
        ) / (volatility * sqrt(time_to_expiry))
        return NormalDist().pdf(d1) / (spot * volatility * sqrt(time_to_expiry))

    @staticmethod
    def vega(spot, strike, time_to_expiry, volatility):
        d1 = (
            log(spot) - log(strike) + (0.5 * volatility * volatility) * time_to_expiry
        ) / (volatility * sqrt(time_to_expiry))
        # print(f"d1: {d1}")
        # print(f"vol: {volatility}")
        # print(f"spot: {spot}")
        # print(f"strike: {strike}")
        # print(f"time: {time_to_expiry}")
        return NormalDist().pdf(d1) * (spot * sqrt(time_to_expiry)) / 100

    @staticmethod
    def implied_volatility(
        call_price, spot, strike, time_to_expiry, max_iterations=200, tolerance=1e-10
    ):
        low_vol = 0.01
        high_vol = 1.0
        volatility = (low_vol + high_vol) / 2.0  # Initial guess as the midpoint
        for _ in range(max_iterations):
            estimated_price = BlackScholes.black_scholes_call(
                spot, strike, time_to_expiry, volatility
            )
            diff = estimated_price - call_price
            if abs(diff) < tolerance:
                break
            elif diff > 0:
                high_vol = volatility
            else:
                low_vol = volatility
            volatility = (low_vol + high_vol) / 2.0
        return volatility

 def get_coconut_coupon_mid_price(
        self, coconut_coupon_order_depth: OrderDepth, traderData: Dict[str, Any]
    ):
        if (
            len(coconut_coupon_order_depth.buy_orders) > 0
            and len(coconut_coupon_order_depth.sell_orders) > 0
        ):
            best_bid = max(coconut_coupon_order_depth.buy_orders.keys())
            best_ask = min(coconut_coupon_order_depth.sell_orders.keys())
            traderData["prev_coupon_price"] = (best_bid + best_ask) / 2
            return (best_bid + best_ask) / 2
        else:
            return traderData["prev_coupon_price"]

    def delta_hedge_coconut_position(
        self,
        coconut_order_depth: OrderDepth,
        coconut_coupon_position: int,
        coconut_position: int,
        coconut_buy_orders: int,
        coconut_sell_orders: int,
        delta: float,
    ) -> List[Order]:
        """
        Delta hedge the overall position in COCONUT_COUPON by creating orders in COCONUT.

        Args:
            coconut_order_depth (OrderDepth): The order depth for the COCONUT product.
            coconut_coupon_position (int): The current position in COCONUT_COUPON.
            coconut_position (int): The current position in COCONUT.
            coconut_buy_orders (int): The total quantity of buy orders for COCONUT in the current iteration.
            coconut_sell_orders (int): The total quantity of sell orders for COCONUT in the current iteration.
            delta (float): The current value of delta for the COCONUT_COUPON product.
            traderData (Dict[str, Any]): The trader data for the COCONUT_COUPON product.

        Returns:
            List[Order]: A list of orders to delta hedge the COCONUT_COUPON position.
        """

        target_coconut_position = -int(delta * coconut_coupon_position)
        hedge_quantity = target_coconut_position - (
            coconut_position + coconut_buy_orders - coconut_sell_orders
        )

        orders: List[Order] = []
        if hedge_quantity > 0:
            # Buy COCONUT
            best_ask = min(coconut_order_depth.sell_orders.keys())
            quantity = min(
                abs(hedge_quantity), -coconut_order_depth.sell_orders[best_ask]
            )
            quantity = min(
                quantity,
                self.LIMIT[Product.COCONUT] - (coconut_position + coconut_buy_orders),
            )
            if quantity > 0:
                orders.append(Order(Product.COCONUT, best_ask, quantity))
        elif hedge_quantity < 0:
            # Sell COCONUT
            best_bid = max(coconut_order_depth.buy_orders.keys())
            quantity = min(
                abs(hedge_quantity), coconut_order_depth.buy_orders[best_bid]
            )
            quantity = min(
                quantity,
                self.LIMIT[Product.COCONUT] + (coconut_position - coconut_sell_orders),
            )
            if quantity > 0:
                orders.append(Order(Product.COCONUT, best_bid, -quantity))

        return orders

    def delta_hedge_coconut_coupon_orders(
        self,
        coconut_order_depth: OrderDepth,
        coconut_coupon_orders: List[Order],
        coconut_position: int,
        coconut_buy_orders: int,
        coconut_sell_orders: int,
        delta: float,
    ) -> List[Order]:
        """
        Delta hedge the new orders for COCONUT_COUPON by creating orders in COCONUT.

        Args:
            coconut_order_depth (OrderDepth): The order depth for the COCONUT product.
            coconut_coupon_orders (List[Order]): The new orders for COCONUT_COUPON.
            coconut_position (int): The current position in COCONUT.
            coconut_buy_orders (int): The total quantity of buy orders for COCONUT in the current iteration.
            coconut_sell_orders (int): The total quantity of sell orders for COCONUT in the current iteration.
            delta (float): The current value of delta for the COCONUT_COUPON product.

        Returns:
            List[Order]: A list of orders to delta hedge the new COCONUT_COUPON orders.
        """
        if len(coconut_coupon_orders) == 0:
            return None

        net_coconut_coupon_quantity = sum(
            order.quantity for order in coconut_coupon_orders
        )
        target_coconut_quantity = -int(delta * net_coconut_coupon_quantity)

        orders: List[Order] = []
        if target_coconut_quantity > 0:
            # Buy COCONUT
            best_ask = min(coconut_order_depth.sell_orders.keys())
            quantity = min(
                abs(target_coconut_quantity), -coconut_order_depth.sell_orders[best_ask]
            )
            quantity = min(
                quantity,
                self.LIMIT[Product.COCONUT] - (coconut_position + coconut_buy_orders),
            )
            if quantity > 0:
                orders.append(Order(Product.COCONUT, best_ask, quantity))
        elif target_coconut_quantity < 0:
            # Sell COCONUT
            best_bid = max(coconut_order_depth.buy_orders.keys())
            quantity = min(
                abs(target_coconut_quantity), coconut_order_depth.buy_orders[best_bid]
            )
            quantity = min(
                quantity,
                self.LIMIT[Product.COCONUT] + (coconut_position - coconut_sell_orders),
            )
            if quantity > 0:
                orders.append(Order(Product.COCONUT, best_bid, -quantity))

        return orders

    def coconut_hedge_orders(
        self,
        coconut_order_depth: OrderDepth,
        coconut_coupon_order_depth: OrderDepth,
        coconut_coupon_orders: List[Order],
        coconut_position: int,
        coconut_coupon_position: int,
        delta: float,
    ) -> List[Order]:
        if coconut_coupon_orders == None or len(coconut_coupon_orders) == 0:
            coconut_coupon_position_after_trade = coconut_coupon_position
        else:
            coconut_coupon_position_after_trade = coconut_coupon_position + sum(
                order.quantity for order in coconut_coupon_orders
            )

        target_coconut_position = -delta * coconut_coupon_position_after_trade

        if target_coconut_position == coconut_position:
            return None

        target_coconut_quantity = target_coconut_position - coconut_position

        orders: List[Order] = []
        if target_coconut_quantity > 0:
            # Buy COCONUT
            best_ask = min(coconut_order_depth.sell_orders.keys())
            quantity = min(
                abs(target_coconut_quantity),
                self.LIMIT[Product.COCONUT] - coconut_position,
            )
            if quantity > 0:
                orders.append(Order(Product.COCONUT, best_ask, round(quantity)))

        elif target_coconut_quantity < 0:
            # Sell COCONUT
            best_bid = max(coconut_order_depth.buy_orders.keys())
            quantity = min(
                abs(target_coconut_quantity),
                self.LIMIT[Product.COCONUT] + coconut_position,
            )
            if quantity > 0:
                orders.append(Order(Product.COCONUT, best_bid, -round(quantity)))

        return orders

    def coconut_coupon_orders(
        self,
        coconut_coupon_order_depth: OrderDepth,
        coconut_coupon_position: int,
        traderData: Dict[str, Any],
        volatility: float,
    ) -> List[Order]:
        traderData["past_coupon_vol"].append(volatility)
        if (
            len(traderData["past_coupon_vol"])
            < self.params[Product.COCONUT_COUPON]["std_window"]
        ):
            return None, None

        if (
            len(traderData["past_coupon_vol"])
            > self.params[Product.COCONUT_COUPON]["std_window"]
        ):
            traderData["past_coupon_vol"].pop(0)

        vol_z_score = (
            volatility - self.params[Product.COCONUT_COUPON]["mean_volatility"]
        ) / np.std(traderData["past_coupon_vol"])
        # print(f"vol_z_score: {vol_z_score}")
        # print(f"zscore_threshold: {self.params[Product.COCONUT_COUPON]['zscore_threshold']}")
        if vol_z_score >= self.params[Product.COCONUT_COUPON]["zscore_threshold"]:
            if coconut_coupon_position != -self.LIMIT[Product.COCONUT_COUPON]:
                target_coconut_coupon_position = -self.LIMIT[Product.COCONUT_COUPON]
                if len(coconut_coupon_order_depth.buy_orders) > 0:
                    best_bid = max(coconut_coupon_order_depth.buy_orders.keys())
                    target_quantity = abs(
                        target_coconut_coupon_position - coconut_coupon_position
                    )
                    quantity = min(
                        target_quantity,
                        abs(coconut_coupon_order_depth.buy_orders[best_bid]),
                    )
                    quote_quantity = target_quantity - quantity
                    if quote_quantity == 0:
                        return [Order(Product.COCONUT_COUPON, best_bid, -quantity)], []
                    else:
                        return [Order(Product.COCONUT_COUPON, best_bid, -quantity)], [
                            Order(Product.COCONUT_COUPON, best_bid, -quote_quantity)
                        ]

        elif vol_z_score <= -self.params[Product.COCONUT_COUPON]["zscore_threshold"]:
            if coconut_coupon_position != self.LIMIT[Product.COCONUT_COUPON]:
                target_coconut_coupon_position = self.LIMIT[Product.COCONUT_COUPON]
                if len(coconut_coupon_order_depth.sell_orders) > 0:
                    best_ask = min(coconut_coupon_order_depth.sell_orders.keys())
                    target_quantity = abs(
                        target_coconut_coupon_position - coconut_coupon_position
                    )
                    quantity = min(
                        target_quantity,
                        abs(coconut_coupon_order_depth.sell_orders[best_ask]),
                    )
                    quote_quantity = target_quantity - quantity
                    if quote_quantity == 0:
                        return [Order(Product.COCONUT_COUPON, best_ask, quantity)], []
                    else:
                        return [Order(Product.COCONUT_COUPON, best_ask, quantity)], [
                            Order(Product.COCONUT_COUPON, best_ask, quote_quantity)
                        ]

        return None, None

```




















## Insider trading.
Our leading hypothesis in trying to replicate Puerto Vallarta's profits were that they must've found some way to predict the future–profits on the order of 1.2 million could reasonably match up with a successful stat. arb strategy across multiple symbols. So, we started blasting away with linear regressions on lagged and synchronous returns across all symbols and all days of our data, with the hypothesis that symbols from different days could have correlations that we'd previously missed. However, we didn't find anything particularly interesting here–starfruits seemed to have a bit of lagged predictive power in all other symbols, but this couldn't explain 1.2 million in additional profits.

As a last-ditch attempt in this front, we recalled that last year's competition (which we read about in Stanford Cardinal's awesome writeup) had many similarities to this competition–especially in the first round, where the symbols we traded basically sounded the exact same. So, we went and sourced last year's data from public GitHub repositories, and performed a linear regression from returns in each of last year's symbols to returns in each symbol of this year. The results we found were surprising: diving gear returns from last year's competition, with a multiplier of ~3, was almost a perfect predictor of roses, with a 
R
2
 of 0.99. Additionally, coconuts from last year was a perfect predictor of coconuts from this year, with a beta of 1.25 and an 
R
2
 of 0.99.

image

These discoveries were quite silly, but nonetheless, our goal was to maximize pnl, and as the data from last year was publically available on the internet, we felt like this was still fair game. The rest of our efforts in this competition centered around maximizing the value we could extract from the market with our new knowledge. We believed that many other teams might find these same relationships, and therefore optimization was key.

As a first pass, we simply bought/sold coconuts and roses when our predicted price rose/fell (beyond some threshold to account for spread costs) over a certain number of future iterations. While this worked spectacularly (in comparison to our pnl from literally all previous rounds), we thought we could do better. Indeed, with the data from last year, we had all local maxima/minima, and thus we could theoretically time our trades perfectly and extract max. value.

To do this systematically across the three symbols we wanted to trade (roses, coconuts, and gift baskets, due to their natural correlation with roses), we developed a dynamic programming algorithm. Our algorithm took many factors into account–costs of crossing spread, the volume we could take at iteration (the volume on the orderbook), and our volume limits.

The motivation behind the complexity of our dp algorithm was the fact that, at each iteration, we couldn't necessarily achieve our full desired position–therefore, we needed a state for each potential position that we could feasibly achieve. A simple example of this is to imagine a product going through the following prices: 
8
→
7
→
12
→
10
 With a position limit of 2, and with sufficient volume on the orderbook, the optimal trades would be: sell 2 -> buy 4 -> sell 4, with a pnl of 16. Now imagine if you could only buy/sell 2 shares at each iteration. Then, the optimal solution would change–you'd want to buy 2 -> buy 2 -> sell 2, with an overall pnl of 14.

our dp code (click to expand)
Our inputs here were prices–we found that generating trades over the predictor timeseries was sufficient due to the high correlation–volume percentage (percent of volume limit on the orderbook at each iteration), and spread (the average spread, cost of each trade), with a target of maximizing pnl. Using this dp algorithm, we generated a string of trades for each symbol, with `'b'` or `'s'` at each index representing the action at each timestamp. Using this algorithm, we achieved an algo pnl of 2.1 million seashells–the highest over all teams in this round! This brought us to a final overall standing of second place.

```
def optimal_trading_dp(prices, spread, volume_pct):
    n = len(prices)
    price_level_cnt = math.ceil(1/volume_pct)
    left_over_pct = 1 - (price_level_cnt - 1) * volume_pct

    dp = [[float('-inf')] * (price_level_cnt * 2 + 1) for _ in range(n)]  # From -3 to 3, 7 positions
    action = [[''] * (price_level_cnt * 2 + 1) for _ in range(n)]  # To store actions

    # Initialize the starting position (no stock held)
    dp[0][price_level_cnt] = 0  # Start with no position, Cash is 0
    action[0][price_level_cnt] = ''  # No action at start

    def position(j):
        if j > price_level_cnt:
            position = min((j - price_level_cnt) * volume_pct, 1)
        elif j < price_level_cnt:
            position = max((j - price_level_cnt) * volume_pct, -1)
        else:
            position = 0
        return position
    
    def position_list(list):
        return np.array([position(x) for x in list])

    for i in range(1, n):
        for j in range(0, price_level_cnt * 2 + 1):
            # Calculate PnL for holding, buying, or selling
            hold = dp[i-1][j] if dp[i-1][j] != float('-inf') else float('-inf')
            if j == price_level_cnt * 2:
                buy = dp[i-1][j-1] - left_over_pct*prices[i-1] -  left_over_pct*spread if j > 0 else float('-inf')
            elif j == 1:
                buy = dp[i-1][j-1] - left_over_pct*prices[i-1] -  left_over_pct*spread if j > 0 else float('-inf')
            else:
                buy = dp[i-1][j-1] - volume_pct*prices[i-1] - volume_pct*spread if j > 0 else float('-inf')

            if j ==  0:
                sell = dp[i-1][j+1] + left_over_pct*prices[i-1] - left_over_pct*spread if j < price_level_cnt * 2 else float('-inf')
            elif j == price_level_cnt * 2 - 1:
                sell = dp[i-1][j+1] + left_over_pct*prices[i-1] - left_over_pct*spread if j < price_level_cnt * 2 else float('-inf')
            else:
                sell = dp[i-1][j+1] + volume_pct*prices[i-1] - volume_pct*spread if j < price_level_cnt * 2 else float('-inf')
                
            # Choose the action with the highest PnL

            hold_pnl = hold + (j - price_level_cnt) * position(j) * prices[i]
            buy_pnl = buy + (j - price_level_cnt) * position(j) * prices[i]
            sell_pnl = sell + (j - price_level_cnt) * position(j) * prices[i]
            
            # print(hold_pnl, buy_pnl, sell_pnl)
            best_action = max(hold_pnl, buy_pnl, sell_pnl)
            if best_action == hold_pnl:
                dp[i][j] = hold
            elif best_action == buy_pnl:
                dp[i][j] = buy
            else:
                dp[i][j] = sell

            if best_action == hold_pnl:
                action[i][j] = 'h'
            elif best_action == buy_pnl:
                action[i][j] = 'b'
            else:
                action[i][j] = 's'
    # Backtrack to find the sequence of actions
    trades_list = []
    # Start from the position with maximum PnL at time n-1

    pnl = np.array(dp[n-1]) + (position_list(np.arange(0,price_level_cnt*2+1)) * prices[n-1])
    current_position = np.argmax(pnl)
    for i in range(n-1, -1, -1):
        trades_list.append(action[i][current_position])
        if action[i][current_position] == 'b':
            current_position -= 1
        elif action[i][current_position] == 's':
            current_position += 1

    trades_list.reverse()
    trades_list.append('h')
    return dp, trades_list, pnl[np.argmax(pnl)]  # Return the actions and the maximum PnL

# Example usage
dp, trades, max_pnl = optimal_trading_dp(coconut_past_price, 0.99, 185/300)
# print(trades)
print("Max PnL:", max_pnl)
```


