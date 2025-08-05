"""
AssetFraction Backend - Main FastAPI Application
RWA Tokenization and Income Distribution on Hedera
"""

import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from api.routes import wallet, kyc, assets, rewards, mirror
from database.database import engine, Base
from services.scheduler import scheduler
from utils.config import settings

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    print("🚀 Starting AssetFraction Backend...")
    scheduler.start()
    print("📅 Scheduler started")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down AssetFraction Backend...")
    scheduler.shutdown()
    print("📅 Scheduler stopped")


# Initialize FastAPI app
app = FastAPI(
    title="AssetFraction Backend",
    description="RWA Tokenization and Income Distribution on Hedera",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
if not os.path.exists("uploads"):
    os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(wallet.router, prefix="/api/v1/wallet", tags=["Wallet"])
app.include_router(kyc.router, prefix="/api/v1/kyc", tags=["KYC"])
app.include_router(assets.router, prefix="/api/v1/assets", tags=["Assets"])
app.include_router(rewards.router, prefix="/api/v1/rewards", tags=["Rewards"])
app.include_router(mirror.router, prefix="/api/v1/mirror", tags=["Mirror Node"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🏠 AssetFraction Backend API",
        "version": "1.0.0",
        "description": "Democratizing Real World Asset Ownership via Hedera",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "scheduler": "running" if scheduler.running else "stopped"
    }


def main():
    """Main entry point"""
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )


if __name__ == "__main__":
    main()
