
## 1. Simple Moving Average (SMA)

**Description:** \
The SMA is the average price over a fixed window. It smooths price data and helps identify the underlying trend.

**Use:**

- Price above SMA can suggest upward trend
- Price below SMA can suggest downward trend
- Crossovers of short and long SMAs are often used as signals

```
import pandas as pd
import numpy as np

def sma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window).mean()
```

## 2. Exponential Moving Averages (EMA)
**Description:** \
The EMA is similar to the SMA, but gives more weight to recent prices, so it reacts faster to new information.

**Use:**

- Faster trend tracking than SMA
- Often used in MACD and crossover systems

def ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()

## 3. Relative Strength Index (RSI)
**Description:** \
RSI is a momentum oscillator that measures the speed and magnitude of recent price moves. It ranges from 0 to 100.

**Typical interpretation:**
- RSI above 70: often called overbought
- RSI below 30: often called oversold

```
def rsi(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
```

## 4. Moving Average Convergence Divergence (MACD)

**Description:** \
MACD measures the difference between two EMAs, usually a fast EMA and a slow EMA. It helps detect trend direction and momentum shifts.

**Components:**
- MACD line = EMA(12) - EMA(26)
- Signal line = EMA of MACD line, usually 9
- Histogram = MACD - Signal

```
def macd(series: pd.Series,
         fast: int = 12,
         slow: int = 26,
         signal: int = 9) -> pd.DataFrame:
    
    ema_fast = ema(series, fast)
    ema_slow = ema(series, slow)
    
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    
    return pd.DataFrame({
        "macd_line": macd_line,
        "signal_line": signal_line,
        "histogram": histogram
    })
```

## 5. Bollinger bands
**Description:**\
Bollinger Bands place upper and lower bands around a moving average using standard deviation. They show relative volatility.

**Typical interpretation:**
- Narrow bands: lower volatility
- Wide bands: higher volatility
- Price touching upper/lower band can indicate stretched conditions

```
def bollinger_bands(series: pd.Series,
                    window: int = 20,
                    num_std: float = 2.0) -> pd.DataFrame:
    
    mid = series.rolling(window=window).mean()
    std = series.rolling(window=window).std()
    
    upper = mid + num_std * std
    lower = mid - num_std * std
    
    return pd.DataFrame({
        "bb_mid": mid,
        "bb_upper": upper,
        "bb_lower": lower
    })
```


## 6. Average True Range (ATR)
**Description:**
ATR measures volatility by looking at the true trading range, including gaps between periods.

**Use:**
- Volatility filter
- Stop-loss sizing
- Position sizing

```
def atr(high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        window: int = 14) -> pd.Series:
    
    prev_close = close.shift(1)
    
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = true_range.rolling(window=window).mean()
    
    return atr
```

## 7. Stochastic Oscillator
**Description:** \
This compares the current close to the recent high-low range. It is a momentum indicator.

**Typical interpretation:**
- High values: close is near recent highs
- Low values: close is near recent lows

```
def stochastic_oscillator(high: pd.Series,
                          low: pd.Series,
                          close: pd.Series,
                          k_window: int = 14,
                          d_window: int = 3) -> pd.DataFrame:
    
    rolling_low = low.rolling(window=k_window).min()
    rolling_high = high.rolling(window=k_window).max()
    
    percent_k = 100 * (close - rolling_low) / (rolling_high - rolling_low)
    percent_d = percent_k.rolling(window=d_window).mean()
    
    return pd.DataFrame({
        "%K": percent_k,
        "%D": percent_d
    })
```

## 8. On-Balance Volume (OBV)
**Description:**\
OBV is a volume-based indicator that adds volume on up days and subtracts volume on down days. It tries to detect whether volume confirms price movement.

```
def obv(close: pd.Series, volume: pd.Series) -> pd.Series:
    direction = np.sign(close.diff()).fillna(0)
    return (direction * volume).cumsum()
```

## 9. VWAP
**Description:**\
VWAP is the volume-weighted average price. It is often used intraday as a benchmark for execution quality and price positioning.

```
def vwap(high: pd.Series,
         low: pd.Series,
         close: pd.Series,
         volume: pd.Series) -> pd.Series:
    
    typical_price = (high + low + close) / 3
    cumulative_tp_vol = (typical_price * volume).cumsum()
    cumulative_vol = volume.cumsum()
    
    return cumulative_tp_vol / cumulative_vol
```


## 10. Momentum
**Description:** \
Momentum is simply the change in price over a chosen window.

**Use:**
- Positive momentum means price is above its earlier value
- Negative momentum means price is below its earlier value

```
def momentum(series: pd.Series, window: int = 10) -> pd.Series:
    return series - series.shift(window)
```
