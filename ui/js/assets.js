let assets = [];
let assetDetails = null;

let currentPage = 1;
let pageSize = setupPageSize(
	"page-size-input",
	"app.assets.pageSize",
	10,
	refreshTableTransactions
);

async function loadAssetDetails()
{
    const symbol = document.getElementById("asset-select").value;

    if (!symbol)
        return;

    const startDate = document.getElementById("filter-start-date").value;
    const endDate = document.getElementById("filter-end-date").value;

    assetDetails = await getAssetDetails(
        symbol,
        startDate,
        endDate
    );

    renderAssetInfo(assetDetails.asset);
	console.log("LoadAssetDetails:", pageSize);
    refreshTableTransactions(pageSize);
	
	renderAssetPriceChart(assetDetails.prices);
	renderAssetVolumeChart(assetDetails.prices);
}

function refreshTableTransactions(page_size)
{
	pageSize = page_size;
	updateTable(
        renderPrices,
        assetDetails.prices,
        "prices-pagination",
        currentPage,
        pageSize
    );
}

async function handleFilters()
{
    currentPage = 1;
    await loadAssetDetails();
}

function resetFilters()
{
    document.getElementById("filter-start-date").value = "";
    document.getElementById("filter-end-date").value = "";

    handleFilters();
}

function renderAssetPriceChart(prices)
{
    const container = document.getElementById("asset-price-chart");
    container.innerHTML = "";

    const chart = LightweightCharts.createChart(
        container,
        {
            width: container.clientWidth || 1000,
            height: container.clientHeight ||400,
            layout: {
                background: { color: "#ffffff" },
                textColor: "#333"
            },
            grid: {
                vertLines: { color: "#f0f0f0" },
                horzLines: { color: "#f0f0f0" }
            }
        }
    );

    const series = chart.addCandlestickSeries({
		upColor: "#22c55e",
		downColor: "#ef4444",

		borderUpColor: "#22c55e",
		borderDownColor: "#ef4444",

		wickUpColor: "#3b82f6",
		wickDownColor: "#3b82f6"
	});
	
    const data = [...prices]
        .sort((a, b) => a.date.localeCompare(b.date))
        .map(price => ({
            time: price.date,
            open: Number(price.open),
            high: Number(price.high),
            low: Number(price.low),
            close: Number(price.close)
        }));

    series.setData(data);

    chart.timeScale().fitContent();
	
	chart.subscribeCrosshairMove(param => {
		if (!param.point || !param.time)
		{
			document.getElementById("chart-legend").innerHTML = "&nbsp;";
			return;
		}
		
		const data = param.seriesData.get(series);

		if (!data)
			return;

		document.getElementById("chart-legend").innerHTML =
			`O: ${data.open.toFixed(2)}
			 H: ${data.high.toFixed(2)}
			 L: ${data.low.toFixed(2)}
			 C: ${data.close.toFixed(2)}`;
	});
}

function renderAssetVolumeChart(prices)
{
    const container = document.getElementById("asset-volume-chart");
    container.innerHTML = "";

    const chart = LightweightCharts.createChart(
        container,
        {
            width: container.clientWidth || 1000,
            height: container.clientHeight || 400,
            layout: {
                background: { color: "#ffffff" },
                textColor: "#333"
            },
            grid: {
                vertLines: { color: "#f0f0f0" },
                horzLines: { color: "#f0f0f0" }
            }
        }
    );

    const series = chart.addHistogramSeries({color: "#26a69a"});

    const data = [...prices]
        .sort((a, b) => a.date.localeCompare(b.date))
        .map(price => ({
            time: price.date,
            value: Number(price.volume),
            color: Number(price.close) >= Number(price.open) ? "#26a69a" : "#ef5350"
        }));

    series.setData(data);

    chart.timeScale().fitContent();

    return chart;
}

function renderAssetInfo(asset)
{
    const table = document.getElementById("asset-info");

    table.innerHTML = `
        <tr><td>Symbol</td><td>
			<a href="asset.html?symbol=${asset.symbol}">
				${asset.symbol}
			</a>
		</td></tr>
        <tr><td>Name</td><td>${asset.name}</td></tr>
        <tr><td>Type</td><td>${asset.type}</td></tr>
        <tr><td>Currency</td><td>${asset.currency}</td></tr>
        <tr><td>Exchange</td><td>${asset.exchange}</td></tr>
    `;

}

function renderPrices(prices)
{
    const table = document.getElementById("prices-table");

    table.innerHTML = "";

    for (const price of prices)
    {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${price.date}</td>
            <td>${Number(price.open).toFixed(2)}</td>
            <td>${Number(price.high).toFixed(2)}</td>
            <td>${Number(price.low).toFixed(2)}</td>
            <td>${Number(price.close).toFixed(2)}</td>
            <td>${price.volume}</td>
        `;

        table.appendChild(row);
    }
}

async function loadAssets()
{
    const response = await fetch("/assets/");

    if (!response.ok)
        throw new Error("Errore caricamento asset");

    return await response.json();
}

async function getAssetDetails(symbol, startDate = "", endDate = "")
{
    const params = new URLSearchParams();

    if (startDate)
        params.append("start_date", startDate);

    if (endDate)
        params.append("end_date", endDate);

    const query = params.toString() ? `?${params.toString()}` : "";

    const response = await fetch(`/assets/${symbol}/details${query}`);

    if (!response.ok)
        throw new Error("Errore caricamento dettagli asset");

    return await response.json();
}

function populateAssetSelect(selectId, assets)
{
    const select = document.getElementById(selectId);

    select.innerHTML = "";
	
	if (assets.length == 0)
	{
		alert("Still no asset in db");
		return;
	}
	
    for (const asset of assets)
    {
        const option = document.createElement("option");

        option.value = asset.symbol;
        option.textContent = `${asset.symbol} - ${asset.name}`;

        select.appendChild(option);
    }
	
}

async function init()
{
    generateMenu();

    assets = await loadAssets();

    populateAssetSelect("asset-select",assets);

    const params = getQueryParams();

    if (params.asset)
        document.getElementById("asset-select").value = params.asset;

    if (params.start_date)
        document.getElementById("filter-start-date").value = params.start_date;

    if (params.end_date)
        document.getElementById("filter-end-date").value = params.end_date;

    if (!params.asset && assets.length > 0)
        document.getElementById("asset-select").value = assets[0].symbol;

    await loadAssetDetails();
}

document.addEventListener("DOMContentLoaded", init);

/*
pageSize = 25;
setSetting("app.assets.pageSize", pageSize);
*/