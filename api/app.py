from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.routes.assets import router as assets_router
from api.routes.analysis import router as analysis_router
from api.routes.portfolio import router as portfolio_router
from api.routes.info import router as info_router
from api.routes.transaction import router as transaction_router

app = FastAPI(
    title="FinanziAI",
    description="AI-Assisted Investment Analysis",
    version="0.1.0"
)

app.include_router(assets_router)
app.include_router(analysis_router)
app.include_router(portfolio_router)
app.include_router(info_router)
app.include_router(transaction_router)

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