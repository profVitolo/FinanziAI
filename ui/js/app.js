let portfolioLoadingError = null;

async function loadWatchlist() 
{
    try 
	{
        const response = await fetch(`${API_BASE}/watchlist`);
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
    const statusElement = document.getElementById("api-status");

    try
    {
        await loadAppInfo();
        statusElement.textContent =  `${appInfo.application} v${appInfo.version}`;
    }
    catch
    {
		const msg = "Server non raggiungibile";
        statusElement.textContent = msg;
		console.error(msg);
    }
}

async function loadPortfolioEvaluation()
{
	if( portfolioLoadingError == null)
	{
		try
		{
			const response = await fetch(`${API_BASE}/evaluation/portfolio`);

			if (!response.ok)
				throw new Error();

			const evaluation = await response.json();

			document.getElementById("dashboard-evaluation-count").innerHTML = `
				<a href="portfolio.html">${evaluation.summary.message_count}</a>`;
				
			document.getElementById("dashboard-evaluation-severity").innerHTML = `
				<span class="${severityClass(evaluation.summary.highest_severity)}">
					${severityIcon(evaluation.summary.highest_severity)}
					${evaluation.summary.highest_severity}
				</span>
			`;
		}
		catch
		{
			document.getElementById("dashboard-evaluation-severity").textContent = "-";
			document.getElementById("dashboard-evaluation-count").textContent = "-";
		}
	}
}

async function loadPortfolioSummary()
{
	let response;
    try
    {
        response = await fetch(`${API_BASE}/portfolio/analysis`);
		portfolioLoadingError = null;
		
		if (response.status === 404)
		{
			const portfolioAnalysis = await response.json();
			portfolioLoadingError = {status: response.status, detail: portfolioAnalysis.detail};
			throw new Error();
		}
		
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
		portfolioLoadingError = {status: response.status, detail: "Errore generico caricamento portfolio" };
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
	try
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
	catch(e)
	{
		console.error(e.message);
	}
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
			try
			{
				if (!confirm(`Passare al vault ${dbName}?`))
				{
					await loadVaults();
					return;
				}

				await selectVault(dbName);
				alert(`Vault attivo: ${dbName}`);
				location.reload();
			}
			catch (error) { console.error("Vault change error:", error);}
        }
	);

    document.getElementById("new-vault-btn").addEventListener("click", createVault);
    document.getElementById("delete-vault-btn").addEventListener("click", deleteVault);
}

//AI Functions
function renderHistory(history)
{
    const container = document.getElementById("advisor-history");
    container.innerHTML = "";

    history.turns.forEach(turn =>
    {
        const user = document.createElement("div");
        user.className = "advisor-user";
        user.textContent = turn.user_message;

        const assistant = document.createElement("div");
        assistant.className = "advisor-assistant";
        assistant.textContent = turn.assistant_message;

        container.appendChild(user);
        container.appendChild(assistant);
    });

    container.scrollTop = container.scrollHeight;
}

async function loadAdvisorHistory()
{
	if( portfolioLoadingError == null)
	{
		try
		{
			const response = await fetch(`${API_BASE}/advisor/history`);
			if (!response.ok)
				throw new Error();

			const history = await response.json();
			renderHistory(history);
		}
		catch (error)
		{
			console.error("Errore caricamento history advisor:", error);
		}
	}
}

async function sendAdvisorMessage()
{
    const textarea = document.getElementById("advisor-prompt");
	const button = document.getElementById("advisor-send-btn");
    const prompt = textarea.value.trim();
	const profileSelect = document.getElementById("investor-profile");
	
    if (!prompt)
        return;

	button.disabled = true;
    textarea.disabled = true;
	const selectedProfile = profileSelect ? profileSelect.value : "balanced";
	
    try
    {
        const response = await fetch(
            `${API_BASE}/advisor/advise`,
            {
                method: "POST",
                headers:
                {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(
                {
                    prompt: prompt,
                    investor_profile: selectedProfile
                })
            });

        if (!response.ok)
        {
            const error = await response.json();
            alert(error.detail);
            return;
        }

        textarea.value = "";

        await loadAdvisorHistory();
    }
    catch (error)
    {
        console.error("Errore advisor:", error);
    }
	finally
    {
        button.disabled = false;
        textarea.disabled = false;
        textarea.focus();
    }
}

function resetAdvisorInput()
{
    document.getElementById("advisor-prompt").value = "";
}

function setupAdvisor()
{
    document.getElementById("advisor-send-btn").addEventListener("click", sendAdvisorMessage);
    document.getElementById("advisor-reset-btn").addEventListener("click", resetAdvisorInput);

}

async function loadInvestorProfiles() 
{
    const selectElement = document.getElementById('investor-profile');

    try 
	{
        const response = await fetch('/advisor/investor-profiles');
        
        if (!response.ok) 
            throw new Error(`Errore HTTP: ${response.status}`);

        const profiles = await response.json();
        
        selectElement.innerHTML = '';

        profiles.forEach(profile => 
		{
            const option = document.createElement('option');
            option.value = profile.value;
            option.textContent = profile.label;
            selectElement.appendChild(option);
        });

    } 
	catch (error) 
	{
        console.error('Impossibile caricare i profili investitore:', error);
    }
}

async function init() 
{
    generateMenu();

	await checkHealth();
	await Promise.all([
		syncTrackedAssets(),
		loadInvestorProfiles(),
		loadPortfolioSummary()
	]);
	await Promise.all([
		loadPortfolioEvaluation(),
		loadWatchlist(),
		loadVaults(),
		loadAdvisorHistory()
	]);
	
	setupVaultSelector();
	setupAdvisor();
	
	setupSearch();
}


document.addEventListener("DOMContentLoaded",init);