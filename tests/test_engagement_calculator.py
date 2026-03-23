"""Unit tests for engagement calculator module."""

import pytest
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.engagement_calculator import (
    normalize_lms_activity,
    calculate_assignment_completion_rate
)


class TestEngagementCalculator:
    """Test cases for engagement scoring."""

    def test_normalize_lms_activity_valid(self):
        """Test LMS activity normalization."""
        lms_logins = [30, 50, 100]
        result = normalize_lms_activity(lms_logins, max_value=100)
        assert result[0] == pytest.approx(30.0, 0.1)
        assert result[1] == pytest.approx(50.0, 0.1)
        assert result[2] == pytest.approx(100.0, 0.1)

    def test_normalize_lms_activity_zero(self):
        """Test LMS activity normalization with zeros."""
        lms_logins = [0, 0, 0]
        result = normalize_lms_activity(lms_logins, max_value=100)
        assert all(x == 0 for x in result)

    def test_assignment_completion_rate_valid(self):
        """Test assignment completion rate calculation."""
        result = calculate_assignment_completion_rate(8, 10)
        assert result == pytest.approx(80.0, 0.1)

    def test_assignment_completion_rate_series(self):
        """Test assignment completion rate with Series."""
        submitted = pd.Series([5, 8, 10])
        total = pd.Series([10, 10, 10])
        result = calculate_assignment_completion_rate(submitted, total)
        assert isinstance(result, pd.Series)
        assert result[0] == pytest.approx(50.0, 0.1)
        assert result[1] == pytest.approx(80.0, 0.1)
        assert result[2] == pytest.approx(100.0, 0.1)

    def test_normalize_lms_series(self):
        """Test LMS normalization with pandas Series."""
        lms_series = pd.Series([10, 50, 100])
        result = normalize_lms_activity(lms_series, max_value=100)
        assert isinstance(result, pd.Series)
        assert result.iloc[0] == pytest.approx(10.0, 0.1)

    def test_assignment_completion_zero_assignments(self):
        """Test assignment completion with zero total assignments."""
        result = calculate_assignment_completion_rate(0, 0)
        # Should handle gracefully
        assert result is not None

    def test_normalize_lms_clipping(self):
        """Test that LMS normalization clips to 0-100 range."""
        lms_logins = [120, -10, 50]
        result = normalize_lms_activity(lms_logins, max_value=100)
        assert all(0 <= x <= 100 for x in result)

    def test_assignment_completion_all_completed(self):
        """Test assignment completion when all are completed."""
        result = calculate_assignment_completion_rate(10, 10)
        assert result == pytest.approx(100.0, 0.1)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
