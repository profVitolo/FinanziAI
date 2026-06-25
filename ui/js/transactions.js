/* ==========================================================
 * STATE
 * ========================================================== */
let assetsMap = {};
let allTransactions = [];
let filteredTransactions = [];

let distributionChart = null;
let valueChart = null;
let buySellChart = null;
let buySellChartType = "bar";
let feesChart = null;
let feesChartType = "bar";

let currentPage = 1;
let pageSize = setupPageSize(
	"page-size-input",
	"app.transactions.pageSize",
	10,
	refreshTableTransactions
);

/* ==========================================================
 * API
 * ========================================================== */

async function loadTransactions(filters = {})
{
    const params = new URLSearchParams();

    if (filters.asset_id)
        params.append("asset_id", filters.asset_id);

    if (filters.start_date)
        params.append("start_date", filters.start_date);

    if (filters.end_date)
        params.append("end_date", filters.end_date);

    const response = await fetch(`${API_BASE}/transactions/?${params.toString()}`);

    if (!response.ok)
        throw new Error("Errore caricamento transazioni");

    return await response.json();
}

async function createTransaction(transaction) 
{
    const response = await fetch(
        `${API_BASE}/transactions/`,
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

async function updateTransaction(transactionId, payload)
{
    const response = await fetch(
        `${API_BASE}/transactions/${transactionId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        }
    );

    if (!response.ok)
        throw new Error("Errore aggiornamento transazione");

    return await response.json();
}

async function deleteTransaction(transactionId)
{
    const response = await fetch(`${API_BASE}/transactions/${transactionId}`, {method: "DELETE"});

    if (!response.ok)
        throw new Error("Errore eliminazione transazione");

    return await response.json();
}

async function getTransaction(transactionId)
{
    const response = await fetch(
        `${API_BASE}/transactions/${transactionId}`
    );

    if (!response.ok)
        throw new Error("Errore caricamento transazione");

    return await response.json();
}

/* ==========================================================
 * RENDERING
 * ========================================================== */

function renderAsset(assetId)
{
    const asset = assetsMap[assetId];

    if (!asset)
        return `#${assetId}`;

    return `
        <a href="asset.html?symbol=${asset.symbol}">
            ${asset.symbol}
        </a>
        <br>
        <small>${asset.name}</small>
    `;
}

function renderTransactions(transactions)
{
    const table = document.getElementById("transactions-table");

    table.innerHTML = "";

    for (const transaction of transactions)
    {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${transaction.id}</td>

            <td>
                ${renderAsset(transaction.asset_id)}
            </td>

            <td>${transaction.date}</td>

            <td>${transaction.type}</td>

            <td>${parseFloat(transaction.quantity.toFixed(6))}</td>

            <td>${Number(transaction.price).toFixed(2)}</td>

            <td>${Number(transaction.fees).toFixed(2)}</td>

            <td>
				<button class="edit" data-id="${transaction.id}" title="Modifica">
					✏️
				</button>

				<button class="delete" data-id="${transaction.id}" title="Elimina" >
					🗑️
				</button>
			</td>
        `;

        table.appendChild(row);
    }

    attachActionHandlers();
}

function attachActionHandlers()
{
    document
        .querySelectorAll("button.edit")
        .forEach(
            button =>
                button.addEventListener(
                    "click",
                    handleEdit
                )
        );

    document
        .querySelectorAll("button.delete")
        .forEach(
            button =>
                button.addEventListener(
                    "click",
                    handleDelete
                )
        );
}

function renderCurrencyLabels(baseCurrency)
{
	const txt = ` (${baseCurrency})`;
    document.getElementById("th-price").textContent += txt;
    document.getElementById("th-fees").textContent += txt;
    document.getElementById("price").placeholder += txt;
    document.getElementById("fees").placeholder += txt;
}

/* ==========================================================
 * GRAFICI
 * ========================================================== */
 
function renderDistributionChart(transactions)
{
    const canvas = document.getElementById("transaction-distribution-chart");

    if (distributionChart)
        distributionChart.destroy();

    const distribution = {};

    transactions.forEach(transaction =>
    {
		//console.log(transaction.asset_id);
		const asset = assetsMap[transaction.asset_id];
		//console.log(assetsMap[transaction.asset_id]);
        const symbol = asset.symbol;
        const value = Number(transaction.quantity) * Number(transaction.price);

        distribution[symbol] = (distribution[symbol] || 0) + value;
    });

    const labels = Object.keys(distribution);

    const values = Object.values(distribution);

    const colors = [
        "#4f46e5",
        "#06b6d4",
        "#10b981",
        "#f59e0b",
        "#ef4444",
        "#8b5cf6",
        "#ec4899",
        "#14b8a6",
        "#84cc16",
        "#f97316"
    ];

    distributionChart = new Chart(canvas, {
        type: "pie",
        data: {
            labels,
            datasets: [{
                data: values,
                backgroundColor: labels.map((_, index) => colors[index % colors.length])
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {position: "right"},
                tooltip: {
                    callbacks: {
                        label: function(context)
                        {
                            const total = context.dataset.data.reduce((sum, value) => sum + value, 0);
                            const percentage = (context.raw / total) * 100;

                            return `${context.label}: ${appInfo.base_currency} ${context.raw.toFixed(2)}(${percentage.toFixed(1)}%)`;
                        }
                    }
                }
            }
        }
    });
}

function renderTransactionDetails(transactions)
{
    const distributionList = document.getElementById("transaction-distribution-list");
    distributionList.innerHTML = "";
    const distribution = {};

    transactions.forEach(transaction =>
    {
		const asset = assetsMap[transaction.asset_id];
        const symbol = asset.symbol;
        const value = Number(transaction.quantity) * Number(transaction.price);
        distribution[symbol] = (distribution[symbol] || 0) + value;
    });

    const total = Object.values(distribution).reduce((sum, value) => sum + value, 0);
    const entries = Object.entries(distribution)
        .map(([symbol, value]) => ({symbol, percentage: total > 0 ? (value / total) * 100 : 0}))
        .sort((a, b) => b.percentage - a.percentage);

    entries.forEach(entry =>
    {
        const li = document.createElement("li");
        li.innerHTML = `<span>${entry.symbol}</span><strong>${entry.percentage.toFixed(2)}%</strong>`;
        distributionList.appendChild(li);
    });
}

function renderValueChart(transactions)
{
    const canvas = document.getElementById("transaction-value-chart");

    if (valueChart)
        valueChart.destroy();

    const valuesByDate = {};
	const detailsByDate = {};
	const buyByDate = {};
	const sellByDate = {};

	transactions.forEach(transaction =>
	{
		const date = transaction.date;
		const asset = assetsMap[transaction.asset_id];
		const symbol = asset?.symbol ?? "?";
		const value = Number(transaction.quantity) * Number(transaction.price);
		valuesByDate[date] = (valuesByDate[date] || 0) + value;
		
		if (transaction.type === "buy")
			buyByDate[date] = (buyByDate[date] || 0) + value;
		else
			sellByDate[date] = (sellByDate[date] || 0) + value;

		if (!detailsByDate[date])
			detailsByDate[date] = [];

		detailsByDate[date].push({symbol, type: transaction.type,value});
	});
	
    const labels = Object.keys(valuesByDate).sort();
    const values = labels.map(date => valuesByDate[date]);
	const colors = labels.map(date =>
	{
		const buy = buyByDate[date] || 0;
		const sell = sellByDate[date] || 0;

		if (buy > 0 && sell > 0)
		{
			return buy >= sell
				? "#4fc3f7"
				: "#ff9800";
		}

		return buy > 0
			? "#4caf50"
			: "#f44336";
	});
	
    valueChart = new Chart(canvas, {
        type: "bar",
        data: {
            labels,
            datasets: [{
                label: "Valore Transato",
                data: values,
                backgroundColor: colors,
                borderColor: colors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context)
                        {
                            return `${appInfo.base_currency} ${context.raw.toFixed(2)}`;
                        },
						afterLabel: function(context)
						{
							const date = context.label;
							return detailsByDate[date].map(detail =>
								`${detail.symbol} - ${appInfo.base_currency} ${detail.value.toFixed(2)} (${detail.type.toUpperCase()})`
							);
						}
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: "Euro"
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: "Data"
                    }
                }
            }
        }
    });
}

function renderBuySellChart(transactions)
{
    const canvas = document.getElementById("buy-sell-chart");

    if (buySellChart)
        buySellChart.destroy();

    const buyByDate = {};
    const sellByDate = {};

    transactions.forEach(transaction =>
    {
        const date = transaction.date;
        const value = Number(transaction.quantity) * Number(transaction.price);

        if (transaction.type === "buy")
            buyByDate[date] = (buyByDate[date] || 0) + value;
        else
            sellByDate[date] = (sellByDate[date] || 0) + value;
    });

    const labels = [...new Set([...Object.keys(buyByDate),...Object.keys(sellByDate)])].sort();
    const buyValues = labels.map(date => buyByDate[date] || 0);
    const sellValues = labels.map(date => sellByDate[date] || 0);

    buySellChart = new Chart(canvas, {
        type: buySellChartType,
        data: {
            labels,
            datasets: [
                {
                    label: "Acquisti",
                    data: buyValues,
                    backgroundColor: "#4caf50",
                    borderColor: "#4caf50",
                    borderWidth: 1
                },
                {
                    label: "Vendite",
                    data: sellValues,
                    backgroundColor: "#f44336",
                    borderColor: "#f44336",
                    borderWidth: 1
                }
            ]
        }, 
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context)
                        {
                            return `${context.dataset.label}: ${appInfo.base_currency} ${context.raw.toFixed(2)}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: appInfo.base_currency
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: "Data"
                    }
                }
            }
        }
    });
}

