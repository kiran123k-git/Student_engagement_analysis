#!/bin/bash

# Student Engagement Analysis System - Quick Start Guide
# ========================================================

echo "=========================================="
echo "Student Engagement Analysis System"
echo "Quick Start Installation"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.10+"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Create virtual environment (optional but recommended)
echo "📦 Setting up Python environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing required packages..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ All packages installed successfully"
else
    echo "❌ Error installing packages"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Installation Complete!"
echo "=========================================="
echo ""
echo "To run the application:"
echo ""
echo "  streamlit run app.py"
echo ""
echo "The dashboard will open at: http://localhost:8501"
echo ""
echo "Optional: Set Groq API key for AI features"
echo "  export GROQ_API_KEY=\"your_api_key_here\""
echo ""
echo "=========================================="
