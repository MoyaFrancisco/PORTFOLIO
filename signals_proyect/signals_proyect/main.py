import time
import yaml
from tabulate import tabulate
from colorama import Fore, Style
import ccxt
import pandas as pd
import pandas_ta as ta
from indicators import add_all_indicators
from signals import get_signal, get_thresholds_for_level
from formatting import print_analysis, build_explanation
from utils import percent
import asyncio
from telegram import Bot

# Variables globales para bot y loop
telegram_bot = None
telegram_loop = None


def print_intro():
    print(Fore.CYAN + '\n' + '='*65 + Style.RESET_ALL)
    print(Fore.YELLOW + 'BIENVENIDO AL SISTEMA DE ANÁLISIS DE SEÑALES MULTITIMEFRAME' + Style.RESET_ALL)
    print(Fore.CYAN + '='*65 + Style.RESET_ALL)
    print('Este programa analiza múltiples criptomonedas en varios marcos temporales (timeframes) usando indicadores técnicos avanzados.')
    print('\nPuedes personalizar dos aspectos clave:')
    print(Fore.GREEN + '1. Nivel de exigencia (1-5):' + Style.RESET_ALL)
    print('   - Un nivel bajo (1) es más flexible: genera más señales, pero pueden ser menos fiables.')
    print('   - Un nivel alto (5) es muy estricto: solo muestra señales de alta calidad, pero serán menos frecuentes.')
    print('   - El nivel de exigencia ajusta los umbrales de los indicadores (ADX, volumen, cercanía a medias, etc.).')
    print(Fore.GREEN + '2. Selección de timeframes:' + Style.RESET_ALL)
    print('   - Timeframes cortos (ej: 1m, 5m) detectan movimientos rápidos, pero pueden dar señales menos robustas.')
    print('   - Timeframes largos (ej: 1h, 4h) detectan tendencias más sólidas, pero las señales son menos frecuentes y más lentas.')
    print('   - Usar muchos timeframes permite validar la señal en diferentes horizontes, pero puede aumentar la penalización si no están alineados.')
    print('   - Usar pocos timeframes hace el análisis más simple, pero menos robusto.')
    print('\nRECOMENDACIÓN:')
    print('- Si buscas oportunidades rápidas, usa niveles bajos y timeframes cortos.')
    print('- Si prefieres calidad y menos ruido, usa niveles altos y timeframes largos.')
    print('- Para un análisis equilibrado, elige 2-3 timeframes (ej: 5m, 15m, 1h) y nivel 3.')
    print('\nDurante la ejecución, verás para cada símbolo:')
    print('- Tendencia principal, checks cumplidos, explicación detallada, confianza, TP/SL y penalizaciones.')
    print('\n¡Comencemos!\n')
    print(Fore.CYAN + '='*65 + Style.RESET_ALL)

async def send_telegram_notification(msg):
    global telegram_bot
    if not config.get('telegram_token') or not config.get('telegram_chat_id'):
        return
    try:
        await telegram_bot.send_message(chat_id=config['telegram_chat_id'], text=msg, parse_mode='HTML')
    except Exception as e:
        print(f"[Telegram] Error al enviar notificación: {e}")

def ask_timeframes():
    tfs = input('¿Qué temporalidades quieres analizar? (ejemplo: 1m,5m,15m,1h,4h): ').strip()
    tfs_list = [tf.strip() for tf in tfs.split(',') if tf.strip()]
    return tfs_list

def ask_strict_level():
    while True:
        try:
            level = int(input('¿Qué nivel de exigencia deseas? (1 = muy flexible, 5 = muy estricto): ').strip())
            if 1 <= level <= 5:
                return level
            else:
                print('Por favor, introduce un número entre 1 y 5.')
        except Exception:
            print('Por favor, introduce un número válido.')

# Cargar configuración (símbolos, timeframes, etc.)
try:
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    config = {
        'symbols': ['BTC/USDT', 'ETH/USDT', 'BNB/USDT'],
        'timeframes': ['1m', '5m', '15m', '1h'],
        'interval_seconds': 60,
        'risk_reward': 2.0,
        'strict_mode': True,
        'strict_level': 3,
        'telegram_token': '',
        'telegram_chat_id': ''
    }

