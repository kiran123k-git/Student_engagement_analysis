# 🤖 Agentic AI - Function-by-Function Reference

## Quick Navigation

- **Want overview?** → Read [AI_QUICK_REFERENCE.md](AI_QUICK_REFERENCE.md)
- **Want deep dive?** → Read [AI_SYSTEM_EXPLANATION.md](AI_SYSTEM_EXPLANATION.md)
- **Want code details?** → Read this file

---

## File: `ai_assistant.py` (598 lines)

### **Function 1: `__init__()`**

**Location:** Line 24-44

**Code:**
```python
def __init__(self, student_df=None, groq_api_key=None, historical_df=None):
    if student_df is not None:
        student_df = self._ensure_numeric_types(student_df)
    if historical_df is not None:
        historical_df = self._ensure_numeric_types(historical_df)
    
    self.student_df = student_df
    self.historical_df = historical_df
    self.api_key = groq_api_key or os.getenv('GROQ_API_KEY')
    self.system_prompt = self._get_system_prompt()
    
    if LANGCHAIN_AVAILABLE and self.api_key:
        try:
            self.llm = ChatGroq(
                groq_api_key=self.api_key,
                model_name="llama-3.1-8b-instant",
                temperature=0.5
            )
```

**What it does:**
- Creates AIAssistant instance
- Loads student data with type conversion
- Initializes Groq LLM connection
- Prepares system prompt

**Parameters:**
- `student_df` - DataFrame with 200 student records
- `groq_api_key` - API key (from env if None)
- `historical_df` - Previous semester data

**Usage:**
```python
assistant = AIAssistant(
    student_df=df,
    groq_api_key="gsk_...",
    historical_df=hist_df
)
```

---

### **Function 2: `_ensure_numeric_types()`**

**Location:** Line 46-60

**Code:**
```python
def _ensure_numeric_types(self, df):
    df = df.copy()
    numeric_cols = ['attendance', 'lms_logins', 'assignments_submitted', 
                   'total_assignments', 'assignments', 'grade', 'engagement_score']
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    return df
```

**What it does:**
- Converts string numbers to floats
- Handles missing values (fills with 0)
- Prevents calculation errors

**Example:**
- Input: `attendance = "80"` (string)
- Output: `attendance = 80.0` (float)

**Why needed:**
- CSVs store numbers as strings
- Prevents TypeError in calculations

---

### **Function 3: `_get_system_prompt()`**

**Location:** Line 62-88

**What it does:**
- Returns instruction prompt for LLM behavior
- Defines institutional decision-support mode
- Emphasizes data-driven responses

**Key Rules:**
```
1. Base ALL answers ONLY on retrieved student records
2. NEVER provide generic advice
3. For list queries, return ACTUAL students
4. NEVER invent students
5. Provide institutional procedures
6. Reference specific departments
```

**Returns:**
```python
"You are an Academic Analytics Decision-Support AI...
Base ALL answers ONLY on retrieved student records...
NEVER invent students not present in the data..."
```

---

### **Function 4: `_get_top_engaged_students()`**

**Location:** Line 90-120

**Code:**
```python
def _get_top_engaged_students(self, top_n=5):
    if self.student_df is None or len(self.student_df) == 0:
        return "Insufficient data..."
    
    if 'engagement_score' not in self.student_df.columns:
        return "Insufficient data..."
    
    top_students = self.student_df.nlargest(min(top_n, len(self.student_df)), 
                                            'engagement_score')
    
    response = "## TOP ENGAGED STUDENTS\n\n"
    for idx, (_, row) in enumerate(top_students.iterrows(), 1):
        name = row.get('name', 'Unknown')
        eng_score = row.get('engagement_score', 'N/A')
        attendance = row.get('attendance', 'N/A')
        assignments = row.get('assignments_submitted', 'N/A')
        
        response += f"{idx}. **{name}**\n"
        response += f"   - Engagement Score: {eng_score}/100\n"
        response += f"   - Attendance: {attendance}%\n"
```

