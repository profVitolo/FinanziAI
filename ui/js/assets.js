let assets = [];
let assetDetails = null;

let currentPage = 1;
let pageSize = 10;

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