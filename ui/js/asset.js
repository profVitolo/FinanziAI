
function getSymbol() 
{
    const params = new URLSearchParams(window.location.search);

    return params.get("symbol")?.toUpperCase();
}

async function syncAsset(symbol) 
{
	const today = new Date().toISOString().split('T')[0];
  
    const response = await fetch(`${API_BASE}/assets/${symbol}/sync`, 
		{
			method: "POST",
			headers: { "Content-Type": "application/json"},
			body: JSON.stringify({ start_date: today })
		}
	);
	
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
    const response = await fetch(`${API_BASE}/portfolio/watchlist/${symbol}`, {method: "POST"});

    if (!response.ok) throw new Error("Errore aggiunta watchlist");

    alert(`${symbol} aggiunto alla watchlist`);
}

async function removeFromWatchlist(symbol) 
{
    const response = await fetch(`${API_BASE}/portfolio/watchlist/${symbol}`, {method: "DELETE"});

    if (!response.ok) throw new Error("Errore rimozione dalla watchlist");

    alert(`${symbol} rimosso dalla watchlist`);
}

function renderAnalysis(data) 
{
    document.getElementById("asset-name").textContent = data.asset.name ?? "-";
    document.getElementById("asset-symbol-info").textContent = data.asset.symbol ?? "-";
    document.getElementById("asset-type").textContent = data.asset.type ?? "-";
    document.getElementById("asset-currency").textContent = data.asset.currency ?? "-";
    document.getElementById("asset-exchange").textContent = data.asset.exchange ?? "-";

    document.getElementById("market-price").textContent = data.market_data.last_close.toFixed(2) ?? "-";
    document.getElementById("last-update").textContent = data.period.end ?? "-";

    document.getElementById("rsi").textContent =  data.indicators.rsi?.toFixed(2) ?? "-";
    document.getElementById("sma20").textContent = data.indicators.sma20?.toFixed(2) ?? "-";
    document.getElementById( "sma50").textContent = data.indicators.sma50?.toFixed(5) ?? "-";
    document.getElementById("volatility").textContent = data.indicators.annualized_volatility?.toFixed(2) ?? "-";
    document.getElementById("trend").textContent = data.analysis.trend ?? "-";
    document.getElementById("volatility-class").textContent = data.analysis.volatility_level ?? "-";
}

async function init() 
{
	generateMenu();
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

        document.getElementById("watchlist-add-btn").addEventListener(
                "click",
                () => addToWatchlist(symbol)
            );
			
		document.getElementById("watchlist-del-btn").addEventListener(
                "click",
                () => removeFromWatchlist(symbol)
            );
    } 
	catch (error) 
	{
        console.error(error);
        alert( "Errore caricamento asset");
    }
}


document.addEventListener("DOMContentLoaded", init);