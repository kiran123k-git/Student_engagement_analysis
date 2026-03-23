"""
Risk Detector Module

Identifies at-risk students based on engagement scores and attendance patterns.
"""

import pandas as pd
import numpy as np
from typing import Tuple


def calculate_engagement_level(engagement_score: float) -> str:
    """
    Determine engagement level based on score.
    
    Rules:
    - >= 80: HIGH ENGAGEMENT
    - 60-79: MODERATE ENGAGEMENT
    - < 60: LOW ENGAGEMENT
    
    Args:
        engagement_score: Score 0-100
        
    Returns:
        Engagement level string
    """
    if engagement_score >= 80:
        return "HIGH ENGAGEMENT"
    elif engagement_score >= 60:
        return "MODERATE ENGAGEMENT"
    else:
        return "LOW ENGAGEMENT"


def calculate_risk_level(row: pd.Series) -> str:
    """
    Determine risk level based on multiple factors.
    
    Rules:
    - attendance < 60 OR assignments_submitted < 50% of total: HIGH RISK
    - Otherwise: evaluate by engagement level
    
    Args:
        row: Student data row with engagement_score, attendance, assignments_submitted, total_assignments
        
    Returns:
        Risk level string
    """
    attendance = row.get('attendance', 0)
    assignments_submitted = row.get('assignments_submitted', 0)
    total_assignments = row.get('total_assignments', 1)
    assignment_percentage = (assignments_submitted / total_assignments * 100) if total_assignments > 0 else 0
    
    # High risk conditions
    if attendance < 60 or assignment_percentage < 50:
        return "HIGH RISK"
    
    # Check engagement score
    engagement_score = row.get('engagement_score', 0)
    if engagement_score < 60:
        return "HIGH RISK"
    elif engagement_score < 75:
        return "AT RISK"
    
    return "LOW RISK"


def add_risk_levels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add engagement level and risk level columns to dataframe.
    
    Args:
        df: DataFrame with engagement scores
        
    Returns:
        DataFrame with engagement_level and risk_level columns
    """
    df = df.copy()
    
    # Ensure numeric columns are properly typed
    numeric_cols = ['attendance', 'lms_logins', 'assignments_submitted', 'total_assignments']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Ensure engagement_score exists
    if 'engagement_score' not in df.columns:
        from modules.engagement_calculator import add_engagement_scores
        df = add_engagement_scores(df)
    
    # Calculate engagement levels
    df['engagement_level'] = df['engagement_score'].apply(calculate_engagement_level)
    
    # Calculate risk levels
    df['risk_level'] = df.apply(calculate_risk_level, axis=1)
    
    return df


def get_at_risk_students(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get students flagged as at-risk or high-risk.
    
    Args:
        df: DataFrame with risk_level column
        
    Returns:
        Filtered DataFrame of at-risk students
    """
    if 'risk_level' not in df.columns:
        df = add_risk_levels(df)
    
    return df[df['risk_level'].isin(['AT RISK', 'HIGH RISK'])].sort_values('engagement_score')


def get_risk_statistics(df: pd.DataFrame) -> dict:
    """
    Get risk statistics.
    
    Args:
        df: DataFrame with risk_level column
        
    Returns:
        Dictionary with risk statistics
    """
    if 'risk_level' not in df.columns:
        df = add_risk_levels(df)
    
    total = len(df)
    high_risk = len(df[df['risk_level'] == 'HIGH RISK'])
    at_risk = len(df[df['risk_level'] == 'AT RISK'])
    low_risk = len(df[df['risk_level'] == 'LOW RISK'])
    
    return {
        'total_students': total,
        'high_risk_count': high_risk,
        'at_risk_count': at_risk,
        'low_risk_count': low_risk,
        'high_risk_percentage': (high_risk / total * 100) if total > 0 else 0,
        'at_risk_percentage': (at_risk / total * 100) if total > 0 else 0,
        'low_risk_percentage': (low_risk / total * 100) if total > 0 else 0
    }


def get_engagement_distribution(df: pd.DataFrame) -> dict:
    """
    Get distribution of engagement levels.
    
    Args:
        df: DataFrame with engagement_level column
        
    Returns:
        Dictionary with counts by engagement level
    """
    if 'engagement_level' not in df.columns:
        df = add_risk_levels(df)
    
    return {
        'high_engagement': len(df[df['engagement_level'] == 'HIGH ENGAGEMENT']),
        'moderate_engagement': len(df[df['engagement_level'] == 'MODERATE ENGAGEMENT']),
        'low_engagement': len(df[df['engagement_level'] == 'LOW ENGAGEMENT'])
    }
