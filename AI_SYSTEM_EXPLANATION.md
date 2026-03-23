# 🤖 Agentic AI System - Complete Explanation

**This document explains the AI/Agent components that power the AI Assistant functionality.**

---

## 📍 File Locations

The agentic AI system consists of **3 Python files** in the `ai/` folder:

```
ai/
├── ai_assistant.py       [598 lines] ← MAIN AI AGENT
├── rag_pipeline.py       [110 lines] ← RETRIEVAL-AUGMENTED GENERATION
└── vector_store.py       [169 lines] ← VECTOR DATABASE MANAGEMENT
```

---

## 🎯 What is "Agentic AI" in This System?

**Agentic AI** = An AI system that:
1. ✅ **Routes queries** to appropriate handlers (institutional procedures)
2. ✅ **Retrieves context** from student data (RAG - Retrieval-Augmented Generation)
3. ✅ **Uses LLM** (Groq) for natural language understanding
4. ✅ **Provides institutional answers** (not generic advice)
5. ✅ **Never fabricates data** (only uses actual student records)

**In simple terms**: The AI "agent" acts like a smart router that takes your question, finds relevant student data, and either answers directly from that data OR uses an LLM to generate a contextual response.

---

## 🗂️ File 1: `ai_assistant.py` (598 lines)

### **Purpose**
The **main intelligence hub** of the system. It's the decision-making agent that:
- Routes queries to 5 institutional procedures
- Falls back to LLM for flexible queries
- Ensures all answers are data-driven

### **Class: AIAssistant**

#### **Constructor: `__init__`**
```python
def __init__(self, student_df, groq_api_key=None, historical_df=None)
```

**What it does:**
- Initializes the AI agent with student data
- Sets up Groq LLM connection
- Prepares system prompt for institutional context

**Parameters:**
- `student_df` - DataFrame with 200 student records
- `groq_api_key` - API key for Groq (from env if not provided)
- `historical_df` - Previous semester data for trend analysis

**Example:**
```python
from ai.ai_assistant import AIAssistant
assistant = AIAssistant(student_df=df, groq_api_key="gsk_...")
```

---

#### **Function 1: `_ensure_numeric_types`**
```python
def _ensure_numeric_types(self, df)
```

**What it does:**
- Converts all numeric columns to proper float types
- Handles string numbers (e.g., "80" → 80.0)
- Fills missing values with 0

**Why it matters:**
- CSV files store numbers as strings
- Prevents calculation errors
- Ensures engagement score calculation works

**Columns it handles:**
- `attendance`, `lms_logins`, `assignments_submitted`, `total_assignments`
- `assignments`, `grade`, `engagement_score`

---

#### **Function 2: `_get_system_prompt`**
```python
def _get_system_prompt(self)
```

**What it does:**
- Returns the instruction prompt for the LLM
- Defines how the AI should behave
- Emphasizes institutional context over generic advice

**Key Rules Enforced:**
1. ✅ Base ONLY on student records (no fabrication)
2. ✅ Return ACTUAL students, never theoretical examples
3. ✅ Provide institutional procedures, not study tips
4. ✅ Reference specific departments (Dean, HOD, Counselors)
5. ✅ State clearly if data is insufficient

**Example response style:**
- ❌ "Students should improve time management"
- ✅ "Priya Nair (ID: 21CSE002) has 65% attendance. HOD should schedule one-on-one meeting."

---

#### **Function 3: `_get_top_engaged_students`**
```python
def _get_top_engaged_students(self, top_n=5)
```

**What it does:**
- Retrieves the TOP N engaged students from dataset
- Formats response with names, engagement scores, metrics
- Provides academic utilization procedures

**Returns:**
```
## TOP ENGAGED STUDENTS

1. Sneha Iyer
   - Engagement Score: 89.5/100
   - Attendance: 95%
   - Assignments: 10/10

2. Aman Gupta
   - Engagement Score: 87.2/100
   - ...

### ACADEMIC UTILIZATION PLAN
- Department/HOD Action: Nominate as peer mentors
- Lab Coordinator: Assign as lab teaching assistants
- Merit Recognition: Include in departmental merit lists
- Student Council: Invite to advisory councils
- Research Opportunities: Consider for research projects
```

