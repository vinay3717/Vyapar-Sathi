from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lifespan startup: initialize connections and graph state
    print(f"Starting Vyapar Sarthi backend in {settings.ENVIRONMENT} mode...")
    app.state.graph = None
    yield
    # Lifespan shutdown
    print("Shutting down Vyapar Sarthi backend...")


app = FastAPI(
    title="Vyapar Sarthi API",
    description="Autonomous AI Teammate for Paytm Merchants",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware for Next.js frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
