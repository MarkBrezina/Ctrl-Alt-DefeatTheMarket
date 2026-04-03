**A note to everyone participating:** \
After some discussion in the server, I want to add something important: please do not let one bad moment, one rough week, or one discouraging comment decide your future for you.

This competition is hard. Learning is hard. Growth is hard. Very few people simply “get it” straight away, and most people improve by making mistakes, correcting them, and continuing anyway. That is normal.

Feeling tired, doubtful, or behind does not mean you are not capable. It means you are human. A moment of vulnerability is not the same as defeat. What matters is whether you keep going, keep learning, and keep reducing your errors over time.

So despite what anyone says, including me: do not give up on yourself too quickly. Rest if you need to. Recalibrate if you need to. Laugh at the setbacks if you can. But keep moving forward.

Even the strongest people fail, struggle, and look foolish before they improve. That is part of the process.

Keep going.


## How to Deal with Prosperity Mentally

Prosperity is exciting, frustrating, addictive, and humbling all at once. That is true whether this is your first time participating or your second or third.

If it is your first time, a lot of what you see will feel completely new. You may begin with simple ideas and quickly realize that the competition is not just about plugging in a few indicators and hoping for the best.

If it is your second time, you already know that. You know this is not just a sandbox for moving averages. It is a difficult challenge that forces you to think more seriously about markets, data, robustness, and adaptation.

Regardless of your experience level, it will not be easy.

By Round 3, some teams will continue and others will fall out. If you are one of the teams that makes it further, do not mock or belittle the rest. Most people worked hard. Outcomes are not driven by effort alone. Skill matters, preparation matters, luck matters, and life outside the competition matters too.

Many people are carrying stress into this challenge: exams, work, finances, family pressure, health problems, relationship problems, and all the rest. Prosperity can be brutal in the same way real life is brutal. Sometimes you work hard and still fall short.

That does not mean the effort was wasted.

The good part is that you can reflect, recover, improve, and come back stronger next time. You may only improve a little at first. You may double your score later. Progress often looks slow until suddenly it is not.

I should be honest: this competition is extremely hard. You need to learn quickly, think clearly, and adapt to problems that often feel much closer to real-world trading than to neat academic exercises.

But that difficulty is also what makes it valuable.

Even if you do not reach the top this year, you will have learned what it feels like to face a hard, open-ended quantitative problem under pressure. And if you really want to keep going, you can. Nobody can stop you from learning, building, and returning better prepared next time.

---

### How Not to Get Demoralized

A good way to avoid getting demoralized is to measure yourself properly.

Do not compare your first serious attempt to the best teams in the world. Compare yourself to where you were a week ago. Did you understand the data better? Did you structure your code better? Did you stop overfitting one stupid trick and start building something repeatable? Did you learn how to debug properly? Those things matter.

Another thing to remember: a bad round does not mean you are bad at this.

Sometimes your model is fragile. Sometimes your assumptions are wrong. Sometimes your implementation is poor. Sometimes you were simply not prepared yet. All of that can be fixed.

What destroys people mentally is not losing. It is attaching too much of their self-worth to one result.

Treat the competition as feedback, not as a final judgment on your intelligence or future.

---

### Why Most Teams Overcomplicate Too Early

A lot of people are drawn to quant because they love mathematics, elegant patterns, and complicated ideas. That curiosity is good. It is one of the reasons many of us ended up here in the first place.

The problem is that beginners often confuse complexity with quality.

Most trading problems are not improved by piling on ten half-understood models, twenty fragile parameters, and a separate subsystem for every tiny statistical blip. In many cases, that just creates a machine that is impossible to reason about and easy to break.

Simple ideas, implemented well, usually outperform messy complexity.

If you want to capture broad behaviours, build broad components. For example:
- one component for stationary / mean-reverting assets
- one component for trend or momentum-like behaviour
- one component for statistical arbitrage
- one component for risk and inventory control

Do not write a whole trader for every tiny observation. Build around the major behaviours you actually understand.

A good rule is this: if you cannot explain your logic simply, you probably do not understand it well enough yet.

---

### Why Robustness Beats One Lucky Run

If you discover that you can hardcode, overfit, or tune parameters to make one particular dataset look amazing, that may feel clever, but it will usually fail when it matters.

Prosperity rewards strategies that survive variation, not just strategies that looked good once.

If your method only works on one specific path, one exact sequence, or one narrow set of assumptions, then it is not really a strategy. It is an accident that happened to line up with a particular test.

