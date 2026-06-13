const API_BASE = "http://127.0.0.1:8000";

async function loadWatchlist() 
{
    try 
	{
        const response = await fetch(`${API_BASE}/portfolio/watchlist`);
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
        const response = await fetch(`${API_BASE}/info`);

        if (!response.ok)
            throw new Error();

        const data = await response.json();
        statusElement.textContent = `${data.application} v${data.version}`;
    }
    catch
    {
        statusElement.textContent = "Server non raggiungibile";
    }
}

document.addEventListener("DOMContentLoaded",() => {  checkHealth(); loadWatchlist(); setupSearch(); });