# Inicializar bot y loop de Telegram si hay token y chat_id
if config.get('telegram_token') and config.get('telegram_chat_id'):
    telegram_bot = Bot(token=config['telegram_token'])
    telegram_loop = asyncio.get_event_loop()

# Mostrar explicación introductoria
print_intro()

# Test de Telegram opcional
if telegram_bot and telegram_loop:
    test_telegram = input('¿Quieres enviar un mensaje de prueba a tu Telegram? (s/n): ').strip().lower()
    if test_telegram == 's':
        telegram_loop.run_until_complete(send_telegram_notification('✅ ¡Conexión exitosa! Tu bot de señales está listo para notificarte.'))
        print(Fore.GREEN + 'Mensaje de prueba enviado a tu Telegram.' + Style.RESET_ALL)

# Preguntar al usuario el modo de operación y timeframes
strict_level = ask_strict_level()
config['strict_level'] = strict_level
thresholds = get_thresholds_for_level(strict_level)
print(Fore.CYAN + f"[Nivel de exigencia seleccionado: {strict_level}]" + Style.RESET_ALL)
print(Fore.YELLOW + f"Umbrales usados: ADX>{thresholds['adx']}, VolRel>{thresholds['vol']}, Penalización tf en contra: {thresholds['penalizacion']}%" + Style.RESET_ALL)

# Preguntar nivel mínimo de confianza para notificar
while True:
    try:
        min_conf = int(input('¿Nivel mínimo de confianza para recibir señales en Telegram? (0-100): ').strip())
        if 0 <= min_conf <= 100:
            break
        else:
            print('Introduce un número entre 0 y 100.')
    except Exception:
        print('Introduce un número válido.')

# Diccionario para guardar la última señal enviada por símbolo
last_notified = {}

user_tfs = ask_timeframes()
if user_tfs:
    config['timeframes'] = user_tfs
    print(Fore.GREEN + f"[Temporalidades seleccionadas: {', '.join(user_tfs)}]" + Style.RESET_ALL)
else:
    print(Fore.RED + '[No se seleccionaron temporalidades, usando las de config.yaml]' + Style.RESET_ALL)

exchange = ccxt.binance()

BARS = 100

def fetch_ohlcv(symbol, timeframe):
    print(f"[DEBUG] Descargando {symbol} {timeframe}...")
    bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=BARS)
    print(f"[DEBUG] Descargado {symbol} {timeframe} OK")
    df = pd.DataFrame(bars, columns=['Time','Open','High','Low','Close','Volume'])
    df['Time'] = pd.to_datetime(df['Time'], unit='ms')
    return df

def tendencia_text(df):
    if df['EMA20'].iloc[-1] > df['EMA50'].iloc[-1] > df['EMA200'].iloc[-1]:
        return 'Alcista fuerte'
    if df['EMA20'].iloc[-1] < df['EMA50'].iloc[-1] < df['EMA200'].iloc[-1]:
        return 'Bajista fuerte'
    return 'Lateral o indefinida'

def calc_tp_sl(price, atr, side, rr):
    if side == 'LONG':
        sl = price - 1.5 * atr
        tp = price + rr * (price - sl)
    elif side == 'SHORT':
        sl = price + 1.5 * atr
        tp = price - rr * (sl - price)
    else:
        sl = tp = None
    return tp, sl

def validate_multitemframe_progressive(dfs, signal, penalizacion_pct):
    tfs = list(dfs.keys())
    main_tf = tfs[0]
    higher_tfs = tfs[1:]
    valid_tfs = []
    invalid_tfs = []
    for tf in higher_tfs:
        df = dfs[tf]
        if signal == 'LONG' and df['EMA20'].iloc[-1] < df['EMA50'].iloc[-1] < df['EMA200'].iloc[-1]:
            invalid_tfs.append(tf)
        elif signal == 'SHORT' and df['EMA20'].iloc[-1] > df['EMA50'].iloc[-1] > df['EMA200'].iloc[-1]:
            invalid_tfs.append(tf)
        else:
            valid_tfs.append(tf)
    penalizacion = penalizacion_pct * len(invalid_tfs)
    return valid_tfs, invalid_tfs, penalizacion

