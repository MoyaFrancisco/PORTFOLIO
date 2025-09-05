import numpy as np

def get_thresholds_for_level(level):
    # Define los umbrales para cada nivel de exigencia
    table = {
        1: {'adx': 10, 'vol': 0.5, 'ema_cercania': 0.02, 'penalizacion': 10},
        2: {'adx': 15, 'vol': 0.8, 'ema_cercania': 0.015, 'penalizacion': 15},
        3: {'adx': 20, 'vol': 1.0, 'ema_cercania': 0.01, 'penalizacion': 20},
        4: {'adx': 25, 'vol': 1.2, 'ema_cercania': 0.007, 'penalizacion': 25},
        5: {'adx': 30, 'vol': 1.5, 'ema_cercania': 0.005, 'penalizacion': 30},
    }
    return table.get(level, table[3])

def is_bullish_engulfing(df):
    prev = df.iloc[-2]
    curr = df.iloc[-1]
    return (curr['Close'] > curr['Open'] and prev['Close'] < prev['Open'] and
            curr['Open'] < prev['Close'] and curr['Close'] > prev['Open'])

def is_bullish_hammer(df):
    curr = df.iloc[-1]
    body = abs(curr['Close'] - curr['Open'])
    lower_wick = curr['Open'] - curr['Low'] if curr['Open'] < curr['Close'] else curr['Close'] - curr['Low']
    upper_wick = curr['High'] - curr['Close'] if curr['Open'] < curr['Close'] else curr['High'] - curr['Open']
    return (body < (curr['High'] - curr['Low']) * 0.3 and lower_wick > body * 2 and upper_wick < body)

def is_bearish_engulfing(df):
    prev = df.iloc[-2]
    curr = df.iloc[-1]
    return (curr['Close'] < curr['Open'] and prev['Close'] > prev['Open'] and
            curr['Open'] > prev['Close'] and curr['Close'] < prev['Open'])

def is_breakout(df, resistance=True, lookback=20):
    if len(df) < lookback:
        return False
    if resistance:
        prev_max = df['High'].iloc[-lookback:-1].max()
        return df['Close'].iloc[-1] > prev_max
    else:
        prev_min = df['Low'].iloc[-lookback:-1].min()
        return df['Close'].iloc[-1] < prev_min

def signal_long(df, strict_level=3):
    thresholds = get_thresholds_for_level(strict_level)
    conds = []
    # EMAs alineadas: flexible o estricto según nivel
    if strict_level >= 3:
        conds.append(df['EMA20'].iloc[-1] > df['EMA50'].iloc[-1] > df['EMA200'].iloc[-1])
    else:
        conds.append(df['EMA20'].iloc[-1] > df['EMA50'].iloc[-1])
    conds.append(df['ADX'].iloc[-1] > thresholds['adx'])
    conds.append(df['VOL_REL'].iloc[-1] >= thresholds['vol'])
    if not all(conds):
        return False, [], 0
    extras = []
    # MACD cruce al alza con histograma creciente
    if (df['MACD'].iloc[-2] < df['MACDs'].iloc[-2] and df['MACD'].iloc[-1] > df['MACDs'].iloc[-1] and (strict_level <= 2 or df['MACDh'].iloc[-1] > df['MACDh'].iloc[-2])):
        extras.append('MACD cruce al alza')
    # RSI subiendo (más flexible en niveles bajos)
    if (df['RSI14'].iloc[-1] > (45 if strict_level == 1 else 48 if strict_level == 2 else 50) and (df['RSI14'].iloc[-1] < 70 or strict_level <= 2) and df['RSI14'].iloc[-1] > df['RSI14'].iloc[-2]):
        extras.append('RSI subiendo')
    # Vela envolvente alcista o martillo sobre EMA20/EMA50
    if (is_bullish_engulfing(df) or is_bullish_hammer(df)) and (
        abs(df['Close'].iloc[-1] - df['EMA20'].iloc[-1]) / df['Close'].iloc[-1] < thresholds['ema_cercania'] or
        abs(df['Close'].iloc[-1] - df['EMA50'].iloc[-1]) / df['Close'].iloc[-1] < thresholds['ema_cercania']):
        extras.append('Patrón alcista sobre EMA')
    # Ruptura con volumen de resistencia
    if is_breakout(df, resistance=True, lookback=20) and df['VOL_REL'].iloc[-1] > (thresholds['vol'] if strict_level <= 2 else 1.2):
        extras.append('Ruptura resistencia con volumen')
    confianza = min(25 * len(extras), 100)
    return (len(extras) > 0), extras, confianza

def signal_short(df, strict_level=3):
    thresholds = get_thresholds_for_level(strict_level)
    conds = []
    if strict_level >= 3:
        conds.append(df['EMA20'].iloc[-1] < df['EMA50'].iloc[-1] < df['EMA200'].iloc[-1])
    else:
        conds.append(df['EMA20'].iloc[-1] < df['EMA50'].iloc[-1])
    conds.append(df['ADX'].iloc[-1] > thresholds['adx'])
    conds.append(df['VOL_REL'].iloc[-1] >= thresholds['vol'])
    if not all(conds):
        return False, [], 0
    extras = []
    if (df['MACD'].iloc[-2] > df['MACDs'].iloc[-2] and df['MACD'].iloc[-1] < df['MACDs'].iloc[-1] and (strict_level <= 2 or df['MACDh'].iloc[-1] < df['MACDh'].iloc[-2])):
        extras.append('MACD cruce a la baja')
    if (df['RSI14'].iloc[-1] < (55 if strict_level == 1 else 52 if strict_level == 2 else 50) and (df['RSI14'].iloc[-1] > 30 or strict_level <= 2) and df['RSI14'].iloc[-1] < df['RSI14'].iloc[-2]):
        extras.append('RSI bajando')
    if is_bearish_engulfing(df) and abs(df['Close'].iloc[-1] - df['EMA20'].iloc[-1]) / df['Close'].iloc[-1] < thresholds['ema_cercania']:
        extras.append('Patrón bajista bajo EMA')
    if is_breakout(df, resistance=False, lookback=20) and df['VOL_REL'].iloc[-1] > (thresholds['vol'] if strict_level <= 2 else 1.2):
        extras.append('Ruptura soporte con volumen')
    confianza = min(25 * len(extras), 100)
    return (len(extras) > 0), extras, confianza

def signal_none(df):
    if df['ADX'].iloc[-1] < 20:
        return True, ['ADX bajo'], 0
    if df['VOL_REL'].iloc[-1] < 0.8:
        return True, ['Volumen bajo'], 0
    if (df['BB_UPPER'].iloc[-1] - df['BB_LOWER'].iloc[-1]) / df['Close'].iloc[-1] < 0.01 and df['ADX'].iloc[-1] < 22:
        return True, ['Rango lateral'], 0
    return False, [], 0

def get_signal(df, strict_level=3):
    none, reasons_none, conf_none = signal_none(df)
    if none:
        return 'NONE', reasons_none, conf_none
    long_, reasons_long, conf_long = signal_long(df, strict_level)
    if long_:
        return 'LONG', reasons_long, conf_long
    short_, reasons_short, conf_short = signal_short(df, strict_level)
    if short_:
        return 'SHORT', reasons_short, conf_short
    return 'NONE', ['Sin condiciones claras'], 0 