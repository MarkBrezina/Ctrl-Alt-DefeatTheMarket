# Inventory Control

Inventory control is the part of trading logic that stops you from becoming accidentally stupid.

You may have good alpha.
You may have good fair values.
You may even have good execution.

But if you keep accumulating position without control, then eventually the market will remind you that being right is not the same as surviving.

This note is about how we think about inventory, why it matters, and how we control it.

---

## What inventory actually is

Inventory is your current position in an asset.

If you have bought more than you have sold, you are **long** inventory.

If you have sold more than you have bought, you are **short** inventory.

If buys and sells balance, you are **flat**.

That sounds trivial, but the important part is this:

> Inventory is not just a number.  
> Inventory is stored risk.

Every unit of inventory means you are exposed to future price movement.

If you are long, you want price to go up.
If you are short, you want price to go down.

So inventory is the bridge between your trading decisions and your market risk.

---

## Why inventory control matters

Inventory control matters because trading is not just about finding edge.

It is also about surviving the path between entering and exiting positions.

A strategy that keeps building inventory without control will eventually run into one or more of these problems:

- large drawdowns,
- inability to exit cleanly,
- forced bad trades,
- loss of flexibility,
- reduced ability to capture better opportunities later.

So inventory control is not there to make trading boring.

It is there to make trading repeatable.

---

## The real problem

The problem is not inventory itself.

The problem is **unmanaged inventory**.

Holding inventory is normal.

In fact, many profitable strategies *must* hold inventory temporarily in order to make money.

The issue is when:

- inventory becomes too large,
- inventory lasts too long,
- inventory is held for the wrong reason,
- or inventory grows faster than your ability to manage it.

This means inventory control is not about "always be flat."

It is about:

- carrying inventory **when justified**,
- reducing inventory **when necessary**,
- and preventing inventory from becoming the thing that kills the strategy.

---

## The core goal

The core goal of inventory control is simple:

> Hold only the amount of position that is justified by expected reward, market state, and execution capacity.

That means we do **not** want:

- unnecessary size,
- unnecessary duration,
- unnecessary concentration,
- or unnecessary panic exits later.

---

## A useful mental model

Inventory control is the balance between two desires:

### 1. Let winners breathe
If the position is good, you do not want to kill it too early.

### 2. Do not become a bag holder
If the market moves against you, or if your position becomes too large, you need a way out.

Good inventory control sits between these two.

Too strict, and you kill edge.
Too loose, and you become exit liquidity.

---

## The basic inventory states

A practical way to think about inventory is in states.

### Flat
You have no position.

This is maximum flexibility and minimum direct price exposure.

### Light inventory
You hold a small position.

This is usually normal and acceptable.

### Moderate inventory
You hold enough position that it should begin affecting quoting, sizing, and execution choices.

At this stage, inventory should influence behaviour.

### Heavy inventory
You hold a large position.

At this point, reducing exposure becomes increasingly important.

Fresh alpha should be treated more cautiously.

### Critical inventory
You are too close to the hard limit.

Now the priority is no longer ideal trading.
The priority is to avoid getting trapped.

---

## Hard limits and soft limits

A useful framework is to distinguish between **hard** and **soft** inventory limits.

### Hard limit
This is the absolute maximum position you are allowed to hold.

You do not cross it.

Ever.

This is the final safety rail.

### Soft limit
This is the level at which your behaviour should already begin changing.

Before you hit the hard limit, you should already be:

- reducing quote size,
- skewing quotes,
- flattening more actively,
- becoming more selective with new entries.

The soft limit is what stops you from constantly smashing into the hard limit like an idiot.

---

## What inventory control actually changes

Inventory control should affect the trading system in several ways.

### 1. Quote placement
If you are long, your quotes should generally shift in a way that helps you sell more easily and buy less aggressively.

If you are short, the reverse applies.

### 2. Quote size
If you are already heavily long, you should usually reduce bid size and allow more ask size.

If you are heavily short, you should reduce ask size and allow more bid size.

### 3. Aggression
If you are near your limits, you should become less willing to add to the wrong side of the position.

### 4. Clearing urgency
The larger the inventory, the more urgent it becomes to reduce it sensibly.

### 5. Risk appetite
Inventory should influence whether you are still in normal trading mode or entering defensive mode.

---

## The simplest inventory rule

The most basic inventory rule is:

- if long, bias toward selling,
- if short, bias toward buying.

That alone already improves a lot of systems.

But in practice, we usually want more structure than that.

---

## Common inventory control mechanisms

---

### 1. Inventory skew

This is the classic approach.

If long:
- lower your fair or effective quote centre,
- sell more aggressively,
- buy less aggressively.

If short:
- raise your effective quote centre,
- buy more aggressively,
- sell less aggressively.

The purpose is not to panic.
It is to naturally pull inventory back toward flat.

---

### 2. Asymmetric sizing

Instead of using the same size on both sides, adjust size according to current position.

For example:

- if long, smaller bids and larger asks,
- if short, larger bids and smaller asks.

