let currentInterval = '1m';
let charts = [];
let latestPrice = 0;
let activeTrade = null;
let tradeHistory = [];

function setIntervalChart(interval, btn) {
  currentInterval = interval;
  document.querySelectorAll('.btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  fetchAndRender();
}

function calcSMA(data, period) {
  const result = [];
  for (let i = 0; i < data.length; i++) {
    if (i < period) {
      result.push(null);
    } else {
      const slice = data.slice(i - period, i);
      const avg = slice.reduce((a, b) => a + b, 0) / period;
      result.push(avg);
    }
  }
  return result;
}

function calcEMA(data, period) {
  const k = 2 / (period + 1);
  const ema = [data[0]];
  for (let i = 1; i < data.length; i++) {
    ema.push(data[i] * k + ema[i - 1] * (1 - k));
  }
  while (ema.length < data.length) {
    ema.unshift(null);
  }
  return ema;
}

function calcRSI(data, period = 14) {
  let gains = 0, losses = 0;
  const rsi = [];

  for (let i = 1; i <= period; i++) {
    const diff = data[i] - data[i - 1];
    if (diff >= 0) gains += diff;
    else losses -= diff;
  }

  gains /= period;
  losses /= period;
  rsi[period] = 100 - 100 / (1 + gains / losses);

  for (let i = period + 1; i < data.length; i++) {
    const diff = data[i] - data[i - 1];
    if (diff >= 0) {
      gains = (gains * (period - 1) + diff) / period;
      losses = (losses * (period - 1)) / period;
    } else {
      gains = (gains * (period - 1)) / period;
      losses = (losses * (period - 1) - diff) / period;
    }
    rsi[i] = 100 - 100 / (1 + gains / losses);
  }

  return rsi.map((val, i) => (i < period ? null : val));
}

function calcMACD(data, shortPeriod = 12, longPeriod = 26, signalPeriod = 9) {
  const emaShort = calcEMA(data, shortPeriod);
  const emaLong = calcEMA(data, longPeriod);
  const macd = emaShort.map((val, i) =>
    val !== null && emaLong[i] !== null ? val - emaLong[i] : null
  );

  const validMACD = macd.filter(v => v !== null);
  const signal = calcEMA(validMACD, signalPeriod);
  const fullSignal = Array(macd.length - signal.length).fill(null).concat(signal);

  const histogram = macd.map((val, i) =>
    val !== null && fullSignal[i] !== null ? val - fullSignal[i] : null
  );

  return { macd, signal: fullSignal, histogram };
}

async function fetchAndRender() {
  const tfHigher = getHigherTimeframe(currentInterval);
  document.getElementById("higherFrame").textContent = `Validando señales con marco mayor: ${tfHigher}`;

  const url = `https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=${currentInterval}&limit=300`;
  const urlHigher = `https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=${tfHigher}&limit=300`;

  const [res, resHigher] = await Promise.all([fetch(url), fetch(urlHigher)]);
  const data = await res.json();
  const dataHigher = await resHigher.json();

  const labels = data.map(d => new Date(d[0]).toLocaleTimeString());
  const close = data.map(d => parseFloat(d[4]));
  const volume = data.map(d => parseFloat(d[5]));

  const sma = calcSMA(close, 10);
  const ema = calcEMA(close, 10);
  const rsi = calcRSI(close);
  const { macd, signal, histogram } = calcMACD(close);

  const lastHigherClose = parseFloat(dataHigher.at(-1)[4]);

  // Borrar gráficos anteriores
  charts.forEach(c => c.destroy());
  charts = [];

  // Anotaciones si hay operación activa
  let annotations = {};

  if (activeTrade) {
    const p = activeTrade.precioEntrada;
    const tipo = activeTrade.tipo;

    annotations.entry = {
      type: 'line',
      yMin: p,
      yMax: p,
      borderColor: tipo === 'LONG' ? '#00ff99' : '#ff4d4d',
      borderWidth: 2,
      label: {
        content: `Entrada ${tipo}`,
        enabled: true,
        position: 'start',
        backgroundColor: 'rgba(0,0,0,0.6)',
        color: '#fff'
      }
    };

    const tp = tipo === 'LONG' ? p * 1.03 : p * 0.97;
    const sl = tipo === 'LONG' ? p * 0.985 : p * 1.015;

    annotations.tp = {
      type: 'line',
      yMin: tp,
      yMax: tp,
      borderColor: '#00ffaa',
      borderWidth: 1.5,
      borderDash: [5, 5],
      label: {
        content: '🎯 TP',
        enabled: true,
        position: 'start',
        backgroundColor: 'rgba(0,255,170,0.3)',
        color: '#000'
      }
    };

    annotations.sl = {
      type: 'line',
      yMin: sl,
      yMax: sl,
      borderColor: '#ff6666',
      borderWidth: 1.5,
      borderDash: [5, 5],
      label: {
        content: '🛑 SL',
        enabled: true,
        position: 'start',
        backgroundColor: 'rgba(255,102,102,0.3)',
        color: '#000'
      }
    };
  }

  // Actualización del último precio
  latestPrice = close[close.length - 1];

    // Gráfico de Precio + SMA + EMA
  const priceChart = new Chart(document.getElementById("priceChart"), {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Precio',
          data: close,
          borderColor: '#00ffc8',
          pointRadius: 0,
          borderWidth: 2
        },
        {
          label: 'SMA(10)',
          data: sma,
          borderColor: '#8888ff',
          borderDash: [5, 5],
          pointRadius: 0
        },
        {
          label: 'EMA(10)',
          data: ema,
          borderColor: '#ffaa00',
          pointRadius: 0
        }
      ]
    },
    options: {
      ...getOptions(),
      plugins: {
        ...getOptions().plugins,
        annotation: { annotations }
      }
    }
  });
  charts.push(priceChart);

  // RSI
  charts.push(new Chart(document.getElementById("rsiChart"), {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'RSI',
        data: rsi,
        borderColor: '#66ccff',
        pointRadius: 0
      }]
    },
    options: getOptions(100)
  }));

  // Volumen
  charts.push(new Chart(document.getElementById("volumeChart"), {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Volumen',
        data: volume,
        backgroundColor: '#888'
      }]
    },
    options: getOptions()
  }));

  // MACD
  charts.push(new Chart(document.getElementById("macdChart"), {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'MACD',
          data: macd,
          type: 'line',
          borderColor: '#00ccff',
          pointRadius: 0
        },
        {
          label: 'Señal',
          data: signal,
          type: 'line',
          borderColor: '#ffaa00',
          pointRadius: 0
        },
        {
          label: 'Histograma',
          data: histogram,
          backgroundColor: histogram.map(v => (v || 0) > 0 ? '#00ff99' : '#ff4d4d')
        }
      ]
    },
    options: getOptions()
  }));

  // Evaluación automática de TP/SL si hay operación
  if (activeTrade) {
    updateTradeStatus();

    const { tipo, takeProfit, stopLoss } = activeTrade;

    if (
      (tipo === 'LONG' && latestPrice >= takeProfit) ||
      (tipo === 'SHORT' && latestPrice <= takeProfit)
    ) {
      closeTrade('TP');
    }

    if (
      (tipo === 'LONG' && latestPrice <= stopLoss) ||
      (tipo === 'SHORT' && latestPrice >= stopLoss)
    ) {
      closeTrade('SL');
    }
  }

  // Señal visual
  let signalText = '⚪ Neutral';
  const lastRSI = rsi.at(-1);
  const lastMACD = macd.at(-1);
  const lastSignal = signal.at(-1);

  if (lastRSI && lastMACD && lastSignal) {
    if (lastRSI < 30 && lastMACD > lastSignal) signalText = '📈 Posible entrada LONG';
    if (lastRSI > 70 && lastMACD < lastSignal) signalText = '📉 Posible entrada SHORT';
  }

  document.getElementById("signal").textContent = signalText;
  document.getElementById("status").textContent = `Última actualización: ${new Date().toLocaleTimeString()}`;
}

