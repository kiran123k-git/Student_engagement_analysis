# 🤖 Agentic AI - Quick Reference Guide

## File Locations & Sizes

```
ai/
├── ai_assistant.py     [598 lines] ← MAIN INTELLIGENCE
├── rag_pipeline.py     [110 lines] ← RETRIEVAL SYSTEM
└── vector_store.py     [169 lines] ← DATABASE
```

---

## Core Classes & Key Functions

### **AIAssistant** (`ai_assistant.py`)

| Function | Purpose | Returns |
|----------|---------|---------|
| `__init__()` | Initialize with student data | Assistant object |
| `_ensure_numeric_types()` | Convert strings to numbers | DataFrame |
| `_get_system_prompt()` | AI behavior instructions | System prompt |
| `_get_top_engaged_students()` | Get best 5 students | Formatted text + procedures |
| `_get_least_engaged_students()` | Get worst 5 students | Formatted text + interventions |
| `_get_at_risk_students()` | List all at-risk students | Student list with actions |
| `_get_semester_wise_analysis()` | LMS trends per semester | Semester analysis |
| `_lookup_student_data()` | Find specific student | Student record + history |
| `generate_response()` | ⭐ MAIN ROUTER | Response (from procedures or LLM) |
| `_llm_response()` | Call Groq LLM | LLM-generated answer |

### **RAGPipeline** (`rag_pipeline.py`)

| Function | Purpose | Returns |
|----------|---------|---------|
| `__init__()` | Setup embedding model | RAG object |
| `index_student_data()` | Convert to embeddings | Success/failure |
| `retrieve_context()` | Find similar students | List of documents |
| `retrieve_context_with_metadata()` | ⭐ MAIN RETRIEVAL | Documents + metadata dict |
| `answer_query()` | Combine context + LLM | Complete answer dict |
| `perform_rag_retrieval()` | Standalone RAG | Results dict |

### **VectorStore** (`vector_store.py`)

| Function | Purpose | Returns |
|----------|---------|---------|
| `__init__()` | Connect to ChromaDB | VectorStore object |
| `create_collection()` | Create storage table | Success/failure |
| `add_documents()` | Store embeddings | Success/failure |
| `search()` | ⭐ FIND SIMILAR | Documents + ids + metadata + distances |

---

## Query Routing Logic

```
"Who are the top engaged?"
    ↓
Keywords match: "top" + "engaged"
    ↓
Route to: _get_top_engaged_students()
    ↓
Return: Top 5 students + utilization procedures

---

"Show Priya's semester 3 data"
    ↓
Keywords match: student name + "semester" + number
    ↓
Route to: _lookup_student_data("Priya", "3")
    ↓
Return: Specific student record + history

---

"How many improved this semester?"
    ↓
No keyword match
    ↓
Route to: _llm_response()
    ├─ RAG retrieves: Relevant student records
    ├─ LLM analyzes: Patterns in data
    ├─ LLM generates: Contextual answer
    ↓
Return: "5 students improved significantly"
```

---

## Data Flow: User Query → Response

### Simple Query (Direct Routing)

```
User: "Show top engaged students"
  ↓
AIAssistant.generate_response()
  ├─ Match keywords
  ├─ No LLM needed
  ├─ Call _get_top_engaged_students()
  ├─ Return top 5 + procedures
  ↓
Display to user
```

### Complex Query (RAG + LLM)

```
User: "How many students struggled this semester and why?"
  ↓
AIAssistant.generate_response()
  ├─ No keyword match
  ├─ Call _llm_response()
  │   ↓
  │   RAGPipeline.retrieve_context_with_metadata()
  │   ├─ VectorStore.search(query)
  │   ├─ Find similar students
  │   ├─ Return top K with metadata
  │   ↓
  │   Groq LLM
  │   ├─ Receive: query + context
  │   ├─ Analyze: student patterns
  │   ├─ Generate: contextual answer
  │   ↓
  │   Return: "X students struggled, reasons..."
  ↓
Display to user
```

