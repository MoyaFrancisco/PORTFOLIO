import pandas as pd
from signals import get_signal
from formatting import print_analysis, build_explanation
from datetime import datetime

# Helper para crear un DataFrame simulado con los campos necesarios
def make_df(signal_type, extras_count=0):
    # Valores base para cumplir obligatorias LONG
    data = {
        'Close': [100, 102],
        'Open': [99, 101],
        'High': [103, 106],  # Para ruptura resistencia
        'Low': [98, 100],
        'EMA20': [103, 103], # Para patrón alcista sobre EMA
        'EMA50': [100, 102],
        'EMA200': [99, 101],
        'ADX': [30, 32],
        'VOL_REL': [2.0, 2.1], # Para ruptura y volumen alto
        'MACD': [0.5, 1.0],
        'MACDs': [0.4, 0.8],
        'MACDh': [0.1, 0.2],
        'RSI14': [60, 65],
        'BB_UPPER': [110, 112],
        'BB_LOWER': [90, 92],
        'BB_MID': [100, 102],
        'STOCHK': [80, 85],
        'STOCHD': [70, 75],
        'CCI': [100, 120],
        '+DI': [25, 27],
        '-DI': [10, 12],
        'ATR': [2, 2],
        'DONCHIAN_UPPER': [105, 106],
        'DONCHIAN_LOWER': [95, 96],
        'KELT_UPPER': [108, 109],
        'KELT_LOWER': [92, 93],
        'VOL_MA20': [1000, 1000],
        'OBV': [10000, 10100],
    }
    df = pd.DataFrame(data)
    # Ajustar para SHORT
    if signal_type == 'SHORT':
        df['EMA20'] = [97, 95]
        df['EMA50'] = [98, 96]
        df['EMA200'] = [99, 97]
        df['ADX'] = [30, 32]
        df['VOL_REL'] = [2.0, 2.1]
        df['MACD'] = [1.0, 0.5]
        df['MACDs'] = [0.8, 0.4]
        df['MACDh'] = [0.2, 0.1]
        df['RSI14'] = [40, 35]
        df['Close'] = [93, 92]  # Para ruptura soporte
        df['Open'] = [101, 98]  # Para patrón bajista
        df['Low'] = [98, 94]    # Para ruptura soporte
        df['EMA20'] = [97, 97]  # Para patrón bajista bajo EMA
    # Ajustar para NONE
    if signal_type == 'NONE':
        df['ADX'] = [10, 12]
        df['VOL_REL'] = [0.5, 0.6]
    # Desactivar extras según extras_count
    if signal_type == 'LONG':
        if extras_count < 4:
            df['High'] = [103, 104]  # No ruptura resistencia
        if extras_count < 3:
            df['Close'] = [100, 102]; df['Open'] = [99, 101]; df['EMA20'] = [101, 103]  # No patrón alcista
        if extras_count < 2:
            df['RSI14'] = [60, 59]  # No RSI subiendo
        if extras_count < 1:
            df['MACD'] = [0.5, 0.4]; df['MACDs'] = [0.4, 0.8]; df['MACDh'] = [0.1, 0.05]  # No MACD cruce
    if signal_type == 'SHORT':
        if extras_count < 4:
            df['Low'] = [98, 96]; df['Close'] = [100, 97]  # No ruptura soporte
        if extras_count < 3:
            df['Close'] = [100, 97]; df['Open'] = [101, 98]; df['EMA20'] = [97, 95]  # No patrón bajista
        if extras_count < 2:
            df['RSI14'] = [40, 41]  # No RSI bajando
        if extras_count < 1:
            df['MACD'] = [1.0, 1.1]; df['MACDs'] = [0.8, 0.9]; df['MACDh'] = [0.2, 0.3]  # No MACD cruce a la baja
    return df

def df_all_long_extras():
    # Simula un escenario que activa los 4 checks de LONG
    data = {
        'Close': [120, 120.6],   # Cierre alto
        'Open': [120.1, 120.2],  # Cuerpo pequeño
        'High': [120.7, 120.8],  # High anterior
        'Low': [119.0, 119.1],   # Mecha inferior larga
        'EMA20': [120.6, 120.6], # Cierre muy cerca de EMA20
        'EMA50': [110, 110],
        'EMA200': [100, 100],
        'ADX': [30, 32],
        'VOL_REL': [2.0, 2.1],
        'MACD': [0.6, 0.9],
        'MACDs': [0.7, 0.8],
        'MACDh': [0.1, 0.2],
        'RSI14': [60, 65],
        'BB_UPPER': [130, 132],
        'BB_LOWER': [90, 92],
        'BB_MID': [110, 112],
        'STOCHK': [80, 85],
        'STOCHD': [70, 75],
        'CCI': [100, 120],
        '+DI': [25, 27],
        '-DI': [10, 12],
        'ATR': [2, 2],
        'DONCHIAN_UPPER': [120.5, 120.8],
        'DONCHIAN_LOWER': [95, 96],
        'KELT_UPPER': [128, 129],
        'KELT_LOWER': [92, 93],
        'VOL_MA20': [1000, 1000],
        'OBV': [10000, 10100],
    }
    return pd.DataFrame(data)