function getOptions(max = undefined) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: false,
        suggestedMax: max,
        ticks: { color: '#aaa' },
        grid: { color: '#333' }
      },
      x: {
        ticks: { color: '#888', maxTicksLimit: 10 },
        grid: { display: false }
      }
    },
    plugins: {
      legend: {
        labels: { color: '#aaa' }
      },
      tooltip: {
        mode: 'index',
        intersect: false
      }
    }
  };
}

function getHigherTimeframe(current) {
  const map = {
    '1m': '15m',
    '5m': '1h',
    '15m': '4h',
    '1h': '1d',
    '4h': '1d',
    '1d': '1w',
    '1w': '1w'
  };
  return map[current] || '1d';
}

function openTrade(type) {
  const lastPrice = latestPrice;
  const tp = type === 'LONG' ? lastPrice * 1.03 : lastPrice * 0.97;
  const sl = type === 'LONG' ? lastPrice * 0.985 : lastPrice * 1.015;

  activeTrade = {
    tipo: type,
    precioEntrada: lastPrice,
    takeProfit: tp,
    stopLoss: sl,
    timestamp: Date.now()
  };

  updateTradeStatus();
}

function updateTradeStatus() {
  if (!activeTrade) {
    document.getElementById("tradeStatus").textContent = "Ninguna operación abierta";
    document.getElementById("candlestickCard").style.display = 'none';
    return;
  }

  const { tipo, precioEntrada, takeProfit, stopLoss } = activeTrade;
  const pnl =
    tipo === 'LONG'
      ? ((latestPrice - precioEntrada) / precioEntrada) * 100
      : ((precioEntrada - latestPrice) / precioEntrada) * 100;

  document.getElementById("tradeStatus").innerHTML = `
    Tipo: <b>${tipo}</b><br>
    Entrada: ${precioEntrada.toFixed(2)}<br>
    Último precio: ${latestPrice.toFixed(2)}<br>
    TP: ${takeProfit.toFixed(2)} | SL: ${stopLoss.toFixed(2)}<br>
    <b>Resultado:</b> ${pnl.toFixed(2)}%
  `;

  document.getElementById("candlestickCard").style.display = 'block';
  renderCandleChart();
}