---

## AI Decision Tree

```
generate_response(query)
│
├─ "top" + "engaged"?           → _get_top_engaged_students()
├─ "least" / "struggling"?      → _get_least_engaged_students()
├─ "risk" / "help"?             → _get_at_risk_students()
├─ "semester" + number?         → _get_semester_wise_analysis()
├─ student_name + semester?     → _lookup_student_data()
│
└─ No match?                    → _llm_response()
                                    ├─ RAG retrieval
                                    ├─ LLM analysis
                                    └─ Return answer
```

---

## Vector Database (ChromaDB) Flow

```
Input: Student DataFrame
  ↓
RAGPipeline.index_student_data()
  ├─ create_student_documents()  (convert rows to text)
  ├─ ChromaDB auto-generates embeddings
  ├─ VectorStore.create_collection()
  ├─ VectorStore.add_documents()
  ↓
Store in ChromaDB
  │
  ├─ Document: "Student: Priya Nair, Engagement: 40.0..."
  ├─ ID: "21CSE006"
  ├─ Metadata: {student_id, name, risk_level, ...}
  ├─ Embedding: [0.12, -0.45, 0.89, ...] (384-dim vector)
  │
  └─ (100+ more students)
  ↓
Later: User asks "Who has low engagement?"
  ├─ VectorStore.search(query)
  ├─ Convert query to embedding
  ├─ Find 5 most similar students
  ├─ Calculate similarity distances
  ↓
Return: [student1, student2, ...] with metadata
```

---

## Function: `retrieve_context_with_metadata()`

**Location**: `rag_pipeline.py` line 65-81

**Input:**
```python
query = "Which students need help?"
top_k = 5
```

**What happens inside:**
```
1. Call: VectorStore.search(query, n_results=5)
   └─ Returns: {documents, ids, metadatas, distances}

2. Combine:
   documents = [doc1, doc2, doc3, doc4, doc5]
   metadatas = [{meta1}, {meta2}, {meta3}, {meta4}, {meta5}]

3. Package as dicts:
   [
       {
           'document': "Student: Priya...",
           'metadata': {'student_id': '21CSE006', ...}
       },
       {
           'document': "Student: Rohan...",
           'metadata': {'student_id': '21CSE004', ...}
       },
       ...
   ]

4. Return: combined list
```

**Output:**
```python
[
    {
        'document': "Student: Priya Nair (21CSE006). Engagement: 40.0/100. 
                     Attendance: 40%. Assignments: 3/10. Risk: HIGH",
        'metadata': {
            'student_id': '21CSE006',
            'name': 'Priya Nair',
            'engagement_score': 40.0,
            'attendance': 40,
            'risk_level': 'HIGH RISK'
        }
    },
    {
        'document': "Student: Rohan Gupta (21CSE004). Engagement: 45.0/100...",
        'metadata': {...}
    },
    ...
]
```

---

## Key Algorithms

### Algorithm 1: Query Routing

```python
def generate_response(query):
    # Convert to lowercase for matching
    query_lower = query.lower()
    
    # Check each pattern
    if ("top" in query_lower and "engaged" in query_lower):
        return _get_top_engaged_students()
    
    elif any(word in query_lower for word in ["least", "struggling", "low"]):
        return _get_least_engaged_students()
    
    elif any(word in query_lower for word in ["risk", "help", "support"]):
        return _get_at_risk_students()
    
    elif "semester" in query_lower:
        return _get_semester_wise_analysis()
    
    elif is_student_lookup(query):
        student_name, semester = parse_student_query(query)
        return _lookup_student_data(student_name, semester)
    
    else:
        return _llm_response(query)
```

### Algorithm 2: Semantic Search

