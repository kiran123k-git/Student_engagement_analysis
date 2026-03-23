# Contributing to Student Engagement Analysis System

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- Virtual environment (recommended)
- Git

### Setup Development Environment
```bash
# Clone the repository
git clone <repository-url>
cd student-engagement-analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8
```

## 📝 How to Contribute

### 1. Report Issues
- Use GitHub Issues for bug reports and feature requests
- Provide clear descriptions and steps to reproduce
- Include relevant logs and error messages

### 2. Code Style Guidelines
- Follow PEP 8 standards
- Use 4 spaces for indentation
- Use meaningful variable and function names
- Add docstrings to functions and classes

**Format Code:**
```bash
black .
flake8 .
```

### 3. Writing Tests
- Write unit tests for new features
- Place tests in `/tests` directory
- Use pytest framework

**Run Tests:**
```bash
pytest tests/
pytest --cov=modules tests/  # With coverage
```

### 4. Commit Guidelines
- Write clear, descriptive commit messages
- Reference issues: `Fixes #123` or `Related to #456`
- Keep commits atomic (one logical change per commit)

**Good Commit Message:**
```
feat: Add wellbeing trend analysis

- Implements trend calculation across semesters
- Adds visualization in reports
- Fixes #45
```

### 5. Pull Request Process
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Write/update tests
5. Update documentation if needed
6. Push to your fork
7. Open a Pull Request with clear description

## 🏗️ Project Structure

```
student-engagement-analysis/
├── ai/                          # AI/ML modules
│   ├── ai_assistant.py         # Natural language queries
│   ├── rag_pipeline.py         # RAG implementation
│   └── vector_store.py         # Vector database
├── modules/                     # Core functionality
│   ├── data_loader.py
│   ├── engagement_calculator.py
│   ├── prediction_model.py
│   ├── report_generator.py
│   ├── risk_detector.py
│   ├── trend_analysis.py
│   └── wellbeing_detector.py
├── utils/                       # Utility functions
│   ├── helpers.py
│   └── visualizations.py
├── data/                        # Data files (CSV)
├── tests/                       # Unit tests
├── docs/                        # Documentation
└── app.py                       # Main Streamlit app
```

## 🧪 Testing Requirements

### Minimum Test Coverage: 70%
- Test critical functions
- Include edge cases
- Test error handling

**Example Test File:**
```python
import pytest
from modules.engagement_calculator import calculate_engagement

def test_calculate_engagement_valid():
    result = calculate_engagement(80, 30, 8)
    assert result == pytest.approx(79.4, 0.1)

def test_calculate_engagement_zero_values():
    result = calculate_engagement(0, 0, 0)
    assert result == 0
```

## 📚 Documentation Standards

- Update README.md for major changes
- Add docstrings to all functions
- Include type hints in function signatures
- Document new features in docs/

## 🐛 Found a Bug?

1. Check if issue already exists
2. Provide clear reproduction steps
3. Include error messages and logs
4. Mention your environment (Python version, OS, etc.)

## ✨ Feature Requests

- Clearly describe the feature
- Explain the use case
- Suggest implementation approach if possible
- Link to related issues

## 📋 Code Review Process

All contributions require:
- ✅ Tests passing (pytest)
- ✅ Code style compliance (flake8, black)
- ✅ Documentation updated
- ✅ At least one approval

## 📞 Questions?

- Check [QUICKSTART.md](QUICKSTART.md) for setup help
- Read [TECHNICAL_REFERENCE.md](docs/TECHNICAL_REFERENCE.md)
- Open a discussion issue

## 📜 License

By contributing, you agree your code will be licensed under the MIT License.

---

**Thank you for contributing! 🙌**
