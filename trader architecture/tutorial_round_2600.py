from datamodel import OrderDepth, TradingState, Order
from typing import Dict, List, Tuple, Optional
import jsonpickle


class Product:
    EMERALDS = "EMERALDS"
    TOMATOES = "TOMATOES"


PARAMS: Dict[str, Dict[str, float]] = {
    Product.EMERALDS: {
        "fair_value": 10000,
        "take_width": 1,
        "clear_width": 0,
        "disregard_edge": 2,
        "join_edge": 1,
        "default_edge": 8,
        "soft_position_limit": 80,
        "hard_position_limit": 80,
        "skew_per_10_inventory": 1,
        "base_order_size": 30,
    },
    Product.TOMATOES: {
        "take_width": 1,
        "clear_width": 0,
        "disregard_edge": 2,
        "join_edge": 1,
        "default_edge": 4,
        "soft_position_limit": 20,
        "hard_position_limit": 80,
        "skew_per_10_inventory": 1,
        "base_order_size": 20,
    },
}


class Trader:
    def __init__(self, params: Optional[Dict[str, Dict[str, float]]] = None):
        self.params = params or PARAMS
        self.position_limits = {
            Product.EMERALDS: 80,
            Product.TOMATOES: 80,
        }

    # =========================
    # Basic helpers
    # =========================
    def get_position(self, state: TradingState, product: str) -> int:
        return state.position.get(product, 0)

    def max_buy_capacity(self, product: str, position: int, buy_order_volume: int) -> int:
        return self.position_limits[product] - position - buy_order_volume

    def max_sell_capacity(self, product: str, position: int, sell_order_volume: int) -> int:
        return self.position_limits[product] + position - sell_order_volume

    def best_ask(self, order_depth: OrderDepth) -> Optional[int]:
        return min(order_depth.sell_orders.keys()) if order_depth.sell_orders else None

    def best_bid(self, order_depth: OrderDepth) -> Optional[int]:
        return max(order_depth.buy_orders.keys()) if order_depth.buy_orders else None

    def get_mid_price(self, order_depth: OrderDepth) -> Optional[float]:
        best_bid = self.best_bid(order_depth)
        best_ask = self.best_ask(order_depth)

        if best_bid is None or best_ask is None:
            return None

        return (best_bid + best_ask) / 2

    # =========================
    # Fair value estimator
    # =========================
    def update_fair_value_history(
        self,
        trader_object: dict,
        product: str,
        order_depth: OrderDepth,
        window: int = 3,
    ) -> Optional[float]:
        """
        Stores rolling mid-price history in traderData and returns
        the average of the last `window` mid-prices.
        """
        mid_price = self.get_mid_price(order_depth)
        if mid_price is None:
            return None

        if "mid_history" not in trader_object:
            trader_object["mid_history"] = {}

        if product not in trader_object["mid_history"]:
            trader_object["mid_history"][product] = []

        history = trader_object["mid_history"][product]
        history.append(mid_price)

        if len(history) > window:
            history[:] = history[-window:]

        return sum(history) / len(history)

    # =========================
    # Taking logic
    # =========================
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
    ) -> Tuple[int, int]:
        
        best_ask = self.best_ask(order_depth)
        if best_ask is not None:
            best_ask_amount = -order_depth.sell_orders[best_ask]

            valid_ask = ((not prevent_adverse or abs(best_ask_amount) <= adverse_volume) and best_ask <= fair_value - take_width)
            
            if valid_ask:
                quantity = min(best_ask_amount,self.max_buy_capacity(product, position, buy_order_volume),)
                
                if quantity > 0:
                    orders.append(Order(product, best_ask, quantity))
                    buy_order_volume += quantity

                    order_depth.sell_orders[best_ask] += quantity
                    if order_depth.sell_orders[best_ask] == 0:
                        del order_depth.sell_orders[best_ask]

        best_bid = self.best_bid(order_depth)
        if best_bid is not None:
            best_bid_amount = order_depth.buy_orders[best_bid]

            valid_bid = ((not prevent_adverse or abs(best_bid_amount) <= adverse_volume) and best_bid >= fair_value + take_width)
            
            if valid_bid:
                quantity = min(best_bid_amount,self.max_sell_capacity(product, position, sell_order_volume),)
                
                if quantity > 0:
                    orders.append(Order(product, best_bid, -quantity))
                    sell_order_volume += quantity

                    order_depth.buy_orders[best_bid] -= quantity
                    if order_depth.buy_orders[best_bid] == 0:
                        del order_depth.buy_orders[best_bid]

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
    ) -> Tuple[List[Order], int, int]:
        orders: List[Order] = []
        buy_order_volume = 0
        sell_order_volume = 0

        buy_order_volume, sell_order_volume = self.take_best_orders(
            product=product,
            fair_value=fair_value,
            take_width=take_width,
            orders=orders,
            order_depth=order_depth,
            position=position,
            buy_order_volume=buy_order_volume,
            sell_order_volume=sell_order_volume,
            prevent_adverse=prevent_adverse,
            adverse_volume=adverse_volume,
        )

        return orders, buy_order_volume, sell_order_volume

    # =========================
    # Clearing logic
    # =========================
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
    ) -> Tuple[int, int]:
        position_after_take = position + buy_order_volume - sell_order_volume
        fair_for_bid = round(fair_value - width)
        fair_for_ask = round(fair_value + width)

        buy_capacity = self.max_buy_capacity(product, position, buy_order_volume)
        sell_capacity = self.max_sell_capacity(product, position, sell_order_volume)

        if position_after_take > 0:
            clear_quantity = sum(
                volume
                for price, volume in order_depth.buy_orders.items()
                if price >= fair_for_ask
            )
            clear_quantity = min(clear_quantity, position_after_take)
            sent_quantity = min(sell_capacity, clear_quantity)

            if sent_quantity > 0:
                orders.append(Order(product, fair_for_ask, -sent_quantity))
                sell_order_volume += sent_quantity

        elif position_after_take < 0:
            clear_quantity = sum(
                abs(volume)
                for price, volume in order_depth.sell_orders.items()
                if price <= fair_for_bid
            )
            clear_quantity = min(clear_quantity, abs(position_after_take))
            sent_quantity = min(buy_capacity, clear_quantity)

            if sent_quantity > 0:
                orders.append(Order(product, fair_for_bid, sent_quantity))
                buy_order_volume += sent_quantity

        return buy_order_volume, sell_order_volume

    def clear_orders(
        self,
        product: str,
        order_depth: OrderDepth,
        fair_value: float,
        clear_width: float,
        position: int,
        buy_order_volume: int,
        sell_order_volume: int,
    ) -> Tuple[List[Order], int, int]:
        orders: List[Order] = []

        buy_order_volume, sell_order_volume = self.clear_position_order(
            product=product,
            fair_value=fair_value,
            width=clear_width,
            orders=orders,
            order_depth=order_depth,
            position=position,
            buy_order_volume=buy_order_volume,
            sell_order_volume=sell_order_volume,
        )

        return orders, buy_order_volume, sell_order_volume

    # =========================
    # Passive market making
    # =========================
    def market_make(
        self,
        product: str,
        orders: List[Order],
        bid: int,
        ask: int,
        position: int,
        buy_order_volume: int,
        sell_order_volume: int,
        buy_size: Optional[int] = None,
        sell_size: Optional[int] = None,
    ) -> Tuple[int, int]:
        max_buy_available = self.max_buy_capacity(product, position, buy_order_volume)
        max_sell_available = self.max_sell_capacity(product, position, sell_order_volume)

        buy_quantity = max_buy_available if buy_size is None else min(buy_size, max_buy_available)
        sell_quantity = max_sell_available if sell_size is None else min(sell_size, max_sell_available)

        if buy_quantity > 0:
            orders.append(Order(product, round(bid), buy_quantity))
            buy_order_volume += buy_quantity

        if sell_quantity > 0:
            orders.append(Order(product, round(ask), -sell_quantity))
            sell_order_volume += sell_quantity

        return buy_order_volume, sell_order_volume

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
    ) -> Tuple[List[Order], int, int]:
        orders: List[Order] = []

        asks_above_fair = [
            price for price in order_depth.sell_orders
            if price > fair_value + disregard_edge
        ]
        bids_below_fair = [
            price for price in order_depth.buy_orders
            if price < fair_value - disregard_edge
        ]

        best_ask_above_fair = min(asks_above_fair) if asks_above_fair else None
        best_bid_below_fair = max(bids_below_fair) if bids_below_fair else None

        ask = round(fair_value + default_edge)
        if best_ask_above_fair is not None:
            ask = (
                best_ask_above_fair
                if abs(best_ask_above_fair - fair_value) <= join_edge
                else best_ask_above_fair - 1
            )

        bid = round(fair_value - default_edge)
        if best_bid_below_fair is not None:
            bid = (
                best_bid_below_fair
                if abs(fair_value - best_bid_below_fair) <= join_edge
                else best_bid_below_fair + 1
            )

        if manage_position:
            if position > soft_position_limit:
                ask -= 1
            elif position < -soft_position_limit:
                bid += 1

        buy_order_volume, sell_order_volume = self.market_make(
            product=product,
            orders=orders,
            bid=bid,
            ask=ask,
            position=position,
            buy_order_volume=buy_order_volume,
            sell_order_volume=sell_order_volume,
        )

        return orders, buy_order_volume, sell_order_volume

    def make_emeralds_orders(
        self,
        order_depth: OrderDepth,
        fair_value: float,
        position: int,
        buy_order_volume: int,
        sell_order_volume: int,
    ) -> Tuple[List[Order], int, int]:
        orders: List[Order] = []
        params = self.params[Product.EMERALDS]

        asks_above_fair = [
            price for price in order_depth.sell_orders
            if price > fair_value + params["disregard_edge"]
        ]
        bids_below_fair = [
            price for price in order_depth.buy_orders
            if price < fair_value - params["disregard_edge"]
        ]

        best_ask_above_fair = min(asks_above_fair) if asks_above_fair else None
        best_bid_below_fair = max(bids_below_fair) if bids_below_fair else None

        base_ask = round(fair_value + params["default_edge"])
        if best_ask_above_fair is not None:
            base_ask = (
                best_ask_above_fair
                if abs(best_ask_above_fair - fair_value) <= params["join_edge"]
                else best_ask_above_fair - 1
            )

        base_bid = round(fair_value - params["default_edge"])
        if best_bid_below_fair is not None:
            base_bid = (
                best_bid_below_fair
                if abs(fair_value - best_bid_below_fair) <= params["join_edge"]
                else best_bid_below_fair + 1
            )

        skew = int(position / 10) * params["skew_per_10_inventory"]
        bid = base_bid - skew
        ask = base_ask - skew

        base_size = int(params["base_order_size"])

        if position > 0:
            buy_size = max(5, base_size - position // 5)
            sell_size = min(30, base_size + position // 5)
        elif position < 0:
            buy_size = min(30, base_size + abs(position) // 5)
            sell_size = max(5, base_size - abs(position) // 5)
        else:
            buy_size = base_size
            sell_size = base_size

        buy_order_volume, sell_order_volume = self.market_make(
            product=Product.EMERALDS,
            orders=orders,
            bid=bid,
            ask=ask,
            position=position,
            buy_order_volume=buy_order_volume,
            sell_order_volume=sell_order_volume,
            buy_size=buy_size,
            sell_size=sell_size,
        )

        return orders, buy_order_volume, sell_order_volume

    # =========================
    # Main
    # =========================
    def run(self, state: TradingState):
        trader_object = {}
        if state.traderData:
            trader_object = jsonpickle.decode(state.traderData)

        result: Dict[str, List[Order]] = {}

        for product in self.params:
            if product not in state.order_depths:
                continue

            position = self.get_position(state, product)
            params = self.params[product]
            order_depth = state.order_depths[product]

            if product == Product.EMERALDS:
                fair_value = params["fair_value"]
            else:
                fair_value = self.update_fair_value_history(
                    trader_object,
                    product,
                    order_depth,
                    window=3,
                )
                if fair_value is None:
                    continue

            take_orders, buy_order_volume, sell_order_volume = self.take_orders(
                product=product,
                order_depth=order_depth,
                fair_value=fair_value,
                take_width=params["take_width"],
                position=position,
            )

            clear_orders, buy_order_volume, sell_order_volume = self.clear_orders(
                product=product,
                order_depth=order_depth,
                fair_value=fair_value,
                clear_width=params["clear_width"],
                position=position,
                buy_order_volume=buy_order_volume,
                sell_order_volume=sell_order_volume,
            )

            if product == Product.EMERALDS:
                make_orders, _, _ = self.make_emeralds_orders(
                    order_depth=order_depth,
                    fair_value=fair_value,
                    position=position,
                    buy_order_volume=buy_order_volume,
                    sell_order_volume=sell_order_volume,
                )
            else:
                make_orders, _, _ = self.make_orders(
                    product=product,
                    order_depth=order_depth,
                    fair_value=fair_value,
                    position=position,
                    buy_order_volume=buy_order_volume,
                    sell_order_volume=sell_order_volume,
                    disregard_edge=params["disregard_edge"],
                    join_edge=params["join_edge"],
                    default_edge=params["default_edge"],
                    manage_position=True,
                    soft_position_limit=int(params["soft_position_limit"]),
                )

            result[product] = take_orders + clear_orders + make_orders

        conversions = 1
        trader_data = jsonpickle.encode(trader_object)
        return result, conversions, trader_data