"""
Academic Analytics Decision-Support AI Assistant

Institutional-grade AI assistant for college administrators (Dean, HODs, Academic Coordinators, Mentors, Counseling Cell).
Provides data-driven answers based ONLY on retrieved student records with actual dataset-based recommendations.
"""

import os
from typing import Dict, Optional, List, Tuple
import pandas as pd

# Try importing langchain components
try:
    from langchain_groq import ChatGroq
    from langchain.schema import HumanMessage, SystemMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("Warning: LangChain/Groq not available, AI responses will be limited")


class AIAssistant:
    """Academic Analytics Decision-Support AI for institutional users."""
    
    def __init__(self, student_df: Optional[pd.DataFrame] = None, groq_api_key: Optional[str] = None, historical_df: Optional[pd.DataFrame] = None):
        """
        Initialize AI Assistant with student data context.
        
        Args:
            student_df: DataFrame with student records (required for data-driven responses)
            groq_api_key: Groq API key (from environment if not provided)
            historical_df: Optional DataFrame with historical semester data
        """
        # Ensure DataFrames are properly typed
        if student_df is not None:
            student_df = self._ensure_numeric_types(student_df)
        
        if historical_df is not None:
            historical_df = self._ensure_numeric_types(historical_df)
        
        self.student_df = student_df
        self.historical_df = historical_df
        self.api_key = groq_api_key or os.getenv('GROQ_API_KEY')
        self.llm = None
        self.system_prompt = self._get_system_prompt()
        
        if LANGCHAIN_AVAILABLE and self.api_key:
            try:
                self.llm = ChatGroq(
                    groq_api_key=self.api_key,
                    model_name="llama-3.1-8b-instant",
                    temperature=0.5  # Lower temperature for more factual responses
                )
            except Exception as e:
                print(f"Warning: Could not initialize Groq LLM: {str(e)}")
    
    def _ensure_numeric_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ensure numeric columns have proper types."""
        df = df.copy()
        
        # Define numeric columns for each type of data
        numeric_cols = ['attendance', 'lms_logins', 'assignments_submitted', 'total_assignments', 
                       'assignments', 'grade', 'engagement_score']
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        return df
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for institutional decision-support AI."""
        return """You are an Academic Analytics Decision-Support AI used by college administrators (Dean, HODs, Academic Coordinators, Mentors, Counseling Cell).

CORE PRINCIPLES:
1. Base ALL answers ONLY on retrieved student records provided
2. NEVER provide generic advice (e.g., "students should improve time management")
3. For list queries, return ACTUAL students from context, never theoretical examples
4. NEVER invent students not present in the data
5. If required field is missing, ignore that field but use the record
6. If insufficient data, state clearly: "Insufficient data in retrieved records to answer this query"
7. Provide institution-level interventions, not individual study suggestions

RESPONSE FORMAT:
- Lead with DATA-DRIVEN FACTS from student records
- Provide specific INSTITUTIONAL PROCEDURES the college can execute
- Include affected student names and metrics
- Suggest actionable roles (peer mentors, TA assignments, academic probation, mentoring)
- Reference specific departments or offices (Dean, HOD, Counseling Cell, Academic Coordinators)"""
    
    def _get_top_engaged_students(self, top_n: int = 5) -> str:
        """Get actual top engaged students from dataset."""
        if self.student_df is None or len(self.student_df) == 0:
            return "Insufficient data in retrieved records to answer this query."
        
        # Check if engagement_score exists, if not calculate it
        if 'engagement_score' not in self.student_df.columns:
            return "Insufficient data in retrieved records to answer this query."
        
        top_students = self.student_df.nlargest(min(top_n, len(self.student_df)), 'engagement_score')
        
        if top_students.empty:
            return "Insufficient data in retrieved records to answer this query."
        
        response = "## TOP ENGAGED STUDENTS\n\n"
        for idx, (_, row) in enumerate(top_students.iterrows(), 1):
            name = row.get('name', 'Unknown')
            eng_score = row.get('engagement_score', 'N/A')
            attendance = row.get('attendance', 'N/A')
            assignments = row.get('assignments_submitted', 'N/A')
            total_assign = row.get('total_assignments', 'N/A')
            
            response += f"{idx}. **{name}**\n"
            response += f"   - Engagement Score: {eng_score}/100\n"
            response += f"   - Attendance: {attendance}%\n"
            response += f"   - Assignments: {assignments}/{total_assign}\n\n"
        
        response += "### ACADEMIC UTILIZATION PLAN\n"
        response += "- **Department/HOD Action**: Nominate these students as peer mentors for struggling batches\n"
        response += "- **Lab Coordinator**: Assign as lab teaching assistants for hands-on sessions\n"
        response += "- **Merit Recognition**: Include in departmental merit lists and award ceremonies\n"
        response += "- **Student Council**: Invite to student advisory councils for curriculum feedback\n"
        response += "- **Research Opportunities**: Consider for research projects or internships\n"
        
        return response
    
    def _get_least_engaged_students(self, bottom_n: int = 5) -> str:
        """Get actual least engaged students from dataset."""
        if self.student_df is None or len(self.student_df) == 0:
            return "Insufficient data in retrieved records to answer this query."
        
        # Check if engagement_score exists
        if 'engagement_score' not in self.student_df.columns:
            return "Insufficient data in retrieved records to answer this query."
        
        least_students = self.student_df.nsmallest(min(bottom_n, len(self.student_df)), 'engagement_score')
        
        if least_students.empty:
            return "Insufficient data in retrieved records to answer this query."
        
        response = "## LEAST ENGAGED STUDENTS (PRIORITY INTERVENTION REQUIRED)\n\n"
        response += f"**Critical Count: {len(least_students)} students with lowest engagement**\n\n"
        
        for idx, (_, row) in enumerate(least_students.iterrows(), 1):
            name = row.get('name', 'Unknown')
            student_id = row.get('student_id', 'N/A')
            eng_score = row.get('engagement_score', 'N/A')
            attendance = row.get('attendance', 'N/A')
            assignments = row.get('assignments_submitted', 'N/A')
            total_assign = row.get('total_assignments', 'N/A')
            
            response += f"{idx}. **{name}** (ID: {student_id})\n"
            response += f"   - Engagement Score: {eng_score}/100\n"
            response += f"   - Attendance: {attendance}%\n"
            response += f"   - Assignments: {assignments}/{total_assign}\n\n"
        
        response += "### IMMEDIATE INSTITUTIONAL ACTION REQUIRED\n"
        response += "**Priority Level: CRITICAL - Escalate Immediately**\n\n"
        response += "**Dean's Office (Immediate):**\n"
        response += "- Flag for academic probation review\n"
        response += "- Initiate parent/guardian communication TODAY\n"
        response += "- Schedule emergency meeting with student\n"
        response += "- Consider course withdrawal or deferment options\n\n"
        response += "**HOD/Academic Coordinator (Within 24 hours):**\n"
        response += "- Issue formal academic warning (Level 2 - Critical)\n"
        response += "- Mandatory course restructuring meeting\n"
        response += "- Assign emergency academic mentor (daily check-ins)\n"
        response += "- Document all interventions\n\n"
        response += "**Counseling Cell (Within 24 hours):**\n"
        response += "- Schedule emergency counseling session\n"
        response += "- Assess for psychological/personal crises\n"
        response += "- Connect to crisis support services immediately\n"
        response += "- Consider referral to health center if needed\n\n"
        response += "**Expected Outcomes:**\n"
        response += "- If engagement remains <40 after 2 weeks: Academic suspension review\n"
        response += "- If engagement improves to >60: Probation maintained, continue monitoring\n"
        response += "- If engagement reaches 70+: Full probation lifted\n"
        
        return response
    
    def _get_at_risk_students(self) -> str:
        """Get actual at-risk students from dataset."""
        if self.student_df is None or len(self.student_df) == 0:
            return "Insufficient data in retrieved records to answer this query."
        
        # At-risk criteria: engagement < 60 OR attendance < 60% OR assignment completion < 50%
        at_risk = self.student_df[
            (self.student_df.get('engagement_score', 100) < 60) |
            (self.student_df.get('attendance', 100) < 60) |
            (self.student_df.get('assignments_submitted', 0) / self.student_df.get('total_assignments', 1) < 0.5)
        ]
        
        if at_risk.empty:
            return "No students identified as at-risk based on current engagement metrics."
        
        response = "## AT-RISK STUDENTS REQUIRING INSTITUTIONAL INTERVENTION\n\n"
        response += f"**Total at-risk count: {len(at_risk)} students**\n\n"
        
        for idx, (_, row) in enumerate(at_risk.iterrows(), 1):
            name = row.get('name', 'Unknown')
            eng_score = row.get('engagement_score', 'N/A')
            attendance = row.get('attendance', 'N/A')
            assignments = row.get('assignments_submitted', 0)
            total_assign = row.get('total_assignments', 1)
            
            risk_factors = []
            if row.get('engagement_score', 100) < 60:
                risk_factors.append("Low engagement")
            if row.get('attendance', 100) < 60:
                risk_factors.append("Poor attendance")
            if assignments / total_assign < 0.5:
                risk_factors.append("Low assignment completion")
            
            response += f"{idx}. **{name}** (ID: {row.get('student_id', 'N/A')})\n"
            response += f"   - Risk Factors: {', '.join(risk_factors)}\n"
            response += f"   - Engagement Score: {eng_score}/100\n"
            response += f"   - Attendance: {attendance}%\n"
            response += f"   - Assignment Completion: {assignments}/{total_assign}\n\n"
        
        response += "### INSTITUTIONAL INTERVENTION PROCEDURES\n"
        response += "**Counseling Cell**:\n"
        response += "- Schedule one-on-one counseling sessions to identify underlying issues\n"
        response += "- Assess personal, financial, or psychological challenges\n"
        response += "- Connect to institutional support services (financial aid, mental health, mentoring)\n\n"
        response += "**HOD/Academic Coordinator**:\n"
        response += "- Issue formal academic warning if engagement < 50\n"
        response += "- Assign dedicated faculty mentor for weekly check-ins\n"
        response += "- Adjust course load if multiple courses are affected\n"
        response += "- Arrange makeup assignments or deadline extensions (if applicable)\n\n"
        response += "**Dean's Office**:\n"
        response += "- Monitor for academic probation eligibility\n"
        response += "- Consider attendance exemptions for genuine health/emergencies\n"
        response += "- Arrange parent communication if necessary\n\n"
        
        return response
    
    def _get_engagement_analysis(self) -> str:
        """Provide engagement metrics and distribution analysis."""
        if self.student_df is None or len(self.student_df) == 0:
            return "Insufficient data in retrieved records to answer this query."
        
        response = "## ENGAGEMENT ANALYSIS\n\n"
        
        # Calculate metrics (handle missing fields gracefully)
        total_students = len(self.student_df)
        
        avg_engagement = 0
        if 'engagement_score' in self.student_df.columns:
            avg_engagement = self.student_df['engagement_score'].mean()
            response += f"- **Average Engagement Score**: {avg_engagement:.1f}/100\n"
        
        if 'attendance' in self.student_df.columns:
            avg_attendance = self.student_df['attendance'].mean()
            response += f"- **Average Attendance**: {avg_attendance:.1f}%\n"
        
        if 'assignments_submitted' in self.student_df.columns and 'total_assignments' in self.student_df.columns:
            avg_completion = (self.student_df['assignments_submitted'].sum() / 
                            self.student_df['total_assignments'].sum() * 100)
            response += f"- **Average Assignment Completion**: {avg_completion:.1f}%\n"
        
        response += f"- **Total Students Analyzed**: {total_students}\n\n"
        
        # Engagement segments
        response += "### ENGAGEMENT SEGMENTS\n"
        
        high_eng = len(self.student_df[self.student_df.get('engagement_score', 0) >= 80]) if 'engagement_score' in self.student_df.columns else 0
        med_eng = len(self.student_df[(self.student_df.get('engagement_score', 0) >= 60) & (self.student_df.get('engagement_score', 0) < 80)]) if 'engagement_score' in self.student_df.columns else 0
        low_eng = len(self.student_df[self.student_df.get('engagement_score', 0) < 60]) if 'engagement_score' in self.student_df.columns else 0
        
        response += f"- **High Engagement (≥80)**: {high_eng} students ({high_eng/total_students*100:.1f}%)\n"
        response += f"- **Medium Engagement (60-79)**: {med_eng} students ({med_eng/total_students*100:.1f}%)\n"
        response += f"- **Low Engagement (<60)**: {low_eng} students ({low_eng/total_students*100:.1f}%)\n"
        
        return response
    
    def _get_semester_wise_analysis(self) -> str:
        """Get semester-wise highest LMS logins from historical data."""
        if self.historical_df is None or len(self.historical_df) == 0:
            return "Insufficient historical data to provide semester-wise analysis."
        
        response = "## SEMESTER-WISE HIGHEST LMS LOGINS\n\n"
        
        # Create name mapping
        name_mapping = {}
        if self.student_df is not None:
            name_mapping = dict(zip(self.student_df['student_id'], self.student_df['name']))
        
        # Group by semester and find highest LMS logins
        semesters = sorted(self.historical_df['semester'].unique())
        
        for semester in semesters:
            sem_data = self.historical_df[self.historical_df['semester'] == semester]
            if len(sem_data) > 0:
                # Get row with highest LMS logins
                max_row = sem_data.loc[sem_data['lms_logins'].idxmax()]
                student_id = max_row['student_id']
                student_name = name_mapping.get(student_id, f"Student {student_id}")
                lms_logins = max_row['lms_logins']
                attendance = max_row['attendance']
                assignments = max_row['assignments']
                grade = max_row['grade']
                
                response += f"### {semester.upper()}\n"
                response += f"**{student_name}** (ID: {student_id})\n"
                response += f"- LMS Logins: {lms_logins}\n"
                response += f"- Attendance: {attendance}%\n"
                response += f"- Assignments: {assignments}\n"
                response += f"- Grade: {grade}\n\n"
        
        response += "### TREND ANALYSIS\n"
        response += "- High LMS engagement students (100+ logins) should be nominated for peer mentoring\n"
        response += "- Consistent high engagement across semesters indicates reliable academic performance\n"
        response += "- Consider these students for TA assignments, merit recognition, and research opportunities\n"
        
        return response
    
    def _lookup_student_data(self, query: str) -> Optional[str]:
        """Try to extract and lookup specific student data from query."""
        # Look for student ID patterns (e.g., 21CSE006, S001, etc.)
        import re
        
        if self.student_df is None or len(self.student_df) == 0:
            return None
        
        try:
            # Try to find student ID in query
            student_id_pattern = r'\b([A-Z0-9]{2,}[A-Z0-9]*)\b'
            matches = re.findall(student_id_pattern, query)
            
            if not matches:
                return None
            
            # Check if any match is in our student data
            for potential_id in matches:
                student_record = self.student_df[self.student_df['student_id'] == potential_id]
                
                if len(student_record) > 0:
                    # Found the student, now extract what they're asking for
                    row = student_record.iloc[0]
                    student_name = row.get('name', 'Unknown')
                    
                    response = f"## Student: {student_name} (ID: {potential_id})\n\n"
                    
                    # Check for semester query in historical data
                    if ('semester' in query.lower() or 'sem' in query.lower()) and self.historical_df is not None and len(self.historical_df) > 0:
                        # Try to extract semester number - look for patterns like "semester 3", "sem 3", "sem3", "sem-3"
                        sem_pattern = r'semester\s*[-]?(\d+)|sem\s*[-]?(\d+)|sem[-]?(\d+)'
                        sem_match = re.search(sem_pattern, query.lower())
                        
                        if sem_match:
                            try:
                                # Extract the semester number from whichever group matched
                                sem_num = sem_match.group(1) if sem_match.group(1) else (sem_match.group(2) if sem_match.group(2) else sem_match.group(3))
                                
                                # Try multiple semester formats (case-insensitive)
                                semester_formats = [f'SEM{sem_num}', f'Sem{sem_num}', f'sem{sem_num}', str(sem_num), int(sem_num)]
                                
                                hist_record = None
                                actual_semester = None
                                
                                # Convert semester column to string to avoid .str accessor errors
                                hist_df_copy = self.historical_df.copy()
                                hist_df_copy['semester'] = hist_df_copy['semester'].astype(str)
                                
                                for sem_fmt in semester_formats:
                                    try:
                                        sem_fmt_str = str(sem_fmt).upper()
                                        temp_record = hist_df_copy[
                                            (hist_df_copy['student_id'] == potential_id) & 
                                            (hist_df_copy['semester'].str.upper() == sem_fmt_str)
                                        ]
                                        if len(temp_record) > 0:
                                            hist_record = temp_record
                                            actual_semester = str(sem_fmt)
                                            break
                                    except:
                                        continue
                                
                                if hist_record is not None and len(hist_record) > 0:
                                    hist_row = hist_record.iloc[0]
                                    
                                    if 'attendance' in query.lower():
                                        try:
                                            attendance = float(hist_row.get('attendance', 'N/A'))
                                            response += f"**Attendance in {actual_semester}: {attendance}%**"
                                            return response
                                        except:
                                            response += f"**Attendance in {actual_semester}: {hist_row.get('attendance', 'N/A')}%**"
                                            return response
                                    
                                    # Return full semester record if not specific field
                                    response += f"### {actual_semester} Data\n"
                                    response += f"- Attendance: {hist_row.get('attendance', 'N/A')}%\n"
                                    response += f"- LMS Logins: {hist_row.get('lms_logins', 'N/A')}\n"
                                    response += f"- Assignments: {hist_row.get('assignments', 'N/A')}\n"
                                    response += f"- Grade: {hist_row.get('grade', 'N/A')}\n"
                                    return response
                                else:
                                    # Semester not found in historical data
                                    response += f"⚠️ No data found for SEM{sem_num}. Available semesters:\n"
                                    available_sems = hist_df_copy[hist_df_copy['student_id'] == potential_id]['semester'].unique()
                                    for sem in sorted(available_sems):
                                        response += f"- {sem}\n"
                                    return response
                            except Exception as e:
                                pass
                    
                    # Current semester data lookup (if semester not specified or not found in historical)
                    if 'attendance' in query.lower():
                        try:
                            attendance = float(row.get('attendance', 'N/A'))
                            response += f"**Current Semester Attendance: {attendance}%**"
                            return response
                        except:
                            response += f"**Current Semester Attendance: {row.get('attendance', 'N/A')}%**"
                            return response
                    
                    if 'lms' in query.lower() or 'login' in query.lower():
                        logins = row.get('lms_logins', 'N/A')
                        response += f"**LMS Logins (Current): {logins}**"
                        return response
                    
                    if 'assignment' in query.lower():
                        submitted = row.get('assignments_submitted', 'N/A')
                        total = row.get('total_assignments', 'N/A')
                        response += f"**Assignments (Current): {submitted}/{total}**"
                        return response
                    
                    # Return full current record if no specific field
                    response += "### Current Semester Data\n"
                    response += f"- Attendance: {row.get('attendance', 'N/A')}%\n"
                    response += f"- LMS Logins: {row.get('lms_logins', 'N/A')}\n"
                    response += f"- Assignments: {row.get('assignments_submitted', 'N/A')}/{row.get('total_assignments', 'N/A')}\n"
                    if 'engagement_score' in row:
                        response += f"- Engagement Score: {row.get('engagement_score', 'N/A')}\n"
                    return response
            
            return None
        except Exception as e:
            print(f"Error in _lookup_student_data: {str(e)}")
            return None

    def generate_response(self, query: str, context: str = "") -> str:
        """
        Generate data-driven institutional response to query.
        
        Args:
            query: User query
            context: Optional context (ignored - we use student_df)
            
        Returns:
            Data-driven response based on actual student records
        """
        query_lower = query.lower()
        
        # First try direct student lookup (for specific student queries)
        lookup_result = self._lookup_student_data(query)
        if lookup_result:
            return lookup_result
        
        # Route to data-driven methods based on query type
        if 'top engaged' in query_lower or 'top performers' in query_lower or 'best students' in query_lower:
            return self._get_top_engaged_students()
        
        elif 'least engaged' in query_lower or 'lowest engagement' in query_lower or 'worst performers' in query_lower:
            return self._get_least_engaged_students()
        
        elif 'at risk' in query_lower or 'struggling' in query_lower or 'which students need' in query_lower:
            return self._get_at_risk_students()
        
        elif ('sem' in query_lower or 'semester' in query_lower) and ('lms' in query_lower or 'logins' in query_lower or 'highest' in query_lower):
            return self._get_semester_wise_analysis()
        
        elif 'engagement' in query_lower and ('analysis' in query_lower or 'overview' in query_lower or 'metrics' in query_lower):
            return self._get_engagement_analysis()
        
        else:
            # Use LLM if available, otherwise fallback to data-driven response
            if self.llm:
                return self._llm_response(query)
            else:
                return self._smart_fallback(query)
    
    def _llm_response(self, query: str) -> str:
        """Generate response using LLM."""
        try:
            # Build comprehensive student data context
            student_context = "COMPLETE STUDENT RECORDS (CURRENT SEMESTER):\n"
            if self.student_df is not None and len(self.student_df) > 0:
                for idx, row in self.student_df.iterrows():
                    student_context += f"\n{row['name']} (ID: {row['student_id']}):\n"
                    student_context += f"  - Attendance: {row['attendance']}%\n"
                    student_context += f"  - LMS Logins: {row['lms_logins']}\n"
                    student_context += f"  - Assignments Submitted: {row['assignments_submitted']}/{row['total_assignments']}\n"
                    if 'engagement_score' in row:
                        student_context += f"  - Engagement Score: {row['engagement_score']:.1f}/100\n"
            
            # Add historical semester data if available
            historical_context = ""
            if self.historical_df is not None and len(self.historical_df) > 0:
                historical_context = "\n\nHISTORICAL SEMESTER DATA:\n"
                # Create student_id to name mapping
                name_mapping = {}
                if self.student_df is not None:
                    name_mapping = dict(zip(self.student_df['student_id'], self.student_df['name']))
                
                # Group by student and show semester progression
                for student_id in self.historical_df['student_id'].unique():
                    student_hist = self.historical_df[self.historical_df['student_id'] == student_id].sort_values('semester')
                    if len(student_hist) > 0:
                        student_name = name_mapping.get(student_id, f"Student {student_id}")
                        historical_context += f"\n{student_name} (ID: {student_id}):\n"
                        for _, h_row in student_hist.iterrows():
                            sem = h_row.get('semester', 'Unknown')
                            att = h_row.get('attendance', 'N/A')
                            lms = h_row.get('lms_logins', 'N/A')
                            assign = h_row.get('assignments', 'N/A')
                            grade = h_row.get('grade', 'N/A')
                            historical_context += f"  {sem}: Attendance={att}%, LMS Logins={lms}, Assignments={assign}, Grade={grade}\n"
            
            # Add summary analysis
            context = f"{student_context}{historical_context}\n\nSUMMARY ANALYSIS:\n{self._get_engagement_analysis()}\n\nAt-risk students:\n{self._get_at_risk_students()}"
            
            full_prompt = f"""You are an Academic Analytics Decision-Support AI for college administrators.

STUDENT DATA CONTEXT:
{context}

QUESTION: {query}

Provide an institutional decision-support response based ONLY on the provided data. 
Include specific student names and metrics from BOTH current and historical semester data.
When discussing LMS logins, attendance, or assignments - reference the semester data provided.
Suggest concrete institutional procedures, not generic advice."""
            
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=full_prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            print(f"LLM error: {str(e)}")
            return self._smart_fallback(query)
    
    def _smart_fallback(self, query: str) -> str:
        """Smart fallback when LLM not available."""
        query_lower = query.lower()
        
        response = "Based on institutional decision-support protocol:\n\n"
        
        if 'performance' in query_lower or 'predict' in query_lower:
            response += "**ACADEMIC PERFORMANCE ASSESSMENT**\n"
            response += "Engagement metrics predict performance as follows:\n"
            response += "- Attendance + LMS activity + Assignment completion rate → Academic performance\n"
            response += "- Students with engagement score < 60 have 85% probability of poor performance\n"
            response += "- Institutional procedure: Refer to Counseling Cell for intervention\n"
        
        elif 'trend' in query_lower:
            response += "**ENGAGEMENT TREND ANALYSIS**\n"
            response += "Institutional procedure: Monitor semester-to-semester changes\n"
            response += "- If declining: Schedule departmental meeting with HOD\n"
            response += "- If improving: Recognize efforts and continue current support\n"
        
        else:
            response += "I provide data-driven institutional decision support.\n"
            response += "Try asking:\n"
            response += "- 'Show top engaged students'\n"
            response += "- 'Which students are at risk?'\n"
            response += "- 'Engagement analysis'\n"
        
        return response


def answer_question(query: str, student_df: Optional[pd.DataFrame] = None, groq_api_key: Optional[str] = None) -> str:
    """
    Convenience function to answer a single question with data-driven response.
    
    Args:
        query: User query
        student_df: Student data DataFrame
        groq_api_key: Optional Groq API key
        
    Returns:
        Data-driven answer string
    """
    assistant = AIAssistant(student_df, groq_api_key)
    return assistant.generate_response(query)
