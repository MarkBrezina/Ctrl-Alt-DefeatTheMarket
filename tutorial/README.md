# Tutorial Round Assets

In the first round, we work with two assets:
- **EMERALDS**, which can be treated as a stationary or stable asset
- **TOMATOES**, which can be treated as a dynamic asset with drift

## EMERALDS

**EMERALDS** maintains a nearly constant mid-price, with a very stable spread of around **16** at each timestep.

After extensive testing, I concluded that the most effective approach is simple **market making on each timestep**, waiting for other participants to match against posted quotes. In practice, this gives the strongest result, with an approximate PnL of **1050**.

I initially explored whether there was additional alpha to capture from participants pushing both the bid and ask across the mid-price. My expectation was that there might be value in also incorporating this behaviour into the strategy. However, after repeated testing, I found that the additional alpha was either effectively zero, or at best only marginally positive if implemented very well. My view is that the extra complexity is not justified by the gain.

Because of this, the **maker-taker logic** from **Linear Utilities in 2024** is not necessary for the tutorial round.

## TOMATOES

**TOMATOES**, unlike EMERALDS, does not maintain a stable mid-price. Instead, its price **drifts over time in different directions**, and its spread also changes throughout the round.

This makes it fundamentally different from EMERALDS. Rather than treating it as a stable quoting environment, it should be approached as a more dynamic asset where **price movement, drift, and changing spread conditions** matter much more.
