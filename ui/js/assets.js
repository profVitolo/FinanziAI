
function getSymbol() 
{
    const params = new URLSearchParams(window.location.search);

    return params.get("symbol")?.toUpperCase();
}

async function updateAsset(symbol) 
{
	const today = new Date().toISOString().split('T')[0];
  
    const response = await fetch(`${API_BASE}/assets/${symbol}/update`, 
		{
			method: "POST",
			headers: { "Content-Type": "application/json"},
			body: JSON.stringify({inital_days: 365})
		}
	);
	
    if (!response.ok) throw new Error("Errore recupero asset");
    
    return await response.json();
}

async function syncAsset(symbol, startDate, endDate = null) {
    const response = await fetch(
        `${API_BASE}/assets/${symbol}/sync`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                start_date: startDate,
                end_date: endDate
            })
        }
    );

    if (!response.ok)
        throw new Error("Errore sincronizzazione asset");

    return await response.json();
}

async function loadAnalysis(symbol) 
{
    const response = await fetch(`${API_BASE}/assets/${symbol}/analysis`);
	
    if (!response.ok) throw new Error("Errore caricamento analisi");

    return await response.json();
}

async function addToWatchlist(symbol) 
{
    const response = await fetch(`${API_BASE}/watchlist/${symbol}`, {method: "POST"});

    if (!response.ok) throw new Error("Errore aggiunta watchlist");

    alert(`${symbol} aggiunto alla watchlist`);
}

async function removeFromWatchlist(symbol) 
{
    const response = await fetch(`${API_BASE}/watchlist/${symbol}`, {method: "DELETE"});

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
	
	document.getElementById("asset-sector").textContent = data.asset.sector ?? "-";
	document.getElementById("asset-industry").textContent = data.asset.industry ?? "-";
	document.getElementById("asset-country").textContent = data.asset.country ?? "-";
	document.getElementById("asset-market-cap").textContent = formatFinancialNumber(data.asset.market_cap);
	document.getElementById("asset-beta").textContent = data.asset.beta?.toFixed(2) ?? "-";
	document.getElementById("asset-website").innerHTML = data.asset.website
			? `<a href="${data.asset.website}" target="_blank">${data.asset.website}</a>`
			: "-";
	
    document.getElementById("market-price").textContent = data.market_data.last_close.toFixed(2) ?? "-";
    document.getElementById("last-update").textContent = data.period.end ?? "-";

    document.getElementById("rsi").textContent =  data.indicators.rsi?.toFixed(2) ?? "-";
    document.getElementById("sma20").textContent = data.indicators.sma20?.toFixed(2) ?? "-";
    document.getElementById( "sma50").textContent = data.indicators.sma50?.toFixed(5) ?? "-";
    document.getElementById("volatility").textContent = data.indicators.annualized_volatility?.toFixed(2) ?? "-";
    document.getElementById("trend").textContent = data.analysis.trend ?? "-";
    document.getElementById("volatility-class").textContent = data.analysis.volatility_level ?? "-";
}

async function deleteAsset(symbol)
{
    const confirmed = confirm(
		`Vuoi davvero cancellare ${symbol}?\n\n` +
		"• Verranno eliminati tutti i prezzi storici\n" +
		"• Verrà rimosso dalla watchlist\n" +
		"• Se esistono transazioni la cancellazione verrà bloccata"
	);

    if (!confirmed)
        return;

    const response = await fetch(`${API_BASE}/assets/${symbol}`, {method: "DELETE"});

    const result = await response.json();

    if (!response.ok)
        throw new Error(result.detail || "Errore cancellazione asset");

    alert(`${symbol} cancellato`);
    window.location.href = "assets.html";
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
        await updateAsset(symbol);
        const analysis = await loadAnalysis(symbol);

        renderAnalysis(analysis);

        document.getElementById("sync-btn").addEventListener(
			"click",
			async () => 
			{
				const _5YearsAgo = new Date();
				_5YearsAgo.setFullYear(_5YearsAgo.getFullYear() - 5);
				const endDate =  _5YearsAgo.toJSON().slice(0, 10);//5 anni fa
				const startDate = prompt("Scarica lo storico a partire da (YYYY-MM-DD):", endDate);
				
				if (!startDate)
					return;
				
				await syncAsset(symbol, startDate);
				const analysis =  await loadAnalysis(symbol);
				renderAnalysis(analysis);
			}
		);

        document.getElementById("watchlist-add-btn").addEventListener("click", () => addToWatchlist(symbol));
		document.getElementById("watchlist-del-btn").addEventListener("click", () => removeFromWatchlist(symbol));
    	document.getElementById("del-btn").addEventListener("click", () => deleteAsset(symbol));
	} 
	catch (error) 
	{
        console.error(error);
        alert( "Errore caricamento asset");
    }
}


document.addEventListener("DOMContentLoaded", init);