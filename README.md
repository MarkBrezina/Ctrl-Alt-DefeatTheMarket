
# Ctrl-Alt-DefeatTheMarket

Before diving in, I would like to express my gratitude to the people who made this possible.

First, thank you to the IMC team for organizing such a rewarding challenge and for their dedication to supporting participants across a wide range of topics. I would also like to thank @Tomas, @Jack, and the forum admins for their consistent help.

A special thanks goes to @Jasper. I owe him full credit for the asset list and the backtester; his decision to share his work openly inspired this guide, which aims to centralize these resources for the community. I’m also grateful to @Fabian, @oats (April), @mr. nobody, and many others for being such active contributors to the Discord server.

To respect a request from @Tomas regarding oversharing, I will be updating this guide retrospectively. Once a round concludes, I will add my specific research and observations. Each round will be organized into its own dedicated folder.

## meet-up for UKers
For anyone interested in meeting other participants for a chat, maybe for showing off how well they did, for sharing ideas or anything like that.

You are all very welcome to meet me and others at the railway tavern outside of IMC's UK offices, near Liverpool Street train station in London.

I will be there on friday 24th of april from 5PM till 8PM unless we get some fun going.


## Phase 2.

Phase 1 has now ended and everyone who managed to score above 200K has passed onto the second phase. We do not know too much about it at this point. But we can prepare for the next phase, like how we did for the first phase.
By studying the previous years.

## Updates

I have updated the following two folders on the rounds so far.
- [Round 1](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/tree/main/Round%201), with notes on what I did and how I f-cked up my own submission
- [Round 2](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/tree/main/Round%201), with notes on the current round and how I intend on improving my submission.

## Quick steps if you're new or feeling lost

If you're completely new and just need a place to start, use the pages below as an index. Otherwise, I recommend reading the rest of the guide as well.

- [**Getting Started**](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/GETTING_STARTED.md) — a page designed specifically for newcomers
- [**Glossary**](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/GLOSSARY.md) — explanations of key terms and concepts
- [**Alpha**](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/alpha/README.md) — ideas on what each round is about and which strategies you may want to explore
- [**Mindset**](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/MINDSET.md) — added in response to questions about the psychological strain involved in this space
- [**Resources**](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/RESOURCES.md) — a dedicated page for reading material and useful references, to be expanded over time with sections such as **books, playlists, online seminars, forums**, and more
- [**Teammates and Roles**](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/TEAMMATES_AND_ROLES.md) — a guide for common Discord questions like “I want to join a team” or “I want a teammate”
- [**Market Basics**](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/market_basics/README.md) — an introduction to how trading works, why strategies sometimes fail, and how to improve
- [**Trader Architecture**](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/trader%20architecture/README.md) — a simpler explanation of the coding structure than IMC currently provides, especially around ideas like memory, calculation flow, and building your own architecture or infrastructure
- [**Research**](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/research/README.md) — For research on previous competitions and potential solutions.

## What this guide is

This guide is a genuine attempt to share everything I can offer to both new and experienced IMC Prosperity participants, both for the challenge itself and for the broader ideas behind it.

It is not intended to create a zero-sum game. In fact, I believe the opposite. If you perform well, I benefit too. In a deeper sense, this is about choosing the strategy that produces the best outcome for both myself and the wider group.

I expect to benefit from **you** gaining knowledge, even if that benefit does not appear at timestep *t+1*, but rather at timestep *t+1000*.

I am not going to hand you a finished solution and ask you to beat me by tuning a few parameters. What I *will* do is share ideas, frameworks, and ways of thinking that can help you develop your own.

To make this easier to navigate, I have divided the guide into different tiers based on starting skill level, so you can jump directly to the parts that are most useful to you.


## Who this guide is for

This guide is mainly for IMC Prosperity participants, but it may also be useful for aspiring quants or anyone interested in algorithmic trading.

I have been experimenting with this style of teaching for a long time, originally through maths, and this guide is an extension of that same approach.


## What IMC Prosperity is, in plain English

IMC Prosperity is an international algorithmic trading challenge.

There are many other competitions and opportunities that might claim to be the best, but honestly, I believe IMC Prosperity stands above the rest.

In this challenge, you get the opportunity to work on problems that are close to real-world algorithmic trading. In the end, you are judged by how much profit your strategies generate.

## A note on expectations

For now, most of us are assuming there will be **five rounds**, not including the tutorial round, as in previous years.

In each round, new assets may be added and old ones may be removed.

Each round is also likely to contain both:

- a **manual trading** challenge
- an **algorithmic trading** challenge

The manual trading side is not really “manual” in the literal sense. It is more conceptual: you are asked to reason through a problem and provide a solution or framework.

We also expect the challenge to include themes similar to earlier editions, such as:

