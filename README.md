# Ctrl-Alt-DefeatTheMarket
An idiot's guide to IMC Prosperity algorithmic trading

IMC Prosperity is about algorithmic trading.

It is divided into two parts.
Manual trading and algorithmic trading. The two are usually linkedin, solutions in manual trading are useful for algorithmic trading.
Manual trading are reflections, questions and topics generally relevant.

Algorithmic trading is implementing on actual market simulations.

Now because I am who i am, I will only be interested in Algorithmic trading, the practical side. I have already made up my mind on what I have reflected on.
So the manual trading questions aren't of interest to me.

I do however respect that others will seek to find solutions to the manual trading parts.

Steps:
1. [How do I get set up?](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/README.md#how-do-i-set-up-my-first-trader)
2. [What is actually going on?](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/README.md#what-the-fuck-is-alpha)
3. [Where do I find resources?](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/README.md#lay-it-down-thick-brother)
4. [What is the system like?]()
5. Just fucking spoon feed me bro!


Now remember that we are all assuming there will be 5 rounds, not including the tutorial round, just like any other year.
We all expect that there will be something like the previous years.
1. stationary asset
2. drifting asset
3. baskets
4. derivatives
5. macroeconomic impacts.

## How do I set up my first trader?

If you are new to the IMC Prosperity Challenge, this is the page you will usually land on first.

![Landing page](utils/Sk%C3%A6rmbillede%202026-03-23%20104551.png)

After signing up and logging in, click **Continue** to move to the initial setup.

![Continue screen](utils/Sk%C3%A6rmbillede%202026-03-23%20104600.png)

You will then see a countdown timer. When available, click **Start Mission** to enter the challenge interface.

![Start mission](utils/Sk%C3%A6rmbillede%202026-03-23%20104609.png)

From here, you have two main options:

- click **Open Challenge** to upload your trading strategy
- scroll down to download the data capsule for products such as **Emeralds** and **Tomatoes**

The data capsule is useful for research, idea generation, and building your first trading strategy.

Clicking **Open Challenge** takes you to the upload page, where you can submit your trading file. Your submission must be a Python file ending in `.py`.

![Upload trader](utils/Sk%C3%A6rmbillede%202026-03-23%20104622.png)

After uploading a trader, you will see performance output such as graphs and results. You can also compare multiple uploads to see which strategy performed best.

![Results graph](utils/Sk%C3%A6rmbillede%202026-03-23%20104649.png)

You can also open the side menu for more resources. I strongly recommend reading the **Wiki** before writing your first strategy.

![Side menu](utils/Sk%C3%A6rmbillede%202026-03-23%20104713.png)

The **Wiki** contains important information about each round, the products, and the overall challenge structure. Read it carefully before you start coding.

![Wiki page](utils/Sk%C3%A6rmbillede%202026-03-23%20104724.png)

### What should I use to code my trader?

A good place to start is **Visual Studio Code**.  
I personally use **Spyder** through **Anaconda**, which also works well.

- [Visual Studio Code](https://code.visualstudio.com/)
- [Anaconda Navigator](https://www.anaconda.com/products/navigator)

### What code do we get from IMC to start with?

Below is the basic starter template provided by IMC:

```python
from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:

    def bid(self):
        return 15
    
    def run(self, state: TradingState):
        """Only method required. It takes all buy and sell orders for all
        symbols as an input, and outputs a list of orders to be sent."""

        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))

        # Orders to be placed on exchange matching engine
        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            acceptable_price = 10  # Participant should calculate this value
            print("Acceptable price : " + str(acceptable_price))
            print(
                "Buy Order depth : " + str(len(order_depth.buy_orders)) +
                ", Sell order depth : " + str(len(order_depth.sell_orders))
            )
    
            if len(order_depth.sell_orders) != 0:
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                if int(best_ask) < acceptable_price:
                    print("BUY", str(-best_ask_amount) + "x", best_ask)
                    orders.append(Order(product, best_ask, -best_ask_amount))
    
            if len(order_depth.buy_orders) != 0:
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                if int(best_bid) > acceptable_price:
                    print("SELL", str(best_bid_amount) + "x", best_bid)
                    orders.append(Order(product, best_bid, -best_bid_amount))
            
            result[product] = orders
    
        # String value holding Trader state data required. 
        # It will be delivered as TradingState.traderData on next execution.
        traderData = "SAMPLE"
        
        # Sample conversion request. Check more details below.
        conversions = 1
        return result, conversions, traderData

```





## What the fuck is alpha?

What is actually going on here?

In the tutorial round, we are given two assets: **Tomatoes** and **Emeralds**. At first glance, the distinction may seem to be simply “edible” versus “inedible”. In practice, though, they behave very differently in market terms.

If you open the data capsules and start exploring the files, you can begin to reverse-engineer the basic mechanics IMC has built into these products.

![Screenshot](utils/Sk%C3%A6rmbillede%202026-03-23%20110755.png)

If you are not sure where to find the data, it is available here: [Tutorial folder](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/tree/main/Tutorial)

Before going through each asset in detail, it is worth keeping one thing in mind: the challenge consists of **5 rounds**, and each round usually introduces a new mechanism, often through one or more additional assets.

For each product, the first step is usually the same:
download the data capsule, extract the `.csv` files, and load them into a notebook or analysis environment of your choice. Use Python, R, Excel, or even Power BI if you must.

It is also worth mentioning that **Jasper Merle’s backtester** was a major help during IMC Prosperity 3. You should not expect the results to match the live challenge one-to-one, but strong backtester performance is generally still a good sign. For example, a backtest result around **35K** roughly translated to about **9K** in Round 1 of IMC 3, which was approximately **top 10%**.

- [jmerle's backtester](https://github.com/jmerle/imc-prosperity-3-backtester)
- [jmerle's optimizer](https://github.com/jmerle/imc-prosperity-3-optimizer)

### Tutorial round assets

**Emeralds**, much like **Rainforest Resin** in IMC 3, behave like a classic stationary asset.  
If you plot the historical data for Emeralds, you will see that the mid-price stays centered around **10,000** and oscillates around that level with a spread of roughly **16**. That makes it a strong candidate for a straightforward market-making strategy.

![Screenshot](utils/Sk%C3%A6rmbillede%202026-03-23%20111444.png)

**Tomatoes**, much like **Kelp** in IMC 3, show drift.  
Because of that, you cannot simply deploy a static market-making strategy and call it a day. You need an approach that either adapts to the drift or actively benefits from it. That could include ideas such as drift-aware market making, short-horizon trend following, short-selling where appropriate, or other models that react to directional behaviour in the data.

![Screenshot](utils/Sk%C3%A6rmbillede%202026-03-23%20111450.png)

### Round 1

At the time of writing, Round 1 has not started yet, so we do not know what new products or mechanics it will introduce.

## Lay it down thick brother!

Now I started out by making a little dump of all the previous repos and a few other useful resources.
But I have removed them! 😈

I will however divide it up like this.

What we need to know is this.
IMC is a challenge in HFT, algorithmic trading, market making.
To some it may therefore be obvious that we must consider all parts of that.
Here is a few general ideas that are used
1. Alpha engine(doooh)
2. Risk engine(not so obvious)
3. Inventory engine(also not so obvious)
4. Execution engine(wtf is that even?)
5. Portfolio management(are we doing long term investing now?)

So here is some more in depth work.

### Alpha
As an easy way to think of things, here is a reflection of each round as problems relating to differentials.

For each of the assets presented, IMC is essentially showcasing scenarios, where different alphas are applied.

On the stationary asset this is "buy low sell high", which is the core idea we all play with. But that is probably the simplest version you can find. The data represented is a curve with gradient 0

For drift, you would want to do the same, but "hit the local minimum", "hit the local maximum", it turns into a curve gradient/linear slope problem. Because the gradient a function unlike, 0 for the stationary asset.
This is trend following.

For the rounds afterwards it essentially escalates along the same line.
As a hypothetical for round 2, IMC introduces an asset which is correlated to the asset with drift, in this way you instead have a problem of multiple gradients to solve. Can you hit that magic moment where the partial derivative is 0 betwen the two correlated assets?
This is pairs trading.

For the rounds afterwards you will have ETF/basket arbitrage, derivatives trading and more. Which is further developments of the same "what does the escalating derivatives do?" problem.
With them come more complex mechanisms to find solutions to the differentials.

### Risk
If by chance you are one of the morons who believe they know everything, skip to the next part.
If you're like me, risk and risk mitigation are essentially the biggest problem in everything.

We want to minimise the chance of losing value, either by mitigation or by allowing some risk, then dumping either parts of our position or by dumping the entire thing.
We therefore want to measure both exposure, current lose and deviations for the assets. This becomes a key component in the next part.

### Inventory
Like anyone with a brain, we want to actually know what we've got, that's where the inventory part comes in.
Your max inventory for Emeralds and tomatoes is 80 for the tutorial round. It is also a GREAT idea to set up soft-limits or multi-layered limits for your inventory.
Remember that your order posting also isn't divided. Sending orders "buy: 10 EMERALDS @ 100$" "buy: 15 EMERALDS @ 100$" is essentially just "buy: 25 EMERALDS @ 100$" It doesn't matter which alpha is sending which order.
If you've implemented inventory adjustments, those two orders may even negate each other if say your adjustments go negative beyond soft-limits with high volatility.
The proper combination of alpha, risk and inventory is therefore extremely important.

### Execution.
Oh! Right, wasn't that what we were just talking about?
The execution of orders as a result of the combination of your inventory, risk and alpha engines is no easy feat.
To add to that you may also want to implement layers that modify, distribute and cancel orders.
Here are two nice hypotheticals.
Imagine for a moment you wouldn't be playing against a simulation. 
By chance, you would be playing against some super smart quant, he always knows the future.
But you are always faster than him. You get to cancel your orders at any time.
You put out an order for "buy: 10 EMERALDS @ 100$" and you see that he is about to match you.
You can now get to cancel your order or let him sell you 10 emeralds. What do you do?
You don't have to cancel, but it might be a good idea to at least have that ready, because you are ALWAYS faster than him.


Hypothetical 2.
Another scenario is this. Your best alpha signal is firing. But you know it is only right 80% of the time.
Sometimes it kinda gets excited and fires a little too early or too late.
A nice execution model to have to correct a bit of the early misfires is a distribution.
VWAP or whatever you like to call it, is a nice little thing.
Take your big order, say instead of your usual 10 pieces of emerald, you instead want 100 pieces.
You just divide it into smaller orders, 10 at a time and fire it over the next 10 time steps.

### Portfolio management.
Dude blew a fuse in his mind box? eh?

Nope. This one is of course less important. But imagine you have 2 alphas to implement on one asset or maybe across some assets.
You need to be able to figure out how much inventory/weight to put into those two alphas, this is where portfolio management comes in.
you could of course simply implement "hey dude I like this strategy best", but that would leave us brainiacs higher on the scoreboard. Try Markowitz(mean-variance) first.



