# 🎯 Complete Query Types Reference

## All Supported Queries

The Academic Analytics Decision-Support AI now supports **4 major query types**:

---

## 1️⃣ Top Engaged Students

**What It Does**: Identifies and lists the best-performing students

**Example Queries**:
```
✅ "Show top engaged students"
✅ "Top performers"
✅ "Best students"
✅ "Top engaged students"
```

**Returns**: 5 actual students with highest engagement scores

**Sample Output**:
```
## TOP ENGAGED STUDENTS

1. **Shreya Sharma** - 99.7/100 (95% attendance, 10/10 assignments)
2. **Rahul Sharma** - 98.7/100 (96% attendance, 10/10 assignments)
3. **Neha Gupta** - 94.6/100 (92% attendance, 10/10 assignments)

### ACADEMIC UTILIZATION PLAN
- Department/HOD: Nominate as peer mentors
- Lab Coordinator: Assign as lab TAs
- Merit Recognition: Include in merit lists
- Student Council: Invite to advisory councils
- Research: Consider for projects
```

**Who Uses It**: HOD, Dean (for merit lists and peer mentoring)

---

## 2️⃣ Least Engaged Students (NEW ⭐)

**What It Does**: Identifies critically struggling students requiring immediate intervention

**Example Queries**:
```
✅ "Show least engaged students"
✅ "Least engaged students"
✅ "Lowest engagement"
✅ "Worst performers"
✅ "Students with lowest engagement"
```

**Returns**: 5 actual students with lowest engagement scores

**Sample Output**:
```
## LEAST ENGAGED STUDENTS (PRIORITY INTERVENTION REQUIRED)

**Critical Count: 5 students**

1. **Vikram Joshi** - 27.2/100 (45% attendance, 3/10 assignments)
2. **Manish Singh** - 32.7/100 (48% attendance, 4/10 assignments)
3. **Aditya Verma** - 37.2/100 (55% attendance, 4/10 assignments)

### IMMEDIATE INSTITUTIONAL ACTION REQUIRED
**Priority Level: CRITICAL - Escalate Immediately**

**Dean's Office (Immediate):**
- Flag for academic probation review
- Initiate parent communication TODAY
- Schedule emergency meeting
- Consider withdrawal/deferment

**HOD/Coordinator (Within 24 hours):**
- Issue formal academic warning
- Assign emergency mentor (daily check-ins)
- Mandatory course restructuring meeting

**Counseling Cell (Within 24 hours):**
- Schedule emergency session
- Assess for psychological crises
- Connect to crisis support services
```

**Who Uses It**: Dean, HOD, Counseling Cell (for emergency interventions)

---

## 3️⃣ At-Risk Students

**What It Does**: Identifies students meeting at-risk criteria

**Criteria**: ANY ONE of:
- Engagement Score < 60/100
- Attendance < 60%
- Assignment Completion < 50%

**Example Queries**:
```
✅ "Which students are at risk?"
✅ "At-risk students"
✅ "Struggling students"
✅ "Which students need support?"
```

**Returns**: All students matching at-risk criteria (typically 5-10 students)

**Sample Output**:
```
## AT-RISK STUDENTS REQUIRING INSTITUTIONAL INTERVENTION

**Total at-risk count: 7 students**

1. **Arjun Kumar** (ID: 21CSE003)
   - Risk Factors: Low engagement, Poor attendance
   - Engagement: 38.8/100, Attendance: 58%

2. **Sneha Patel** (ID: 21CSE004)
   - Risk Factors: Low engagement
   - Engagement: 44.8/100, Attendance: 62%

### INSTITUTIONAL INTERVENTION PROCEDURES

**Counseling Cell**:
- One-on-one counseling sessions
- Assess root causes
- Connect to support services

**HOD/Academic Coordinator**:
- Issue formal academic warning (if engagement < 50)
- Assign dedicated faculty mentor
- Adjust course load if needed
- Arrange makeup assignments

**Dean's Office**:
- Monitor probation eligibility
- Consider exemptions for emergencies
- Arrange parent communication
```

**Who Uses It**: Counseling Cell, HOD, Dean (for standard interventions)

---

## 4️⃣ Engagement Analysis

**What It Does**: Overall engagement metrics and distribution analysis

**Example Queries**:
```
✅ "Engagement analysis"
✅ "Show engagement metrics"
✅ "Engagement overview"
✅ "Engagement distribution"
```

**Returns**: Aggregate statistics and segment breakdown

