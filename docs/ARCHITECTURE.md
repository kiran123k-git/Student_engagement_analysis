# System Architecture

## 🏗️ Overview

The Student Engagement Analysis System follows a modular architecture designed for scalability, maintainability, and institutional deployment.

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│         Streamlit UI (app.py)                           │
│    - 7 Decision Support Pages                           │
│    - Authentication & Authorization                     │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│         Core Application Layer (modules/)               │
│  ┌──────────────────────────────────────────────────┐  │
│  │ • data_loader.py         - Data I/O              │  │
│  │ • engagement_calculator.py - Scoring Engine      │  │
│  │ • risk_detector.py       - Risk Assessment       │  │
│  │ • wellbeing_detector.py  - Behavioral Analysis   │  │
│  │ • trend_analysis.py      - Time Series Analysis  │  │
│  │ • prediction_model.py    - ML Predictions        │  │
│  │ • report_generator.py    - Report Creation       │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│         AI & NLP Layer (ai/)                            │
│  ┌──────────────────────────────────────────────────┐  │
│  │ • ai_assistant.py        - Natural Language Q&A  │  │
│  │ • rag_pipeline.py        - Retrieval Augmented   │  │
│  │ • vector_store.py        - Vector Database       │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│         Utility Layer (utils/)                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │ • helpers.py        - Utility Functions          │  │
│  │ • visualizations.py - Charting & Graphs          │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│         Data Layer                                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │ • CSV Data Files (data/)                         │  │
│  │ • ChromaDB Vector Store (chroma_db/)             │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow

### 1. Data Ingestion
```
CSV Files (students.csv, wellbeing_data.csv, historical_semesters.csv)
    ↓
data_loader.py (load & validate)
    ↓
Pandas DataFrames (in-memory cache)
```

### 2. Processing Pipeline
```
Raw Student Data
    ↓
engagement_calculator.py (Score: 0-100)
    ↓
risk_detector.py (Categorize: HIGH/AT-RISK/LOW)
    ↓
wellbeing_detector.py (Analyze patterns)
    ↓
trend_analysis.py (Historical comparison)
    ↓
prediction_model.py (Forecast future risk)
```

### 3. AI Pipeline
```
User Query
    ↓
rag_pipeline.py (Retrieve relevant context)
    ↓
vector_store.py (ChromaDB lookup)
    ↓
ai_assistant.py (LLM processing)
    ↓
Groq API (Response generation)
    ↓
Natural Language Response
```

### 4. Report Generation
```
Processed Data
    ↓
report_generator.py (Format & structure)
    ↓
visualizations.py (Create charts)
    ↓
PDF/Excel Output
```

## 📦 Module Responsibilities

### Core Modules (modules/)

#### data_loader.py
- **Purpose**: Load and validate data
- **Functions**: 
  - `load_students_data()` - Load student information
  - `load_wellbeing_data()` - Load wellbeing metrics
- **Dependencies**: pandas, CSV files

#### engagement_calculator.py
- **Purpose**: Calculate engagement scores
- **Formula**: (Attendance × 0.4) + (LMS Logins × 0.3) + (Assignments × 0.3)
- **Output**: Score 0-100
- **Used by**: Dashboard, risk detector, reports

#### risk_detector.py
- **Purpose**: Classify student risk levels
- **Categories**: HIGH_RISK, AT_RISK, LOW_RISK
- **Thresholds**:
  - HIGH: Attendance < 60% OR Assignments < 50%
  - AT_RISK: Engagement 60-79%
  - LOW: Engagement ≥ 80%

#### wellbeing_detector.py
- **Purpose**: Behavioral pattern analysis
- **Detects**: Stress indicators, behavioral changes
- **Output**: Wellbeing risk flags

#### trend_analysis.py
- **Purpose**: Historical performance tracking
- **Compares**: Semester-to-semester metrics
- **Output**: Trend classifications (improving, stable, declining)

