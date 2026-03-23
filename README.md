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

<br>
<br>
<p align="center">
If you are new to the entire IMC prosperity challenge, you will initially land on this page. 
</p>

![Screenshot](utils/Skærmbillede%202026-03-23%20104551.png)

<br>
<br>
<p align="center">
Pressing the button(continue) will lead you to the initial setup, I mean if you've signed up and all.
</p>

![Screenshot](utils/Sk%C3%A6rmbillede%202026-03-23%20104600.png)

<br>
<br>
<p align="center">
The timer is just counting down, but pressing "start mission", should lead you here.
</p>

![Screenshot](utils/Sk%C3%A6rmbillede%202026-03-23%20104609.png)

<p align="center">
On this interface you can upload your algorithmic trading strategy by hitting "open challenge", otherwise you can scroll down and download the data capsule for the Emeralds and Tomatoes.
The data capsule will help you find alpha, research and develop initial ideas for your algorithmic trading upload.
</p>

<p align="center">
As mentioned hitting "open challenge" leads to here, where you can upload your trading file. It is important that it is a .py file.
</p>

![Screenshot](utils/Sk%C3%A6rmbillede%202026-03-23%20104622.png)

<p align="center">
After uploading a trader you will get a graph like below, you can also select between your different uploads to see which one performed best.
</p>
  
![Screenshot](utils/Sk%C3%A6rmbillede%202026-03-23%20104649.png)



<p align="center">
Pressing the side menu opens up the following. Where I would recommend everyone to read the "wiki"
</p>
  
![Screenshot](utils/Sk%C3%A6rmbillede%202026-03-23%20104713.png)


<p align="center">
Pressing "wiki" leads here. Much of the information about each round and the overall behaviour is provided here. DO READ IT THOROUGHLY.
</p>
  
![Screenshot](utils/Sk%C3%A6rmbillede%202026-03-23%20104724.png)



### How do you start coding your python code to run algorithmic trading for prosperity 4?
I would recommend Visual Studio Code. I am however using Spyder through Anaconda. That is also a choice.
[Visual Studio](https://code.visualstudio.com/) \
[Anaconda Navigator](https://www.anaconda.com/products/navigator)







## What the fuck is alpha?

What is actually going on?


For this tutorial round, we are given two assets.
Tomatoes and Emeralds. Which behave in two distinct ways. Two the untrained eye, that is "edible" and "unedible".
But if you open the data capsules, you can build research and figure out the generalistic mechanics that IMC has put out for those.

![Screenshot](utils/Sk%C3%A6rmbillede%202026-03-23%20110755.png)
If you ain't got no idea of where to get the data. It is right here -> [link]



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
