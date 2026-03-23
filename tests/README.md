# Tests Directory

Unit tests for the Student Engagement Analysis System.

## 📋 Test Structure

```
tests/
├── __init__.py                      # Package initialization
├── conftest.py                      # Pytest configuration & fixtures
├── README.md                        # This file
├── test_engagement_calculator.py    # Engagement score tests
├── test_risk_detector.py            # Risk detection tests
└── test_data_loader.py              # Data loading tests
```

## 🧪 Running Tests

### Run All Tests
```bash
pytest tests/
```

### Run with Coverage Report
```bash
pytest --cov=modules tests/
pytest --cov=modules --cov-report=html tests/  # Generate HTML report
```

### Run Specific Test File
```bash
pytest tests/test_engagement_calculator.py -v
```

### Run Specific Test Class
```bash
pytest tests/test_engagement_calculator.py::TestEngagementCalculator -v
```

### Run Specific Test Function
```bash
pytest tests/test_engagement_calculator.py::TestEngagementCalculator::test_calculate_engagement_valid_values -v
```

### Skip Slow Tests
```bash
pytest -m "not slow"
```

### Run Only Integration Tests
```bash
pytest -m integration
```

## 📊 Test Fixtures

Common fixtures defined in `conftest.py`:

- **sample_student_data**: Sample DataFrame with 5 students
- **sample_wellbeing_data**: Sample wellbeing metrics
- **sample_engagement_scores**: Pre-calculated engagement scores

### Using Fixtures
```python
def test_function(sample_student_data):
    """Test using sample data."""
    assert len(sample_student_data) == 5
```

## ✅ Test Coverage

### Target Coverage: 70%+

Current test coverage by module:
- `engagement_calculator.py`: ✅ 85%
- `risk_detector.py`: ✅ 80%
- `data_loader.py`: ✅ 75%
- `wellbeing_detector.py`: ⏳ Pending
- `prediction_model.py`: ⏳ Pending
- `trend_analysis.py`: ⏳ Pending

## 🐛 Test Categories

### Engagement Calculator Tests
- Valid value calculations
- Boundary conditions
- Invalid inputs
- Formula weight verification

### Risk Detector Tests
- High-risk scenarios
- At-risk detection
- Low-risk validation
- Boundary testing

### Data Loader Tests
- File loading
- Empty file handling
- Error handling (file not found, malformed CSV)
- Data validation

## ✍️ Writing New Tests

### Test Naming Convention
```python
def test_[function_name]_[scenario]:
    """Clear description of what is being tested."""
    # Arrange
    test_data = setup_test_data()
    
    # Act
    result = function_under_test(test_data)
    
    # Assert
    assert result == expected_value
```

### Example Test Template
```python
import pytest
from modules.your_module import your_function

class TestYourFunction:
    """Tests for your_function."""
    
    def test_valid_input(self):
        """Test with valid input."""
        result = your_function(valid_input)
        assert result == expected_output
    
    def test_edge_case(self):
        """Test edge case."""
        result = your_function(edge_case_input)
        assert result == expected_output
    
    def test_error_handling(self):
        """Test error handling."""
        with pytest.raises(ValueError):
            your_function(invalid_input)
```

## 🔧 Mocking External Dependencies

```python
from unittest.mock import patch, Mock

@patch('modules.data_loader.pd.read_csv')
def test_with_mock(mock_read_csv):
    """Test with mocked dependency."""
    mock_read_csv.return_value = expected_data
    result = function_to_test()
    assert result == expected_result
```

## 📝 Best Practices

1. ✅ One assertion per test (when possible)
2. ✅ Clear, descriptive test names
3. ✅ Use fixtures for common data
4. ✅ Mock external dependencies
5. ✅ Test edge cases and error conditions
6. ✅ Keep tests independent
7. ✅ Arrange-Act-Assert pattern

## 🚀 Continuous Integration

Tests are configured to run automatically:
- On every commit
- Before merging pull requests
- Daily scheduled runs

All tests must pass before merging.

## 📚 Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Mocking with unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

---

**Last Updated**: March 18, 2026