#### prediction_model.py
- **Purpose**: Predictive analytics
- **Methods**: ML models (may include logistic regression, random forest)
- **Output**: Future risk predictions

#### report_generator.py
- **Purpose**: Create exportable reports
- **Formats**: PDF, Excel, JSON
- **Contents**: Student analysis, trends, recommendations

### AI Modules (ai/)

#### ai_assistant.py
- **Purpose**: Natural language query interface
- **Integration**: Groq API
- **Features**: Q&A, context-aware responses
- **Powered by**: LangChain, Groq LLM

#### rag_pipeline.py
- **Purpose**: Retrieval-Augmented Generation
- **Process**: Retrieve context → Augment query → Generate response
- **Storage**: ChromaDB vectors

#### vector_store.py
- **Purpose**: Vector database management
- **Backend**: ChromaDB
- **Use**: Store embeddings, semantic search

### Utility Modules (utils/)

#### helpers.py
- **Purpose**: Common utility functions
- **Includes**: Data validation, formatting, calculations

#### visualizations.py
- **Purpose**: Chart and graph generation
- **Library**: Plotly, Matplotlib
- **Components**: Engagement charts, risk heatmaps, trend graphs

## 🔐 Security Architecture

```
┌─────────────────────────────────┐
│   User Login (Streamlit Auth)   │
└────────────────┬────────────────┘
                 ↓
         ┌──────────────────┐
         │  Session Token   │
         └────────┬─────────┘
                  ↓
      ┌──────────────────────────┐
      │  Role-Based Access       │
      │  (Admin/View Only)       │
      └────────┬─────────────────┘
               ↓
      ┌──────────────────────────┐
      │  Data Access Layer       │
      │  (Filter by permission)  │
      └──────────────────────────┘
```

## 🔄 Deployment Architecture

### Local Development
```
Python Virtual Environment
└── Streamlit Server (localhost:8501)
    ├── ChromaDB (local)
    ├── Data Files (local)
    └── Groq API (cloud)
```

### Production Deployment
```
Docker Container
├── Streamlit App
├── Python Modules
├── ChromaDB
├── Data Storage
└── Environment Variables
    ├── GROQ_API_KEY
    ├── DATABASE_URL
    └── Authentication tokens
```

## 🧵 Threading & Concurrency

- **Main Thread**: Streamlit UI rendering
- **Background Tasks**: Data loading, model training
- **Async Operations**: API calls to Groq

## 📈 Scalability Considerations

1. **Data**: Move from CSV to SQL database for 1000+ students
2. **Caching**: Implement Redis for frequent queries
3. **APIs**: Create REST API for external integrations
4. **ML Models**: Move to dedicated ML model server
5. **Vector Store**: Scale ChromaDB or move to Pinecone/Weaviate

## 🔧 Configuration Management

```
Environment Variables
├── GROQ_API_KEY
├── DATABASE_URL
├── LOG_LEVEL
├── MAX_STUDENTS
└── CACHE_TTL
```

## 📊 Data Models

### Student Entity
```python
{
    "student_id": int,
    "name": str,
    "semester": int,
    "attendance": float,
    "lms_logins": int,
    "assignments": int,
    "engagement_score": float,
    "risk_level": str,
    "wellbeing_status": str
}
```

### Report Entity
```python
{
    "report_id": str,
    "created_at": datetime,
    "report_type": str,  # "individual" | "class" | "semester"
    "students_analyzed": int,
    "high_risk_count": int,
    "at_risk_count": int,
    "recommendations": list
}
```

## 🚦 Error Handling Strategy

1. **Data Validation**: Check data before processing
2. **Try-Catch**: Graceful error handling in modules
3. **Logging**: Track errors for debugging
4. **User Feedback**: Clear error messages in UI

## 📝 API Boundaries

### Input Validation
- CSV format validation
- Data type checking
- Range validation

### Output Standardization
- Consistent JSON responses
- Typed DataFrames
- Validated reports

---

**Document Version**: 1.0
**Last Updated**: March 18, 2026