**Data Validation:**
- Checks if student_df exists
- Checks if engagement_score column exists
- Returns error message if insufficient data

---

#### **Function 4: `_get_least_engaged_students`**
```python
def _get_least_engaged_students(self, bottom_n=5)
```

**What it does:**
- Retrieves BOTTOM N engaged students (at-risk students)
- Formats with intervention procedures
- Provides specific action items for each risk level

**Returns:**
```
## LEAST ENGAGED STUDENTS (PRIORITY INTERVENTION REQUIRED)

Critical Count: 5 students with lowest engagement

1. 21CSE006 - Priya Nair
   Engagement: 40.0/100 | Attendance: 40.0%
   
   ### INTERVENTION PROCEDURE (HIGH RISK)
   **Immediate Academic Support (Next 48 hours)**
   - Action: HOD to initiate 1-on-1 meeting
   - Purpose: Understand reasons for disengagement
   - Timeline: Schedule within 48 hours
   
   **Support Assignment (Within 1 week)**
   - Assign dedicated academic advisor/mentor
   - Refer to counseling cell for personal concerns
   - Establish daily/weekly check-in schedule
```

**Risk Categories:**
- 🔴 **HIGH RISK**: Attendance < 60% OR Assignments < 50%
- 🟡 **AT-RISK**: Engagement 60-79%
- 🟢 **LOW RISK**: Engagement ≥ 80%

---

#### **Function 5: `_get_at_risk_students`**
```python
def _get_at_risk_students(self)
```

**What it does:**
- Identifies all students with risk_level = "HIGH RISK" or "AT RISK"
- Returns list with specific intervention procedures
- Uses multi-factor detection

**Example:**
```
21CSE026 - Priya Nair
Status: HIGH RISK
- Attendance: 40.0%
- Assignments: 3/10 (30%)

Intervention: Academic probation + mandatory counseling
```

---

#### **Function 6: `_get_semester_wise_analysis`**
```python
def _get_semester_wise_analysis(self)
```

**What it does:**
- Analyzes highest LMS logins per semester
- Shows engagement patterns across time
- Identifies best/worst performing semesters

**Returns:**
```
## SEMESTER-WISE HIGHEST LMS ENGAGEMENT ANALYSIS

Semester 1:
  Best: 21CSE003 - Ritika Nair (39 logins)
  
Semester 2:
  Best: 21CSE001 - Aarav Kumar (39 logins)
  
Semester 3:
  Best: 21CSE004 - Rohan Gupta (32 logins)
```

---

#### **Function 7: `_lookup_student_data`**
```python
def _lookup_student_data(self, query)
```

**What it does:**
- Searches for specific student by name/ID
- Handles flexible semester format (1, Sem1, SEM1, "1")
- Retrieves historical data for that student

**Example Queries:**
- "Priya Nair semester 3"
- "21CSE006 SEM1"
- "Show data for student 021CSE010"

**Returns:**
```
Student: Priya Nair (21CSE006)
Semester 3:
- Attendance: 96%
- LMS Logins: 11
- Assignments: 4/10
- Grade: B
```

---

#### **Function 8: `generate_response` (MAIN ROUTER)**
```python
def generate_response(self, query)
```

**⭐ THIS IS THE MAIN AGENT FUNCTION**

**What it does:**
- Acts as the intelligent query router
- Matches user query to one of 5 institutional procedures
- Falls back to LLM for flexible queries

**How it works (Step-by-step):**

```
User Query: "Who are the top engaged students?"
           ↓
    Match keywords?
           ↓
    "top" + "engaged" found
           ↓
    Call _get_top_engaged_students()
           ↓
    Return formatted response
```

**The 5 Institutional Procedures It Routes To:**