**What it does:**
- Gets top N engaged students
- Formats with names and metrics
- Adds utilization procedures

**Returns:**
```
## TOP ENGAGED STUDENTS

1. Sneha Iyer
   - Engagement Score: 89.5/100
   - Attendance: 95%
   - Assignments: 10/10

### ACADEMIC UTILIZATION PLAN
- Department/HOD Action: Nominate as peer mentors
- Lab Coordinator: Assign as lab teaching assistants
- Merit Recognition: Include in merit lists
- Student Council: Invite to advisory councils
- Research Opportunities: Consider for research projects
```

---

### **Function 5: `_get_least_engaged_students()`**

**Location:** Line 122-180

**Code:**
```python
def _get_least_engaged_students(self, bottom_n=5):
    if self.student_df is None:
        return "Insufficient data..."
    
    least_students = self.student_df.nsmallest(min(bottom_n, len(self.student_df)), 
                                               'engagement_score')
    
    response = "## LEAST ENGAGED STUDENTS (PRIORITY INTERVENTION REQUIRED)\n\n"
    
    for idx, (_, row) in enumerate(least_students.iterrows(), 1):
        name = row.get('name', 'Unknown')
        engagement = row.get('engagement_score', 'N/A')
        attendance = row.get('attendance', 'N/A')
        
        response += f"{idx}. {row['student_id']} - {name}\n"
        response += f"Engagement: {engagement}/100 | Attendance: {attendance}%\n"
        
        # Add intervention based on risk level
        if attendance < 60:
            response += "### INTERVENTION PROCEDURE (HIGH RISK)\n"
            response += "**Immediate Academic Support (Next 48 hours)**\n"
            response += "- Action: HOD to initiate 1-on-1 meeting\n"
```

**What it does:**
- Gets bottom N engaged students (at-risk)
- Formats with detailed info
- Adds risk-based intervention procedures

**Risk Levels:**
- 🔴 **HIGH RISK**: Attendance < 60% OR Assignments < 50%
- 🟡 **AT-RISK**: Engagement 60-79%

---

### **Function 6: `_get_at_risk_students()`**

**Location:** Line 182-230

**Code:**
```python
def _get_at_risk_students(self):
    if self.student_df is None:
        return "Insufficient data..."
    
    # Filter for risk_level column
    at_risk = self.student_df[
        self.student_df['risk_level'].isin(['HIGH RISK', 'AT RISK'])
    ]
    
    response = "## AT-RISK STUDENTS\n\n"
    response += f"**Total At-Risk Count: {len(at_risk)}**\n\n"
    
    for _, row in at_risk.iterrows():
        response += f"{row['student_id']} - {row['name']}\n"
        response += f"Status: {row['risk_level']}\n"
        response += f"Engagement: {row['engagement_score']}\n"
```

**What it does:**
- Lists all at-risk students
- Groups by risk level
- Provides intervention procedures

**Returns:**
```
## AT-RISK STUDENTS

Total At-Risk Count: 139

21CSE006 - Priya Nair
Status: HIGH RISK
Engagement: 40.0
- Attendance: 40.0%
- Assignments: 3/10

Intervention: Academic probation + mandatory counseling
```

---

### **Function 7: `_get_semester_wise_analysis()`**

**Location:** Line 232-280

**Code:**
```python
def _get_semester_wise_analysis(self):
    if self.historical_df is None:
        return "Insufficient historical data..."
    
    response = "## SEMESTER-WISE HIGHEST LMS ENGAGEMENT\n\n"
    
    # Group by semester
    for semester in sorted(self.historical_df['semester'].unique()):
        semester_data = self.historical_df[
            self.historical_df['semester'] == semester
        ]
        
        # Get highest LMS logins
        best_student = semester_data.loc[semester_data['lms_logins'].idxmax()]
        
        response += f"Semester {semester}:\n"
        response += f"  Best: {best_student['student_id']} - "
        response += f"{best_student['name']} ({best_student['lms_logins']} logins)\n"
```