function renderFeesChart(transactions)
{
    const canvas = document.getElementById("transaction-fees-chart");

    if (feesChart)
        feesChart.destroy();

    const feesByDate = {};
    const detailsByDate = {};

    transactions.forEach(transaction =>
    {
        const date = transaction.date;
        const asset = assetsMap[transaction.asset_id];
        const symbol = asset?.symbol ?? "?";
        const fees = Number(transaction.fees || 0);

        feesByDate[date] = (feesByDate[date] || 0) + fees;

        if (!detailsByDate[date])
            detailsByDate[date] = [];

        detailsByDate[date].push({symbol, fees});
    });

    const labels = Object.keys(feesByDate).sort();
    const values = labels.map(date => feesByDate[date]);

    feesChart = new Chart(canvas, {
        type: feesChartType,
        data: {
            labels,
            datasets: [{
                label: "Commissioni",
                data: values,
                backgroundColor: "#ff9800",
                borderColor: "#ff9800",
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context)
                        {
                            return `${appInfo.base_currency} ${context.raw.toFixed(2)}`;
                        },
                        afterLabel: function(context)
                        {
                            const date = context.label;

                            return detailsByDate[date].map(detail =>
                                `${detail.symbol} - ${appInfo.base_currency} ${detail.fees.toFixed(2)}`
                            );
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: appInfo.base_currency
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: "Data"
                    }
                }
            }
        }
    });
}

