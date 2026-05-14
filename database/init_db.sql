CREATE TABLE assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL UNIQUE,
    name TEXT,
    type TEXT,
    currency TEXT,
    exchange TEXT
);

CREATE TABLE prices (
    asset_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume REAL,

    PRIMARY KEY (asset_id, date),
    FOREIGN KEY (asset_id) REFERENCES assets(id)
);

CREATE TABLE indicators (
    asset_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    rsi REAL,
    sma_50 REAL,
    sma_200 REAL,
    volatility REAL,
    trend TEXT,

    PRIMARY KEY (asset_id, date),
    FOREIGN KEY (asset_id) REFERENCES assets(id)
);

-- Sezione Personal DATA --
CREATE TABLE portfolio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    avg_price REAL,
    last_update TEXT,

    FOREIGN KEY (asset_id) REFERENCES assets(id)
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    type TEXT NOT NULL, -- buy / sell
    quantity REAL NOT NULL,
    price REAL NOT NULL,

    FOREIGN KEY (asset_id) REFERENCES assets(id)
);

CREATE TABLE watchlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL UNIQUE,

    FOREIGN KEY (asset_id) REFERENCES assets(id)
);

-- Sezione AInalisys --
CREATE TABLE analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    input_snapshot TEXT,   -- JSON
    output_text TEXT,
    version TEXT           -- rule-based / llm
);

CREATE TABLE market_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    market_trend TEXT,
    volatility_index REAL,
    sentiment TEXT,
    notes TEXT
);

-- =========================
-- ASSETS.TYPE
-- =========================
-- Possibili valori:
-- 'stock'       -- azioni
-- 'etf'         -- ETF
-- 'crypto'      -- criptovalute
-- 'commodity'   -- materie prime (oro, petrolio…)
-- 'forex'       -- valute
-- 'index'       -- indici (S&P500, NASDAQ)
-- 'bond'        -- obbligazioni
-- 'other'       -- fallback


-- =========================
-- ASSETS.CURRENCY
-- =========================
-- NON è un vero enum rigido → usa codici ISO 4217
-- Esempi:
-- 'USD'
-- 'EUR'
-- 'GBP'
-- 'JPY'
-- 'CHF'
-- 'BTC'   -- per crypto
-- 'ETH'


-- =========================
-- ASSETS.EXCHANGE
-- =========================
-- Esempi:
-- 'NYSE'
-- 'NASDAQ'
-- 'XETRA'
-- 'BIT'        -- Borsa Italiana
-- 'CRYPTO'     -- exchange crypto generico
-- 'BINANCE'
-- 'COINBASE'
-- 'FOREX'
-- 'OTHER'


-- =========================
-- INDICATORS.TREND
-- =========================
-- 'bullish'
-- 'bearish'
-- 'neutral'


-- =========================
-- TRANSACTIONS.TYPE
-- =========================
-- 'buy'
-- 'sell'


-- =========================
-- ANALYSIS.VERSION
-- =========================
-- 'rule_based'   -- logica semplice
-- 'ml'           -- modelli Python
-- 'llm'          -- LLM (locale o API)
-- 'hybrid'       -- combinazione


-- =========================
-- MARKET_SUMMARY.MARKET_TREND
-- =========================
-- 'bullish'
-- 'bearish'
-- 'neutral'
-- 'sideways'     -- mercato laterale


-- =========================
-- MARKET_SUMMARY.SENTIMENT
-- =========================
-- 'fear'
-- 'greed'
-- 'neutral'
-- 'optimistic'
-- 'pessimistic'
-- 'uncertain'