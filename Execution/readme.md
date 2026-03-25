# Execution Schemas

Execution is the part that turns an idea into actual orders.

You can have a good fair value model, a good signal, and a good inventory framework, but if your execution is poor, then your realised performance will also be poor.

This note is about the execution schemas we use to place, manage, and remove orders appropriately.

---

## What execution is actually doing

At the simplest level, execution answers the question:

> Given what we currently believe, what orders should we send right now?

That sounds trivial, but it is not.

Execution has to decide:

- whether to **take** liquidity or provide it,
- where to place quotes,
- how much size to send,
- how aggressively to flatten inventory,
- when to avoid bad fills,
- and how to behave under changing market conditions.

So execution is not just "send order."
It is the layer that translates:

- fair value,
- alpha,
- inventory,
- risk,
- and market state

into an actual set of orders.

---

## The core execution schema

A very common schema we use is:

1. **Take orders**
2. **Clear orders**
3. **Make orders**

This is also the structure used in the EMERALDS execution logic. :contentReference[oaicite:1]{index=1}

This can be understood as:

### 1. Take
If the market is already giving us a very good price, we immediately trade against it.

This is the aggressive part.

Examples:

- buy when the best ask is sufficiently below fair value,
- sell when the best bid is sufficiently above fair value.

This is the part where we say:

> "That price is already wrong enough. Just hit it."

---

### 2. Clear
After taking trades, we may now hold inventory.

If we are long or short and the market gives us an acceptable chance to reduce that position without too much pain, we do so.

This is the inventory-cleaning part.

Examples:

- if we are long, post or send sells near acceptable exit levels,
- if we are short, post or send buys near acceptable exit levels.

This is the part where we say:

> "We have risk on. Can we reduce it sensibly?"

---

### 3. Make
If there is no immediate gift in the market, we become the market.

We place resting bids and asks around fair value and try to earn spread.

This is the passive market making part.

Examples:

- quote bid below fair value,
- quote ask above fair value,
- skew those quotes depending on inventory.

This is the part where we say:

> "If nobody is giving us a free trade, we will stand there and get paid for being available."

---

## Why this schema is useful

This structure is useful because it separates three very different execution intentions:

- **Take** = exploit immediate opportunity
- **Clear** = manage inventory and reduce exposure
- **Make** = earn spread passively

Those are not the same thing.

A lot of bad trading logic comes from mixing them together into one vague blob of "place some orders."

That usually creates problems like:

- taking when you should be flattening,
- quoting passively when you should be aggressive,
- adding inventory when you should be reducing it,
- or flattening too early and killing good expected value.

The schema forces clarity.

---

## The main execution styles

In practice, the schemas we use tend to fall into a few common styles.

---

### 1. Aggressive taking schema

Used when the market is obviously mispriced relative to our fair value.

#### Logic
- Look at best bid and best ask.
- Compare them to fair value.
- If the edge is large enough, trade immediately.
- Respect position limits.

#### Purpose
- Capture obvious edge fast.
- Do not wait for passive fills if the current market is already offering profit.

#### Risks
- Adverse selection
- Overtrading
- Building inventory too quickly

#### Typical controls
- maximum take size,
- minimum edge threshold,
- adverse volume filters,
- inventory-aware reductions in aggressiveness.

In your EMERALDS example, this appears as best-price taking and also as a stronger tiered version where larger mispricings allow larger take size. :contentReference[oaicite:2]{index=2}

---

### 2. Passive market making schema

Used when fair value is stable enough and spread capture is attractive.

#### Logic
- Quote around fair value.
- Join existing good prices or slightly improve them.
- Rest orders and wait to be filled.

#### Purpose
- Earn spread repeatedly.
- Provide liquidity rather than crossing the spread.

#### Risks
- Being picked off
- Sitting with stale quotes
- Building one-sided inventory

#### Typical controls
- default quote distance,
- join/disregard rules,
- size control,
- quote refresh logic,
- inventory skew.

This is the classic:
> buy a bit below fair, sell a bit above fair.

---

### 3. Inventory-skewed making schema

Used when passive quoting is still desired, but inventory must influence behaviour.

#### Logic
- If long, shift quotes downward and/or bias toward selling.
- If short, shift quotes upward and/or bias toward buying.
- Reduce size on the side that worsens inventory.
- Increase size on the side that helps flatten.

#### Purpose
- Keep making markets without losing control of exposure.

#### Risks
- Over-skewing and missing profitable fills
- Under-skewing and accumulating too much inventory

#### Typical controls
- skew per inventory bucket,
- soft position limits,
- asymmetric order sizing,
- hard inventory protection.

