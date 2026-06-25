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
		icon: "📊",
		url: "assets.html",
		title: "Archivio Asset"
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

function paginate(data, page = 1, pageSize = 10)
{
    const start = (page - 1) * pageSize;
    const end = start + pageSize;

    return {
        items: data.slice(start, end),
        totalPages: Math.ceil(data.length / pageSize),
        currentPage: page
    };
}

function renderPagination(containerId, currentPage, totalPages, onPageChange)
{
    const container = document.getElementById(containerId);

    if (!container)
        return;

    let html = "";

    function addPage(page)
    {
        html += `
            <button
                class="${page === currentPage ? "active" : ""}"
                data-page="${page}">
                ${page}
            </button>
        `;
    }

    if (currentPage > 1)
        html += `<button data-page="${currentPage - 1}">←</button>`;

    const pages = new Set();

    pages.add(1);

    for (let i = currentPage - 2; i <= currentPage + 2; i++)
    {
        if (i > 1 && i < totalPages)
            pages.add(i);
    }

    if (totalPages > 1)
        pages.add(totalPages);

    const sortedPages = [...pages].sort((a, b) => a - b);

    let previous = null;

    for (const page of sortedPages)
    {
        if (previous !== null && page - previous > 1)
            html += `<span class="ellipsis">...</span>`;

        addPage(page);
        previous = page;
    }

    if (currentPage < totalPages)
        html += `<button data-page="${currentPage + 1}">→</button>`;

    container.innerHTML = html;

    container.querySelectorAll("button[data-page]").forEach(button =>
    {
        button.addEventListener("click", () =>
        {
            onPageChange(Number(button.dataset.page));
        });
    });
}

function updateTable(renderFunc, items, paginationId, currentPage, pageSize)
{
    const page = paginate(
        items,
        currentPage,
        pageSize
    );

    renderFunc(page.items);

    renderPagination(
        paginationId,
        page.currentPage,
        page.totalPages,
        newPage =>
        {
            currentPage = newPage;
            updateTable(renderFunc, items, paginationId, currentPage, pageSize);
        }
    );
}

function getSetting(key, defaultValue)
{
    const value = localStorage.getItem(key);

    if (value === null)
        return defaultValue;

    return JSON.parse(value);
}

function setSetting(key, value)
{
    localStorage.setItem(key, JSON.stringify(value));
}

function setupPageSize(inputId, storageKey, defaultPageSize, onPageSizeChanged)
{
    let pageSize = Number(localStorage.getItem(storageKey)) || defaultPageSize;
		//console.log(localStorage.getItem(storageKey)) ;
    setSetting(storageKey, pageSize);

    const input = document.getElementById(inputId);
    input.value = pageSize;

    input.addEventListener("change", function()
    {
        const value = Number(this.value);

        if (value < 1)
        {
            this.value = pageSize;
            return;
        }

        pageSize = value;

        setSetting(storageKey, pageSize);

        if (onPageSizeChanged)
            onPageSizeChanged(pageSize);
    });

    return pageSize;
}

function generateMenu() 
{
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

function formatFinancialNumber(value)
{
    if (!value) return "-";

    if (value >= 1_000_000_000_000)
        return (value / 1_000_000_000_000).toFixed(2) + " T";

    if (value >= 1_000_000_000)
        return (value / 1_000_000_000).toFixed(2) + " B";

    if (value >= 1_000_000)
        return (value / 1_000_000).toFixed(2) + " M";

    return value.toLocaleString();
}