/* ==========================================================
 * EDIT MODAL
 * ========================================================== */

function openEditModal()
{
    document
        .getElementById("edit-modal")
        .classList.remove("hidden");
}

function closeEditModal()
{
    document
        .getElementById("edit-modal")
        .classList.add("hidden");
}

function populateEditModal(transaction)
{
    const asset = assetsMap[transaction.asset_id];

    document.getElementById("edit-transaction-id").value =
        transaction.id;

    document.getElementById("edit-asset-id").value =
        transaction.asset_id;

    document.getElementById("edit-symbol").value =
        asset ? asset.symbol : transaction.asset_id;

    document.getElementById("edit-operation-type").value =
        transaction.type;

    document.getElementById("edit-quantity").value =
        transaction.quantity;

    document.getElementById("edit-price").value =
        transaction.price;

    document.getElementById("edit-fees").value =
        transaction.fees;

    document.getElementById("edit-transaction-date").value =
        transaction.date;
}

async function handleEdit(event)
{
    const transactionId = event.currentTarget.dataset.id;

    try
    {
        const transaction =
            await getTransaction(transactionId);

        populateEditModal(transaction);

        openEditModal();
    }
    catch(error)
    {
        console.error(error);
        alert("Errore caricamento transazione");
    }
}

async function handleEditSubmit(event)
{
    event.preventDefault();

    const transactionId =
        document.getElementById("edit-transaction-id").value;

    const payload =
    {
        asset_id: parseInt(
            document.getElementById("edit-asset-id").value
        ),

        operation_type:
            document.getElementById("edit-operation-type").value,

        quantity: parseFloat(
            document.getElementById("edit-quantity").value
        ),

        price: parseFloat(
            document.getElementById("edit-price").value
        ),

        fees: parseFloat(
            document.getElementById("edit-fees").value
        ),

        transaction_date:
            document.getElementById("edit-transaction-date").value
    };

    try
    {
        await updateTransaction(
            transactionId,
            payload
        );

        closeEditModal();

        await refreshTransactions();
    }
    catch(error)
    {
        console.error(error);
        alert("Errore modifica transazione");
    }
}

