const API_BASE = "http://127.0.0.1:8000";

function getSymbol() 
{
    const params = new URLSearchParams(window.location.search);

    return params.get("symbol")?.toUpperCase();
}

async function syncAsset(symbol) 
{
    const response = await fetch(`${API_BASE}/assets/${symbol}/sync`, {method: "POST"});

    if (!response.ok) throw new Error("Errore sincronizzazione asset");
    
    return await response.json();
}


async function loadAnalysis(symbol) 
{
    const response = await fetch(`${API_BASE}/analysis/${symbol}`);

    if (!response.ok) throw new Error("Errore caricamento analisi");

    return await response.json();
}


async function addToWatchlist(symbol) 
{
    const response = await fetch(`${API_BASE}/watchlist/${symbol}`, {method: "POST"});

    if (!response.ok) throw new Error("Errore aggiunta watchlist");

    alert(`${symbol} aggiunto alla watchlist`);
}

function renderAnalysis(data) 
{
	document.getElementById("asset-symbol").textContent = data.asset.symbol;
    document.getElementById("asset-name").textContent = data.asset.name ?? "-";
    document.getElementById("asset-symbol-info").textContent = data.asset.symbol ?? "-";
    document.getElementById("asset-type").textContent = data.asset.type ?? "-";
    document.getElementById("asset-currency").textContent = data.asset.currency ?? "-";
    document.getElementById("asset-exchange").textContent = data.asset.exchange ?? "-";

    document.getElementById("market-price").textContent = data.market_data.last_close ?? "-";
    document.getElementById("last-update").textContent = data.period.end ?? "-";

    document.getElementById("rsi").textContent =  data.indicators.rsi ?? "-";
    document.getElementById("sma20").textContent = data.indicators.sma20 ?? "-";
    document.getElementById( "sma50").textContent = data.indicators.sma50 ?? "-";
    document.getElementById("volatility").textContent = data.indicators.annualized_volatility ?? "-";
    document.getElementById("trend").textContent = data.analysis.trend ?? "-";
    document.getElementById("volatility-class").textContent = data.analysis.volatility_class ?? "-";
}

async function init() 
{
    const symbol = getSymbol();

    if (!symbol) 
	{
        alert("Simbolo non specificato"  );
        return;
    }

    try 
	{
        await syncAsset(symbol);
        const analysis = await loadAnalysis(symbol);

        renderAnalysis(analysis);

        document.getElementById("sync-btn").addEventListener(
                "click",
                async () => 
				{
                    await syncAsset(symbol);
                    const analysis =  await loadAnalysis(symbol);
                    renderAnalysis(analysis);
                }
            );

        document.getElementById("watchlist-btn").addEventListener(
                "click",
                () => addToWatchlist(symbol)
            );
    } 
	catch (error) 
	{
        console.error(error);
        alert( "Errore caricamento asset");
    }
}


document.addEventListener("DOMContentLoaded", init);