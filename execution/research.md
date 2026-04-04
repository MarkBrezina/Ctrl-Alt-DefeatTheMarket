
## Take best orders
as given by Linear Utility 2024.

A kind of strategy?

```
def take_best_orders(
        self,
        product: str,
        fair_value: float,
        take_width: float,
        orders: List[Order],
        order_depth: OrderDepth,
        position: int,
        buy_order_volume: int,
        sell_order_volume: int,
        prevent_adverse: bool = False,
        adverse_volume: int = 0,
    ) -> (int, int):
        position_limit = self.LIMIT[product]

        if len(order_depth.sell_orders) != 0:
            best_ask = min(order_depth.sell_orders.keys())
            best_ask_amount = -1 * order_depth.sell_orders[best_ask]

            if not prevent_adverse or abs(best_ask_amount) <= adverse_volume:
                if best_ask <= fair_value - take_width:
                    quantity = min(best_ask_amount, position_limit - position - buy_order_volume)
                    if quantity > 0:
                        orders.append(Order(product, best_ask, quantity))
                        buy_order_volume += quantity
                        order_depth.sell_orders[best_ask] += quantity
                        if order_depth.sell_orders[best_ask] == 0:
                            del order_depth.sell_orders[best_ask]

        if len(order_depth.buy_orders) != 0:
            best_bid = max(order_depth.buy_orders.keys())
            best_bid_amount = order_depth.buy_orders[best_bid]

            if not prevent_adverse or abs(best_bid_amount) <= adverse_volume:
                if best_bid >= fair_value + take_width:
                    quantity = min(best_bid_amount, position_limit + position - sell_order_volume)
                    if quantity > 0:
                        orders.append(Order(product, best_bid, -1 * quantity))
                        sell_order_volume += quantity
                        order_depth.buy_orders[best_bid] -= quantity
                        if order_depth.buy_orders[best_bid] == 0:
                            del order_depth.buy_orders[best_bid]

        return buy_order_volume, sell_order_volume

```






## Market make
A kind of strategy by Linear utility

```
 def market_make(
      self,
      product: str,
      orders: List[Order],
      bid: int,
      ask: int,
      position: int,
      buy_order_volume: int,
      sell_order_volume: int,
      buy_size: int = None,
      sell_size: int = None,
  ) -> (int, int):
      max_buy_available = self.LIMIT[product] - (position + buy_order_volume)
      max_sell_available = self.LIMIT[product] + (position - sell_order_volume)

      if buy_size is None:
          buy_quantity = max_buy_available
      else:
          buy_quantity = min(buy_size, max_buy_available)

      if sell_size is None:
          sell_quantity = max_sell_available
      else:
          sell_quantity = min(sell_size, max_sell_available)

      if buy_quantity > 0:
          orders.append(Order(product, round(bid), buy_quantity))

      if sell_quantity > 0:
          orders.append(Order(product, round(ask), -sell_quantity))

      return buy_order_volume, sell_order_volume
```

## Execution logic.

