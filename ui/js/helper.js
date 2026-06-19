const API_BASE = "http://127.0.0.1:8000";
let appInfo = null;

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

