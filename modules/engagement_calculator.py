"""
Engagement Calculator Module

Computes engagement scores based on attendance, LMS activity, and assignment completion.
"""

import pandas as pd
import numpy as np
from typing import Union


def normalize_lms_activity(lms_logins: Union[pd.Series, np.ndarray], max_value: float = None) -> Union[pd.Series, np.ndarray]:
    """
    Normalize LMS login activity to 0-100 scale.
    
    Args:
        lms_logins: LMS login counts
        max_value: Maximum expected value (auto-detected if None)
        
    Returns:
        Normalized values 0-100
    """
    if isinstance(lms_logins, pd.Series):
        series_input = True
        data = lms_logins.values
    else:
        series_input = False
        data = np.array(lms_logins)
    
    if len(data) == 0 or np.max(data) == 0:
        return lms_logins if series_input else data
    
    max_val = max_value if max_value else np.max(data)
    normalized = (data / max_val) * 100
    normalized = np.clip(normalized, 0, 100)
    
    if series_input:
        return pd.Series(normalized, index=lms_logins.index)
    else:
        return normalized


def calculate_assignment_completion_rate(assignments_submitted: Union[pd.Series, int], 
                                         total_assignments: Union[pd.Series, int]) -> Union[pd.Series, float]:
    """
    Calculate assignment completion rate as percentage.
    
    Args:
        assignments_submitted: Number of assignments submitted
        total_assignments: Total assignments assigned
        
    Returns:
        Completion rate 0-100
    """
    # Handle division by zero
    if isinstance(total_assignments, pd.Series):
        rate = (assignments_submitted / total_assignments.replace(0, 1)) * 100
        rate = rate.where(total_assignments != 0, 0)
    else:
        rate = (assignments_submitted / total_assignments * 100) if total_assignments > 0 else 0
    
    return np.clip(rate, 0, 100)


def calculate_engagement_score(df: pd.DataFrame) -> pd.Series:
    """
    Calculate engagement score for each student.
    
    Formula:
    Engagement Score = 0.4 × Attendance + 0.3 × LMS Activity + 0.3 × Assignment Completion Rate
    
    Args:
        df: DataFrame with columns: attendance, lms_logins, assignments_submitted, total_assignments
        
    Returns:
        Series with engagement scores 0-100
    """
    # Normalize components
    attendance = np.clip(df['attendance'], 0, 100)
    
    lms_activity = normalize_lms_activity(df['lms_logins'])
    
    assignment_rate = calculate_assignment_completion_rate(
        df['assignments_submitted'], 
        df['total_assignments']
    )
    
    # Apply weights
    engagement_score = (0.4 * attendance + 
                       0.3 * lms_activity + 
                       0.3 * assignment_rate)
    
    # Ensure score is between 0-100
    engagement_score = np.clip(engagement_score, 0, 100)
    
    return pd.Series(engagement_score, index=df.index)


def add_engagement_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add engagement score column to dataframe.
    
    Args:
        df: Student data DataFrame
        
    Returns:
        DataFrame with added engagement_score column
    """
    df = df.copy()
    
    # Ensure all required columns are numeric
    numeric_cols = ['attendance', 'lms_logins', 'assignments_submitted', 'total_assignments']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    df['engagement_score'] = calculate_engagement_score(df)
    return df


def get_engagement_statistics(df: pd.DataFrame) -> dict:
    """
    Get engagement statistics.
    
    Args:
        df: DataFrame with engagement_score column
        
    Returns:
        Dictionary with statistics
    """
    if 'engagement_score' not in df.columns:
        df = add_engagement_scores(df)
    
    scores = df['engagement_score']
    
    return {
        'total_students': len(df),
        'average_score': round(scores.mean(), 2),
        'median_score': round(scores.median(), 2),
        'min_score': round(scores.min(), 2),
        'max_score': round(scores.max(), 2),
        'std_dev': round(scores.std(), 2),
        'quartile_25': round(scores.quantile(0.25), 2),
        'quartile_75': round(scores.quantile(0.75), 2)
    }
