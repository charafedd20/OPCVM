"""
Optimization models
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class OptimizationMethod(str, Enum):
    """Optimization method types"""
    MEAN_VARIANCE = "mean_variance"
    CVAR = "cvar"
    ROBUST = "robust"


class ConstraintType(str, Enum):
    """Constraint types"""
    BUDGET = "budget"  # Sum of weights = 1
    LONG_ONLY = "long_only"  # Weights >= 0
    MAX_WEIGHT = "max_weight"  # Individual weight limit
    SECTOR = "sector"  # Sector constraint
    DIVERSIFICATION = "diversification"  # HHI constraint


class OptimizationRequest(BaseModel):
    """Portfolio optimization request"""
    symbols: List[str] = Field(..., description="List of asset symbols")
    target_return: Optional[float] = Field(None, description="Target return (if None, maximize Sharpe)")
    method: OptimizationMethod = Field(OptimizationMethod.MEAN_VARIANCE, description="Optimization method")
    
    # Risk parameters
    alpha: float = Field(0.05, description="Confidence level for CVaR (e.g., 0.05 for 95%)")
    cvar_max: Optional[float] = Field(None, description="Maximum CVaR constraint")
    volatility_max: Optional[float] = Field(None, description="Maximum volatility constraint")
    
    # Constraints
    max_weight: float = Field(0.1, description="Maximum weight per asset (10% default)")
    min_weight: float = Field(0.0, description="Minimum weight per asset")
    sector_constraints: Optional[dict] = Field(None, description="Sector constraints {sector: max_weight}")
    hhi_max: Optional[float] = Field(None, description="Maximum Herfindahl-Hirschman Index")
    
    # Robust optimization
    uncertainty_radius: Optional[float] = Field(None, description="Uncertainty radius for robust optimization")
    
    # Data period
    lookback_period: int = Field(252, description="Lookback period in days (default: 1 year)")
    use_ledoit_wolf: bool = Field(True, description="Use Ledoit-Wolf shrinkage for covariance estimation")


class OptimizationResponse(BaseModel):
    """Portfolio optimization response"""
    weights: List[float] = Field(..., description="Optimal portfolio weights")
    expected_return: float = Field(..., description="Expected portfolio return")
    volatility: float = Field(..., description="Portfolio volatility (standard deviation)")
    sharpe_ratio: Optional[float] = Field(None, description="Sharpe ratio")
    cvar: Optional[float] = Field(None, description="Conditional Value at Risk")
    var: Optional[float] = Field(None, description="Value at Risk")
    diversification_ratio: Optional[float] = Field(None, description="Diversification ratio (1/HHI)")
    method_used: str = Field(..., description="Optimization method used")


class EfficientFrontierRequest(BaseModel):
    """Efficient frontier calculation request"""
    symbols: List[str] = Field(..., description="List of asset symbols")
    num_points: int = Field(50, description="Number of points on efficient frontier")
    lookback_period: int = Field(252, description="Lookback period in days")
    use_ledoit_wolf: bool = Field(True, description="Use Ledoit-Wolf shrinkage")


class EfficientFrontierPoint(BaseModel):
    """Single point on efficient frontier"""
    return_value: float
    volatility: float
    weights: List[float]


class EfficientFrontierResponse(BaseModel):
    """Efficient frontier response"""
    points: List[EfficientFrontierPoint] = Field(..., description="Points on efficient frontier")
    min_variance_return: float = Field(..., description="Return of minimum variance portfolio")
    min_variance_volatility: float = Field(..., description="Volatility of minimum variance portfolio")

