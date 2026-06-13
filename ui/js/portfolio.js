const API_BASE = "http://127.0.0.1:8000";

async function loadPortfolioAnalysis() 
{
	const response = await fetch(`${API_BASE}/portfolio/analysis`);

    if (!response.ok) throw new Error("Errore caricamento portfolio");

    return await response.json();
}

async function createTransaction(transaction) 
{
    const response = await fetch(
        `${API_BASE}/portfolio/transactions`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(transaction)
        }
    );

    if (!response.ok) throw new Error("Errore registrazione transazione");

    return await response.json();
}

function renderSummary(data) 
{
    document.getElementById("portfolio-value").textContent = data.portfolio_value.toFixed(2) ?? "-";
    document.getElementById("risk-level").textContent = data.risk?.concentration_level 
        ? `${data.risk.concentration_level} (${data.risk.largest_position_weight}%)`
        : "-";

    let largestPosition = "-";

    if (data.positions && data.positions.length > 0) 
	{
        const sorted = [...data.positions].sort( (a, b) =>  b.market_value - a.market_value );
        largestPosition =sorted[0].symbol;
    }

    document.getElementById("largest-position").textContent = largestPosition;
}

function renderPositions(data) 
{
    const table = document.getElementById("positions-table");

    table.innerHTML = "";

    for (const position of data.positions) 
	{
        const row =  document.createElement("tr");

        row.innerHTML = `
            <td>
				<a href="asset.html?symbol=${position.symbol}">
					${position.symbol}
				</a>
			</td>
            <td>${position.quantity}</td>
            <td>${position.avg_price.toFixed(2)}</td>
            <td>${position.market_price.toFixed(2)}</td>
            <td>
				${position.performance.pnl.toFixed(2)}  (${position.performance.pnl_percent.toFixed(2)}%)
			</td>
        `;
        table.appendChild(row);
    }
}

function renderExposure(data) 
{
	const exposureList = document.getElementById("exposure-list");

    exposureList.innerHTML = "";

    for (const [symbol, value] of Object.entries( data.exposure )) 
	{
		const li = document.createElement("li");

        li.textContent = `${symbol}: ${value}%`;
        exposureList.appendChild(li);
    }
}

function renderPortfolio(data) 
{
	renderSummary(data);
	renderPositions(data);
	renderExposure(data);
}

async function refreshPortfolio() 
{
    const data = await loadPortfolioAnalysis();
    renderPortfolio(data);
}

async function handleTransaction(event) 
{
    event.preventDefault();
	
	const assetId = document.getElementById("asset-id").value;

	if (!assetId)
	{
		alert("Selezionare un asset valido");
		return;
	}
	
    const transaction = {
        asset_id: parseInt(assetId),
        operation_type: document.getElementById("transaction-type").value,
        quantity: parseFloat(document.getElementById("quantity").value),
        price: parseFloat(document.getElementById("price").value),
        fees: parseFloat(document.getElementById("fees").value),
		transaction_date: document.getElementById("transaction-date").value
    };

    try 
	{
        await createTransaction(transaction);
        await refreshPortfolio();
		resetTransactionForm(event.target);
    }
    catch (error) 
	{
        console.error(error);
		clearAssetSelection();
        alert("Errore registrazione transazione");
    }
}

async function resolveAsset(symbol) 
{
    try 
	{
        let response = await fetch(`${API_BASE}/assets/${symbol}`);

        if (!response.ok) 
		{
            const syncResponse = await fetch(`${API_BASE}/assets/${symbol}/sync`, {method: "POST"});
			
			if (!syncResponse.ok)
                throw new Error("Errore sincronizzazione asset");
            
            response = await fetch(`${API_BASE}/assets/${symbol}`);
        }

        if (!response.ok)throw new Error("Asset non trovato");

        return await response.json();
    }
    catch 
	{
	    clearAssetSelection();
		alert(`Asset '${symbol}' non valido`);
        return null;
    }
}

function clearAssetSelection()
{
    document.getElementById("asset-id").value = "";
}

function resetTransactionForm(form)
{
    form.reset();
    clearAssetSelection();
    initializeTransactionDate();
}

function initializeTransactionDate()
{
    const today = new Date().toISOString().split("T")[0];
    document.getElementById("transaction-date").value = today;
}

async function handleSymbolBlur()
{
    const symbol = document.getElementById("symbol").value.trim().toUpperCase();
    if (!symbol) 
		return;
	
	const asset = await resolveAsset(symbol);
    if (!asset)
        return;

    document.getElementById("asset-id").value = asset.id;
}

async function init() 
{
	const symbolInput = document.getElementById("symbol");
	symbolInput.addEventListener("blur",handleSymbolBlur);
	symbolInput.addEventListener("input", clearAssetSelection);
	
	initializeTransactionDate();
	
    try 
	{
        await refreshPortfolio();
        document.getElementById("transaction-form").addEventListener("submit", handleTransaction);
    }
    catch (error) 
	{
        console.error(error);
		alert("Errore caricamento portfolio");
    }
}

document.addEventListener("DOMContentLoaded", init);
