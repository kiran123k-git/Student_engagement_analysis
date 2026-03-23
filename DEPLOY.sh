#!/bin/bash

# Student Engagement Analysis System - Deployment Guide
# =====================================================
# Complete setup and deployment instructions

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
cat << "EOF"
╔════════════════════════════════════════════════════════════════════╗
║   STUDENT ENGAGEMENT ANALYSIS & WELLBEING MONITORING SYSTEM       ║
║                     Deployment Guide v1.0                         ║
╚════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# === SYSTEM REQUIREMENTS CHECK ===
echo -e "${YELLOW}[1/5] Checking System Requirements...${NC}"

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} Python 3 found: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 3 not found. Please install Python 3.10+"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓${NC} pip3 found"
else
    echo -e "${RED}✗${NC} pip3 not found"
    exit 1
fi

# === ENVIRONMENT SETUP ===
echo ""
echo -e "${YELLOW}[2/5] Setting up Python Environment...${NC}"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment already exists"
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo -e "${GREEN}✓${NC} Virtual environment activated"

# === DEPENDENCY INSTALLATION ===
echo ""
echo -e "${YELLOW}[3/5] Installing Dependencies...${NC}"

# Upgrade pip
pip install --upgrade pip --quiet

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "Installing packages from requirements.txt..."
    pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} All dependencies installed successfully"
    else
        echo -e "${RED}✗${NC} Error installing dependencies"
        exit 1
    fi
else
    echo -e "${RED}✗${NC} requirements.txt not found"
    exit 1
fi

# === CONFIGURATION ===
echo ""
echo -e "${YELLOW}[4/5] System Configuration...${NC}"

# Check for Groq API key
if [ -z "$GROQ_API_KEY" ]; then
    echo -e "${YELLOW}⚠${NC}  Groq API key not set (optional for AI features)"
    read -p "Would you like to set Groq API key? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -sp "Enter Groq API Key: " GROQ_API_KEY
        echo
        export GROQ_API_KEY=$GROQ_API_KEY
        echo -e "${GREEN}✓${NC} Groq API key configured"
    fi
else
    echo -e "${GREEN}✓${NC} Groq API key already set"
fi

# Check data files
if [ -f "data/students.csv" ] && [ -f "data/historical_semesters.csv" ]; then
    echo -e "${GREEN}✓${NC} Sample data files found"
else
    echo -e "${RED}✗${NC} Sample data files missing"
fi

# === VERIFICATION ===
echo ""
echo -e "${YELLOW}[5/5] Verifying Installation...${NC}"

# Verify Python packages
python3 -c "import streamlit; print('Streamlit:', streamlit.__version__)" 2>/dev/null && \
    echo -e "${GREEN}✓${NC} Streamlit installed" || \
    echo -e "${RED}✗${NC} Streamlit not found"

python3 -c "import pandas; print('Pandas:', pandas.__version__)" 2>/dev/null && \
    echo -e "${GREEN}✓${NC} Pandas installed" || \
    echo -e "${RED}✗${NC} Pandas not found"

python3 -c "import sklearn; print('Scikit-learn: OK')" 2>/dev/null && \
    echo -e "${GREEN}✓${NC} Scikit-learn installed" || \
    echo -e "${RED}✗${NC} Scikit-learn not found"

python3 -c "import chromadb; print('ChromaDB: OK')" 2>/dev/null && \
    echo -e "${GREEN}✓${NC} ChromaDB installed" || \
    echo -e "${YELLOW}⚠${NC}  ChromaDB may need configuration"

# === COMPLETION ===
echo ""
echo -e "${GREEN}"
cat << "EOF"
╔════════════════════════════════════════════════════════════════════╗
║                  ✓ SETUP COMPLETE                                  ║
╚════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo "Next steps:"
echo ""
echo -e "${BLUE}1. Start the application:${NC}"
echo "   streamlit run app.py"
echo ""
echo -e "${BLUE}2. Dashboard will open at:${NC}"
echo "   http://localhost:8501"
echo ""
echo -e "${BLUE}3. Load sample data:${NC}"
echo "   Sidebar → Data Management → Load Sample Data"
echo ""
echo -e "${BLUE}4. Explore features:${NC}"
echo "   Navigate through 7 dashboard sections"
echo ""
echo -e "${BLUE}Additional commands:${NC}"
echo "   - View documentation: cat README.md"
echo "   - Quick start guide: cat QUICKSTART.md"
echo "   - View requirements: cat requirements.txt"
echo ""
echo "For support, check PROJECT_SUMMARY.md or README.md"
echo ""
