# Sistema de Análisis Técnico por Terminal

Herramienta de análisis técnico en tiempo real para criptomonedas, que muestra señales de trading, niveles de take profit/stop loss y explicación de la señal en la terminal.

## Instalación

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

## Configuración

Edita `config.yaml` para definir los símbolos, timeframes y parámetros principales.

## Estructura del Proyecto

- `main.py`: Loop principal y orquestación.
- `config.yaml`: Configuración de símbolos, timeframes, parámetros.
- `indicators.py`: Cálculo de indicadores técnicos.
- `signals.py`: Lógica de generación de señales.
- `multitimeframe.py`: Validación multitemporal.
- `formatting.py`: Presentación en terminal.
- `utils.py`: Funciones auxiliares y logging.

## Ejemplo de Salida

```
[BTC/USDT] ⏱️ 12:31
▶ Tendencia: Alcista fuerte
▶ Entrada potencial: LONG
▶ Señales:
  ✓ EMA20 > EMA50 > EMA200
  ✓ ADX: 34
  ✓ MACD: cruce al alza
  ✓ RSI: 63, subiendo
📍 TP: +2.1% | SL: -1.1% | R/R: 1.91
🧠 Explicación: BTC rompe resistencia con volumen y patrón alcista sobre EMA20.
``` 