
async function loadWatchlist() 
{
    try 
	{
        const response = await fetch(`${API_BASE}/watchlist/`);
        const data = await response.json();
        const list = document.getElementById("watchlist");

        list.innerHTML = "";

        data.forEach(
			asset => 
			{
				const li = document.createElement("li");
				li.innerHTML = `
					<a href="asset.html?symbol=${asset.symbol}">
						${asset.symbol}
					</a>
				`;
				list.appendChild(li);
			}
		);

    } 
	catch (error) 
	{
        console.error("Errore caricamento watchlist:", error);
    }
}

function setupSearch()
{
    const form = document.getElementById("search-form");

    form.addEventListener(
        "submit",
        event => 
		{
            event.preventDefault();
            const symbol = document.getElementById("symbol-input").value.trim().toUpperCase();

            if (!symbol) return;

            window.location.href = `asset.html?symbol=${symbol}`;
        }
    );

}

async function checkHealth()
{
    const statusElement =
        document.getElementById("api-status");

    try
    {
        await loadAppInfo();
        statusElement.textContent =  `${appInfo.application} v${appInfo.version}`;
    }
    catch
    {
        statusElement.textContent = "Server non raggiungibile";
    }
}

async function loadPortfolioSummary()
{
    try
    {
        const response = await fetch(`${API_BASE}/portfolio/analysis`);

        if (!response.ok)
            throw new Error();

        const data = await response.json();

        document.getElementById("portfolio-value").textContent = appInfo.base_currency ?? "";
        document.getElementById("portfolio-value").textContent += appInfo.base_currency ? " " : "";
        document.getElementById("portfolio-value").textContent += data.portfolio_value.toFixed(2) ?? "-";

        document.getElementById("positions-count").textContent = data.positions?.length ?? 0;
    }
    catch
    {
        document.getElementById("portfolio-value").textContent = "-";
        document.getElementById("positions-count").textContent = "-";
    }
}

async function syncTrackedAssets()
{
    try
    {
        const response = await fetch(`${API_BASE}/assets/sync-tracked`,{method: "PUT"});

        if (!response.ok)
            throw new Error();

        const data = await response.json();

        //console.log("Tracked assets sincronizzati:", data);
    }
    catch (error)
    {
        console.error("Errore sincronizzazione asset tracciati:", error);
    }
}

async function loadVaults()
{
    const response = await fetch(`${API_BASE}/info/databases`);

    if (!response.ok)
        throw new Error("Errore caricamento vault");

    const data = await response.json();

    const select = document.getElementById("databases");
    select.innerHTML = "";

    data.databases.forEach(db =>
    {
        const option = document.createElement("option");
        option.value = db;
        option.textContent = db;

        if (db === data.selected)
            option.selected = true;

        select.appendChild(option);
    });
}

async function createVault()
{
    const dbName = prompt("Nome del nuovo vault");

    if (!dbName)
        return;

    const response = await fetch(
        `${API_BASE}/info/database/create`,
        {
            method: "POST",
            headers:
            {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                db_name: dbName
            })
        }
    );

    if (!response.ok)
        throw new Error("Errore creazione vault");
	
	await selectVault(dbName);
	location.reload();
}

async function deleteVault()
{
    const select = document.getElementById("databases");

    if (select.options.length <= 1)
    {
        alert("Impossibile eliminare l'ultimo vault");
        return;
    }

    const currentIndex = select.selectedIndex;
    const dbName = select.value;

    let nextIndex = currentIndex > 0 ? currentIndex - 1 : 1;
    const nextVault = select.options[nextIndex].value;
	
	if (!confirm(`Eliminare ${dbName}?\n\nVerrà selezionato automaticamente ${nextVault}.`))
		return;

    await selectVault(nextVault);
    const response = await fetch(`${API_BASE}/info/database/${dbName}`,{method: "DELETE"});

    if (!response.ok)
    {
        const error = await response.json();
        throw new Error(error.detail);
    }

    location.reload();
}

async function selectVault(dbName)
{
    const response = await fetch(
        `${API_BASE}/info/database/select`,
        {
            method: "POST",
            headers:
            {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                db_name: dbName
            })
        }
    );

    if (!response.ok)
        throw new Error("Errore selezione vault");

    return await response.json();
}

function setupVaultSelector()
{
    document.getElementById("databases").addEventListener(
		"change", 
		async function()
        {
            const dbName = this.value;

            if (!confirm(`Passare al vault ${dbName}?`))
            {
                await loadVaults();
                return;
            }

            await selectVault(dbName);
            alert(`Vault attivo: ${dbName}`);
            location.reload();
        });

    document.getElementById("new-vault-btn").addEventListener("click", createVault);
    document.getElementById("delete-vault-btn").addEventListener("click", deleteVault);
}

async function init() 
{
    generateMenu();

    try 
	{
        await checkHealth();
        await Promise.all([
			syncTrackedAssets(),
			loadPortfolioSummary(),
			loadWatchlist(),
			loadVaults()
		]);
		
		setupVaultSelector();
    } catch (error) {
        console.error("Init failed:", error);
    }
	
	setupSearch();
}


document.addEventListener("DOMContentLoaded",init);