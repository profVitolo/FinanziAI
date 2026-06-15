const API_BASE = "http://127.0.0.1:8000";

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

function getFiltersFromQueryString()
{
    const params = new URLSearchParams(window.location.search);

    return {
        asset_id: params.get("asset_id"),
        start_date: params.get("start_date"),
        end_date: params.get("end_date")
    };
}