| Query Type | Keywords | Function Called |
|-----------|----------|-----------------|
| **Top Students** | "top", "best", "engaged", "highest" | `_get_top_engaged_students()` |
| **Least Engaged** | "least", "struggling", "low", "worst", "at-risk" | `_get_least_engaged_students()` |
| **At-Risk List** | "at-risk", "risk", "intervention", "help", "support" | `_get_at_risk_students()` |
| **Semester Analysis** | "semester", "lms", "logins", "per semester" | `_get_semester_wise_analysis()` |
| **Student Lookup** | Student name or ID + semester number | `_lookup_student_data()` |

**Fallback to LLM:**
If no keywords match → Use Groq LLM for natural language understanding

**Example:**
```python
response = assistant.generate_response("Show me students who need help")
# → Matches "need help" → calls _get_at_risk_students()

response = assistant.generate_response("What's Priya's grade in semester 3?")
# → Matches student lookup → calls _lookup_student_data()

response = assistant.generate_response("How many students improved this semester?")
# → No exact match → Uses LLM via _llm_response()
```

---

#### **Function 9: `_llm_response` (LLM INTEGRATION)**
```python
def _llm_response(self, query)
```

**What it does:**
- Calls Groq LLM for flexible natural language queries
- Provides full student context to LLM
- Gets AI-generated response

**How it works:**

```python
# 1. Prepare context
context = "You have data on 200 students with..."
context += "Available student: Priya Nair, ID: 21CSE006, Engagement: 40.0, Attendance: 40%..."

# 2. Send to LLM
llm.invoke([
    SystemMessage(content=self.system_prompt),
    HumanMessage(content=query),
    HumanMessage(content=context)
])

# 3. Return LLM response
```

**Used for queries like:**
- "How many students have wellbeing concerns?"
- "Which students improved from semester 2 to 3?"
- "What's the average attendance by semester?"

---

---

## 🗂️ File 2: `rag_pipeline.py` (110 lines)

### **Purpose**
Implements **RAG (Retrieval-Augmented Generation)** - a system that retrieves relevant student data before generating responses. This ensures the AI answers are grounded in actual data.

### **Class: RAGPipeline**

#### **What is RAG?**

**RAG = Retrieval + Augmented + Generation**

```
User Query
    ↓
RETRIEVE relevant student records (via embeddings)
    ↓
AUGMENT the query with retrieved context
    ↓
GENERATE response based on context
    ↓
Return data-driven answer
```

**Why RAG matters:**
- ✅ Reduces "hallucinations" (AI making up answers)
- ✅ Grounds responses in actual student data
- ✅ Improves accuracy and relevance

---

#### **Constructor: `__init__`**
```python
def __init__(self, model_name="all-MiniLM-L6-v2")
```

**What it does:**
- Initializes embedding model (converts text to vectors)
- Sets up ChromaDB vector store
- Prepares for document indexing

**Embedding Model:**
- `all-MiniLM-L6-v2` - Fast, lightweight sentence embedding
- Converts text into 384-dimensional vectors
- Used for semantic similarity search

---

#### **Function 1: `index_student_data`**
```python
def index_student_data(self, df)
```

**What it does:**
- Converts student records into embeddings
- Stores in ChromaDB vector database
- Prepares for semantic search

**Steps:**
```
1. Create ChromaDB collection
2. Convert students to documents:
   "Student: Priya Nair, ID: 21CSE006, Engagement: 40.0, Attendance: 40%..."
3. Generate embeddings (text → vectors)
4. Store in vector database
```

**Why embeddings?**
- Semantic search: Find similar students based on meaning
- Query: "Who's struggling?" → Finds low-engagement students
- Fast retrieval: Vector similarity is faster than text search

---

#### **Function 2: `retrieve_context`**
```python
def retrieve_context(self, query, top_k=5)
```

**What it does:**
- Takes user query
- Converts to embedding
- Finds most similar student records
- Returns top K results

**Example:**
```python
query = "Which students have low engagement?"

# RAG Pipeline does:
1. Convert "Which students have low engagement?" to vector
2. Find 5 most similar student records in database
3. Return those 5 students' full data

# Result:
["Student: Priya Nair, Engagement: 40.0, ...",
 "Student: Rohan Gupta, Engagement: 45.0, ...",
 ...]
```

**Parameters:**
- `query` - User question
- `top_k` - Number of results (default: 5)

