from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import bi_routes, workflow_routes
from app.config.settings import settings

app = FastAPI(
    title="AI Business Intelligence Platform",
    description="An agentic AI platform for business intelligence powered by AutoGEN, LiteLLM, and Ollama",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(bi_routes.router, prefix=f"{settings.API_V1_STR}/bi", tags=["business-intelligence"])
app.include_router(workflow_routes.router, prefix=f"{settings.API_V1_STR}/workflow", tags=["workflow"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to AI Business Intelligence Platform",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    } 