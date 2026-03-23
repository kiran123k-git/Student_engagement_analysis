"""
Prediction Model Module

Predicts academic performance using engagement metrics.
"""

import pandas as pd
import numpy as np
from typing import Dict
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')


class AcademicPerformancePredictor:
    """Predicts student academic performance based on engagement metrics."""
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_columns = ['attendance', 'lms_logins', 'assignments_submitted']
        self.r2_score = None
        self.mse = None
    
    def train(self, historical_df: pd.DataFrame) -> Dict:
        """
        Train prediction model on historical data.
        
        Args:
            historical_df: DataFrame with columns: attendance, lms_logins, assignments, grade
            
        Returns:
            Dictionary with training metrics
        """
        if historical_df.empty:
            return {'error': 'No training data available'}
        
        # Prepare data
        X = historical_df[['attendance', 'lms_logins', 'assignments']].copy()
        y = historical_df['grade'].copy()
        
        # Remove rows with NaN values
        valid_indices = ~(X.isna().any(axis=1) | y.isna())
        X = X[valid_indices]
        y = y[valid_indices]
        
        if len(X) < 5:
            return {'error': 'Insufficient training data'}
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        self.r2_score = r2_score(y_test, y_pred)
        self.mse = mean_squared_error(y_test, y_pred)
        self.is_trained = True
        
        return {
            'r2_score': round(self.r2_score, 4),
            'mse': round(self.mse, 4),
            'rmse': round(np.sqrt(self.mse), 4),
            'training_samples': len(X_train),
            'testing_samples': len(X_test)
        }
    
    def predict(self, current_df: pd.DataFrame) -> pd.Series:
        """
        Predict grades for students using current engagement data.
        
        Args:
            current_df: DataFrame with attendance, lms_logins, assignments_submitted
            
        Returns:
            Series with predicted grades
        """
        if not self.is_trained:
            # Train on available data if not already trained
            if 'grade' in current_df.columns:
                self.train(current_df.rename(columns={'assignments_submitted': 'assignments'}))
            else:
                return pd.Series([0] * len(current_df), index=current_df.index)
        
        # Prepare features
        X = current_df[['attendance', 'lms_logins', 'assignments_submitted']].copy()
        X.columns = ['attendance', 'lms_logins', 'assignments']
        
        # Fill NaN values
        X = X.fillna(0)
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Predict
        predictions = self.model.predict(X_scaled)
        predictions = np.clip(predictions, 0, 10)  # Clip to reasonable grade range
        
        return pd.Series(predictions, index=current_df.index)
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance from trained model.
        
        Returns:
            Dictionary with feature importance scores
        """
        if not self.is_trained:
            return {}
        
        importances = self.model.feature_importances_
        feature_names = ['attendance', 'lms_logins', 'assignments']
        
        return dict(zip(feature_names, [round(float(imp), 4) for imp in importances]))


def add_predicted_grades(current_df: pd.DataFrame, historical_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add predicted grades to current student data.
    
    Args:
        current_df: Current semester student data
        historical_df: Historical semester data for training
        
    Returns:
        DataFrame with predicted_grade column
    """
    predictor = AcademicPerformancePredictor()
    
    df = current_df.copy()
    
    # Train if historical data available
    if not historical_df.empty:
        predictor.train(historical_df)
    
    # Make predictions
    df['predicted_grade'] = predictor.predict(current_df)
    
    return df


def get_performance_segments(current_df: pd.DataFrame) -> Dict:
    """
    Segment students by predicted performance.
    
    Args:
        current_df: Current data with predicted grades or historical grades
        
    Returns:
        Dictionary with performance segments
    """
    grade_column = 'predicted_grade' if 'predicted_grade' in current_df.columns else 'grade' if 'grade' in current_df.columns else None
    
    if not grade_column:
        return {}
    
    grades = current_df[grade_column]
    
    high_performers = len(current_df[grades >= 8])
    average_performers = len(current_df[(grades >= 6) & (grades < 8)])
    struggling_students = len(current_df[grades < 6])
    
    total = len(current_df)
    
    return {
        'high_performers': high_performers,
        'average_performers': average_performers,
        'struggling_students': struggling_students,
        'high_performers_pct': (high_performers / total * 100) if total > 0 else 0,
        'average_performers_pct': (average_performers / total * 100) if total > 0 else 0,
        'struggling_students_pct': (struggling_students / total * 100) if total > 0 else 0
    }

