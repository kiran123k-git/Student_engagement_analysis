"""Pytest configuration and shared fixtures."""

import pytest
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_student_data():
    """Fixture providing sample student data."""
    return pd.DataFrame({
        'student_id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'semester': [3, 3, 3, 3, 3],
        'attendance': [85, 70, 95, 55, 80],
        'lms_logins': [45, 30, 50, 20, 40],
        'assignments': [9, 6, 10, 4, 8]
    })


@pytest.fixture
def sample_wellbeing_data():
    """Fixture providing sample wellbeing data."""
    return pd.DataFrame({
        'student_id': [1, 2, 3, 4, 5],
        'stress_level': [3, 7, 2, 8, 4],
        'sleep_quality': [6, 4, 8, 3, 7],
        'mental_health': [7, 4, 8, 2, 6],
        'family_issues': [False, True, False, True, False]
    })


@pytest.fixture
def sample_engagement_scores():
    """Fixture providing sample engagement scores."""
    return {
        1: 85.0,
        2: 65.5,
        3: 92.0,
        4: 45.0,
        5: 78.5
    }


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test items during collection."""
    for item in items:
        # Add markers based on test characteristics
        if "slow" in item.nodeid:
            item.add_marker(pytest.mark.slow)
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
