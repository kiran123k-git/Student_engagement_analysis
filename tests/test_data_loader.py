"""Unit tests for data loader module."""

import pytest
import pandas as pd
import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.data_loader import load_student_data, load_wellbeing_data


class TestDataLoader:
    """Test cases for data loading functionality."""

    @patch('modules.data_loader.pd.read_csv')
    def test_load_student_data_success(self, mock_read_csv):
        """Test successful loading of student data."""
        mock_df = pd.DataFrame({
            'student_id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie'],
            'attendance': [85, 70, 90],
            'lms_logins': [45, 30, 50],
            'assignments_submitted': [8, 6, 9],
            'total_assignments': [10, 10, 10]
        })
        mock_read_csv.return_value = mock_df

        result = load_student_data('data/students.csv')
        
        assert not result.empty
        assert len(result) == 3
        assert 'student_id' in result.columns

    @patch('modules.data_loader.pd.read_csv')
    def test_load_student_data_empty_file(self, mock_read_csv):
        """Test loading empty student data file."""
        # Empty dataframe without required columns should raise ValueError
        mock_read_csv.return_value = pd.DataFrame()
        
        with pytest.raises(ValueError):
            load_student_data('data/students.csv')

    @patch('modules.data_loader.pd.read_csv')
    def test_load_wellbeing_data_success(self, mock_read_csv):
        """Test successful loading of wellbeing data."""
        mock_df = pd.DataFrame({
            'student_id': [1, 2, 3],
            'sleep_hours': [6, 4, 8],
            'stress_level': [3, 7, 2],
            'missed_deadlines': [0, 2, 1],
            'class_participation': [8, 5, 9]
        })
        mock_read_csv.return_value = mock_df

        result = load_wellbeing_data('data/wellbeing_data.csv')
        
        assert not result.empty
        assert len(result) == 3

    @patch('modules.data_loader.pd.read_csv')
    def test_load_data_file_not_found(self, mock_read_csv):
        """Test handling of missing data file."""
        mock_read_csv.side_effect = FileNotFoundError()
        
        with pytest.raises(FileNotFoundError):
            load_student_data('data/nonexistent.csv')

    @patch('modules.data_loader.pd.read_csv')
    def test_load_data_malformed_csv(self, mock_read_csv):
        """Test handling of malformed CSV."""
        mock_read_csv.side_effect = pd.errors.ParserError()
        
        with pytest.raises(ValueError):  # Wrapped in ValueError
            load_student_data('data/malformed.csv')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