A robust approach should still make sense when conditions change.

That matters even more because the visible backtest is not the whole story. Final evaluation is not just about doing well on the exact path you have already seen. The more your logic depends on memorising the past instead of modelling behaviour, the more fragile it becomes.

In other words: do not aim for one lucky screenshot. Aim for something that would still make sense tomorrow.

---

### How to Work in Weeks / Phases

A lot of participants will have exams, coursework, jobs, or other responsibilities during Prosperity. Time management matters almost as much as technical skill.

If you are working alone, you need to be realistic. If you leave everything until the last moment, you may miss the chance to submit something decent at all.

If you are in a team, split the workload sensibly. But do not let people disappear into isolated silos. Everyone should still understand the broad logic of what the team is doing.

A practical approach is to work in phases:

**Phase 1: Understand the round**
Read the task carefully. Identify the asset types, likely behaviours, constraints, and possible traps.

**Phase 2: Build something simple that works**
Do not aim for brilliance immediately. Get a basic system running, test assumptions, and make sure your code is stable.

**Phase 3: Improve the logic**
Only once the baseline works should you begin refining signals, risk handling, inventory logic, or interactions across products.

**Phase 4: Review and simplify**
Before submission, ask what can be removed, clarified, or made safer. Cleaner systems often perform better than clever-looking ones.

The main point is not to spend all your time fantasising about an ideal strategy while failing to submit a solid one.

---

## How to Practice Before, During, and After Prosperity

Prosperity ends, but the skill-building does not.

When the competition finishes, many people feel a strange drop. For weeks, they were thinking hard, learning quickly, testing ideas, and engaging with something genuinely challenging. Then suddenly it is over.

That is exactly when you should keep going.

The obvious route is to return to your studies, coursework, or job applications. But if the competition gave you a real taste for this kind of work, there are many ways to continue:
- build research notebooks
- collect and clean your own datasets
- backtest ideas outside the competition
- study execution, microstructure, or portfolio construction
- develop better infrastructure and data pipelines

Crypto is one practical place to start because the data is widely available and relatively accessible. The market is messy, but many useful patterns and research habits carry across to other asset classes.

The point is not that Prosperity is everything. The point is that it can be the beginning of serious, independent research.

---

## Sharpe Over Raw PnL

Raw PnL can be seductive. Big numbers look impressive.

But in real trading and in serious research, risk-adjusted performance matters more. A strategy that makes money in a repeatable, controlled, understandable way is much more valuable than one that occasionally explodes upward and then collapses.

That is why Sharpe, drawdown control, and repeatability matter so much.

A smaller but steadier edge is often better than a flashy system that only works when everything lines up perfectly.

If your strategy makes money with less chaos, less overexposure, and less dependence on luck, it is usually the stronger strategy.

---

### How to Think in Sharpe, Drawdown, and Repeatability

When reviewing your strategy, do not just ask:
“Did it make money?”

Also ask:
- How volatile were the returns?
- How deep were the losses on the way there?
- Could I explain why it worked?
- Would I trust this logic on another dataset?
- Is this driven by a real behaviour or by accidental curve-fitting?

Repeatability matters because one good result proves very little on its own. Multiple decent results under different conditions tell you much more.

This is one of the biggest mindset shifts in Prosperity: stop chasing the prettiest single run, and start building something you would actually trust.

---

## Expected Types of Participants

Like anywhere else, you will meet a mix of personalities.

Some people will talk loudly and know little. Some will say almost nothing and quietly build very strong systems. Some will have wild ideas and poor implementation. Others will be technically disciplined but less imaginative. Some will start weak and improve very fast. Some will start overconfident and get humbled.

That is normal.

Try not to waste too much energy comparing yourself to stereotypes, flexing, or competition theatre. Focus on learning, building, and improving.

The leaderboard matters, but it is not the only thing that matters.

---

## Final Mental Note

The best mindset I have found is curiosity.

You will fail many times, both in small ways and large ones. That is normal. The challenge becomes much easier to handle if you treat it as something to explore rather than something you must already be brilliant at.

And stay respectful.

If you spend all your time trying to impress others, acting like you know everything, or arguing aggressively, people will usually cut that down quickly. In the worst case, you can damage your reputation or get yourself removed from the community entirely.

Prosperity is hard enough without ego getting in the way.

There is a separate page dedicated to the mental side of the challenge because this affects everyone: strong participants, weak participants, first-timers, and veterans alike.

