"""
Utility Helpers Module

Common utility functions for data processing and analysis.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
import os


def ensure_required_columns(df: pd.DataFrame, required_columns: List[str]) -> bool:
    """
    Check if DataFrame has all required columns.
    
    Args:
        df: DataFrame to check
        required_columns: List of required column names
        
    Returns:
        True if all columns present
    """
    return all(col in df.columns for col in required_columns)


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names to lowercase with underscores.
    
    Args:
        df: DataFrame to standardize
        
    Returns:
        DataFrame with standardized column names
    """
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    return df


def handle_missing_values(df: pd.DataFrame, strategy: str = 'fill_zero') -> pd.DataFrame:
    """
    Handle missing values in DataFrame.
    
    Args:
        df: DataFrame with potential missing values
        strategy: Strategy for handling ('fill_zero', 'fill_mean', 'drop')
        
    Returns:
        DataFrame with handled missing values
    """
    if strategy == 'fill_zero':
        return df.fillna(0)
    elif strategy == 'fill_mean':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        return df.fillna(df[numeric_cols].mean())
    elif strategy == 'drop':
        return df.dropna()
    else:
        return df


def remove_duplicates(df: pd.DataFrame, subset: List[str] = None) -> pd.DataFrame:
    """
    Remove duplicate rows.
    
    Args:
        df: DataFrame
        subset: Columns to check for duplicates
        
    Returns:
        DataFrame without duplicates
    """
    return df.drop_duplicates(subset=subset, keep='first')


def detect_outliers(series: pd.Series, method: str = 'iqr', threshold: float = 1.5) -> pd.Series:
    """
    Detect outliers in a numeric series.
    
    Args:
        series: Numeric series
        method: Detection method ('iqr' or 'zscore')
        threshold: Threshold for outlier detection
        
    Returns:
        Boolean series indicating outliers
    """
    if method == 'iqr':
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        return (series < (Q1 - threshold * IQR)) | (series > (Q3 + threshold * IQR))
    elif method == 'zscore':
        z_scores = np.abs((series - series.mean()) / series.std())
        return z_scores > threshold
    else:
        return pd.Series([False] * len(series))


def normalize_column(series: pd.Series, min_val: float = 0, max_val: float = 100) -> pd.Series:
    """
    Normalize series to specified range.
    
    Args:
        series: Series to normalize
        min_val: Minimum value for range
        max_val: Maximum value for range
        
    Returns:
        Normalized series
    """
    if series.max() == series.min():
        return pd.Series([min_val] * len(series), index=series.index)
    
    normalized = (series - series.min()) / (series.max() - series.min())
    return normalized * (max_val - min_val) + min_val


def create_engagement_categories(score: float) -> str:
    """
    Create category label for engagement score.
    
    Args:
        score: Engagement score 0-100
        
    Returns:
        Category string
    """
    if score >= 85:
        return "Excellent"
    elif score >= 75:
        return "Very Good"
    elif score >= 60:
        return "Good"
    elif score >= 45:
        return "Fair"
    else:
        return "Poor"


def get_semester_label(date_str: str) -> str:
    """
    Convert date string to semester label.
    
    Args:
        date_str: Date string
        
    Returns:
        Semester label (e.g., "Sem1", "Sem2")
    """
    if 'sem' in date_str.lower():
        return date_str
    # Add more conversion logic as needed
    return date_str


def validate_percentage(value: float) -> float:
    """
    Ensure value is valid percentage (0-100).
    
    Args:
        value: Value to validate
        
    Returns:
        Clipped value between 0-100
    """
    return np.clip(value, 0, 100)


def safe_divide(numerator: float, denominator: float, default: float = 0) -> float:
    """
    Safely divide two numbers.
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if denominator is 0
        
    Returns:
        Division result or default
    """
    return (numerator / denominator) if denominator != 0 else default


def get_data_summary(df: pd.DataFrame) -> Dict:
    """
    Get comprehensive data summary.
    
    Args:
        df: DataFrame to summarize
        
    Returns:
        Dictionary with summary statistics
    """
    return {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values': df.isnull().sum().to_dict(),
        'dtypes': df.dtypes.to_dict(),
        'numeric_summary': df.describe().to_dict()
    }


def export_to_csv(df: pd.DataFrame, file_path: str, include_index: bool = False) -> bool:
    """
    Export DataFrame to CSV.
    
    Args:
        df: DataFrame to export
        file_path: Output file path
        include_index: Whether to include index
        
    Returns:
        True if successful
    """
    try:
        df.to_csv(file_path, index=include_index)
        return True
    except Exception as e:
        print(f"Error exporting to CSV: {str(e)}")
        return False


def create_backup(file_path: str) -> bool:
    """
    Create backup of file.
    
    Args:
        file_path: File to backup
        
    Returns:
        True if successful
    """
    try:
        if os.path.exists(file_path):
            backup_path = f"{file_path}.backup"
            import shutil
            shutil.copy(file_path, backup_path)
            return True
    except Exception as e:
        print(f"Error creating backup: {str(e)}")
    return False
