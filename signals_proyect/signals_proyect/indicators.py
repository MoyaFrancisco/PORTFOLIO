import pandas as pd
import pandas_ta as ta

def add_all_indicators(df):
    # Medias móviles
    for period in [9, 20, 50, 100, 200]:
        df[f'SMA{period}'] = df['Close'].rolling(window=period).mean()
        df[f'EMA{period}'] = df['Close'].ewm(span=period, adjust=False).mean()
        df[f'WMA{period}'] = ta.wma(df['Close'], length=period)
        df[f'VWMA{period}'] = ta.vwma(df['Close'], df['Volume'], length=period)
        df[f'HMA{period}'] = ta.hma(df['Close'], length=period)
        df[f'DEMA{period}'] = ta.dema(df['Close'], length=period)
        df[f'TEMA{period}'] = ta.tema(df['Close'], length=period)
    # RSI
    df['RSI14'] = ta.rsi(df['Close'], length=14)
    # MACD
    macd = ta.macd(df['Close'], fast=12, slow=26, signal=9)
    df['MACD'] = macd['MACD_12_26_9']
    df['MACDh'] = macd['MACDh_12_26_9']
    df['MACDs'] = macd['MACDs_12_26_9']
    # Estocástico
    stoch = ta.stoch(df['High'], df['Low'], df['Close'], k=14, d=3)
    df['STOCHK'] = stoch['STOCHk_14_3_3']
    df['STOCHD'] = stoch['STOCHd_14_3_3']
    # CCI
    df['CCI'] = ta.cci(df['High'], df['Low'], df['Close'], length=20)
    # ADX
    adx = ta.adx(df['High'], df['Low'], df['Close'], length=14)
    df['ADX'] = adx['ADX_14']
    df['+DI'] = adx['DMP_14']
    df['-DI'] = adx['DMN_14']
    # ATR
    df['ATR'] = ta.atr(df['High'], df['Low'], df['Close'], length=14)
    # Bollinger Bands
    bbands = ta.bbands(df['Close'], length=20, std=2)
    df['BB_UPPER'] = bbands['BBU_20_2.0']
    df['BB_LOWER'] = bbands['BBL_20_2.0']
    df['BB_MID'] = bbands['BBM_20_2.0']
    # Donchian Channel (corregido)
    donchian = ta.donchian(df['High'], df['Low'], lower_length=20, upper_length=20)
    df['DONCHIAN_UPPER'] = donchian['DCU_20_20']
    df['DONCHIAN_LOWER'] = donchian['DCL_20_20']
    # Keltner Channel (corregido)
    kelt = ta.kc(df['High'], df['Low'], df['Close'], length=20)
    df['KELT_UPPER'] = kelt['KCUe_20_2']
    df['KELT_LOWER'] = kelt['KCLe_20_2']
    # Volumen Relativo
    df['VOL_MA20'] = df['Volume'].rolling(window=20).mean()
    df['VOL_REL'] = df['Volume'] / df['VOL_MA20']
    # OBV
    df['OBV'] = ta.obv(df['Close'], df['Volume'])
    return df 