This prevents the system from carelessly adding more to an already large position.

---

### 3. Inventory buckets

Rather than reacting to every single unit of position, divide inventory into ranges.

Example:

- **0 to 20**: normal behaviour
- **20 to 40**: mild skew
- **40 to 60**: strong skew
- **60+**: defensive behaviour

This gives you a cleaner and more stable control system.

---

### 4. Time-based inventory control

Inventory is not only about size.

It is also about **how long** you have been holding it.

A position that was fine 2 seconds ago may become a problem after 200 timesteps.

So inventory control can include rules like:

- if held briefly, allow it room,
- if held too long, begin reducing more aggressively,
- if held far too long, switch to exit mode.

Because sometimes the issue is not that the position is large.

The issue is that it is stale.

---

### 5. Mark-to-market pain control

Inventory should also respond to whether it is actually hurting.

If your held position is moving against you, it may deserve stricter treatment than an equally large position that is stable or profitable.

This does **not** mean emotional stop-loss behaviour.

It means acknowledging that:

- inventory size,
- holding time,
- and unrealised pain

all matter together.

---

### 6. Market-state dependent control

Inventory should not be treated the same way in every regime.

For example:

- in stable mean-reverting markets, you may tolerate more inventory,
- in trending markets, wrong-sided inventory is more dangerous,
- in thin or volatile markets, exit may be harder.

So inventory tolerance should depend partly on market state.

---

## A good way to think about inventory pressure

Inventory creates pressure on the system.

The more inventory you hold, the more the following questions start to matter:

- Can I still exit cleanly?
- Am I still acting on alpha, or am I now just managing old mistakes?
- Is this position intentional, or did it drift into existence?
- If a better opportunity appears, do I still have capacity?

This is why large inventory is costly even before it becomes directly unprofitable.

It reduces optionality.

---

## Inventory is connected to execution

Inventory control and execution should not be separated too much.

Execution asks:

> How should I place orders?

Inventory asks:

> Given my current exposure, how should that answer change?

That means inventory control should directly modify execution behaviour.

Examples:

- skew quotes,
- change size,
- change urgency,
- disable certain trades,
- switch from passive making to active clearing.

So inventory is not a reporting variable.

It is an active input into decision-making.

---

## Inventory is also connected to alpha

A common mistake is to think alpha and inventory are separate.

They are not.

A signal may say:
> buy

But inventory may say:
> not with this much size already on

A signal may say:
> keep holding

But inventory duration may say:
> this trade has overstayed its welcome

Good trading systems do not blindly obey alpha.

They combine alpha with inventory and execution constraints.

---

## A practical hierarchy

A useful hierarchy is:

### Small inventory
Let alpha dominate.

### Medium inventory
Let alpha and inventory share control.

### Large inventory
Let inventory dominate more of the decision.

### Extreme inventory
Prioritise survival and controlled reduction.

This keeps the system from behaving as if a beautiful theoretical signal matters more than getting stuck.

---

## What bad inventory control looks like

Bad inventory control often looks like this:

- averaging into everything forever,
- hitting hard limits constantly,
- refusing to realise that the market regime changed,
- holding positions because "it should come back,"
- flattening only after the damage is already done,
- or forcing exits so early that no strategy ever gets room to work.

All of these are versions of the same problem:

> no clear framework for how much risk should be carried, for how long, and under what conditions.

---

## What good inventory control looks like

Good inventory control usually has the following properties:

- hard limits are respected,
- soft limits influence behaviour early,
- quoting is skewed sensibly,
- size adjusts with exposure,
- stale positions get treated differently from fresh ones,
- inventory tolerance changes with market state,
- and the system remains able to take future opportunities.

In short:

> good inventory control protects the strategy without suffocating it.

---

## A baseline inventory schema

A simple and robust baseline is:

1. Define a hard position limit.
2. Define a softer warning threshold.
3. Skew quotes based on current inventory.
4. Reduce order size on the side that worsens exposure.
5. Increase urgency to flatten as inventory grows.
6. Track how long inventory has been held.
7. Become more defensive when inventory is both large and stale.
8. Allow market state to affect how much inventory is acceptable.

That is already enough to make a strategy much more robust.

---

## Example intuition

Imagine a stationary asset where fair value is stable.

- Small long inventory is acceptable.
- Larger long inventory means your asks should become more attractive.
- Very large long inventory means you should stop being enthusiastic about buying more.
- Long inventory held for too long means spread capture is no longer the only goal; now you want to reduce risk.

So the logic evolves from:

> make markets

to:

> make markets carefully

to:

> clear this position before it becomes a problem

That transition is the whole point of inventory control.

---

## Final note

Alpha finds opportunities.

Execution places orders.

Inventory control decides how much pain, patience, and exposure the system is allowed to carry while doing either.

Without inventory control, a trading strategy is just a smart way of eventually becoming too long or too short.

With good inventory control, the strategy stays alive long enough to keep exploiting edge.