function closeTrade(result) {
  let msg = '';
  const now = new Date().toLocaleString();

  if (!activeTrade) return;

  const salida = latestPrice;
  const entrada = activeTrade.precioEntrada;
  const tipo = activeTrade.tipo;
  const beneficio =
    tipo === 'LONG'
      ? ((salida - entrada) / entrada) * 100
      : ((entrada - salida) / entrada) * 100;

  if (result === 'TP') msg = '✅ Objetivo alcanzado.';
  else if (result === 'SL') msg = '🛑 Stop Loss ejecutado.';
  else msg = 'ℹ️ Cerrada manualmente.';

  tradeHistory.push({
    tipo,
    entrada,
    salida,
    resultado: beneficio.toFixed(2),
    motivo: msg,
    hora: now
  });

  renderTradeHistory();
  document.getElementById("tradeStatus").innerHTML += `<br><b>${msg}</b>`;
  activeTrade = null;

  const priceChart = charts.find(c => c.canvas.id === 'priceChart');
  if (priceChart && priceChart.options.plugins.annotation) {
    priceChart.options.plugins.annotation.annotations = {};
    priceChart.update();
  }

  document.getElementById("candlestickCard").style.display = 'none';
}

function renderTradeHistory() {
  const list = document.getElementById("historyList");
  list.innerHTML = '';

  tradeHistory.slice().reverse().forEach(trade => {
    const li = document.createElement('li');
    li.innerHTML = `
      <b>${trade.tipo}</b> | Entrada: ${trade.entrada.toFixed(2)} → Salida: ${trade.salida.toFixed(2)} |
      <span style="color:${trade.resultado >= 0 ? '#00ff99' : '#ff4d4d'}">${trade.resultado}%</span>
      <br><small>${trade.motivo} (${trade.hora})</small>
    `;
    list.appendChild(li);
  });
}

async function renderCandleChart() {
  if (!activeTrade) return;

  const limit = 80;
  const url = `https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=${currentInterval}&limit=${limit}`;
  const res = await fetch(url);
  const data = await res.json();

  const labels = data.map(d => new Date(d[0]).toLocaleTimeString());
  const prices = data.map(d => parseFloat(d[4]));

  const entrada = parseFloat(activeTrade.entrada);
  const tp = parseFloat(activeTrade.tp);
  const sl = parseFloat(activeTrade.sl);

  const entryLine = Array(labels.length).fill(entrada);
  const tpLine = Array(labels.length).fill(tp);
  const slLine = Array(labels.length).fill(sl);

  const allValues = [...prices, entrada, tp, sl];
  const minY = Math.min(...allValues) * 0.995;
  const maxY = Math.max(...allValues) * 1.005;

  if (window.candleChart) window.candleChart.destroy();

  const ctx = document.getElementById("candlestickChart").getContext("2d");

  window.candleChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Precio',
          data: prices,
          borderColor: '#00ffff',
          borderWidth: 2,
          tension: 0.4,
          pointRadius: 0
        },
        {
          label: 'Entrada',
          data: entryLine,
          borderColor: '#ffffff',
          borderDash: [5, 5],
          borderWidth: 1.2,
          pointRadius: 2,
          pointBackgroundColor: '#ffffff',
        },
        {
          label: 'TP',
          data: tpLine,
          borderColor: '#00ff99',
          borderDash: [4, 4],
          borderWidth: 1.2,
          pointRadius: 2,
          pointBackgroundColor: '#00ff99'
        },
        {
          label: 'SL',
          data: slLine,
          borderColor: '#ff4d4d',
          borderDash: [4, 4],
          borderWidth: 1.2,
          pointRadius: 2,
          pointBackgroundColor: '#ff4d4d'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: { color: '#ccc' }
        },
        tooltip: {
          mode: 'index',
          intersect: false
        }
      },
      scales: {
        x: {
          ticks: { color: '#aaa' },
          grid: { color: '#222' }
        },
        y: {
          min: minY,
          max: maxY,
          ticks: { color: '#ccc' },
          grid: { color: '#333' }
        }
      }
    }
  });
}

// Ejecutar al cargar
fetchAndRender();
setInterval(fetchAndRender, 10000); // cada 10 segundos