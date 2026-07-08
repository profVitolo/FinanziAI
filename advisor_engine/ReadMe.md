# AdvisorEngine

## Descrizione
L'AdvisorEngine rappresenta il livello più alto dell'architettura di FinanziAI.
Il suo compito **non è eseguire analisi finanziarie**, ma trasformare le informazioni già prodotte dal sistema in una consulenza comprensibile e contestualizzata.

L'AdvisorEngine utilizza esclusivamente:
- `DataEngine`
- `EvaluationEngine`
- un LLM locale tramite `llama-cpp-python`

L'LLM non rappresenta la fonte della verità del sistema. Tutte le informazioni numeriche, gli indicatori, le valutazioni e i dati di mercato sono prodotti dai moduli deterministici (DataEngine ed EvaluationEngine). Il modello linguistico ha esclusivamente il compito di interpretare tali informazioni e comunicarle in linguaggio naturale.

Riceve esclusivamente dati già elaborati e produce:
- spiegazioni
- suggerimenti
- motivazioni
- confronto con la watchlist
- risposta alle domande dell'utente

---

# Architettura
```text
advisor_engine/
│
├── advisor_engine.py          # Facade principale
├── advisor_context_builder.py # Raccolta dati da DataEngine/EvaluationEngine
├── prompt_builder.py          # Costruzione automatica del prompt
├── llama_provider.py          # Wrapper llama-cpp-python
├── advisor_models.py          # DTO interni
│
├── prompts/
│   ├── system_prompt.txt
│   └── user_prompt.txt
│
└── models/
    └── model.gguf
```

---

# Componenti

## AdvisorEngine

### Responsabilità
È la facade dell'intero modulo.
Orchestra tutte le operazioni necessarie per ottenere una consulenza.
Non contiene logica di costruzione del prompt né di accesso al modello.

### Input
- richiesta dell'utente
- profilo investitore

### Output
- risposta dell'Advisor

### Possibile interfaccia
```python
class AdvisorEngine:

    def advise(
        self,
        user_prompt: str,
        investor_profile: InvestorProfile
    ) -> AdvisorResponse:
        ...
```

---

## AdvisorContextBuilder

### Responsabilità
Recupera tutte le informazioni necessarie dagli engine esistenti.

Utilizza:
- DataEngine
- EvaluationEngine

Costruisce un unico oggetto contenente tutto il contesto necessario.

### Recupera
- Portfolio
- Asset
- Valutazioni del portafoglio
- Valutazioni degli asset
- Watchlist
- Informazioni applicative
- Profilo investitore

### Input
```python
InvestorProfile
```

### Output
```python
AdvisorContext
```

### Possibile interfaccia
```python
class AdvisorContextBuilder:

    def build(
        self,
        profile: InvestorProfile
    ) -> AdvisorContext:
        ...
```

---

## PromptBuilder

### Responsabilità
Trasforma l'intero contesto in un prompt ottimizzato per il modello.
Internamente utilizza un ```PromptFormatter``` per convertire i DTO dell'applicazione in una rappresentazione testuale semplice e compatta, eliminando dettagli implementativi inutili e riducendo il numero di token.
Successivamente inserisce il contesto formattato nei template Jinja e costruisce il prompt finale.
Non dialoga con il modello.

### Input
```python
AdvisorContext
user_prompt
```

### Output
```text
Prompt completo
```

### Possibile interfaccia
```python
class PromptBuilder:

    def build(
        self,
        context: AdvisorContext,
        user_prompt: str
    ) -> Prompt:
        ...
```

---

## LlamaProvider

### Responsabilità
Incapsula completamente `llama-cpp-python`.
Il resto dell'applicazione non conosce il modello utilizzato.
Permette in futuro di sostituire il backend con altri provider.

### Input
Prompt

### Output
Risposta del modello

### Possibile interfaccia

```python
class LlamaProvider:

    def generate(
		*,
		system_prompt: str,
		user_prompt: str,
    ) -> AdvisorResponse:
        ...
```

Internamente utilizza:
```python
from llama_cpp import Llama
```

---

## InvestorProfile

### Responsabilità
Descrive il profilo dell'investitore.
Può essere utilizzato per modificare il comportamento dell'Advisor.

Esempio:
- Prudente
- Bilanciato
- Dinamico
- Aggressivo

### Possibile modello
```python
class InvestorProfile(Enum):

    PRUDENT = "prudent"
    BALANCED = "balanced"
    DYNAMIC = "dynamic"
    AGGRESSIVE = "aggressive"
```

---

## AdvisorModels
Contiene esclusivamente DTO.

Ad esempio:
```text
AdvisorContext

AdvisorRequest

Prompt

AdvisorResponse

InvestorProfile
```

Nessuna logica.

---

# Flusso di esecuzione
```mermaid
flowchart LR

A[Endpoint HTTP]
    --> B[AdvisorEngine]

B --> C[AdvisorContextBuilder]

C --> D[DataEngine]
C --> E[EvaluationEngine]

D --> C
E --> C

C --> F[PromptBuilder]

F --> G[LlamaProvider]

G --> H[LLM Locale<br/>llama.cpp]

H --> G

G --> I[AdvisorResponse]

I --> B

B --> J[HTTP Response]
```

---

# Sequenza delle operazioni
```text
1. L'utente invia una richiesta.

2. L'AdvisorEngine riceve la richiesta.

3. AdvisorContextBuilder recupera:

   • portfolio
   • asset
   • watchlist
   • valutazioni
   • profilo investitore

4. PromptBuilder costruisce il prompt.

5. LlamaProvider invia il prompt al modello locale.

6. Il modello produce una risposta.

7. L'AdvisorEngine restituisce la risposta all'utente.
```

---

# Filosofia dell'architettura
Ogni componente ha una singola responsabilità.

| Componente | Responsabilità |
|------------|----------------|
| DataEngine | Produce dati quantitativi |
| EvaluationEngine | Interpreta i dati con regole deterministiche |
| AdvisorContextBuilder | Recupera e aggrega tutte le informazioni |
| PromptBuilder | Costruisce il prompt per l'LLM |
| LlamaProvider | Comunica con il modello locale |
| AdvisorEngine | Orchestration dell'intero processo |

---

# Vantaggi
- Separazione completa delle responsabilità.
- Il modello AI è completamente isolato.
- Possibilità di sostituire il modello senza modificare il resto del sistema.
- Prompt centralizzato e facilmente migliorabile.
- Architettura facilmente testabile tramite mock.
- Nessuna logica finanziaria delegata al modello.

---

# Roadmap

## Fase 1 — Infrastruttura
- integrazione `llama-cpp-python`
- caricamento del modello locale
- gestione del contesto
- costruzione automatica del prompt

## Fase 2 — Contestualizzazione
- definizione dei profili investitore
- utilizzo delle analisi del DataEngine
- utilizzo delle valutazioni dell'EvaluationEngine
- confronto con la watchlist

## Fase 3 — Consulenza
- suggerimenti motivati
- spiegazione dei rischi
- spiegazione dei benefici
- risposta alle domande dell'utente
- conversazione contestuale
- memoria della sessione (eventuale evoluzione futura)