def validate_multitemframe(df_1m, df_5m, df_15m, signal):
    # Si la señal es LONG pero en 15m la estructura es bajista, anular
    if signal == 'LONG':
        if df_15m['EMA20'].iloc[-1] < df_15m['EMA50'].iloc[-1] < df_15m['EMA200'].iloc[-1]:
            return False, 'Estructura bajista en 15m'
    # Si la señal es SHORT pero en 15m la estructura es alcista, anular
    if signal == 'SHORT':
        if df_15m['EMA20'].iloc[-1] > df_15m['EMA50'].iloc[-1] > df_15m['EMA200'].iloc[-1]:
            return False, 'Estructura alcista en 15m'
    return True, ''

def validate_multitemframe_1h(df_1m, df_5m, df_15m, df_1h, signal):
    # Validación clásica en 15m
    valid, motivo = validate_multitemframe(df_1m, df_5m, df_15m, signal)
    if not valid:
        return False, motivo
    # Nueva validación en 1h
    if df_1h is not None:
        if signal == 'LONG' and df_1h['EMA20'].iloc[-1] < df_1h['EMA50'].iloc[-1] < df_1h['EMA200'].iloc[-1]:
            return False, 'Estructura bajista en 1h'
        if signal == 'SHORT' and df_1h['EMA20'].iloc[-1] > df_1h['EMA50'].iloc[-1] > df_1h['EMA200'].iloc[-1]:
            return False, 'Estructura alcista en 1h'
    return True, '' 