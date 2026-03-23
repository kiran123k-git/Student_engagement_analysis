"""
Wellbeing Detector Module

Detects psychological and behavioral risk indicators from student data.
"""

import pandas as pd
import numpy as np
from typing import Tuple


def calculate_wellbeing_status(row: pd.Series) -> str:
    """
    Determine wellbeing status based on behavioral indicators.
    
    Rules:
    - attendance < 60 AND assignments_submitted < 50%: HIGH WELLBEING RISK
    - attendance < 70: MEDIUM WELLBEING RISK
    - Else: NORMAL
    
    Args:
        row: Student data row
        
    Returns:
        Wellbeing status string
    """
    attendance = row.get('attendance', 0)
    assignments_submitted = row.get('assignments_submitted', 0)
    total_assignments = row.get('total_assignments', 1)
    
    assignment_percentage = (assignments_submitted / total_assignments * 100) if total_assignments > 0 else 0
    
    # High risk conditions
    if attendance < 60 and assignment_percentage < 50:
        return "HIGH WELLBEING RISK"
    
    # Medium risk
    if attendance < 70:
        return "MEDIUM WELLBEING RISK"
    
    return "NORMAL"


def detect_sudden_engagement_drop(current_row: pd.Series, historical_df: pd.DataFrame) -> bool:
    """
    Detect sudden attendance drop from previous semester.
    
    Args:
        current_row: Current semester student data
        historical_df: Historical semester data
        
    Returns:
        True if sudden drop detected
    """
    student_id = current_row.get('student_id')
    current_attendance = current_row.get('attendance', 0)
    
    # Get last semester data
    student_history = historical_df[historical_df['student_id'] == student_id].sort_values('semester')
    
    if len(student_history) == 0:
        return False
    
    last_attendance = student_history.iloc[-1].get('attendance', 0)
    
    # Check for drop > 15 percentage points
    return (last_attendance - current_attendance) > 15


def add_wellbeing_status(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add wellbeing_status column to dataframe.
    
    Args:
        df: Student data DataFrame
        
    Returns:
        DataFrame with wellbeing_status column
    """
    df = df.copy()
    
    # Ensure numeric columns are properly typed
    numeric_cols = ['attendance', 'assignments_submitted', 'total_assignments']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    df['wellbeing_status'] = df.apply(calculate_wellbeing_status, axis=1)
    return df
    df['wellbeing_status'] = df.apply(calculate_wellbeing_status, axis=1)
    return df


def get_wellbeing_alerts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get students with wellbeing alerts.
    
    Args:
        df: DataFrame with wellbeing_status column
        
    Returns:
        Filtered DataFrame of students with risk flags
    """
    if 'wellbeing_status' not in df.columns:
        df = add_wellbeing_status(df)
    
    return df[df['wellbeing_status'] != 'NORMAL'].sort_values('wellbeing_status', 
                                                              key=lambda x: x.map({'HIGH WELLBEING RISK': 0, 'MEDIUM WELLBEING RISK': 1, 'NORMAL': 2}))


def get_wellbeing_statistics(df: pd.DataFrame) -> dict:
    """
    Get wellbeing statistics.
    
    Args:
        df: DataFrame with wellbeing_status column
        
    Returns:
        Dictionary with wellbeing statistics
    """
    if 'wellbeing_status' not in df.columns:
        df = add_wellbeing_status(df)
    
    total = len(df)
    high_risk = len(df[df['wellbeing_status'] == 'HIGH WELLBEING RISK'])
    medium_risk = len(df[df['wellbeing_status'] == 'MEDIUM WELLBEING RISK'])
    normal = len(df[df['wellbeing_status'] == 'NORMAL'])
    
    return {
        'total_students': total,
        'high_risk_count': high_risk,
        'medium_risk_count': medium_risk,
        'normal_count': normal,
        'high_risk_percentage': (high_risk / total * 100) if total > 0 else 0,
        'medium_risk_percentage': (medium_risk / total * 100) if total > 0 else 0
    }


def identify_behavioral_indicators(df: pd.DataFrame) -> dict:
    """
    Identify key behavioral risk indicators across student population.
    
    Args:
        df: Student data DataFrame
        
    Returns:
        Dictionary with indicators
    """
    indicators = {
        'low_attendance': len(df[df['attendance'] < 70]),
        'low_lms_activity': len(df[df['lms_logins'] < df['lms_logins'].quantile(0.25)]),
        'low_assignment_submission': len(df[df['assignments_submitted'] / df['total_assignments'] < 0.5]),
        'no_lms_activity': len(df[df['lms_logins'] == 0]),
        'no_submissions': len(df[df['assignments_submitted'] == 0])
    }
    
    return indicators
