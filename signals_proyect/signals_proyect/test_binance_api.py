import ccxt
import time
import pandas as pd

exchange = ccxt.binance()
SYMBOL = 'BTC/USDT'
TIMEFRAME = '1m'
LIMIT = 5

print(f"Probando descarga de {SYMBOL} {TIMEFRAME}...")
start = time.time()
bars = exchange.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, limit=LIMIT)
elapsed = time.time() - start

df = pd.DataFrame(bars, columns=['Time','Open','High','Low','Close','Volume'])
df['Time'] = pd.to_datetime(df['Time'], unit='ms')
print(df)
print(f"Tiempo de respuesta: {elapsed:.2f} segundos") 