def df_all_short_extras():
    # Simula un escenario que activa los 4 checks de SHORT
    data = {
        'Close': [80, 79.4],    # Cierre bajo
        'Open': [80.3, 80.2],    # Cuerpo pequeño
        'High': [80.5, 80.6],
        'Low': [78.0, 77.8],      # Mecha inferior
        'EMA20': [79.4, 79.4],   # Cierre muy cerca de EMA20
        'EMA50': [90, 90],
        'EMA200': [100, 100],
        'ADX': [30, 32],
        'VOL_REL': [2.0, 2.1],
        'MACD': [0.5, 0.2],
        'MACDs': [0.4, 0.3],
        'MACDh': [0.1, 0.1],
        'RSI14': [40, 35],
        'BB_UPPER': [110, 112],
        'BB_LOWER': [70, 72],
        'BB_MID': [90, 92],
        'STOCHK': [20, 15],
        'STOCHD': [30, 25],
        'CCI': [-100, -120],
        '+DI': [10, 12],
        '-DI': [25, 27],
        'ATR': [2, 2],
        'DONCHIAN_UPPER': [80.5, 80.6],
        'DONCHIAN_LOWER': [77.8, 77.8],
        'KELT_UPPER': [108, 109],
        'KELT_LOWER': [72, 73],
        'VOL_MA20': [1000, 1000],
        'OBV': [10000, 9900],
    }
    return pd.DataFrame(data)

def df_20_long_extras():
    base = 18
    data = {
        'Close': [100]*base,
        'Open': [99]*base,
        'High': [101]*base,
        'Low': [98]*base,
        'EMA20': [100]*base,
        'EMA50': [99]*base,
        'EMA200': [98]*base,
        'ADX': [30]*base,
        'VOL_REL': [1.5]*base,
        'MACD': [0.5]*base,
        'MACDs': [0.6]*base,
        'MACDh': [0.1]*base,
        'RSI14': [60]*base,
        'BB_UPPER': [110]*base,
        'BB_LOWER': [90]*base,
        'BB_MID': [100]*base,
        'STOCHK': [80]*base,
        'STOCHD': [70]*base,
        'CCI': [100]*base,
        '+DI': [25]*base,
        '-DI': [10]*base,
        'ATR': [2]*base,
        'DONCHIAN_UPPER': [101]*base,
        'DONCHIAN_LOWER': [98]*base,
        'KELT_UPPER': [108]*base,
        'KELT_LOWER': [92]*base,
        'VOL_MA20': [1000]*base,
        'OBV': [10000]*base,
    }
    # Penúltima fila: MACD cruce (MACD < MACDs)
    last1 = {
        'Close': 120, 'Open': 119.5, 'High': 120, 'Low': 119, 'EMA20': 120, 'EMA50': 110, 'EMA200': 100,
        'ADX': 35, 'VOL_REL': 2.0, 'MACD': 0.4, 'MACDs': 0.7, 'MACDh': 0.05, 'RSI14': 62, 'BB_UPPER': 130,
        'BB_LOWER': 90, 'BB_MID': 110, 'STOCHK': 85, 'STOCHD': 75, 'CCI': 120, '+DI': 27, '-DI': 12, 'ATR': 2,
        'DONCHIAN_UPPER': 101, 'DONCHIAN_LOWER': 98, 'KELT_UPPER': 129, 'KELT_LOWER': 93, 'VOL_MA20': 1000, 'OBV': 10100
    }
    # Última fila: MACD cruce (MACD > MACDs), RSI subiendo, patrón alcista sobre EMA, ruptura resistencia
    last2 = {
        'Close': 122, 'Open': 121.5, 'High': 122, 'Low': 120, 'EMA20': 122, 'EMA50': 110, 'EMA200': 100,
        'ADX': 35, 'VOL_REL': 2.0, 'MACD': 1.0, 'MACDs': 0.8, 'MACDh': 0.2, 'RSI14': 65, 'BB_UPPER': 130,
        'BB_LOWER': 90, 'BB_MID': 110, 'STOCHK': 85, 'STOCHD': 75, 'CCI': 120, '+DI': 27, '-DI': 12, 'ATR': 2,
        'DONCHIAN_UPPER': 101, 'DONCHIAN_LOWER': 98, 'KELT_UPPER': 129, 'KELT_LOWER': 93, 'VOL_MA20': 1000, 'OBV': 10100
    }
    for k in data:
        data[k].append(last1[k])
        data[k].append(last2[k])
    return pd.DataFrame(data)