---

#### **Function 3: `retrieve_context_with_metadata`** ⭐
```python
def retrieve_context_with_metadata(self, query, top_k=5)
```

**What it does:**
- Same as `retrieve_context()` BUT
- **Also returns metadata** (student_id, name, etc.)
- Returns as structured dictionary

**Returns:**
```python
[
    {
        'document': "Student: Priya Nair, Engagement: 40.0, ...",
        'metadata': {
            'student_id': '21CSE006',
            'name': 'Priya Nair',
            'engagement': 40.0,
            'risk_level': 'HIGH'
        }
    },
    {
        'document': "Student: Rohan Gupta, Engagement: 45.0, ...",
        'metadata': {
            'student_id': '21CSE004',
            ...
        }
    }
]
```

**Why separate metadata?**
- ✅ Easier to parse and process
- ✅ Can access data programmatically
- ✅ Better for LLM context building

---

#### **Function 4: `answer_query`**
```python
def answer_query(self, query, llm_response)
```

**What it does:**
- Combines retrieval + LLM response
- Returns comprehensive answer with context
- Useful for audit trail

**Returns:**
```python
{
    'query': "Who needs help?",
    'context': "Retrieved 5 student records...",
    'response': "LLM generated response based on context",
    'context_count': 5
}
```

**Use case:**
```python
context = rag.retrieve_context("Who needs help?", top_k=3)
llm_answer = llm.invoke(context)  # LLM generates answer from context
final_answer = rag.answer_query("Who needs help?", llm_answer)
```

---

#### **Function 5: `perform_rag_retrieval` (Helper)**
```python
def perform_rag_retrieval(student_df, query, top_k=5)
```

