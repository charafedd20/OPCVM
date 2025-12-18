"""
Portfolio Optimizer Pro - FastAPI Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import optimization, data, health

app = FastAPI(
    title="Portfolio Optimizer Pro API",
    description="Advanced Portfolio Optimization API with Risk Constraints",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(data.router, prefix="/api/v1", tags=["Data"])
app.include_router(optimization.router, prefix="/api/v1", tags=["Optimization"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Portfolio Optimizer Pro API",
        "version": "1.0.0",
        "docs": "/docs"
    }