**What it does:**
- Analyzes LMS activity per semester
- Shows best-performing student each semester
- Identifies engagement patterns

**Returns:**
```
## SEMESTER-WISE HIGHEST LMS ENGAGEMENT

Semester 1:
  Best: 21CSE003 - Ritika Nair (39 logins)

Semester 2:
  Best: 21CSE001 - Aarav Kumar (39 logins)

Semester 3:
  Best: 21CSE004 - Rohan Gupta (32 logins)
```

---

### **Function 8: `_lookup_student_data()`**

**Location:** Line 282-350

**Code:**
```python
def _lookup_student_data(self, query):
    # Parse query for student name/ID and semester
    parts = query.lower().split()
    
    # Find semester number
    semester = None
    for part in parts:
        if part.isdigit():
            semester = int(part)
        elif 'sem' in part:
            semester = int(''.join(filter(str.isdigit, part)))
    
    # Find student (by name or ID)
    student = None
    query_lower = query.lower()
    
    for _, row in self.student_df.iterrows():
        if (row['name'].lower() in query_lower or 
            row['student_id'].lower() in query_lower):
            student = row
            break
    
    if student is None:
        return "Student not found in records."
    
    if semester and self.historical_df is not None:
        # Get historical data
        history = self.historical_df[
            (self.historical_df['student_id'] == student['student_id']) &
            (self.historical_df['semester'] == semester)
        ]
```

**What it does:**
- Parses student query (name/ID + semester)
- Looks up specific student
- Returns individual record with history

**Handles multiple formats:**
- "Priya Nair semester 3"
- "21CSE006 SEM1"
- "Show data for 021CSE010 in sem 3"

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

### **Function 9: `generate_response()` ⭐ MAIN FUNCTION**

**Location:** Line 352-400

**Code:**
```python
def generate_response(self, query):
    query_lower = query.lower()
    
    # Check each pattern
    if any(word in query_lower for word in ["top", "best"]) and \
       any(word in query_lower for word in ["engaged", "engagement"]):
        return self._get_top_engaged_students()
    
    elif any(word in query_lower for word in ["least", "worst", "struggling", "low"]):
        return self._get_least_engaged_students()
    
    elif any(word in query_lower for word in ["risk", "at-risk", "help", "support"]):
        return self._get_at_risk_students()
    
    elif "semester" in query_lower:
        return self._get_semester_wise_analysis()
    
    elif any(char.isdigit() for char in query):  # Contains number (ID or semester)
        return self._lookup_student_data(query)
    
    else:
        return self._llm_response(query)
```

**What it does:**
- Routes query to appropriate handler
- Uses keyword matching
- Falls back to LLM

**Decision Tree:**
```
"top" + "engaged" → _get_top_engaged_students()
"least" / "struggling" → _get_least_engaged_students()
"risk" / "help" → _get_at_risk_students()
"semester" → _get_semester_wise_analysis()
student_name + number → _lookup_student_data()
else → _llm_response()
```

---

### **Function 10: `_llm_response()` (LLM Integration)**

**Location:** Line 402-460

**Code:**
```python
def _llm_response(self, query):
    if not self.llm:
        return "LLM not available. Please check Groq API key."
    
    # Get context from RAG
    try:
        from ai.rag_pipeline import perform_rag_retrieval
        rag_results = perform_rag_retrieval(
            self.student_df, 
            query, 
            top_k=10
        )
        context_str = self._format_rag_context(rag_results['results'])
    except:
        context_str = "Student data available for analysis."
    
    # Create messages
    messages = [
        SystemMessage(content=self.system_prompt),
        HumanMessage(content=f"Query: {query}"),
        HumanMessage(content=f"Context: {context_str}")
    ]
    
    try:
        response = self.llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"Error calling LLM: {str(e)}"
```

**What it does:**
- Calls Groq LLM for flexible queries
- Uses RAG for context
- Returns AI-generated answer

