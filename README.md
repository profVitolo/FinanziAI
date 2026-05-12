# 📈 FinanziAI App (AI-Assisted)

## 🧠 Descrizione
Questa applicazione è uno strumento locale per supportare decisioni di investimento.
L’obiettivo NON è automatizzare il trading, ma:
- analizzare dati di mercato
- monitorare il portafoglio
- generare suggerimenti intelligenti
- fornire spiegazioni chiare e comprensibili

Tutte le decisioni operative (acquisto/vendita) restano all’utente.

---

## 🏗️ Architettura
L’applicazione è strutturata in **componenti modulari indipendenti**, senza server e senza database remoto.

### Componenti principali:
1. **Database**
- Gestione dati locale tramite SQLite (file unico `.db`)
- Persistenza di prezzi, indicatori e portafoglio

2. **Data Collector**
- Scarica dati finanziari (es. Yahoo Finance)
- Salva i dati nel database

3. **Data Engine**
- Calcola indicatori finanziari:
  - RSI
  - trend
  - volatilità
- Analizza il portafoglio

4. **Advisor**
- Genera suggerimenti basati su:
- regole logiche (fase iniziale)
- modelli AI/LLM (fase avanzata)
- Produce output testuale comprensibile

5. **UI (Frontend)**
- Interfaccia HTML/JavaScript
- Visualizzazione dati e suggerimenti

---

## 📁 Struttura del progetto
```
FinanziAI/
│
├── main.py
├── config.py
│
├── database/
│ ├── db.py
│ ├── schema.py
│ └── repository.py
│
├── data_collector/
│ └── yahoo_collector.py
│
├── data_engine/
│ ├── indicators.py
│ ├── market_analysis.py
│ └── portfolio_analysis.py
│
├── advisor/
│ ├── rules_engine.py
│ ├── llm_engine.py
│ └── explanation.py
│
├── ui/
│ ├── index.html
│ ├── app.js
│ └── style.css
│
└── utils/
└── helpers.py
```

---

## ⚙️ Tecnologie utilizzate

### Backend
- Python 3
- sqlite3 (database embedded)
- pandas / numpy (analisi dati)
- yfinance (download dati finanziari)

### AI / Analisi
- Rule-based engine (fase iniziale)
- LLM locali o API (fase futura)

### Frontend
- HTML5
- JavaScript
- CSS

---

## 🔄 Flusso applicativo
```
Yahoo Finance
↓
Data Collector
↓
SQLite (database locale)
↓
Data Engine (indicatori)
↓
Advisor (logica / AI)
↓
Output testuale
↓
Interfaccia utente (HTML/JS)
```

---

## ⚠️ Note importanti
- L'app NON esegue operazioni di trading
- NON è un consulente finanziario
- Fornisce solo supporto decisionale
- Tutte le scelte sono responsabilità dell’utente

---

## 🚀 Roadmap

### Fase 1
- Database SQLite
- Download dati
- Indicatori base
- Regole semplici

### Fase 2
- Analisi portafoglio avanzata
- Miglioramento output testuale

### Fase 3
- Integrazione LLM
- Suggerimenti più sofisticati

### Fase 4
- Ottimizzazione strategie
- Simulazioni / backtesting

---

## 🎯 Obiettivo finale

Costruire un sistema modulare, locale e controllabile che:
- unisce analisi quantitativa e AI
- resta trasparente nelle decisioni
- supporta (ma non sostituisce) l’investitore