def main():
    while True:
        now = pd.Timestamp.now()
        for symbol in config['symbols']:
            try:
                print(f"[DEBUG] Analizando {symbol}")
                # Descargar datos multitemporales
                dfs = {}
                for tf in config['timeframes']:
                    df = fetch_ohlcv(symbol, tf)
                    df = add_all_indicators(df)
                    dfs[tf] = df
                # Ordenar timeframes de menor a mayor
                tfs_sorted = sorted(dfs.keys(), key=lambda x: (int(x[:-1]) if x[:-1].isdigit() else 1000, x[-1]))
                dfs_sorted = {tf: dfs[tf] for tf in tfs_sorted}
                main_tf = tfs_sorted[0]
                main_df = dfs_sorted[main_tf]
                # Señal principal en el timeframe más bajo
                signal, checks, confianza = get_signal(main_df, strict_level=config['strict_level'])
                # Validación multitemporal progresiva
                valid_tfs, invalid_tfs, penalizacion = validate_multitemframe_progressive(dfs_sorted, signal, thresholds['penalizacion'])
                confianza = max(0, confianza - penalizacion)
                # Mensaje de validación
                valid_msg = f"Validan: {', '.join(valid_tfs) if valid_tfs else 'ninguna'}"
                invalid_msg = f"En contra: {', '.join(invalid_tfs) if invalid_tfs else 'ninguna'}"
                # TP/SL
                price = main_df['Close'].iloc[-1]
                atr = main_df['ATR'].iloc[-1]
                tp, sl = calc_tp_sl(price, atr, signal, config.get('risk_reward', 2.0))
                tp_pct = percent(tp, price) if tp else '-'
                sl_pct = percent(sl, price) if sl else '-'
                rr = abs((tp - price) / (price - sl)) if tp and sl and (price - sl) != 0 else '-'
                # Tendencias
                tendencias = {tf: tendencia_text(dfs_sorted[tf]) for tf in tfs_sorted}
                # Explicación detallada
                explicacion = build_explanation(signal, checks, strict_level=config['strict_level'], thresholds=thresholds)
                # Mostrar tendencias
                for tf in tfs_sorted:
                    print(f"{Fore.MAGENTA}Tendencia {tf}:{Style.RESET_ALL} {tendencias[tf]}")
                print(Fore.GREEN + valid_msg + Style.RESET_ALL)
                print(Fore.RED + invalid_msg + Style.RESET_ALL)
                print_analysis(symbol, now, tendencias[main_tf], signal, checks, tp_pct, sl_pct, rr, explicacion, price, confianza)
                # Notificación por Telegram si hay señal LONG o SHORT y supera el umbral de confianza
                if telegram_bot and telegram_loop and signal in ("LONG", "SHORT"):
                    try:
                        conf_int = int(confianza)
                    except Exception:
                        conf_int = 0
                    print(f"[DEBUG] {symbol} señal={signal} confianza={conf_int} min_conf={min_conf}")
                    if conf_int >= min_conf:
                        last = last_notified.get(symbol)
                        current = (signal, main_tf, conf_int)
                        if last != current:
                            checks_str = '\n'.join(f'✅ {c}' for c in checks)
                            color_emoji = '🟩' if signal == 'LONG' else '🟥'
                            notif_msg = (
                                f"{color_emoji} <b>SEÑAL {signal}</b>\n"
                                "———————————————\n"
                                f"<b>Par:</b> {symbol}\n"
                                f"<b>Timeframe:</b> {main_tf}\n"
                                f"<b>Precio:</b> {price:.4f}\n"
                                f"<b>Confianza:</b> {conf_int}%\n"
                                "———————————————\n"
                                f"<b>Checks:</b>\n{checks_str}\n"
                                "———————————————\n"
                                f"<b>TP:</b> {tp_pct}   <b>SL:</b> {sl_pct}   <b>R/R:</b> {rr}\n"
                                "———————————————\n"
                                f"�� <b>Explicación:</b>\n"
                                f"{explicacion.split('[')[0].strip()}\n"
                                f"[Nivel de exigencia: {config['strict_level']}]\n"
                                "———————————————"
                            )
                            telegram_loop.run_until_complete(send_telegram_notification(notif_msg))
                            last_notified[symbol] = current
            except Exception as e:
                print(f"[{symbol}] Error: {e}")
        time.sleep(config['interval_seconds'])

if __name__ == "__main__":
    main() 