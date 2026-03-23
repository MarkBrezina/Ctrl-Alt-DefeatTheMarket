Like in any other type of work, risk is always present, and the goal is to minimise it.

Risk can be measured in a simple way, such as **how far price has moved against us**, but it can also be measured more practically through **current PnL**. In industry settings, these measures are often paired with risk limits such as **3%, 5%, or 10%**, depending on the strategy and tolerance level. These limits can be applied either at the **portfolio level** or at the level of **individual trades**.

This naturally ties into **inventory management**. Once a position or loss threshold is reached, the strategy may begin reducing exposure in order to limit further losses over time.

When you start combining alpha generation with risk controls, inventory rules, and execution logic, the implementation quickly becomes much more complex. That is why many strong solutions to the IMC Prosperity Challenge contain **far more than just**:
```
alpha -> order
```

They also include dedicated logic for position clearing, inventory adjustment, and execution control.

Here is a piece of code I use for that purpose:
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
```

The idea here is to adjust the orders I am about to send and, when needed, actively reduce an existing position.

Alongside this, I also adjust my quoting behaviour once inventory starts moving too close to my limits. For example, I do not want to find myself holding **60 lots of Emeralds** if a sudden price drop occurs. Because of that, I start becoming more defensive once my inventory reaches **20 lots**, gradually encouraging the strategy to reduce exposure before risk becomes too large.

Emeralds is the stable asset in this case, but hopefully the general idea still comes across clearly.