**Flow:**
1. Retrieve context via RAG
2. Create prompt with context
3. Call Groq LLM
4. Return response

---

---

## File: `rag_pipeline.py` (110 lines)

### **Class: RAGPipeline**

#### **Function 1: `__init__()`**

**Location:** Line 18-30

**Code:**
```python
def __init__(self, model_name="all-MiniLM-L6-v2"):
    try:
        self.embedding_model = SentenceTransformer(model_name)
    except Exception as e:
        print(f"Warning: Could not load embedding model: {str(e)}")
        self.embedding_model = None
    
    self.vector_store = VectorStore()
    self.student_data = None
```

**What it does:**
- Initializes embedding model
- Sets up vector store
- Prepares for document indexing

**Embedding Model:**
- `all-MiniLM-L6-v2` - 384-dimensional vectors
- Fast and lightweight
- Perfect for semantic search

---

#### **Function 2: `index_student_data()`**

**Location:** Line 32-52

**Code:**
```python
def index_student_data(self, df):
    try:
        self.student_data = df
        
        # Create collection
        if not self.vector_store.create_collection("student_records"):
            return False
        
        # Convert to documents
        documents, ids, metadatas = create_student_documents(df)
        
        # Add to vector store
        return self.vector_store.add_documents(documents, ids, metadatas)
    except Exception as e:
        print(f"Error indexing data: {str(e)}")
        return False
```

**What it does:**
- Converts DataFrame to embeddings
- Stores in ChromaDB
- Prepares for search

---

#### **Function 3: `retrieve_context()`**

**Location:** Line 54-65

**Code:**
```python
def retrieve_context(self, query, top_k=5):
    try:
        results = self.vector_store.search(query, n_results=top_k)
        return results['documents']
    except Exception as e:
        print(f"Error retrieving context: {str(e)}")
        return []
```

**What it does:**
- Searches vector database
- Returns text documents only

**Returns:**
```python
[
    "Student: Priya Nair, Engagement: 40.0...",
    "Student: Rohan Gupta, Engagement: 45.0...",
    ...
]
```

---

#### **Function 4: `retrieve_context_with_metadata()` ⭐**

**Location:** Line 67-81

**Code:**
```python
def retrieve_context_with_metadata(self, query, top_k=5):
    try:
        results = self.vector_store.search(query, n_results=top_k)
        
        combined = []
        for doc, meta in zip(results['documents'], results['metadatas']):
            combined.append({
                'document': doc,
                'metadata': meta
            })
        
        return combined
    except Exception as e:
        print(f"Error retrieving context: {str(e)}")
        return []
```

**What it does:**
- Searches and retrieves with metadata
- Returns structured dictionary
- Better for programmatic use

**Returns:**
```python
[
    {
        'document': "Student: Priya Nair (21CSE006)...",
        'metadata': {
            'student_id': '21CSE006',
            'name': 'Priya Nair',
            'engagement_score': 40.0,
            'risk_level': 'HIGH RISK'
        }
    },
    ...
]
```

---

#### **Function 5: `answer_query()`**

**Location:** Line 83-97

**Code:**
```python
def answer_query(self, query, llm_response):
    context = self.retrieve_context(query, top_k=5)
    context_str = "\n---\n".join(context)
    
    return {
        'query': query,
        'context': context_str,
        'response': llm_response,
        'context_count': len(context)
    }
```

**What it does:**
- Combines query + context + response
- Returns audit trail

**Returns:**
```python
{
    'query': "Who needs help?",
    'context': "Retrieved student records...",
    'response': "5 students need immediate intervention...",
    'context_count': 5
}
```

---

#### **Function 6: `perform_rag_retrieval()` (Standalone)**

**Location:** Line 101-120

**Code:**
```python
def perform_rag_retrieval(student_df, query, top_k=5):
    pipeline = RAGPipeline()
    
    if not pipeline.index_student_data(student_df):
        return {'error': 'Failed to index data'}
    
    results = pipeline.retrieve_context_with_metadata(query, top_k)
    
    return {
        'query': query,
        'results': results,
        'count': len(results)
    }
```