/* ==========================================================
 * DELETE ACTIONS
 * ========================================================== */

async function handleDelete(event)
{
    const transactionId =
        event.currentTarget.dataset.id;

    if (!confirm(
        `Eliminare la transazione ${transactionId}?`
    ))
    {
        return;
    }

    try
    {
        await deleteTransaction(transactionId);

        await refreshTransactions();
    }
    catch(error)
    {
        console.error(error);
        alert("Errore eliminazione transazione");
    }
}

/* ==========================================================
 * PAGE REFRESH
 * ========================================================== */
 
async function refreshTransactions()
{
    const filters = getQueryParams();
	const [map, data ] = await Promise.all([
        loadAssetsMap(),
        loadTransactions(filters)
    ]);

    assetsMap = map;
	if (allTransactions.length == 0)
		allTransactions = data;
	filteredTransactions = data;
	refreshTableTransactions(pageSize);	
	renderValueChart(filteredTransactions);
	renderBuySellChart(filteredTransactions);
	renderFeesChart(filteredTransactions);
}

function refreshTableTransactions(page_size) 
{ 
	pageSize = page_size;
	updateTable(
		renderTransactions, 
		filteredTransactions, 
		"transactions-pagination", 
		currentPage, 
		pageSize
	); 
}

/* ==========================================================
 * FILTERS
 * ========================================================== */

async function handleFilters()
{
    const filters = {};

    const symbol = document.getElementById("filter-symbol").value.trim().toUpperCase();
    const startDate = document.getElementById("filter-start-date").value;
    const endDate = document.getElementById("filter-end-date").value;

    if (symbol)
    {
        const asset = Object.values(assetsMap).find(asset => asset.symbol === symbol);

        if (asset)
            filters.asset_id = asset.id;
    }

    if (startDate)
        filters.start_date = startDate;

    if (endDate)
        filters.end_date = endDate;

    const params = new URLSearchParams(filters);

    //window.history.replaceState({}, "", `transactions.html?${params.toString()}`);
    updateQueryParams(filters);
    await refreshTransactions();
}

async function resetFilters()
{
    document.getElementById("filter-symbol").value = "";
    document.getElementById("filter-start-date").value = "";
    document.getElementById("filter-end-date").value = "";

    await handleFilters();
}

/* ==========================================================
 * TRANSACTION FORM
 * ========================================================== */
 
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
        await refreshTransactions();
		renderDistributionChart(allTransactions);
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


/* ==========================================================
 * INITIALIZATION
 * ========================================================== */
 
async function init()
{
	generateMenu();
	const symbolInput = document.getElementById("symbol");
	symbolInput.addEventListener("blur",handleSymbolBlur);
	symbolInput.addEventListener("input", clearAssetSelection);
	
	initializeTransactionDate();

    try
    {	
		await loadAppInfo();
        await refreshTransactions();
		
		renderCurrencyLabels(appInfo.base_currency); 
		renderDistributionChart(allTransactions);
		renderTransactionDetails(allTransactions);
    }
    catch (error)
    {
        console.error(error);
        alert("Errore caricamento transazioni");
    }
	
	document.getElementById("transaction-form").addEventListener("submit", handleTransaction);
	document.getElementById("edit-transaction-form").addEventListener("submit", handleEditSubmit);
	document.getElementById("close-modal").addEventListener("click", closeEditModal);
	document.getElementById("cancel-edit").addEventListener("click", closeEditModal);
	
	document.getElementById("edit-modal").addEventListener(
		"click",
		event =>
		{
			if (event.target.id === "edit-modal")
			{
				closeEditModal();
			}
		}
	);
	
	document.getElementById("toggle-fees-chart").addEventListener("click", () =>
	{
		feesChartType = feesChartType === "bar" ? "line" : "bar";
		renderFeesChart(filteredTransactions);
	});	
	
	document.getElementById("toggle-buy-sell-chart").addEventListener("click", () =>
	{
		buySellChartType = buySellChartType === "bar" ? "line" : "bar";
		renderBuySellChart(filteredTransactions);
	});
}

document.addEventListener("DOMContentLoaded", init);