def df_20_short_extras():
    base = 18
    data = {
        'Close': [100]*base,
        'Open': [101]*base,
        'High': [102]*base,
        'Low': [99]*base,
        'EMA20': [98]*base,
        'EMA50': [99]*base,
        'EMA200': [100]*base,
        'ADX': [30]*base,
        'VOL_REL': [1.5]*base,
        'MACD': [1.0]*base,
        'MACDs': [0.8]*base,
        'MACDh': [0.2]*base,
        'RSI14': [40]*base,
        'BB_UPPER': [110]*base,
        'BB_LOWER': [90]*base,
        'BB_MID': [100]*base,
        'STOCHK': [20]*base,
        'STOCHD': [30]*base,
        'CCI': [-100]*base,
        '+DI': [10]*base,
        '-DI': [25]*base,
        'ATR': [2]*base,
        'DONCHIAN_UPPER': [102]*base,
        'DONCHIAN_LOWER': [99]*base,
        'KELT_UPPER': [108]*base,
        'KELT_LOWER': [92]*base,
        'VOL_MA20': [1000]*base,
        'OBV': [10000]*base,
    }
    # Penúltima fila: MACD cruce (MACD > MACDs)
    last1 = {
        'Close': 98, 'Open': 98.5, 'High': 98, 'Low': 97, 'EMA20': 98, 'EMA50': 99, 'EMA200': 100,
        'ADX': 35, 'VOL_REL': 2.0, 'MACD': 0.9, 'MACDs': 0.7, 'MACDh': 0.15, 'RSI14': 38, 'BB_UPPER': 110,
        'BB_LOWER': 90, 'BB_MID': 100, 'STOCHK': 15, 'STOCHD': 25, 'CCI': -120, '+DI': 12, '-DI': 27, 'ATR': 2,
        'DONCHIAN_UPPER': 98, 'DONCHIAN_LOWER': 96, 'KELT_UPPER': 109, 'KELT_LOWER': 93, 'VOL_MA20': 1000, 'OBV': 9900
    }
    # Última fila: MACD cruce (MACD < MACDs), RSI bajando, patrón bajista bajo EMA, ruptura soporte
    last2 = {
        'Close': 96, 'Open': 97, 'High': 97, 'Low': 95, 'EMA20': 96, 'EMA50': 98, 'EMA200': 99,
        'ADX': 35, 'VOL_REL': 2.0, 'MACD': 0.2, 'MACDs': 0.3, 'MACDh': 0.1, 'RSI14': 35, 'BB_UPPER': 110,
        'BB_LOWER': 90, 'BB_MID': 100, 'STOCHK': 15, 'STOCHD': 25, 'CCI': -120, '+DI': 12, '-DI': 27, 'ATR': 2,
        'DONCHIAN_UPPER': 97, 'DONCHIAN_LOWER': 95, 'KELT_UPPER': 109, 'KELT_LOWER': 93, 'VOL_MA20': 1000, 'OBV': 9900
    }
    for k in data:
        data[k].append(last1[k])
        data[k].append(last2[k])
    return pd.DataFrame(data)

# Test de señales
def test_scenarios():
    now = pd.Timestamp.now()
    price = 122
    print("\n--- Señal LONG con 4 extras (confianza 100%) ---")
    df = df_20_long_extras()
    signal, checks, confianza = get_signal(df)
    explicacion = build_explanation(signal, checks)
    print_analysis('TEST/LONG', now, 'Alcista fuerte', signal, checks, '+2.0%', '-1.0%', '2.0', explicacion, price, confianza)

    price = 96
    print("\n--- Señal SHORT con 4 extras (confianza 100%) ---")
    df = df_20_short_extras()
    signal, checks, confianza = get_signal(df)
    explicacion = build_explanation(signal, checks)
    print_analysis('TEST/SHORT', now, 'Bajista fuerte', signal, checks, '+2.0%', '-1.0%', '2.0', explicacion, price, confianza)

if __name__ == "__main__":
    test_scenarios() 