"""
Portfolio optimization endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.api.models.optimization import (
    OptimizationRequest,
    OptimizationResponse,
    EfficientFrontierRequest,
    EfficientFrontierResponse
)
from app.api.services.optimization_service import OptimizationService

router = APIRouter()
optimization_service = OptimizationService()


@router.post("/optimize/mean-variance", response_model=OptimizationResponse)
async def optimize_mean_variance(request: OptimizationRequest):
    """
    Optimize portfolio using Mean-Variance optimization (Markowitz)
    """
    try:
        result = await optimization_service.optimize_mean_variance(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize/cvar", response_model=OptimizationResponse)
async def optimize_cvar(request: OptimizationRequest):
    """
    Optimize portfolio using CVaR (Conditional Value at Risk)
    """
    try:
        result = await optimization_service.optimize_cvar(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize/robust", response_model=OptimizationResponse)
async def optimize_robust(request: OptimizationRequest):
    """
    Optimize portfolio using Robust Optimization
    """
    try:
        result = await optimization_service.optimize_robust(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/efficient-frontier", response_model=EfficientFrontierResponse)
async def get_efficient_frontier(request: EfficientFrontierRequest):
    """
    Calculate efficient frontier for given assets
    """
    try:
        result = await optimization_service.calculate_efficient_frontier(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stress-test")
async def stress_test(request: OptimizationRequest):
    """
    Perform stress testing on optimized portfolio
    """
    try:
        result = await optimization_service.stress_test(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

