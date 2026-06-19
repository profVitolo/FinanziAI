/* ==========================================================
 * STATE
 * ========================================================== */
let assetsMap = {};

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
    const data = await loadTransactions(filters);
	
    renderTransactions(data);
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
	const symbolInput = document.getElementById("symbol");
	symbolInput.addEventListener("blur",handleSymbolBlur);
	symbolInput.addEventListener("input", clearAssetSelection);
	
	initializeTransactionDate();

    try
    {	
		await loadAppInfo();
        assetsMap = await loadAssetsMap();
        await refreshTransactions();
		renderCurrencyLabels(appInfo.base_currency); 
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
}

document.addEventListener("DOMContentLoaded", init);