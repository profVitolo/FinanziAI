let assetsMap = {};

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

            <td>${transaction.quantity}</td>

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
    document.querySelectorAll("button.delete").forEach(
		button =>
        {
            button.addEventListener("click", handleDelete);
        });

    document.querySelectorAll("button.edit").forEach(
		button =>
        {
            button.addEventListener("click", handleEdit);
        });
}

async function handleDelete(event)
{
    const transactionId = event.target.dataset.id;

    if (!confirm(`Eliminare la transazione ${transactionId}?`))
        return;

    try
    {
        await deleteTransaction(transactionId);
        await refreshTransactions();
    }
    catch (error)
    {
        console.error(error);
        alert("Errore eliminazione transazione");
    }
}

async function handleEdit(event)
{
    const transactionId = event.target.dataset.id;

    try
    {
        const response = await fetch(`${API_BASE}/transactions/${transactionId}`);

        if (!response.ok)
            throw new Error();

        const transaction = await response.json();

        const quantity = prompt("Quantità", transaction.quantity);

        if (quantity === null)
            return;

        const price = prompt("Prezzo", transaction.price);

        if (price === null)
            return;

        const fees = prompt("Commissioni", transaction.fees);

        if (fees === null)
            return;

        await updateTransaction(
            transactionId,
            {
                asset_id: transaction.asset_id,
                operation_type: transaction.type,
                quantity: parseFloat(quantity),
                price: parseFloat(price),
                fees: parseFloat(fees),
                transaction_date: transaction.date
            }
        );

        await refreshTransactions();
    }
    catch (error)
    {
        console.error(error);
        alert("Errore modifica transazione");
    }
}

async function refreshTransactions()
{
    const filters = getFiltersFromQueryString();
    const transactions = await loadTransactions(filters);
	
    renderTransactions(transactions);
}

async function init()
{
	const symbolInput = document.getElementById("symbol");
	symbolInput.addEventListener("blur",handleSymbolBlur);
	symbolInput.addEventListener("input", clearAssetSelection);
	
	initializeTransactionDate();

	
    try
    {
        assetsMap = await loadAssetsMap();
        await refreshTransactions();
    }
    catch (error)
    {
        console.error(error);
        alert("Errore caricamento transazioni");
    }
	
	document.getElementById("filter-form").addEventListener("submit", handleFilters);
	document.getElementById("reset-filters").addEventListener("click", handleResetFilters);
	document.getElementById("transaction-form").addEventListener("submit", handleTransaction);
}

function buildFiltersFromForm()
{
    const filters = {};

    const symbol = document.getElementById("filter-symbol").value.trim();
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

    return filters;
}

async function handleFilters(event)
{
    event.preventDefault();

    const filters = buildFiltersFromForm();

    const params = new URLSearchParams(filters);

    window.history.replaceState(
        {},
        "",
        `transactions.html?${params.toString()}`
    );

    await refreshTransactions();
}

async function handleResetFilters()
{
    window.history.replaceState(
        {},
        "",
        "transactions.html"
    );

    document.getElementById("filter-form").reset();

    await refreshTransactions();
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


document.addEventListener("DOMContentLoaded", init);