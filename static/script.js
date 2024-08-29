function getQueryParam(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}
// symbols = ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA', 'NVDA']
const stockSymbol = getQueryParam('symbol') || 'AMZN';
const predictionElement = document.getElementById("prediction");

window.onload = function() {
    new TradingView.widget({
        container_id: "tradingview_chart",
        width: "100%",
        height: "100%",
        symbol: stockSymbol,
        interval: "1",
        timezone: "Etc/UTC",
        theme: "dark",
        style: "2",
        locale: "en",
        toolbar_bg: "#2e2e2e",
        hide_watermark: true,
        hide_timeframes: true,
        withdateranges: false,
        hide_side_toolbar: true,
        hide_legend: true,
        hide_volume: true,
        hide_top_toolbar: false,
        studies: [],
        hideideas: true,
        enable_publishing: false,
        allow_symbol_change: false,
        hide_logo: true
    });
}

fetch('http://localhost:8000/api/predict', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ stock: stockSymbol })
})
.then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
})
.then(data => {
    if (data.prediction) {
        predictionElement.style.display = 'block';
        predictionElement.textContent = `${stockSymbol} ${data.prediction}`;
    } else {
        throw new Error('Prediction data not available');
    }
})
.catch(error => {
    console.error('Error fetching prediction:', error);
    predictionElement.style.display = 'block';
    predictionElement.textContent = `Error fetching predicted price: ${error.message}`;
});