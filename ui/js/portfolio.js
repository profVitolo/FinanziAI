const API_BASE = "http://127.0.0.1:8000";

async function loadPortfolioAnalysis()
{
    const response = await fetch(`${API_BASE}/portfolio/analysis`);

    if (response.status === 404)
    {
        return {
            portfolio_value: 0,
            positions: [],
            exposure: {},
            risk: null
        };
    }

    if (!response.ok)
        throw new Error("Errore caricamento portfolio");

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

        li.textContent = `${symbol}: ${value.toFixed(2)}%`;
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

async function init() 
{
	
    try 
	{
        await refreshPortfolio();
    }
    catch (error) 
	{
        console.error(error);
		alert("Errore caricamento portfolio");
    }
}

document.addEventListener("DOMContentLoaded", init);