```python
def search(query):
    # 1. Convert query to embedding
    query_embedding = embedding_model.encode(query)
    # → [0.15, -0.42, 0.89, ..., 0.12]  (384 dimensions)
    
    # 2. Compare to all student embeddings
    for student in all_students:
        distance = cosine_distance(query_embedding, student_embedding)
        scores.append((student, distance))
    
    # 3. Sort by distance (lower = more similar)
    scores.sort()
    
    # 4. Return top K
    return scores[:n_results]
```

### Algorithm 3: LLM Integration

```python
def _llm_response(query):
    # 1. Get context from RAG
    context = rag_pipeline.retrieve_context_with_metadata(query, top_k=5)
    
    # 2. Build context string
    context_str = format_context(context)
    
    # 3. Create messages for LLM
    messages = [
        SystemMessage(content=self.system_prompt),  # Instructions
        HumanMessage(content=query),                # User question
        HumanMessage(content=context_str)           # Retrieved context
    ]
    
    # 4. Call Groq LLM
    response = self.llm.invoke(messages)
    
    # 5. Return response
    return response.content
```

---

## Institutional Procedures Enforced

### For Top Engaged Students:
```
✓ Nominate as peer mentors
✓ Assign as lab teaching assistants
✓ Include in merit lists
✓ Invite to student councils
✓ Offer research opportunities
```

### For At-Risk Students:
```
✓ HIGH RISK: Immediate HOD meeting + counselor referral
✓ AT-RISK: Personalized tutoring + progress monitoring
✓ LOW-RISK: Maintain current engagement
```

### For Wellbeing Concerns:
```
✓ Refer to counseling cell
✓ Schedule check-ins
✓ Connect with mentors
✓ Provide support resources
```

---

## Error Handling

**What if student data missing?**
```python
if self.student_df is None or len(self.student_df) == 0:
    return "Insufficient data in retrieved records to answer this query."
```

**What if engagement_score column missing?**
```python
if 'engagement_score' not in self.student_df.columns:
    return "Insufficient data in retrieved records to answer this query."
```

**What if LLM fails?**
```python
try:
    response = self.llm.invoke(messages)
    return response.content
except Exception as e:
    return f"Could not generate response: {str(e)}"
```

**What if vector search returns no results?**
```python
results = self.vector_store.search(query, n_results=top_k)
if not results or len(results['documents']) == 0:
    return []
```

---

## Configuration & Constants

**In `ai_assistant.py`:**
```python
# Groq LLM Configuration
model_name = "llama-3.1-8b-instant"
temperature = 0.5  # Lower = more factual (not creative)
```

**In `rag_pipeline.py`:**
```python
# Embedding Model
model_name = "all-MiniLM-L6-v2"  # 384-dimensional embeddings
```

**In `vector_store.py`:**
```python
# ChromaDB Configuration
similarity_metric = "cosine"  # Vector similarity measure
persist_directory = "./chroma_db"  # Storage location
```

---

## Performance Tips

| Optimization | Method |
|---|---|
| **Faster queries** | Use direct routing (keyword matching) instead of LLM |
| **Better relevance** | Use RAG to ground LLM responses in actual data |
| **Reduced cost** | Groq API is cheaper than OpenAI |
| **Offline capability** | Vector DB works locally (no external calls needed) |

---

## Integration Example

**In Streamlit app:**

```python
from ai.ai_assistant import AIAssistant

# Initialize once
@st.cache_resource
def get_assistant():
    return AIAssistant(
        student_df=load_student_data(),
        historical_df=load_historical_data(),
        groq_api_key="gsk_..."
    )

# Use on every query
assistant = get_assistant()
query = st.text_input("Ask about students:")
response = assistant.generate_response(query)
st.markdown(response)
```

---

## Summary

| Component | What It Does | Used For |
|-----------|------|----------|
| **AIAssistant** | Routes queries, makes decisions | Main query handler |
| **RAGPipeline** | Retrieves relevant context | Grounding LLM responses |
| **VectorStore** | Stores/searches embeddings | Fast semantic search |

**Flow: Query → Routing → Context → Response**

---

**Complete AI System Explained! 🚀**