**Sample Output**:
```
## ENGAGEMENT ANALYSIS

- **Average Engagement Score**: 69.8/100
- **Average Attendance**: 75.9%
- **Average Assignment Completion**: 74.5%
- **Total Students Analyzed**: 20

### ENGAGEMENT SEGMENTS

- **High Engagement (≥80)**: 9 students (45.0%)
  → Can be peer mentors, TAs, merit list
  
- **Medium Engagement (60-79)**: 4 students (20.0%)
  → Provide support to reach high engagement
  → Pair with peer mentors
  
- **Low Engagement (<60)**: 7 students (35.0%)
  → Immediate intervention required
  → Counseling, faculty mentoring, course adjustment
```

**Who Uses It**: Dean, Coordinator (for strategic planning and resource allocation)

---

## Query Comparison Table

| Query Type | Focus | Sample Count | Priority | Timeline | Office Lead |
|------------|-------|---------|----------|----------|-------------|
| **Top Engaged** | Excellence | 5 best | Medium | Ongoing | HOD/Dean |
| **Least Engaged** | Crisis | 5 worst | CRITICAL | Immediate | Dean |
| **At-Risk** | Intervention | Variable | High | 24-48 hrs | Counseling |
| **Analysis** | Strategy | All | Low | Weekly | Coordinator |

---

## Decision Tree: Which Query to Use?

```
START: I want to analyze students
│
├─ For MERIT/AWARDS/MENTORING?
│  └─→ Use: "Show top engaged students"
│      Who: HOD, Dean
│      When: End of semester, merit list season
│      Action: Nominate as mentors, award recognition
│
├─ For EMERGENCY INTERVENTION?
│  └─→ Use: "Show least engaged students"
│      Who: Dean, Counseling Cell
│      When: Immediately upon query
│      Action: Emergency procedures, parent contact
│
├─ For ONGOING SUPPORT?
│  └─→ Use: "Which students are at risk?"
│      Who: Counseling Cell, HOD
│      When: Regular monitoring
│      Action: Counseling, faculty mentoring
│
└─ For PLANNING/RESOURCES?
   └─→ Use: "Engagement analysis"
       Who: Coordinator, Dean
       When: Strategic planning
       Action: Allocate mentors, resources, support
```

---

## Examples by User Role

### Dean's Daily Workflow

**Monday 9 AM**: 
```
Query: "Show least engaged students"
Action: Review critical cases, authorize emergencies
```

**Friday 3 PM**: 
```
Query: "Engagement analysis"
Action: Weekly report to leadership
```

---

### HOD's Weekly Tasks

**Day 1**: 
```
Query: "Show top engaged students"
Action: Identify peer mentors, assign TA roles
```

**Day 3**: 
```
Query: "Which students are at risk?"
Action: Schedule meetings, assign faculty mentors
```

---

### Counseling Cell's Triage

**Priority 1 (Immediate)**: 
```
Query: "Show least engaged students"
Action: Emergency sessions, crisis assessment
```

**Priority 2 (24 hours)**: 
```
Query: "Which students are at risk?"
Action: Regular counseling sessions
```

---

### Academic Coordinator's Planning

**Semester Start**: 
```
Query: "Engagement analysis"
Action: Allocate mentoring resources
```

**Mid-semester**: 
```
Query: "Which students are at risk?"
Action: Adjust support plans
```

---

## Key Points

✅ **Always Data-Driven**: Every response uses actual student records
✅ **Never Fabricated**: All students shown are real (verified from students.csv)
✅ **Institutional Focus**: Procedures for actual college offices, not generic advice
✅ **Actionable**: Each response includes specific steps each office can take
✅ **Timelines**: Clear escalation procedures with time limits
✅ **Measurable**: Expected outcomes with monitoring metrics

---

## All Query Keywords Supported

```
TOP ENGAGED:
  - "top engaged", "top performers", "best students"

LEAST ENGAGED (NEW):
  - "least engaged", "lowest engagement", "worst performers"

AT-RISK:
  - "at risk", "struggling", "which students need"

ENGAGEMENT ANALYSIS:
  - "engagement" + ("analysis" OR "overview" OR "metrics")

ERROR HANDLING:
  - Insufficient data → "Insufficient data in retrieved records..."
  - Ambiguous query → Smart fallback response
```

---

## Testing Your Queries

### In Streamlit App

1. Run: `streamlit run app.py`
2. Navigate to: "🤖 Academic Analytics Assistant"
3. Type your query
4. Click: "🔍 Get AI Response"
5. See: Actual institutional response

### Via Python

```python
from ai.ai_assistant import AIAssistant
import pandas as pd

df = pd.read_csv('data/students.csv')
# Calculate engagement_score...

assistant = AIAssistant(student_df=df)

# Try any query:
response = assistant.generate_response("Show least engaged students")
print(response)
```

---

## Summary

**Query Types Supported**: 4 major categories

**Least Engaged Students**: ✅ NEW FEATURE

**Data Source**: 100% from actual student database

**Response Quality**: Institutional procedures, real metrics, actionable steps

**Status**: ✅ COMPLETE & TESTED

