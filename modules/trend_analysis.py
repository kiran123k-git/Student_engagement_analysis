"""
Trend Analysis Module

Analyzes engagement and academic metrics across semesters.
"""

import pandas as pd
import numpy as np
from typing import Dict, List


def analyze_semester_trends(historical_df: pd.DataFrame, student_id: str = None) -> Dict:
    """
    Analyze engagement trends across semesters.
    
    Args:
        historical_df: DataFrame with columns: student_id, semester, attendance, lms_logins, assignments, grade
        student_id: Optional student ID to filter (None = all students)
        
    Returns:
        Dictionary with semester trends
    """
    if student_id:
        data = historical_df[historical_df['student_id'] == student_id].sort_values('semester')
    else:
        data = historical_df.sort_values(['student_id', 'semester'])
    
    if data.empty:
        return {}
    
    # Group by semester if analyzing all students
    if not student_id:
        semester_data = data.groupby('semester').agg({
            'attendance': 'mean',
            'lms_logins': 'mean',
            'assignments': 'mean',
            'grade': 'mean'
        }).reset_index()
    else:
        semester_data = data[['semester', 'attendance', 'lms_logins', 'assignments', 'grade']]
    
    trends = {
        'semesters': semester_data['semester'].tolist(),
        'attendance_trend': semester_data['attendance'].tolist(),
        'lms_trend': semester_data['lms_logins'].tolist(),
        'assignments_trend': semester_data['assignments'].tolist(),
        'grade_trend': semester_data['grade'].tolist()
    }
    
    return trends


def calculate_trend_direction(values: List[float]) -> str:
    """
    Determine if trend is improving, declining, or stable.
    
    Args:
        values: List of metric values over time
        
    Returns:
        'IMPROVING', 'DECLINING', or 'STABLE'
    """
    if len(values) < 2:
        return 'STABLE'
    
    # Calculate slope using linear regression
    x = np.arange(len(values))
    y = np.array(values)
    
    # Remove NaN values
    valid_indices = ~np.isnan(y)
    x_valid = x[valid_indices]
    y_valid = y[valid_indices]
    
    if len(y_valid) < 2:
        return 'STABLE'
    
    # Calculate slope
    slope = np.polyfit(x_valid, y_valid, 1)[0]
    
    # Threshold for significance
    if abs(slope) < 0.5:
        return 'STABLE'
    elif slope > 0:
        return 'IMPROVING'
    else:
        return 'DECLINING'


def get_student_progress(historical_df: pd.DataFrame, student_id: str) -> Dict:
    """
    Get detailed progress report for a specific student.
    
    Args:
        historical_df: Historical data DataFrame
        student_id: Student ID
        
    Returns:
        Dictionary with progress metrics
    """
    trends = analyze_semester_trends(historical_df, student_id)
    
    if not trends:
        return {}
    
    attendance_trend = calculate_trend_direction(trends['attendance_trend'])
    grade_trend = calculate_trend_direction(trends['grade_trend'])
    
    return {
        'student_id': student_id,
        'total_semesters': len(trends['semesters']),
        'attendance_trend': attendance_trend,
        'grade_trend': grade_trend,
        'latest_attendance': trends['attendance_trend'][-1] if trends['attendance_trend'] else 0,
        'latest_grade': trends['grade_trend'][-1] if trends['grade_trend'] else 0,
        'average_grade': np.mean(trends['grade_trend']) if trends['grade_trend'] else 0,
        'trends': trends
    }


def identify_improving_students(historical_df: pd.DataFrame) -> List[str]:
    """
    Identify students showing improvement over semesters.
    
    Args:
        historical_df: Historical data DataFrame
        
    Returns:
        List of student IDs with improving trends
    """
    improving_students = []
    
    for student_id in historical_df['student_id'].unique():
        progress = get_student_progress(historical_df, student_id)
        if progress.get('grade_trend') == 'IMPROVING':
            improving_students.append(student_id)
    
    return improving_students


def identify_declining_students(historical_df: pd.DataFrame) -> List[str]:
    """
    Identify students showing declining performance.
    
    Args:
        historical_df: Historical data DataFrame
        
    Returns:
        List of student IDs with declining trends
    """
    declining_students = []
    
    for student_id in historical_df['student_id'].unique():
        progress = get_student_progress(historical_df, student_id)
        if progress.get('grade_trend') == 'DECLINING':
            declining_students.append(student_id)
    
    return declining_students


def get_semester_summary(historical_df: pd.DataFrame) -> pd.DataFrame:
    """
    Get summary statistics for each semester.
    
    Args:
        historical_df: Historical data DataFrame
        
    Returns:
        DataFrame with semester summaries
    """
    summary = historical_df.groupby('semester').agg({
        'student_id': 'count',
        'attendance': ['mean', 'min', 'max'],
        'lms_logins': ['mean', 'min', 'max'],
        'assignments': ['mean', 'min', 'max'],
        'grade': ['mean', 'min', 'max']
    }).round(2)
    
    summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
    summary = summary.rename(columns={'student_id_count': 'total_students'})
    
    return summary
