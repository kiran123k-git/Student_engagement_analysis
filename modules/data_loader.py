"""
Data Loader Module

Handles loading and validation of student engagement CSV datasets.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional


def load_student_data(file_path: str) -> pd.DataFrame:
    """
    Load and validate student engagement data from CSV.
    
    Args:
        file_path: Path to CSV file
        
    Returns:
        Cleaned DataFrame with required columns
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If required columns are missing
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise ValueError(f"Error reading CSV: {str(e)}")
    
    # Define required columns
    required_columns = ['student_id', 'name', 'attendance', 'lms_logins', 
                       'assignments_submitted', 'total_assignments']
    
    # Validate required columns exist
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Handle missing values
    df = df.fillna(0)
    
    # Convert numeric columns to appropriate types
    numeric_columns = ['attendance', 'lms_logins', 'assignments_submitted', 'total_assignments']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Ensure no negative values
    df[numeric_columns] = df[numeric_columns].clip(lower=0)
    
    return df


def load_historical_data(file_path: str) -> pd.DataFrame:
    """
    Load historical semester data.
    
    Args:
        file_path: Path to CSV file
        
    Returns:
        Cleaned DataFrame with semester history
    """
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Error reading CSV: {str(e)}")
    
    required_columns = ['student_id', 'semester', 'attendance', 'lms_logins', 
                       'assignments', 'grade']
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Handle missing values
    df = df.fillna(0)
    
    # Convert numeric columns to appropriate types
    numeric_columns = ['attendance', 'lms_logins', 'assignments', 'grade']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Ensure no negative values (except for grades which can vary)
    df[['attendance', 'lms_logins', 'assignments']] = df[['attendance', 'lms_logins', 'assignments']].clip(lower=0)
    
    # Convert semester to string for consistency
    df['semester'] = df['semester'].astype(str)
    
    return df    # Convert numeric columns
    numeric_columns = ['attendance', 'lms_logins', 'assignments', 'grade']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    return df


def load_wellbeing_data(file_path: str) -> pd.DataFrame:
    """
    Load wellbeing indicators data.
    
    Args:
        file_path: Path to CSV file
        
    Returns:
        Cleaned DataFrame with wellbeing indicators
    """
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Error reading CSV: {str(e)}")
    
    required_columns = ['student_id', 'sleep_hours', 'stress_level', 
                       'missed_deadlines', 'class_participation']
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Handle missing values
    df = df.fillna(0)
    
    # Convert numeric columns
    numeric_columns = ['sleep_hours', 'stress_level', 'missed_deadlines', 'class_participation']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    return df


def validate_data_integrity(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate data integrity.
    
    Args:
        df: DataFrame to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    if df.empty:
        return False, "DataFrame is empty"
    
    if 'student_id' in df.columns and df['student_id'].duplicated().any():
        return False, "Duplicate student IDs found"
    
    return True, "Data validation passed"