- stationary assets
- drifting assets
- correlated assets
- baskets
- derivatives
- macroeconomic impacts
- informed traders
- conversions


## Recommended reading paths

I recommend three different paths through this repository:

1. **If you are new**, continue to the next section, **Quickstart**, and then move on to **Getting Started**.
2. **If you already have a basic understanding**, jump directly to the sections most relevant to the help you need.
3. **If you are more advanced**, head to the research-oriented sections, where I share my own frameworks, interpretations, and conceptual ideas.


## Quickstart: get your first trader running

IMC Prosperity is about trading, and in practice it is split into two parts:

- **Manual trading**
- **Algorithmic trading**

The two are usually connected. Ideas from the manual side can often help with the algorithmic side, because the manual questions tend to highlight useful patterns, themes, and ways of thinking.

That said, this guide is mainly about **algorithmic trading** — the practical side.

That is the part I care most about, and the part I want to focus on here.

I fully respect that many people will also want to work through the manual trading section, and there is definitely value in doing so. It is simply not the main focus of this guide.

*There will be a section added soon covering manual trading walk-throughs and recommended reading.*

If you want an early **leaderboard**, you can use [this one](https://prosperity.equirag.com/) or [this one]().  
They are not “stealing your strategy” — you are simply uploading the log from your run on IMC’s website.

You may also want to sign up for the [IMC webinar: Discover Prosperity 4](https://job-boards.eu.greenhouse.io/imc/jobs/4790350101?gh_src=tt0n71b2teu).

If you are in London, there may also be a chance to grab a pint and have a chat near Citadel’s offices.

In the algorithmic trading challenge, we are given assets together with historical data for research.

Each asset tends to exhibit a certain type of behaviour, such as:

- stationary behaviour
- drift
- correlation
- baskets
- derivatives
- macroeconomic effects
- informed trading
- conversions

Each of these comes with its own associated ways to make money.

We translate those ideas into code inside the `Trader.py` file, upload that file, and receive a corresponding PnL graph and score.

Ultimately, we are judged by the final PnL.

To go through this in more detail, see the [Getting Started](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/GETTING_STARTED.md) file.

**note:** participation beyond round 3, is based on a set limit for Xirecs, you must have reached 200K by round 3.

## Strategy building and developing serious submissions

If you have already read the *Getting Started* section — or simply want to jump straight into strategy development — this is where the real work begins.

Grab the trader file and start building.

Getting from the basic starter trader to a genuinely better strategy usually requires three things to go right:

1. **You need a basic understanding of the challenge and the market environment.**  
   You do not need to know everything, but you do need at least a rough sense of what kind of market you are interacting with and what the data is telling you.

2. **You need an idea for how the trader might make money.**  
   This is where actual trading ideas start to matter. For example, you might believe that prices revert to a mean, or that prices drift for periods of time.

3. **You need to turn that idea into code that works in practice.**  
   It is one thing to say “buy low, sell high.” It is another thing to implement that logic in a way that behaves well inside the challenge.

The basic starter trader uses a very simple rule:

- if the current lowest sell price is below 10, it buys
- if the current highest buy price is above 10, it sells

At its core, this is just a simple **buy low, sell high** idea.

But once you try to improve on that, deeper questions start to matter:

- What do **bid** and **ask** actually mean?
- Do you want to trade immediately against existing orders, or place your own orders and wait to be filled?
- Do you want to approach buyers and sellers with better prices, or only trade when the market comes to you?
- How do you turn those choices into actual trading logic?

These are exactly the kinds of questions you will spend most of your time working on.

Improvements can be made at every level. Even if two people have the same broad idea, the one who understands the market better, implements the logic more clearly, and writes cleaner code will usually end up with the stronger trader.

If you are still figuring out the basics, head over to the **Glossary**.

If you already understand the core terms, move on to **Indicators**.

If you have both of those down, the next step is the **Trader Architecture** section.

After that, the five pillars below provide a useful way to structure how algorithmic trading systems are built.


## Round ideas

### What is actually going on here?

In the tutorial round, we are given two assets: **Tomatoes** and **Emeralds**. At first glance, the distinction may seem to be simply “edible” versus “inedible”. In practice, though, they behave very differently in market terms.

If you open the data capsules and start exploring the files, you can begin to reverse-engineer the basic mechanics IMC has built into these products.

![Screenshot](utils/assets.png)

If you are not sure where to find the data, it is available here: [Tutorial folder](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/tree/main/Tutorial)

Before going through each asset in detail, it is worth keeping one thing in mind: the challenge consists of **five rounds**, and each round usually introduces a new mechanism, often through one or more additional assets.

For each product, the first step is usually the same:

- download the data capsule
- extract the `.csv` files
- load them into a notebook or analysis environment of your choice

Use Python, R, Excel, or even Power BI if you must.

It is also worth mentioning that **Jasper Merle’s backtester** was a major help during IMC Prosperity 3. You should not expect the results to match the live challenge one-to-one, but strong backtester performance is generally still a good sign.

For example, a backtest result around **35K** roughly translated to about **9K** in Round 1 of IMC 3, which was approximately **top 10%**.


### Tutorial round assets

**Emeralds**, much like **Rainforest Resin** in IMC 3, behave like a classic stationary asset.  
If you plot the historical data for Emeralds, you will see that the mid-price stays centred around **10,000** and oscillates around that level with a spread of roughly **16**. That makes it a strong candidate for a straightforward market-making strategy.

![Screenshot](utils/Emeralds.png)

**Tomatoes**, much like **Kelp** in IMC 3, show drift.  
Because of that, you cannot simply deploy a static market-making strategy and call it a day. You need an approach that either adapts to the drift or actively benefits from it.

That could include ideas such as:

- drift-aware market making
- short-horizon trend following
- short-selling where appropriate
- other models that react to directional behaviour in the data

![Screenshot](utils/tomatoes.png)

### Round 1

For the first round, we traded two primary assets: **Intarian Pepper Root** and **Ash Coated Osmium**. These followed patterns similar to **Emeralds** and **Tomatoes** from the tutorial round, but with a few key evolutions in their behavior:

**Intarian Pepper Root** mirrored the reliability of **Emeralds**, but transitioned from a static price to a consistent **linear upward trend**. This steady climb aligns with the moderators' sentiment: reaching the 200K cutoff this year remains a very realistic goal despite the high target.

**Ash Coated Osmium** functioned as the dynamic counterpart, similar to **Tomatoes**, but displayed much more aggressive **mean-reversion**. It remained tightly anchored to a baseline (around 10,000), frequently snapping back to its center after brief bouts of volatility.

![Screenshot](utils/pepper_root.png)

Similar to **Tomatoes**, **Ash Coated Osmium** functioned as a dynamic asset; however, it was characterized by much more aggressive mean-reversion behavior. It consistently oscillated within a tight range, frequently snapping back to its 10,000-unit baseline after brief deviations.
![Screenshot](utils/osmium.png)

Here is a link to the folder for [round 1](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/tree/main/Round%201)

### Round 2

No updates until the round finishes.

Here is a link to the folder for [round 2](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/tree/main/Round%202)

## The five pillars: Alpha, Risk, Inventory, Execution, Portfolio Management

At its heart, IMC Prosperity is a challenge in **high-frequency trading**, **algorithmic trading**, and **market making**.

That means we should think beyond simply “finding alpha” and consider the full system behind a trading strategy.

A useful way to break that system down is into five parts:

1. **Alpha engine**
2. **Risk engine**
3. **Inventory engine**
4. **Execution engine**
5. **Portfolio management**

Below is a more detailed view of each.

### Alpha

A simple way to think about many IMC rounds is as a sequence of increasingly difficult pricing and prediction problems.

For each asset, IMC is effectively presenting a different type of alpha opportunity.

For a **stationary asset**, the core idea is simple: **buy low, sell high**.  
The price moves around a stable level, so the job is to identify when it is temporarily cheap or expensive relative to that anchor.

For an asset with **drift**, things become more interesting.  
Now the goal is no longer just “buy low, sell high” around a fixed centre. Instead, you want to identify **local minima**, **local maxima**, and the direction of movement.

That is the beginning of **trend-following**.

As the rounds progress, IMC usually increases the complexity in the same direction.

Imagine, for example, that Round 2 introduces an asset correlated with the drifting one. Now you are not just dealing with one moving curve, but with a relationship between multiple assets.

That is the beginning of **pairs trading**.

Later rounds may introduce **basket arbitrage**, **derivatives**, or more complex combinations of assets. These are really just further extensions of the same core question:

**What is mispriced, relative to what, and why?**

As the products become more complex, the methods used to extract alpha become more complex too.

[Alpha resources](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/tree/main/alpha)


### Risk

If you think you can ignore risk, skip this section and enjoy the leaderboard consequences.

For the rest of us, risk is one of the central problems in trading.

It is not enough to have a profitable signal. You also need to control how much you can lose when the signal is wrong, late, noisy, or overwhelmed by changing market conditions.

That means thinking about:

- current exposure
- unrealised loss
- adverse price movement
- volatility
- concentration of positions

Sometimes risk mitigation means reducing size.  
Sometimes it means exiting part of a position.  
Sometimes it means closing the trade entirely.

A strategy without risk controls is not really a strategy. It is just an opinion with leverage.

[Risk resources](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/tree/main/risk)


### Inventory

You also need to know what you actually hold.

That is where inventory management comes in.

In the tutorial round, the maximum inventory for **Emeralds** and **Tomatoes** is **80**.  
That does **not** mean you should trade right up to the edge all the time. It is usually much better to introduce **soft limits**, or even multiple layers of limits, before you ever hit the hard cap.

One important thing to remember is that your orders are not magically separated by “idea” once they hit the market.

For example:

```text
buy 10 EMERALDS @ 100
buy 15 EMERALDS @ 100
```

is effectively just:
```
buy 25 EMERALDS @ 100
```

The market does not care whether one order came from your alpha model and the other came from your inventory logic. They combine into the same net exposure.

This is why alpha, risk, and inventory cannot be designed in isolation. They must work together, otherwise one component may accidentally amplify or cancel another.

[Inventory resources](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/tree/main/inventory)


### Execution

Execution is where everything comes together.

Your alpha may be good.
Your risk logic may be sensible.
Your inventory controls may be clean.

But if your execution is poor, the whole system still underperforms.

Execution is the process of deciding how orders should actually be placed, sized, split, updated, cancelled, or held back.

That includes questions like:

- Should you cross the spread or quote passively?
- Should you place one large order or several smaller ones?
- Should you cancel an order when conditions change?
- Should you stagger execution over time?

Here are two useful ways to think about it.

#### Hypothetical 1: cancelling bad fills

Imagine you are not trading against a simulation, but against a brilliant opponent who always knows the future.

The only advantage you have is speed: you can cancel your orders before they are hit.

You post:
```
buy 10 EMERALDS @ 100
```
Then you notice that your opponent is about to sell into it.

Do you keep the order live, or cancel it?

Sometimes the answer is to keep it.
But often, having a cancellation rule ready is the difference between being a liquidity provider and being someone else’s exit liquidity.

#### Hypothetical 2: distributing a large order

Now imagine your best alpha signal fires.

It is strong, but not perfect. Maybe it is right **80%** of the time, and sometimes it fires slightly too early or too late.

Rather than sending one large order immediately, you might distribute the trade over time.

For example, instead of buying **100 EMERALDS** all at once, you could split that into **10 smaller orders** over the next **10 time steps.**

That kind of execution logic can reduce the damage from early entries, poor timing, or short-term noise.

Call it **distribution, slicing,** or **VWAP-style execution**. The exact method matters less than the principle:

good execution helps imperfect signals survive reality.

[Execution resources](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/tree/main/execution)

### Portfolio management

This one sounds fancier than it needs to.

Portfolio management here does **not** mean long-term investing.
It simply means deciding how to allocate capital, risk, and inventory across multiple strategies or assets.

For example:

- you may have two alpha signals on the same asset
- you may have one market-making signal and one trend signal
- you may have multiple related assets competing for limited inventory

At that point, you need some way to decide how much weight each idea should receive.

You could just go with:
“I like this one more.”

That is a valid human strategy.
It is also a good way to let more systematic people outrank you.

A better starting point is to think in terms of expected return, variance, correlation, and capital allocation.

[Portfolio management resources](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/tree/main/portmng)


## Where beginners should stop, and where advanced readers should continue
For those who want to go deeper into the challenge, it helps to understand what the system actually looks like so that we can approach it as a simplified version of a real market.

As with any trading simulation, a few things are worth keeping in mind:

1. We are the trader, and we are competing against other traders — in this case, bots.
2. There is a matching engine, much like on a real exchange.
3. From the exchange data and messages, you can reconstruct the order book. At the moment, it is only 3 levels deep.
4. This is also where realism stops: your orders do not appear to affect the bots beyond the decisions they are already making. There is no psychological component or adaptive behaviour on the other side.

The dataset provided by the exchange contains only price and volume. That means you cannot identify who is placing which orders or build strategies around specific counterparties.

Everything beyond that is essentially your own trading shop setup.

We have effectively unlimited capital, but performance is measured by PnL, which is at least familiar territory. Given that, it makes sense to approach the challenge as scientifically and systematically as possible.

A few technical principles are worth keeping in mind:

1. Keep memory usage and computation time as efficient as possible.
2. Maintain strong internal control over inventory, risk, current PnL, exposures, executions, forecasting, signal quality, and anything else that matters to your process.
3. Build something generalisable. Yes, you can hand-tailor strategies for every tiny scenario and hard-code edge cases everywhere, and some teams did exactly that last year. But for most people, that is not the best lesson to take away from the competition.

Try not to build nonsense.

You are not coding tomorrow’s market prices in advance. A better approach is to build a general framework that makes sense and could still be useful outside the competition. Use sensible tools: estimate mid-prices, fit simple models, and test ideas properly.

Use something like a linear regression for mid-price prediction.

Do not write:
```
at time t = 10, mid-price = 100
at time t = 101, mid-price = 103.5
```
That is not modelling. That is just hard-coded fantasy.







