"""
Covariance estimation utilities
"""
import numpy as np
import pandas as pd
from sklearn.covariance import LedoitWolf


class CovarianceEstimator:
    """Covariance matrix estimation with shrinkage"""
    
    @staticmethod
    def estimate_ledoit_wolf(returns: pd.DataFrame) -> pd.DataFrame:
        """
        Estimate covariance using Ledoit-Wolf shrinkage
        
        Args:
            returns: DataFrame with returns (columns = assets, rows = time)
        
        Returns:
            Estimated covariance matrix
        """
        lw = LedoitWolf()
        cov_matrix = lw.fit(returns.values).covariance_
        return pd.DataFrame(cov_matrix, index=returns.columns, columns=returns.columns)
    
    @staticmethod
    def estimate_sample(returns: pd.DataFrame) -> pd.DataFrame:
        """Estimate sample covariance"""
        return returns.cov()
    
    @staticmethod
    def estimate_regularized(returns: pd.DataFrame, lambda_reg: float = 0.01) -> pd.DataFrame:
        """
        Estimate regularized covariance: Σ + λI
        
        Args:
            returns: DataFrame with returns
            lambda_reg: Regularization parameter
        
        Returns:
            Regularized covariance matrix
        """
        cov_sample = returns.cov()
        n = len(cov_sample)
        cov_reg = cov_sample + lambda_reg * np.eye(n)
        return cov_reg

