let activeTrade = null;

function openTrade(type) {
  const lastPrice = latestPrice;
  activeTrade = {
    tipo: type,
    precioEntrada: lastPrice,
    timestamp: Date.now()
  };
  updateTradeStatus();
}

function updateTradeStatus() {
  const el = document.getElementById("tradeStatus");
  if (!activeTrade) {
    el.textContent = "Ninguna operación abierta";
    return;
  }

  const diff = latestPrice - activeTrade.precioEntrada;
  const pct = ((diff / activeTrade.precioEntrada) * 100).toFixed(2);
  const beneficio = activeTrade.tipo === 'LONG' ? pct : (-pct).toFixed(2);
  const color = beneficio >= 0 ? '#00ff99' : '#ff4d4d';

  el.innerHTML = `
    <b>Tipo:</b> ${activeTrade.tipo} <br>
    <b>Entrada:</b> ${activeTrade.precioEntrada.toFixed(2)} <br>
    <b>Precio actual:</b> ${latestPrice.toFixed(2)} <br>
    <b>Resultado:</b> <span style="color:${color}">${beneficio}%</span>
  `;
}
