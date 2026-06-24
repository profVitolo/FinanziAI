
let rates = [];
let missingDates = [];
let fromCurrencies = [];
let currentPage = 1;
let pageSize = setupPageSize(
	"page-size-input",
	"app.exchange.pageSize",
	10,
	refreshTableTransactions
);

function bindEvents()
{
    document.getElementById("from-currency").addEventListener("change", refreshRates);
    document.getElementById("start-date").addEventListener("change", refreshRates);
    document.getElementById("end-date").addEventListener("change", refreshRates);
    document.getElementById("sync-range").addEventListener("click", syncRates);
}

function buildFilters()
{
    const params = new URLSearchParams();

    const fromCurrency = document.getElementById("from-currency").value;
    const startDate = document.getElementById("start-date").value;
    const endDate = document.getElementById("end-date").value;

    if (fromCurrency)
        params.append("from_currency", fromCurrency);

    if (startDate)
        params.append("start_date", startDate);

    if (endDate)
        params.append("end_date", endDate);

    return params;
}

async function refreshRates()
{
    await loadRates();
	renderRatesChart(rates);
	refreshTableTransactions(pageSize);
	renderCoverage();

    await loadMissingDates();
}

function refreshTableTransactions(page_size)
{
	pageSize = page_size;
	updateTable(renderRates, rates, "rates-pagination",currentPage, pageSize);
}

async function loadRates()
{
    const response = await fetch(`${API_BASE}/exchange/rates?${buildFilters()}`);

    if (!response.ok)
        throw new Error("Unable to load exchange rates");

    rates = await response.json();
}

function renderRates(rates)
{
    const table = document.getElementById("rates-table");

    table.innerHTML = "";

    for (const rate of rates)
    {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${rate.rate_date}</td>
            <td>${rate.from_currency}</td>
            <td>${rate.to_currency}</td>
            <td>${rate.rate.toFixed(6)}</td>
        `;

        table.appendChild(row);
    }
}

function renderCoverage()
{
    const info = document.getElementById("coverage-info");

    if (rates.length === 0)
    {
        info.textContent = "Nessun dato disponibile.";

        return;
    }

    const newest = rates[0].rate_date;
    const oldest = rates[rates.length - 1].rate_date;

    info.textContent = `Copertura dati dal ${oldest} al ${newest}`;
}

function renderRatesChart(rates)
{
	let chartTitle = "";
	if (rates.length == 0)
		chartTitle = "No data to graph";
	else
	{
		const container = document.getElementById("exchange-chart");

		container.innerHTML = "";

		const chart = LightweightCharts.createChart(
			container,
			{
				width: container.clientWidth || 1000,
				height: container.clientHeight ||400
			}
		);

		const series = chart.addLineSeries();
		const data = rates
		.map(rate => ({
			time: rate.rate_date,
			value: Number(rate.rate)
		}))
		.sort((a, b) => a.time.localeCompare(b.time));

		series.setData(data);

		chart.timeScale().fitContent();
		
		const fromCurrency = document.getElementById("from-currency").selectedOptions[0].value;
		chartTitle = `${fromCurrency}/${appInfo.base_currency}`;
	}
	
	document.getElementById("chart-title").innerText = chartTitle;
}

function renderFromCurrencies()
{
	const selector = document.getElementById("from-currency");
	let html = "";
			
	if (fromCurrencies.length === 0)
		html = `<option value="USD">USD</option>`; //di default vedi solo USD
	else
	{

		for(const curr of fromCurrencies)
			html += `<option value="${curr}">${curr}</option>`;
		
	}	
	selector.innerHTML = html;
}

async function loadMissingDates()
{
    const fromCurrency = document.getElementById("from-currency").value;
    const startDate = document.getElementById("start-date").value;
    const endDate = document.getElementById("end-date").value;

    if (!startDate || !endDate)
        return;

    const params = new URLSearchParams();

    params.append("from_currency",fromCurrency);
    params.append("to_currency",appInfo.baseCurrency);
    params.append("start_date",startDate);
    params.append("end_date",endDate);

    const response = await fetch(`${API_BASE}/exchange/missing?${params}`);

    if (!response.ok)
        throw new Error("Unable to load missing dates");

    const data = await response.json();
    missingDates = data.missing_dates;

    renderMissingSummary();
}

function renderMissingSummary()
{
    const container = document.getElementById("missing-summary");

    if (missingDates.length === 0)
    {
        container.textContent = "Nessun buco rilevato.";

        return;
    }

    container.textContent = `Date mancanti: ${missingDates.length}`;
}

async function syncRates()
{
    const fromCurrency = document.getElementById("from-currency").value;
    const startDate = document.getElementById("sync-start-date").value;
    const endDate = document.getElementById("sync-end-date").value;

    if (!startDate)
    {
        alert("Data iniziale richiesta");
        return;
    }

	if (!fromCurrency)
	{
		return;
	}
	
    const response = await fetch(`${API_BASE}/exchange/sync-range`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                from_currency: fromCurrency,
                to_currency: appInfo.base_currency,
                start_date: startDate,
                end_date: endDate
            })
        }
    );

    if (!response.ok)
        throw new Error("Sync exchange rates failed");

    const result = await response.json();

    alert(
        `Processati: ${result.processed}\n` +
        `Salvati: ${result.saved}\n` +
        `Falliti: ${result.failed}`
    );

    await refreshRates();
}

async function loadFromCurrencies()
{
    const response =
        await fetch(`${API_BASE}/exchange/from-currencies`);

    if (!response.ok)
        throw new Error("Unable to load currencies");

    const data = await response.json();
	fromCurrencies = data;
	renderFromCurrencies();
}
 
async function init()
{
	generateMenu();
    bindEvents();
	await loadAppInfo();
	document.querySelector("#to-currency").innerText = " ►► " + appInfo.base_currency;
	await loadFromCurrencies();
    await refreshRates();
}

document.addEventListener("DOMContentLoaded", init);