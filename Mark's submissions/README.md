
## Concept
The overarching idea:
shared framework + per-product state + strategy-specific modules

So for each product we will have
- inventory
- realized/unrealized PnL
- local drawdown / risk usage
- fair value or reference price
- volatility / spread regime
- order book imbalance
- order flow features
- microprice / queue position features
- strategy flags or allocation weights
- execution state

On a central column we will have:
- market data ingestion
- feature calculation framework
- order management
- risk checks
- inventory accounting
- PnL accounting
- logging / replay / simulation
- configuration and deployment

such that it can be deployed easily.

Per product we will have.
- inventory
- drawdown
- local PnL
- current price / fair value
- mean-reversion score
- volatility state
- order book distribution
- order flow
- queue / fill statistics
- strategy activation or weighting

Where we will take
$$
u(t) = \pi(x(t))
$$
With u(t) being the quoting/taking/cancelling/skewing logic.
In practice, different products often share the same skeleton:

compute fair value
compute edge
skew by inventory
widen/narrow by volatility
adjust by fill probabilities
cap by risk

But the parameters, and sometimes a few feature definitions, differ by product.

So for one product you may have:

stronger mean reversion
tighter quote widths
higher inventory tolerance

and for another:

drift-sensitive fair value
more directional skew
lower hold time
more aggressive risk reduction
4. Asset templates are common

A lot of firms effectively work with templates:

stable market-making template
trending / directional template
options template
ETF / basket template
futures template
very illiquid template


![Landing page](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/utils/Sk%C3%A6rmbillede%202026-03-24%20113913.png)

## Inventory