Your EMERALDS market-making logic does exactly this by shifting both quotes with inventory and adjusting buy/sell size asymmetrically. :contentReference[oaicite:3]{index=3}

---

### 4. Inventory-clearing schema

Used when position reduction becomes more important than fresh spread capture.

#### Logic
- Measure current inventory after earlier trades.
- Find acceptable prices where the position can be reduced.
- Send flattening orders without crossing too far into bad value.

#### Purpose
- Reduce risk.
- Free capacity for better future trades.
- Avoid getting stuck in large one-sided positions.

#### Risks
- Exiting too early
- Giving up too much edge
- Repeatedly churning around fair value

#### Typical controls
- clear width,
- soft vs hard position thresholds,
- urgency schedule,
- size caps on flattening.

---

### 5. Tiered aggression schema

Used when not all mispricings deserve the same response.

#### Logic
- Small edge -> small size
- Medium edge -> medium size
- Large edge -> large size

#### Purpose
- Match aggression to opportunity.
- Avoid using maximum size on weak signals.

#### Risks
- Poor threshold design
- Too many arbitrary tiers
- Missing subtle but repeatable edge

This is often much better than a binary rule like:

- take everything, or
- take nothing.

The market is rarely that simple.

---

### 6. Adverse-selection-aware schema

Used when visible liquidity may be dangerous.

#### Logic
- Avoid taking or joining suspiciously large or fast-moving quotes.
- Filter on volume, flow, spread behaviour, or order book changes.
- Require stronger confirmation before trading.

#### Purpose
- Avoid getting trapped by informed flow or unstable price moves.

#### Risks
- Becoming too cautious
- Missing real opportunities

#### Typical controls
- adverse volume threshold,
- book instability flags,
- recent flow imbalance filters,
- quote lifetime checks.

Your execution framework already leaves room for this through `prevent_adverse` and `adverse_volume` logic on taking orders. :contentReference[oaicite:4]{index=4}

---

## The key inputs execution should consume

Execution should not exist in isolation.

It should consume outputs from the rest of the trading system.

At minimum, execution should know:

- **fair value**  
  What we think the asset is worth right now.

- **position / inventory**  
  Whether we are long, short, or flat.

- **position limits**  
  How much room we have left.

- **market state**  
  Stable, trending, volatile, mean-reverting, dislocated, thin, etc.

- **book state**  
  Spread, depth, imbalance, queue, nearby liquidity.

- **risk state**  
  Whether we are in normal mode, cautious mode, or flattening mode.

Without these, execution becomes blind order placement.

---

## The real purpose of execution

Execution is not just about getting filled.

It is about getting filled:

- at the right price,
- in the right size,
- for the right reason,
- at the right time.

That means good execution should improve:

- realised PnL,
- inventory control,
- risk usage,
- and repeatability.

A bad execution layer destroys good strategy.

A good execution layer rescues mediocre strategy.

---

## A simple mental model

You can think of execution as a hierarchy of questions:

### First question
**Is the market already offering me a very good trade?**

If yes, **take**.

### Second question
**If I already hold risk, can I reduce it sensibly?**

If yes, **clear**.

### Third question
**If neither of those apply, can I provide liquidity profitably?**

If yes, **make**.

That gives us the full loop:

> take edge -> manage inventory -> provide liquidity -> repeat

---

## Practical takeaway

A robust execution framework usually needs all three:

- a way to **take**
- a way to **clear**
- a way to **make**

and then a way to adjust those based on:

- inventory,
- market state,
- signal strength,
- and risk constraints.

That is what makes execution a schema rather than a single function.

It is not one order rule.

It is a structured way of deciding how to behave in the market.

---

## Current baseline schema

Our current baseline execution schema can be summarised as:

1. **Aggressively take obvious mispricings**
2. **Reduce inventory when sensible opportunities appear**
3. **Passively quote around fair value**
4. **Skew quotes and size according to inventory**
5. **Respect hard position limits at all times**
6. **Increase caution when fills are likely to be adverse**

That is the foundation.

Everything else is refinement.

---

## Future extensions

Some obvious future upgrades to execution include:

- multi-level passive quote ladders,
- queue-position-aware quoting,
- regime-dependent spread placement,
- urgency schedules for inventory reduction,
- flow-aware cancelling and reposting,
- cross-asset execution coordination,
- execution-cost modelling,
- stealth execution logic for larger positions.

---

## Final note

Alpha tells you **what** might be profitable.

Execution determines **whether you actually realise it**.

That is why execution should be treated as a first-class system, not an afterthought.
