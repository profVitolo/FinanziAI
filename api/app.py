from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.routes.assets import router as assets_router
from api.routes.portfolio import router as portfolio_router
from api.routes.watchlist import router as watchlist_router
from api.routes.info import router as info_router
from api.routes.transactions import router as transaction_router
from api.routes.exchange import router as exchange_router
from api.routes.evaluation import router as evaluation_router

from config import TITLE, DESCRIPTION, VERSION

app = FastAPI(
    title=TITLE,
    description=DESCRIPTION,
    version=VERSION
)

app.include_router(assets_router)
app.include_router(portfolio_router)
app.include_router(watchlist_router)
app.include_router(info_router)
app.include_router(transaction_router)
app.include_router(exchange_router)
app.include_router(evaluation_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/", StaticFiles(directory="ui", html=True), name="ui")

"""
@app.get("/")
def root():
    return {
        "application": "FinanziAI",
        "status": "running"
    }
"""