**What it does:**
- Standalone function (doesn't require class instantiation)
- Performs complete RAG pipeline in one call
- Useful for quick retrieval

**Example:**
```python
results = perform_rag_retrieval(
    student_df=df,
    query="Students with attendance problems",
    top_k=10
)

# Returns:
# {
#     'query': "Students with attendance problems",
#     'results': [5 student records],
#     'count': 5
# }
```

---

---

## 🗂️ File 3: `vector_store.py` (169 lines)

### **Purpose**
Manages **ChromaDB** - the vector database that stores and retrieves student data embeddings.

### **Class: VectorStore**

#### **What is ChromaDB?**

**ChromaDB** = Vector database optimized for embedding storage and semantic search

**Why use it?**
- ✅ Fast semantic search (find similar records)
- ✅ Handles embeddings efficiently
- ✅ Persistent storage (survives restarts)
- ✅ Built for AI applications

---

#### **Constructor: `__init__`**
```python
def __init__(self, persist_dir="./chroma_db")
```

**What it does:**
- Initializes ChromaDB connection
- Sets up persistent storage directory
- Configures for cosine similarity search

**Parameters:**
- `persist_dir` - Where to store vector database (default: `./chroma_db/`)

**Storage:**
- Creates a local database directory
- Persists across sessions
- No external service needed

---

#### **Function 1: `create_collection`**
```python
def create_collection(self, name="student_records")
```

**What it does:**
- Creates a new collection (like a table in SQL)
- Deletes old collection if exists
- Configures similarity metric (cosine)

**Collections = Organized storage**
```
ChromaDB
├── student_records (collection)
│   ├── Document 1 + Embedding
│   ├── Document 2 + Embedding
│   └── Document 3 + Embedding
│
└── other_collection (collection)
```

**Cosine Similarity:**
- Measures angle between vectors
- Perfect for finding similar students
- Range: 0 (opposite) to 1 (identical)

---

#### **Function 2: `add_documents`**
```python
def add_documents(self, documents, ids, metadatas=None)
```

**What it does:**
- Adds student documents to vector store
- ChromaDB automatically generates embeddings
- Associates metadata (student_id, name, etc.)

**Parameters:**
- `documents` - List of text descriptions (e.g., "Student: Priya...")
- `ids` - Unique identifier for each (e.g., "21CSE006")
- `metadatas` - Extra info (optional)

**Example:**
```python
vector_store.add_documents(
    documents=[
        "Student: Priya Nair, Engagement: 40.0, Attendance: 40%",
        "Student: Rohan Gupta, Engagement: 92.5, Attendance: 95%",
    ],
    ids=["21CSE006", "21CSE004"],
    metadatas=[
        {'risk_level': 'HIGH', 'name': 'Priya Nair'},
        {'risk_level': 'LOW', 'name': 'Rohan Gupta'},
    ]
)
```

---

#### **Function 3: `search`** ⭐ KEY FUNCTION
```python
def search(self, query, n_results=5)
```

**What it does:**
- Searches vector database for similar students
- Returns top N matches based on semantic similarity
- **This is where RAG magic happens**

**How it works:**

```
Input: "Who has low attendance?"
           ↓
1. Convert query to embedding (vector)
2. Calculate similarity to all student vectors
3. Sort by similarity score
4. Return top 5 most similar students
           ↓
Output: Students with low attendance
```

**Returns:**
```python
{
    'documents': [
        "Student: Priya Nair, Engagement: 40.0, Attendance: 40%",
        "Student: Rajesh Kumar, Engagement: 45.0, Attendance: 50%",
        ...
    ],
    'ids': ["21CSE006", "21CSE010", ...],
    'metadatas': [
        {'risk_level': 'HIGH', ...},
        {'risk_level': 'AT RISK', ...},
        ...
    ],
    'distances': [0.15, 0.23, ...]  # Lower = more similar
}
```

**Parameters:**
- `query` - Search query (natural language)
- `n_results` - Number of results (default: 5)

**Example Queries That Work:**
- "Low engagement students"
- "High attendance"
- "Improving trends"
- "Wellbeing concerns"

---

#### **Helper Function: `create_student_documents`**
```python
def create_student_documents(df)
```

**What it does:**
- Converts DataFrame rows into text documents
- Creates embeddings-friendly format
- Generates metadata for each student

**Example Output:**
```
Document: "Student: Priya Nair (21CSE006). Engagement Score: 40.0/100. 
           Attendance: 40%. Assignments: 3/10. LMS Logins: 5. 
           Risk Level: HIGH RISK. Status: Needs immediate intervention."

ID: "21CSE006"

Metadata: {
    'student_id': '21CSE006',
    'name': 'Priya Nair',
    'engagement_score': 40.0,
    'attendance': 40,
    'risk_level': 'HIGH RISK'
}
```

---

---

## 🔄 How All 3 Components Work Together

### **Complete AI Flow Example:**

**User asks:** "Who are the students struggling the most?"

```
Step 1: User Query
    ↓
app.py (user interface)
    ↓
Step 2: AIAssistant.generate_response()
    ├─ Check keywords: "struggling", "most"
    ├─ Matches "least engaged" pattern
    ├─ Calls _get_least_engaged_students()
    ├─ Returns formatted list with interventions
    ↓
Step 3: Return to User
    ├─ Show: Top 5 struggling students
    ├─ Show: Risk levels
    ├─ Show: Intervention procedures
    ├─ Show: Contact person (HOD, Counselor)
```

---

### **Complex Query Flow (Using RAG + LLM):**

**User asks:** "How many students improved from last semester?"

```
Step 1: User Query
    ↓
Step 2: AIAssistant.generate_response()
    ├─ Check keywords
    ├─ No exact match → Fallback to LLM
    ├─ Call _llm_response()
    ↓
Step 3: RAG Pipeline Activation
    ├─ rag_pipeline.retrieve_context(query, top_k=10)
    ├─ vector_store.search(query)
    ├─ Find 10 students with improvement patterns
    ├─ Return with metadata
    ↓
Step 4: LLM Processing
    ├─ Pass query + context to Groq LLM
    ├─ LLM analyzes: "These 10 students improved"
    ├─ LLM generates: "5 students improved significantly..."
    ↓
Step 5: Return Final Answer
    ├─ "Based on analysis: 5 students improved 
    |   from semester 2 to 3"
    └─ Lists specific students with metrics
```

---

## 📊 Query Routing Decision Tree

```
User Query: "?"
    ↓
AIAssistant.generate_response()
    ↓
    ├─ Contains "top" + "engaged"?
    │  └─ YES → _get_top_engaged_students()
    │
    ├─ Contains "least" / "struggling"?
    │  └─ YES → _get_least_engaged_students()
    │
    ├─ Contains "risk" / "help" / "support"?
    │  └─ YES → _get_at_risk_students()
    │
    ├─ Contains "semester" + number?
    │  └─ YES → _get_semester_wise_analysis()
    │
    ├─ Contains student name + semester?
    │  └─ YES → _lookup_student_data()
    │
    └─ No match?
       └─ USE LLM (_llm_response)
          ├─ RAG retrieves context
          ├─ LLM generates answer
          └─ Return response
```

---

## 🎯 Key Design Principles

### **1. Institutional First**
- All responses formatted for college administrators
- Action items reference departments (HOD, Dean, Counselors)
- Never generic study advice

### **2. Data-Driven**
- Only uses actual student records (no hallucinations)
- Specific names and metrics
- Clear citation of data sources

### **3. Failure-Safe**
- Checks for data availability
- Returns "Insufficient data" if needed
- Never invents students

### **4. Efficient**
- Keyword matching for quick queries
- RAG for semantic search
- LLM only when needed

### **5. Transparent**
- Shows how conclusion was reached
- Cites specific student records
- Explains intervention procedures

---

## 🔌 Integration with Streamlit App

**In `app.py` (AI Assistant page):**

```python
# Initialize
assistant = AIAssistant(
    student_df=df,
    historical_df=historical_df,
    groq_api_key=GROQ_API_KEY
)

# Get response
user_query = st.text_input("Ask a question about students")
response = assistant.generate_response(user_query)

# Display
st.markdown(response)
```

**The flow:**
1. User types question in Streamlit
2. Passes to AIAssistant.generate_response()
3. Routes to appropriate function or LLM
4. Returns formatted response
5. Displays in Streamlit UI

---

## 📈 Performance Metrics

| Operation | Time | Tool |
|-----------|------|------|
| Keyword matching | < 10ms | AIAssistant |
| Data lookup | < 100ms | Direct DataFrame |
| RAG retrieval | < 500ms | VectorStore + RAG |
| LLM response | 2-5 seconds | Groq API |

---

## 🚀 Example Usage

### **In Your Code:**

```python
from ai.ai_assistant import AIAssistant
from modules.data_loader import load_student_data
import pandas as pd

# Load data
df = load_student_data('data/students.csv')
historical_df = pd.read_csv('data/historical_semesters.csv')

# Initialize AI Assistant
assistant = AIAssistant(
    student_df=df,
    historical_df=historical_df,
    groq_api_key="gsk_..."
)

# Query Examples:
print(assistant.generate_response("Who are my top engaged students?"))
# → Shows top 5 with utilization procedures

print(assistant.generate_response("Which students need help?"))
# → Shows at-risk students with interventions

print(assistant.generate_response("Show Priya's progress in semester 3"))
# → Shows specific student data with trends

print(assistant.generate_response("How many improved this semester?"))
# → Uses LLM to analyze and answer
```

---

## ✅ Summary Table

| Component | File | Purpose | Key Function |
|-----------|------|---------|--------------|
| **AI Agent** | `ai_assistant.py` | Query routing & decisions | `generate_response()` |
| **RAG System** | `rag_pipeline.py` | Semantic search & retrieval | `retrieve_context_with_metadata()` |
| **Vector DB** | `vector_store.py` | Embedding storage | `search()` |

---

## 🎓 Learning Path

To understand agentic AI, study in this order:

1. **Start**: `ai_assistant.py` → understand routing logic
2. **Then**: `rag_pipeline.py` → understand retrieval
3. **Finally**: `vector_store.py` → understand storage

Or if you prefer bottom-up:

1. **Start**: `vector_store.py` → understand embeddings
2. **Then**: `rag_pipeline.py` → understand search
3. **Finally**: `ai_assistant.py` → understand routing

---

**That's the complete agentic AI system! 🤖**

Questions? Check the inline code comments in each file.
