const API_BASE = "http://127.0.0.1:8000";
let appInfo = null;

const menuItems = {
	homepage: {
		icon: "🏠",
		url: "index.html",
		title: "Dashboard"
	},
	portfolio: {
		icon: "💼",
		url: "portfolio.html",
		title: "Portafoglio"
	},
	transactions: {
		icon: "💱",
		url: "transactions.html",
		title: "Transazioni"
	},
	assets: {
		icon: "📈",
		url: "assets.html",
		title: "Asset"
	},
	exchange: {
		icon: "💵",
		url: "exchange.html",
		title: "Cambi Valutari"
	}
};

async function loadAssetsMap()
{
    const response = await fetch(`${API_BASE}/assets/`);

    if (!response.ok)
        throw new Error("Errore caricamento asset");

    const assets = await response.json();

    const assetsMap = {};

    for (const asset of assets)
    {
        assetsMap[asset.id] = asset;
    }

    return assetsMap;
}

function getQueryParams()
{
    const params = new URLSearchParams(window.location.search);
    const result = {};

    for (const [key, value] of params.entries())
        result[key] = value;

    return result;
}

function updateQueryParams(params)
{
    const searchParams = new URLSearchParams();

    for (const [key, value] of Object.entries(params))
    {
        if (value !== null && value !== undefined && value !== "")
            searchParams.set(key, value);
    }

    window.history.replaceState({}, "", `${window.location.pathname}?${searchParams.toString()}`);
}

async function loadAppInfo()
{
    if (appInfo)
        return appInfo;

    const response = await fetch(`${API_BASE}/info`);

    if (!response.ok)
        throw new Error("Errore caricamento configurazione");

    appInfo = await response.json();

    return appInfo;
}

function generateMenu() {
    const container = document.querySelector(".nav-links");
    const pageTitle = document.querySelector("#page-title");

    if (!container)
        return;

    const currentPage = window.location.pathname.split("/").pop();

    let linksHtml = "";

    for (const item of Object.values(menuItems)) 
	{
        const active = currentPage === item.url ? "active" : "";

        if (active && pageTitle) 
            pageTitle.textContent = item.title;

        linksHtml += `
            <a href="${item.url}" class="${active}">
                <span>${item.icon}</span>
                <span>${item.title}</span>
            </a>
        `;
    }

    container.innerHTML = `
        <nav class="nav-menu">
            <button class="menu-toggle" type="button">☰</button>

            <div class="menu-items">
                ${linksHtml}
            </div>
        </nav>
    `;

    const mn_btn = container.querySelector(".menu-toggle")
    mn_btn.addEventListener("click", () => { container.querySelector(".nav-menu").classList.toggle("open");});
}