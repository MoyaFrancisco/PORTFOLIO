from colorama import Fore, Style

EXPLANATIONS = {
    "EMA20 > EMA50 > EMA200": "la media móvil exponencial de 20 periodos está por encima de la de 50 y esta, a su vez, por encima de la de 200, lo que indica una tendencia alcista sólida.",
    "EMA20 < EMA50 < EMA200": "la media móvil exponencial de 20 periodos está por debajo de la de 50 y esta, a su vez, por debajo de la de 200, lo que indica una tendencia bajista clara.",
    "ADX alto": "el ADX es superior al umbral configurado, lo que confirma la presencia de una tendencia fuerte en el mercado.",
    "ADX bajo": "el ADX está por debajo del umbral configurado, lo que indica ausencia de tendencia clara en el mercado.",
    "MACD cruce al alza": "el MACD ha cruzado al alza con un histograma creciente, señalizando un impulso alcista renovado.",
    "MACD cruce a la baja": "el MACD ha cruzado a la baja con un histograma decreciente, lo que sugiere un impulso bajista.",
    "RSI subiendo": "el RSI está en ascenso y supera el umbral configurado, lo que refuerza el momentum comprador.",
    "RSI bajando": "el RSI está descendiendo y cae por debajo del umbral configurado, lo que refuerza el momentum vendedor.",
    "Patrón alcista sobre EMA": "se ha detectado un patrón de vela alcista (envolvente o martillo) sobre una media móvil relevante, lo que sugiere un posible rebote alcista.",
    "Patrón bajista bajo EMA": "se ha detectado un patrón de vela bajista (envolvente) bajo una media móvil relevante, lo que sugiere un posible rechazo bajista.",
    "Ruptura resistencia con volumen": "el precio ha superado una resistencia importante acompañado de un volumen significativamente alto, lo que refuerza la validez del movimiento alcista.",
    "Ruptura soporte con volumen": "el precio ha perforado un soporte clave acompañado de un volumen significativamente alto, lo que refuerza la validez del movimiento bajista.",
    "Volumen bajo": "el volumen actual es inferior al 80% de la media, lo que sugiere falta de interés o liquidez en el mercado.",
    "Rango lateral": "las Bandas de Bollinger están muy estrechas y el ADX es plano, lo que indica un mercado en consolidación o rango sin dirección clara.",
    "Sin condiciones claras": "no se cumplen condiciones relevantes para operar en este momento.",
    "Estructura bajista en 15m": "en el marco temporal de 15 minutos, la estructura es bajista, por lo que se desaconseja abrir posiciones largas.",
    "Estructura alcista en 15m": "en el marco temporal de 15 minutos, la estructura es alcista, por lo que se desaconseja abrir posiciones cortas."
}

def color_signal(signal):
    if signal == 'LONG':
        return Fore.GREEN + 'LONG' + Style.RESET_ALL
    elif signal == 'SHORT':
        return Fore.RED + 'SHORT' + Style.RESET_ALL
    else:
        return Fore.YELLOW + 'NONE' + Style.RESET_ALL

def build_explanation(signal, checks, strict_level=None, thresholds=None):
    if not checks:
        return "No se cumplen condiciones relevantes para operar."
    # Personalizar checks con umbrales si corresponde
    def personalize(check):
        if thresholds:
            if check == 'ADX alto':
                return f"ADX>{thresholds['adx']} (tendencia fuerte)"
            if check == 'RSI subiendo':
                rsi_thr = 45 if strict_level == 1 else 48 if strict_level == 2 else 50
                return f"RSI>{rsi_thr} y subiendo"
            if check == 'RSI bajando':
                rsi_thr = 55 if strict_level == 1 else 52 if strict_level == 2 else 50
                return f"RSI<{rsi_thr} y bajando"
            if check == 'Volumen bajo':
                return f"VolRel<{thresholds['vol']} (bajo volumen)"
            if check == 'Ruptura resistencia con volumen' or check == 'Ruptura soporte con volumen':
                return f"{check} (VolRel>{thresholds['vol']})"
        return check
    joined = " Además, ".join([EXPLANATIONS.get(c, c) if not thresholds else EXPLANATIONS.get(c, c).replace('umbral configurado', str(thresholds['adx']) if 'ADX' in c else str(thresholds['vol']) if 'volumen' in c.lower() else str(thresholds['ema_cercania'])) for c in checks])
    checks_str = ", ".join([personalize(c) for c in checks])
    base = ""
    if signal == "LONG":
        base = f"Se detecta una oportunidad de compra porque {checks_str}."
    elif signal == "SHORT":
        base = f"Se detecta una oportunidad de venta porque {checks_str}."
    else:
        base = f"No se recomienda operar porque {checks_str}."
    if strict_level and thresholds:
        base += f"\n[Nivel de exigencia: {strict_level} | Umbrales: ADX>{thresholds['adx']}, VolRel>{thresholds['vol']}, Penalización tf en contra: {thresholds['penalizacion']}%]"
    return base

def confidence_bar(conf):
    # conf: 0-100
    filled = int(conf // 20)
    empty = 5 - filled
    bar = f"{'█'*filled}{'░'*empty}"
    color = Fore.GREEN if conf >= 75 else (Fore.YELLOW if conf >= 50 else Fore.RED)
    return color + bar + Style.RESET_ALL + f" {conf}%"

def print_analysis(symbol, now, tendencia, signal, checks, tp, sl, rr, explicacion, price, confianza):
    print(Fore.CYAN + f"\n{'═'*60}" + Style.RESET_ALL)
    print(f"{Fore.MAGENTA}■ {symbol} {Style.RESET_ALL}| ⏱️ {now.strftime('%H:%M')} | 💰 Precio actual: {Fore.YELLOW}{price:.4f}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Tendencia:{Style.RESET_ALL} {tendencia}")
    print(f"{Fore.BLUE}Señal:{Style.RESET_ALL} {color_signal(signal)}   Confianza: {confidence_bar(confianza)}")
    print(f"{Fore.BLUE}Checks cumplidos:{Style.RESET_ALL}")
    for c in checks:
        print(f"  ✓ {c}")
    print(f"{Fore.BLUE}TP:{Style.RESET_ALL} {tp}   {Fore.BLUE}SL:{Style.RESET_ALL} {sl}   {Fore.BLUE}R/R:{Style.RESET_ALL} {rr}")
    print(f"{Fore.BLUE}Explicación:{Style.RESET_ALL}\n{explicacion}")
    print(Fore.CYAN + f"{'═'*60}" + Style.RESET_ALL) 