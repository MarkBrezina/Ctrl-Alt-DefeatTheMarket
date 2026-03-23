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

What is actually going on?

Starting out in the tutorial round we are given two assets.
Tomatoes and Emeralds. Which behave in two distinct ways. To the untrained eye, that is "edible" and "unedible".
But if you open the data capsules, you can build research and figure out the generalistic mechanics that IMC has put out for those.

![Screenshot](utils/Sk%C3%A6rmbillede%202026-03-23%20110755.png)
If you ain't got no idea of where to get the data. It is right here -> [Tutorial folder](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/tree/main/Tutorial)

Before we go over each of the assets and their properties/behaviours, it is worth noting for everyone that there are 5 rounds and that each round adds a new mechanism usually either a new asset or bunch of assets to be considered.
For each asset, it is worth considering the behaviours of the assets by taking the data capsule out, extracting the .csv files and loading them into a notebook of some sort. I won't judge if you use R, Python notebooks, excel or god forbid, power BI.

### Tutorial Round assets

Emeralds, like rainforest Resin in IMC 3, are a straight textbook stationary asset. If you plot the past days of data for Emeralds, you will find that it stays around the same mid price
10,000$ and swings up-down with about a 16$ spread. this means we can implement a neat market-making algorithm and that is about it.

![Screenshot](utils/Sk%C3%A6rmbillede%202026-03-23%20111444.png)

Tomatoes, like Kelp in IMC 3, has a drift, we can therefore not simply implement market making and go home for the day, we need to implement something that either adjust to the drift or benefits from it.
I've heard many good ideas, trend-following HFT, market-making with drift, short-selling(assuming the behaviour follows the data capsule) and many more.

![Screenshot](utils/Sk%C3%A6rmbillede%202026-03-23%20111450.png)



https://github.com/jmerle/imc-prosperity-3-backtester \
https://github.com/jmerle/imc-prosperity-3-optimizer

## Lay it down thick brother!
resources pretty please.

https://github.com/Tim-Wolstenholme/IMC-Prosperity3/tree/main \
https://github.com/JamesCole809/IMC-Prosperity-3 \
https://github.com/itsam/imc \
https://github.com/milesmitchell/imc_prosperity_3 \
https://github.com/CarterT27/imc-prosperity-3 \
https://github.com/chrispyroberts/imc-prosperity-3 \
https://github.com/YBansal95/imc-prosperity-3 \
https://github.com/awatatani/imc-prosperity3-trading \
https://github.com/ShubhamAnandJain/IMC-Prosperity-2023-Stanford-Cardinal \
https://github.com/ericcccsliu/imc-prosperity-2 \
https://github.com/TimoDiehm/imc-prosperity-3 \
https://github.com/pe049395/IMC-Prosperity-2024 \
https://github.com/jmerle/imc-prosperity-3 \
https://github.com/kzqiu/imc-2023 \ 
https://github.com/BakerStreetPhantom/IMC-Prosperity-Trading-Challenge-2023 \ 
https://github.com/monoclonalAb/tax-haven \ 
https://github.com/andrewliu08/prosperity-goats \ 
https://github.com/IMC-Prosperity-Granite-Flow/IMC_Prosperity3_GraniteFlow \ 
https://github.com/VincentTLe/imc-prosperity-4-prep

https://github.com/Robin-Guilliou/Option-Pricing \
https://www.kaggle.com/competitions/optiver-realized-volatility-prediction/writeups/pksha-life-is-volatile-tentative-3rd-place-solutio
https://www.kaggle.com/competitions/optiver-realized-volatility-prediction/writeups/nyanp-1st-place-solution-nearest-neighbors
https://github.com/taher-software/Optiver-Realized-Volatility-Prediction/tree/master


https://www.kaggle.com/competitions/optiver-trading-at-the-close/writeups/adam-9th-place-solution
https://www.kaggle.com/competitions/optiver-trading-at-the-close/writeups/hyd-1st-place-solution
https://github.com/liyiyan128/optiver-trading-at-the-close
https://fan2goa1.github.io/mkdocs-material/blog/2023/12/24/kaggle-optiver---trading-at-the-close/
https://github.com/xhshenxin/Micro_Price
