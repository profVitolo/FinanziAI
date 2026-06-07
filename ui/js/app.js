const API_BASE = "http://127.0.0.1:8000";

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
            const symbol = document.getElementById("symbol").value.trim().toUpperCase();

            if (!symbol) return;

            window.location.href = `asset.html?symbol=${symbol}`;
        }
    );

}

document.addEventListener("DOMContentLoaded",() => { loadWatchlist(); setupSearch(); });