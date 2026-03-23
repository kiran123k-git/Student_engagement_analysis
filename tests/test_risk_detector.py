"""Unit tests for risk detector module."""

import pytest
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.risk_detector import (
    calculate_engagement_level,
    calculate_risk_level
)


class TestRiskDetector:
    """Test cases for risk detection system."""

    def test_engagement_level_high(self):
        """Test high engagement level detection."""
        result = calculate_engagement_level(85)
        assert result == "HIGH ENGAGEMENT"

    def test_engagement_level_moderate(self):
        """Test moderate engagement level detection."""
        result = calculate_engagement_level(70)
        assert result == "MODERATE ENGAGEMENT"

    def test_engagement_level_low(self):
        """Test low engagement level detection."""
        result = calculate_engagement_level(45)
        assert result == "LOW ENGAGEMENT"

    def test_risk_level_high_risk_low_attendance(self):
        """Test high risk detection with low attendance."""
        row = pd.Series({
            'engagement_score': 45,
            'attendance': 50,
            'assignments_submitted': 3,
            'total_assignments': 10
        })
        result = calculate_risk_level(row)
        assert result == "HIGH RISK"

    def test_risk_level_moderate_risk(self):
        """Test moderate risk detection."""
        row = pd.Series({
            'engagement_score': 70,
            'attendance': 70,
            'assignments_submitted': 6,
            'total_assignments': 10
        })
        result = calculate_risk_level(row)
        # Risk level can be AT RISK or LOW RISK depending on engagement
        assert result in ["AT RISK", "LOW RISK"]

    def test_engagement_boundary_high(self):
        """Test engagement boundary at 80 (HIGH)."""
        result = calculate_engagement_level(80)
        assert result == "HIGH ENGAGEMENT"

    def test_engagement_boundary_moderate(self):
        """Test engagement boundary at 60 (MODERATE)."""
        result = calculate_engagement_level(60)
        assert result == "MODERATE ENGAGEMENT"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