**What it does:**
- One-shot RAG retrieval
- No need to instantiate class
- Quick semantic search

---

---

## File: `vector_store.py` (169 lines)

### **Class: VectorStore**

#### **Function 1: `__init__()`**

**Location:** Line 15-28

**Code:**
```python
def __init__(self, persist_dir="./chroma_db"):
    try:
        settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_dir,
            anonymized_telemetry=False
        )
        self.client = chromadb.Client(settings)
    except:
        self.client = chromadb.PersistentClient(path=persist_dir)
    
    self.collection = None
```

**What it does:**
- Connects to ChromaDB
- Sets up persistent storage
- Initializes database client

---

#### **Function 2: `create_collection()`**

**Location:** Line 30-48

**Code:**
```python
def create_collection(self, name="student_records"):
    try:
        # Delete existing if exists
        try:
            self.client.delete_collection(name=name)
        except:
            pass
        
        self.collection = self.client.create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"}
        )
        return True
    except Exception as e:
        print(f"Error creating collection: {str(e)}")
        return False
```

**What it does:**
- Creates or recreates collection
- Sets similarity metric to cosine
- Initializes for document storage

---

#### **Function 3: `add_documents()`**

**Location:** Line 50-68

**Code:**
```python
def add_documents(self, documents, ids, metadatas=None):
    try:
        if metadatas is None:
            metadatas = [{}] * len(documents)
        
        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )
        return True
    except Exception as e:
        print(f"Error adding documents: {str(e)}")
        return False
```

**What it does:**
- Adds text documents to ChromaDB
- ChromaDB auto-generates embeddings
- Stores with metadata

**Parameters:**
- `documents` - List of text strings
- `ids` - Unique identifiers
- `metadatas` - Optional metadata dicts

---

#### **Function 4: `search()` ⭐ MAIN SEARCH**

**Location:** Line 70-87

**Code:**
```python
def search(self, query, n_results=5):
    try:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        # Flatten results (ChromaDB returns nested lists)
        return {
            'documents': results['documents'][0],
            'ids': results['ids'][0],
            'metadatas': results['metadatas'][0],
            'distances': results['distances'][0]
        }
    except Exception as e:
        print(f"Error searching: {str(e)}")
        return {}
```

**What it does:**
- Semantic search in vector database
- Returns relevant documents
- Includes similarity distances

**Returns:**
```python
{
    'documents': ["Student: Priya...", "Student: Rohan..."],
    'ids': ["21CSE006", "21CSE004"],
    'metadatas': [{'risk': 'HIGH'}, {'risk': 'LOW'}],
    'distances': [0.15, 0.23]  # Lower = more similar
}
```

---

---

## Summary Table

| File | Class | Main Function | Purpose |
|------|-------|---|---------|
| `ai_assistant.py` | AIAssistant | `generate_response()` | Query routing & decision making |
| `rag_pipeline.py` | RAGPipeline | `retrieve_context_with_metadata()` | Context retrieval |
| `vector_store.py` | VectorStore | `search()` | Embedding search |

---

## How They Work Together

```
Query: "Who needs help?"
  ↓
AIAssistant.generate_response()
  ├─ Check keywords
  ├─ Match "help" → route to _get_at_risk_students()
  ├─ OR no match → _llm_response()
  │   ├─ RAGPipeline.retrieve_context_with_metadata()
  │   ├─ VectorStore.search(query)
  │   ├─ Find 5 similar students
  │   ├─ Return with metadata
  │   ├─ Pass to Groq LLM
  │   └─ Return LLM answer
  ↓
Response to user
```

---

**Complete function reference done! 🚀**

For each function:
- ✅ Location in file
- ✅ Code snippet
- ✅ What it does
- ✅ Parameters
- ✅ Returns
- ✅ Usage examples