```
def clear_position_order(
        self,
        product: str,
        fair_value: float,
        width: float,
        orders: List[Order],
        order_depth: OrderDepth,
        position: int,
        buy_order_volume: int,
        sell_order_volume: int,
    ) -> (int, int):
        position_after_take = position + buy_order_volume - sell_order_volume
        fair_for_bid = round(fair_value - width)
        fair_for_ask = round(fair_value + width)

        buy_quantity = self.LIMIT[product] - (position + buy_order_volume)
        sell_quantity = self.LIMIT[product] + (position - sell_order_volume)

        if position_after_take > 0:
            clear_quantity = sum(
                volume
                for price, volume in order_depth.buy_orders.items()
                if price >= fair_for_ask
            )
            clear_quantity = min(clear_quantity, position_after_take)
            sent_quantity = min(sell_quantity, clear_quantity)
            if sent_quantity > 0:
                orders.append(Order(product, fair_for_ask, -abs(sent_quantity)))
                sell_order_volume += abs(sent_quantity)

        if position_after_take < 0:
            clear_quantity = sum(
                abs(volume)
                for price, volume in order_depth.sell_orders.items()
                if price <= fair_for_bid
            )
            clear_quantity = min(clear_quantity, abs(position_after_take))
            sent_quantity = min(buy_quantity, clear_quantity)
            if sent_quantity > 0:
                orders.append(Order(product, fair_for_bid, abs(sent_quantity)))
                buy_order_volume += abs(sent_quantity)

        return buy_order_volume, sell_order_volume

    def take_orders(
        self,
        product: str,
        order_depth: OrderDepth,
        fair_value: float,
        take_width: float,
        position: int,
        prevent_adverse: bool = False,
        adverse_volume: int = 0,
    ) -> (List[Order], int, int):
        orders: List[Order] = []
        buy_order_volume = 0
        sell_order_volume = 0

        buy_order_volume, sell_order_volume = self.take_best_orders(
            product,
            fair_value,
            take_width,
            orders,
            order_depth,
            position,
            buy_order_volume,
            sell_order_volume,
            prevent_adverse,
            adverse_volume,
        )
        return orders, buy_order_volume, sell_order_volume

    def clear_orders(
        self,
        product: str,
        order_depth: OrderDepth,
        fair_value: float,
        clear_width: float,
        position: int,
        buy_order_volume: int,
        sell_order_volume: int,
    ) -> (List[Order], int, int):
        orders: List[Order] = []
        buy_order_volume, sell_order_volume = self.clear_position_order(
            product,
            fair_value,
            clear_width,
            orders,
            order_depth,
            position,
            buy_order_volume,
            sell_order_volume,
        )
        return orders, buy_order_volume, sell_order_volume

    def make_orders(
        self,
        product: str,
        order_depth: OrderDepth,
        fair_value: float,
        position: int,
        buy_order_volume: int,
        sell_order_volume: int,
        disregard_edge: float,
        join_edge: float,
        default_edge: float,
        manage_position: bool = False,
        soft_position_limit: int = 0,
    ):
        orders: List[Order] = []

        asks_above_fair = [
            price
            for price in order_depth.sell_orders.keys()
            if price > fair_value + disregard_edge
        ]
        bids_below_fair = [
            price
            for price in order_depth.buy_orders.keys()
            if price < fair_value - disregard_edge
        ]

        best_ask_above_fair = min(asks_above_fair) if len(asks_above_fair) > 0 else None
        best_bid_below_fair = max(bids_below_fair) if len(bids_below_fair) > 0 else None

        ask = round(fair_value + default_edge)
        if best_ask_above_fair is not None:
            if abs(best_ask_above_fair - fair_value) <= join_edge:
                ask = best_ask_above_fair
            else:
                ask = best_ask_above_fair - 1

        bid = round(fair_value - default_edge)
        if best_bid_below_fair is not None:
            if abs(fair_value - best_bid_below_fair) <= join_edge:
                bid = best_bid_below_fair
            else:
                bid = best_bid_below_fair + 1

        if manage_position:
            if position > soft_position_limit:
                ask -= 1
            elif position < -1 * soft_position_limit:
                bid += 1

        buy_order_volume, sell_order_volume = self.market_make(
            product,
            orders,
            bid,
            ask,
            position,
            buy_order_volume,
            sell_order_volume,
        )

        return orders, buy_order_volume, sell_order_volume



    def make_emeralds_orders(
        self,
        order_depth: OrderDepth,
        fair_value: float,
        position: int,
        buy_order_volume: int,
        sell_order_volume: int,
    ):
        orders: List[Order] = []

        params = self.params[Product.EMERALDS]

        asks_above_fair = [
            price for price in order_depth.sell_orders.keys()
            if price > fair_value + params["disregard_edge"]
        ]
        bids_below_fair = [
            price for price in order_depth.buy_orders.keys()
            if price < fair_value - params["disregard_edge"]
        ]

        best_ask_above_fair = min(asks_above_fair) if len(asks_above_fair) > 0 else None
        best_bid_below_fair = max(bids_below_fair) if len(bids_below_fair) > 0 else None

        base_ask = round(fair_value + params["default_edge"])
        if best_ask_above_fair is not None:
            if abs(best_ask_above_fair - fair_value) <= params["join_edge"]:
                base_ask = best_ask_above_fair
            else:
                base_ask = best_ask_above_fair - 1

        base_bid = round(fair_value - params["default_edge"])
        if best_bid_below_fair is not None:
            if abs(fair_value - best_bid_below_fair) <= params["join_edge"]:
                base_bid = best_bid_below_fair
            else:
                base_bid = best_bid_below_fair + 1

        # inventory skew: shift BOTH quotes based on current position
        skew = int(position / 10) * params["skew_per_10_inventory"]
        bid = base_bid - skew
        ask = base_ask - skew

        # size asymmetry: reduce the side that worsens inventory, increase the side that helps flatten
        base_size = params["base_order_size"]

        if position > 0:
            buy_size = max(5, base_size - position // 5)
            sell_size = min(30, base_size + position // 5)
        elif position < 0:
            buy_size = min(30, base_size + abs(position) // 5)
            sell_size = max(5, base_size - abs(position) // 5)
        else:
            buy_size = base_size
            sell_size = base_size

        # extra flattening if inventory becomes large
        if position > params["hard_position_limit"]:
            ask -= 1
            buy_size = max(1, buy_size // 2)
            sell_size = min(40, sell_size + 5)
        elif position < -params["hard_position_limit"]:
            bid += 1
            buy_size = min(40, buy_size + 5)
            sell_size = max(1, sell_size // 2)

        buy_order_volume, sell_order_volume = self.market_make(
            Product.EMERALDS,
            orders,
            bid,
            ask,
            position,
            buy_order_volume,
            sell_order_volume,
            buy_size=buy_size,
            sell_size=sell_size,
        )

        return orders, buy_order_volume, sell_order_volume
```
