**Note:** I was asked by the mods not to give away code and too big hints, so I will present the simple description of the assets until after the round is over.

# Algorithmic challenge

## Interian Pepper Root
Pepper root is similar to EMERALDS from the tutorial round, but instead of a straight line with 0 slope, it has a slope of X > 0. \
This changes a key part of the ideal strategy significantly.

![Pepper Root](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/utils/pepper_root.png)

The optimal strategy was Buy and hold. I put in an *idiot* script to simply buy as quickly as possible and hold \
This was suboptimal, despite being along the right path, this makes for higher transaction costs. \
As @(April <- not a dude) mentioned, there are also opportunities to take advantage of the increasing spread.

## Ash-covered Osmium
Osmium is similar to Tomatoes from the tutorial round, it is another "asset with drift", ideally one could therefore do a similar setup \
and adjust for the behaviour of Osmium compared to Tomatoes.
![Osmium](https://github.com/MarkBrezina/Ctrl-Alt-DefeatTheMarket/blob/main/utils/osmium.png)

I cocked this up quite significantly, going back over my code I not only reversed my Z-score entry and exit. \
But also force my market making to return negative orders for some timestamps, leading to random orderbook crosses at will. \
I knew that my inventory adjustments were suboptimal, but simply had to load in.

The optimal strategy I was going for was a combination of market-making, market-taking on mispricings, mean reversion and a bit of drift.
The goal than becomes finding the proper quoting mixes of this. Talking with several people on the discord, we all struggled to find this
ideal combination and that is what I suspect gets the difference between all of us.


# Manual

DRYLANX_FLAX: bid 9999 @30. This leads to a clearing price of 29, and a fill of 9999 for our bid order. Profit is therefore 9999(30-29) = 9999. Increasing our order size to 10k would push the clearing price up to 30, leading to 0 profit despite our bid getting filled, and bidding lower either leads to our bid not getting filled, or getting 5k filled @29, leading to a smaller profit of 5000.

EMBER_MUSHROOM: bid 19999 @17. This leads to a clearing price of 16 (matched volume of 91k), meaning our profit is 19999(19.9-16). Note here that 19.9 is the buyback at 20 minus transaction costs (0.05 for buying and 0.05 for selling per unit). Profit here is therefore 77996.1, and increasing our bid volume to 20k would push the clearing price up to 17, leading to less profit.
