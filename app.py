"""
Student Engagement Analysis and Wellbeing Monitoring System
Streamlit Dashboard Application

Main interactive dashboard for analyzing student engagement metrics,
identifying at-risk students, and monitoring wellbeing indicators.
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# Add modules to path
sys.path.insert(0, os.path.dirname(__file__))

# Import modules
from modules.data_loader import load_student_data, load_historical_data, load_wellbeing_data
from modules.engagement_calculator import add_engagement_scores, get_engagement_statistics
from modules.risk_detector import add_risk_levels, get_at_risk_students, get_risk_statistics, get_engagement_distribution
from modules.wellbeing_detector import add_wellbeing_status, get_wellbeing_alerts, get_wellbeing_statistics
from modules.trend_analysis import analyze_semester_trends, get_student_progress
from modules.prediction_model import AcademicPerformancePredictor, get_performance_segments
from modules.report_generator import ReportGenerator
from utils.helpers import validate_percentage, safe_divide, get_data_summary
from utils.visualizations import (
    create_engagement_histogram, create_risk_level_pie_chart,
    create_engagement_level_bar_chart, create_top_students_bar_chart,
    create_attendance_vs_assignment_scatter, create_semester_trend_line_chart,
    create_wellbeing_status_pie_chart
)

# Configure page
st.set_page_config(
    page_title="Student Engagement Analysis System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Color Palette
COLOR_PALETTE = {
    'primary': '#1e40af',          # Professional Blue
    'secondary': '#0369a1',        # Sky Blue
    'success': '#059669',          # Green
    'warning': '#d97706',          # Amber
    'danger': '#dc2626',           # Red
    'info': '#0369a1',             # Cyan
    'light': '#f8fafb',            # Light Gray
    'dark': '#1f2937',             # Dark Gray
    'border': '#e5e7eb',           # Border Gray
}

# Plotly Color Scheme
PLOTLY_COLORS = ['#1e40af', '#0369a1', '#059669', '#d97706', '#dc2626', '#6366f1', '#8b5cf6', '#ec4899']
RISK_COLORS = {
    'HIGH RISK': '#dc2626',
    'AT RISK': '#d97706', 
    'LOW RISK': '#059669'
}

# Custom CSS
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1e40af;
        font-size: 2.8em;
        font-weight: 800;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.08);
        letter-spacing: -0.5px;
    }
    .subtitle {
        text-align: center;
        color: #4b5563;
        font-size: 1.1em;
        margin-bottom: 30px;
        font-weight: 500;
    }
    .metric-card {
        background: linear-gradient(135deg, #f8fafb 0%, #f3f4f6 100%);
        padding: 20px;
        border-radius: 12px;
        margin: 10px 0;
        border-left: 4px solid #1e40af;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    /* Risk Level Colors */
    .high-risk { 
        color: #dc2626; 
        font-weight: bold; 
        background-color: #fee2e2;
        padding: 4px 8px;
        border-radius: 4px;
        display: inline-block;
    }
    .at-risk { 
        color: #d97706; 
        font-weight: bold; 
        background-color: #fef3c7;
        padding: 4px 8px;
        border-radius: 4px;
        display: inline-block;
    }
    .low-risk { 
        color: #059669; 
        font-weight: bold; 
        background-color: #d1fae5;
        padding: 4px 8px;
        border-radius: 4px;
        display: inline-block;
    }
    
    /* Category Colors */
    .both-issues {
        background-color: #fee2e2;
        color: #dc2626;
        padding: 8px 12px;
        border-radius: 6px;
        font-weight: 600;
    }
    .at-risk-only {
        background-color: #fef3c7;
        color: #d97706;
        padding: 8px 12px;
        border-radius: 6px;
        font-weight: 600;
    }
    .wellbeing-only {
        background-color: #dbeafe;
        color: #0369a1;
        padding: 8px 12px;
        border-radius: 6px;
        font-weight: 600;
    }
    .high-performers {
        background-color: #d1fae5;
        color: #059669;
        padding: 8px 12px;
        border-radius: 6px;
        font-weight: 600;
    }
    
    /* Status Badges */
    .badge-success {
        background-color: #d1fae5;
        color: #059669;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.85em;
        font-weight: 600;
    }
    .badge-warning {
        background-color: #fef3c7;
        color: #d97706;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.85em;
        font-weight: 600;
    }
    .badge-danger {
        background-color: #fee2e2;
        color: #dc2626;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.85em;
        font-weight: 600;
    }
    .badge-info {
        background-color: #dbeafe;
        color: #0369a1;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.85em;
        font-weight: 600;
    }
    
    /* Section Styling */
    .section-header {
        border-bottom: 3px solid #1e40af;
        padding-bottom: 10px;
        margin-bottom: 20px;
        color: #1e40af;
        font-weight: 600;
    }
    
    /* Card with shadow */
    .card-container {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'student_data' not in st.session_state:
    st.session_state.student_data = None
if 'historical_data' not in st.session_state:
    st.session_state.historical_data = None
if 'wellbeing_data' not in st.session_state:
    st.session_state.wellbeing_data = None


def load_sample_data():
    """Load sample data from CSV files."""
    try:
        student_df = pd.read_csv('data/students.csv')
        historical_df = pd.read_csv('data/historical_semesters.csv')
        wellbeing_df = pd.read_csv('data/wellbeing_data.csv')
        return student_df, historical_df, wellbeing_df
    except Exception as e:
        st.error(f"Error loading sample data: {str(e)}")
        return None, None, None


def process_student_data(df):
    """Process student data through all modules."""
    try:
        # Add engagement scores
        df = add_engagement_scores(df)
        
        # Add risk levels
        df = add_risk_levels(df)
        
        # Add wellbeing status
        df = add_wellbeing_status(df)
        
        return df
    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        return None


# ============================================================================
# HEADER
# ============================================================================

st.markdown('<div class="main-title">📊 STUDENT ENGAGEMENT ANALYSIS SYSTEM</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Powered Analytics for Student Wellbeing & Academic Performance</div>', unsafe_allow_html=True)

st.divider()

# ============================================================================
# SIDEBAR - FILE UPLOAD & NAVIGATION
# ============================================================================

with st.sidebar:
    st.header("📁 Data Management")
    
    # Data source selection
    data_source = st.radio(
        "Select Data Source",
        ["Sample Data", "Upload CSV Files"],
        help="Choose between sample data or upload your own CSV files"
    )
    
    if data_source == "Sample Data":
        if st.button("📂 Load Sample Data", key="load_sample"):
            with st.spinner("Loading sample data..."):
                student_df, historical_df, wellbeing_df = load_sample_data()
                if student_df is not None:
                    st.session_state.student_data = process_student_data(student_df)
                    st.session_state.historical_data = historical_df
                    st.session_state.wellbeing_data = wellbeing_df
                    st.success("✅ Sample data loaded successfully!")
    else:
        st.subheader("Upload CSV Files")
        st.info("📌 Uploaded files will be saved permanently and used for all future queries")
        
        # File uploaders
        student_file = st.file_uploader(
            "Upload Student Engagement Data (students.csv)",
            type="csv",
            key="student_upload"
        )
        
        historical_file = st.file_uploader(
            "Upload Historical Semester Data (historical_semesters.csv)",
            type="csv",
            key="historical_upload"
        )
        
        wellbeing_file = st.file_uploader(
            "Upload Wellbeing Data (wellbeing_data.csv)",
            type="csv",
            key="wellbeing_upload"
        )
        
        if st.button("📤 Process & Save Uploaded Files", key="process_upload"):
            if student_file is not None:
                try:
                    # Create data directory if it doesn't exist
                    data_dir = os.path.join(os.path.dirname(__file__), 'data')
                    os.makedirs(data_dir, exist_ok=True)
                    
                    # Save student file
                    student_path = os.path.join(data_dir, 'students.csv')
                    with open(student_path, 'wb') as f:
                        f.write(student_file.getbuffer())
                    
                    # Read and process student data
                    student_df = pd.read_csv(student_path)
                    st.session_state.student_data = process_student_data(student_df)
                    st.success("✅ Student data saved and loaded!")
                    
                    # Save historical file if provided
                    if historical_file is not None:
                        historical_path = os.path.join(data_dir, 'historical_semesters.csv')
                        with open(historical_path, 'wb') as f:
                            f.write(historical_file.getbuffer())
                        
                        hist_df = pd.read_csv(historical_path)
                        st.session_state.historical_data = hist_df
                        st.success("✅ Historical semester data saved and loaded!")
                    
                    # Save wellbeing file if provided
                    if wellbeing_file is not None:
                        wellbeing_path = os.path.join(data_dir, 'wellbeing_data.csv')
                        with open(wellbeing_path, 'wb') as f:
                            f.write(wellbeing_file.getbuffer())
                        
                        wellbeing_df = pd.read_csv(wellbeing_path)
                        st.session_state.wellbeing_data = wellbeing_df
                        st.success("✅ Wellbeing data saved and loaded!")
                    
                    st.success("🎉 All files processed and saved successfully! Your data will be used for all future queries.")
                    
                except Exception as e:
                    st.error(f"❌ Error processing files: {str(e)}")
            else:
                st.error("Please upload at least the student engagement data file")
    
    st.divider()
    
    # Navigation
    st.header("🗂️ Navigation")
    page = st.radio(
        "Select Section",
        [
            "📊 Dashboard",
            "📈 Analytics",
            "⚠️ Risk Assessment",
            "💚 Wellbeing Monitor",
            "📉 Trend Analysis",
            "🤖 AI Assistant",
            "📋 Reports"
        ],
        key="page_select"
    )
    
    st.divider()
    
    # About
    with st.expander("ℹ️ About System", expanded=False):
        st.markdown("""
        **Student Engagement Analysis System v1.0**
        
        AI-powered platform for analyzing student engagement and predicting academic performance.
        
        **Features:**
        - Engagement score calculation
        - Risk level detection
        - Wellbeing monitoring
        - Trend analysis
        - Academic prediction
        - AI-powered queries
        
        **Technology:**
        - Python, Streamlit, Pandas
        - Scikit-learn, ChromaDB
        - LangChain, Groq API
        """)


# ============================================================================
# MAIN CONTENT AREAS
# ============================================================================

# Check if data is loaded
if st.session_state.student_data is None:
    st.warning("⚠️ Please load data using the sidebar first!")
    st.info("👈 Use the sidebar to either load sample data or upload your CSV files")
else:
    df = st.session_state.student_data
    historical_df = st.session_state.historical_data
    
    # ========================================================================
    # PAGE: DASHBOARD
    # ========================================================================
    
    if page == "📊 Dashboard":
        st.header("📊 Dashboard Overview")
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Students",
                len(df),
                help="Total number of students in dataset"
            )
        
        with col2:
            avg_engagement = round(df['engagement_score'].mean(), 2)
            st.metric(
                "Avg Engagement Score",
                f"{avg_engagement:.2f}/100",
                help="Average engagement across all students"
            )
        
        with col3:
            at_risk = len(df[df['risk_level'].isin(['AT RISK', 'HIGH RISK'])])
            st.metric(
                "At-Risk Students",
                at_risk,
                help="Students requiring attention"
            )
        
        with col4:
            wellbeing_alerts = len(df[df['wellbeing_status'] != 'NORMAL'])
            st.metric(
                "Wellbeing Alerts",
                wellbeing_alerts,
                help="Students with wellbeing concerns"
            )
        
        st.divider()
        
        # Data Preview
        col_preview1, col_preview2 = st.columns([1, 1])
        
        with col_preview1:
            st.subheader("📋 Data Preview (All Students)")
            st.dataframe(
                df[['student_id', 'name', 'attendance', 'engagement_score', 'risk_level']],
                use_container_width=True,
                height=400
            )
        
        with col_preview2:
            st.subheader("📊 Engagement Score Distribution")
            fig = go.Figure(data=[
                go.Histogram(
                    x=df['engagement_score'],
                    nbinsx=20,
                    marker_color='steelblue',
                    name='Engagement Score'
                )
            ])
            fig.update_layout(
                xaxis_title="Engagement Score",
                yaxis_title="Number of Students",
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Risk Distribution
        col_risk1, col_risk2 = st.columns([1, 1])
        
        with col_risk1:
            st.subheader("⚠️ Risk Level Distribution")
            risk_counts = df['risk_level'].value_counts()
            fig = go.Figure(data=[go.Pie(
                labels=risk_counts.index,
                values=risk_counts.values,
                marker=dict(colors=['#ff6b6b', '#ffd93d', '#6bcf7f'])
            )])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col_risk2:
            st.subheader("💚 Wellbeing Status")
            wellbeing_counts = df['wellbeing_status'].value_counts()
            fig = go.Figure(data=[go.Pie(
                labels=wellbeing_counts.index,
                values=wellbeing_counts.values,
                marker=dict(colors=['#e74c3c', '#f39c12', '#2ecc71'])
            )])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Complete Student Categorization
        st.subheader("📊 Complete Student Categorization (All 200 Students)")
        
        # Calculate all categories
        both_issues = df[(df['risk_level'].isin(['AT RISK', 'HIGH RISK'])) & (df['wellbeing_status'] != 'NORMAL')]
        at_risk_only = df[(df['risk_level'].isin(['AT RISK', 'HIGH RISK'])) & (df['wellbeing_status'] == 'NORMAL')]
        wellbeing_only = df[(df['risk_level'] == 'LOW RISK') & (df['wellbeing_status'] != 'NORMAL')]
        high_performers = df[(df['risk_level'] == 'LOW RISK') & (df['wellbeing_status'] == 'NORMAL')]
        
        # Display metrics in 4 columns
        col_cat1, col_cat2, col_cat3, col_cat4 = st.columns(4)
        
        with col_cat1:
            st.metric(
                "🚨 Both At-Risk & Wellbeing",
                len(both_issues),
                help="Students with BOTH academic AND wellbeing concerns - HIGHEST PRIORITY"
            )
        
        with col_cat2:
            st.metric(
                "⚠️ At-Risk Only",
                len(at_risk_only),
                help="Students struggling academically but normal wellbeing"
            )
        
        with col_cat3:
            st.metric(
                "💙 Wellbeing Only",
                len(wellbeing_only),
                help="Low-risk academically but have wellbeing concerns"
            )
        
        with col_cat4:
            st.metric(
                "⭐ High Performers",
                len(high_performers),
                help="Low-risk academically AND normal wellbeing - EXCELLENT students"
            )
        
        # Categorization Chart
        st.subheader("📈 Student Distribution by Category")
        
        categories = ['Both Issues\n(At-Risk+Wellbeing)', 'At-Risk Only', 'Wellbeing Only', 'High Performers']
        counts = [len(both_issues), len(at_risk_only), len(wellbeing_only), len(high_performers)]
        colors = ['#ff6b6b', '#ffd93d', '#3498db', '#2ecc71']
        
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=counts,
                marker=dict(color=colors),
                text=counts,
                textposition='auto',
            )
        ])
        fig.update_layout(
            title="Complete Breakdown of All 200 Students",
            xaxis_title="Student Category",
            yaxis_title="Number of Students",
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        col_summary1, col_summary2 = st.columns(2)
        
        with col_summary1:
            st.info(f"""
            **📌 Key Insights:**
            - **Highest Priority:** {len(both_issues)} students need immediate intervention (both at-risk + wellbeing issues)
            - **Academic Support:** {len(at_risk_only)} students need academic help
            - **Counseling Focus:** {len(wellbeing_only)} students may benefit from counseling despite low academic risk
            - **Positive Note:** {len(high_performers)} high-performing students are doing well
            """)
        
        with col_summary2:
            st.success(f"""
            **✅ Total Verification:**
            - {len(both_issues)} + {len(at_risk_only)} + {len(wellbeing_only)} + {len(high_performers)} = {len(both_issues) + len(at_risk_only) + len(wellbeing_only) + len(high_performers)} students ✓
            
            **Intervention Priority:**
            1. Both Issues ({len(both_issues)}) - URGENT
            2. At-Risk Only ({len(at_risk_only)}) - HIGH  
            3. Wellbeing Only ({len(wellbeing_only)}) - MEDIUM
            4. High Performers ({len(high_performers)}) - MONITOR
            """)
    
    # ========================================================================
    # PAGE: ANALYTICS
    # ========================================================================
    
    elif page == "📈 Analytics":
        st.header("📈 Engagement Analytics")
        
        # Engagement Statistics
        col_stats1, col_stats2 = st.columns(2)
        
        with col_stats1:
            st.subheader("📊 Engagement Statistics")
            stats = get_engagement_statistics(df)
            
            for key, value in stats.items():
                if isinstance(value, float):
                    st.metric(key.replace('_', ' ').title(), f"{value:.2f}")
                else:
                    st.metric(key.replace('_', ' ').title(), value)
        
        with col_stats2:
            st.subheader("📈 Engagement Distribution")
            dist = get_engagement_distribution(df)
            fig = go.Figure(data=[
                go.Bar(
                    x=list(dist.keys()),
                    y=list(dist.values()),
                    marker_color=['#2ecc71', '#f39c12', '#e74c3c']
                )
            ])
            fig.update_layout(
                xaxis_title="Engagement Level",
                yaxis_title="Number of Students",
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Top Engaged Students
        st.subheader("🌟 Top Engaged Students")
        top_n = st.slider("Select number of top students to display", 5, 20, 10)
        
        top_students = df.nlargest(top_n, 'engagement_score')[
            ['student_id', 'name', 'attendance', 'engagement_score', 'risk_level']
        ]
        
        # Create a combined label with name and student_id for unique identification
        top_students = top_students.copy()
        top_students['label'] = top_students['name'] + ' (' + top_students['student_id'] + ')'
        
        # Calculate dynamic height based on number of students (50px per student + 150px for margins)
        chart_height = max(400, top_n * 40 + 150)
        
        fig = go.Figure(data=[
            go.Bar(
                y=top_students['label'],
                x=top_students['engagement_score'],
                orientation='h',
                marker_color='steelblue'
            )
        ])
        fig.update_layout(
            xaxis_title="Engagement Score",
            height=chart_height,
            showlegend=False,
            margin=dict(l=200)  # Add left margin for student names
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(top_students, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Attendance vs Assignments
        st.subheader("📊 Attendance vs Assignment Completion")
        
        df_viz = df.copy()
        df_viz['assignment_rate'] = (df_viz['assignments_submitted'] / df_viz['total_assignments'] * 100).clip(0, 100)
        
        fig = px.scatter(
            df_viz,
            x='attendance',
            y='assignment_rate',
            color='engagement_score',
            size='engagement_score',
            hover_name='name',
            hover_data=['student_id', 'risk_level'],
            color_continuous_scale='RdYlGn',
            title='Attendance vs Assignment Completion Rate'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # PAGE: RISK ASSESSMENT
    # ========================================================================
    
    elif page == "⚠️ Risk Assessment":
        st.header("⚠️ Risk Assessment & Intervention")
        
        # Risk Statistics
        col_risk1, col_risk2 = st.columns(2)
        
        with col_risk1:
            st.subheader("📊 Risk Statistics")
            risk_stats = get_risk_statistics(df)
            
            st.metric("Total Students", risk_stats['total_students'])
            st.metric("High Risk", f"{risk_stats['high_risk_count']} ({risk_stats['high_risk_percentage']:.1f}%)")
            st.metric("At Risk", f"{risk_stats['at_risk_count']} ({risk_stats['at_risk_percentage']:.1f}%)")
            st.metric("Low Risk", f"{risk_stats['low_risk_count']} ({risk_stats['low_risk_percentage']:.1f}%)")
        
        with col_risk2:
            st.subheader("Risk Distribution")
            fig = go.Figure(data=[
                go.Pie(
                    labels=['High Risk', 'At Risk', 'Low Risk'],
                    values=[risk_stats['high_risk_count'], risk_stats['at_risk_count'], risk_stats['low_risk_count']],
                    marker=dict(colors=['#ff6b6b', '#ffd93d', '#6bcf7f'])
                )
            ])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # At-Risk Students Detail
        st.subheader("🚨 At-Risk Students")
        
        at_risk_df = get_at_risk_students(df)
        
        if len(at_risk_df) > 0:
            # Display table
            display_cols = ['student_id', 'name', 'attendance', 'assignments_submitted', 'total_assignments', 'engagement_score', 'risk_level']
            st.dataframe(
                at_risk_df[display_cols],
                use_container_width=True,
                hide_index=True
            )
            
            st.divider()
            
            # Individual student analysis
            st.subheader("🔍 Individual Student Analysis")
            
            selected_student = st.selectbox(
                "Select a student for detailed analysis",
                at_risk_df['name'].values,
                key="risk_student_select"
            )
            
            student_data = at_risk_df[at_risk_df['name'] == selected_student].iloc[0]
            
            col_detail1, col_detail2, col_detail3 = st.columns(3)
            
            with col_detail1:
                st.metric("Attendance", f"{student_data['attendance']:.1f}%")
                st.metric("LMS Logins", int(student_data['lms_logins']))
            
            with col_detail2:
                st.metric("Assignments", f"{student_data['assignments_submitted']}/{student_data['total_assignments']}")
                st.metric("Engagement Score", f"{student_data['engagement_score']:.1f}")
            
            with col_detail3:
                st.metric("Risk Level", student_data['risk_level'])
                st.metric("Wellbeing Status", student_data['wellbeing_status'])
            
            st.divider()
            
            # Recommendations
            st.subheader("💡 Intervention Recommendations")
            
            recommendations = []
            
            if student_data['attendance'] < 60:
                recommendations.append("🔴 **Critical Attendance**: Immediate intervention needed")
            elif student_data['attendance'] < 70:
                recommendations.append("🟡 **Low Attendance**: Regular check-ins recommended")
            
            if student_data['assignments_submitted'] / student_data['total_assignments'] < 0.5:
                recommendations.append("🔴 **Critical Assignment Rate**: Provide tutoring support")
            
            if student_data['engagement_score'] < 50:
                recommendations.append("🔴 **Very Low Engagement**: Consider mentorship program")
            
            for rec in recommendations:
                st.markdown(rec)
            
            st.markdown("""
            ### Suggested Actions
            1. Schedule one-on-one meeting with student
            2. Identify barriers to engagement
            3. Provide academic support (tutoring, study groups)
            4. Connect with counseling services if needed
            5. Weekly follow-up and monitoring
            """)
        else:
            st.success("✅ No at-risk students detected!")
    
    # ========================================================================
    # PAGE: WELLBEING MONITOR
    # ========================================================================
    
    elif page == "💚 Wellbeing Monitor":
        st.header("💚 Wellbeing & Behavioral Monitoring")
        
        # Wellbeing Statistics
        col_well1, col_well2 = st.columns(2)
        
        with col_well1:
            st.subheader("📊 Wellbeing Statistics")
            wellbeing_stats = get_wellbeing_statistics(df)
            
            st.metric("Total Students", wellbeing_stats['total_students'])
            st.metric("High Wellbeing Risk", f"{wellbeing_stats['high_risk_count']} ({wellbeing_stats['high_risk_percentage']:.1f}%)")
            st.metric("Medium Wellbeing Risk", f"{wellbeing_stats['medium_risk_count']} ({wellbeing_stats['medium_risk_percentage']:.1f}%)")
            st.metric("Normal Wellbeing", wellbeing_stats['normal_count'])
        
        with col_well2:
            st.subheader("Wellbeing Distribution")
            fig = go.Figure(data=[
                go.Pie(
                    labels=['High Risk', 'Medium Risk', 'Normal'],
                    values=[wellbeing_stats['high_risk_count'], wellbeing_stats['medium_risk_count'], wellbeing_stats['normal_count']],
                    marker=dict(colors=['#e74c3c', '#f39c12', '#2ecc71'])
                )
            ])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Wellbeing Alerts
        st.subheader("🚨 Wellbeing Alerts")
        
        wellbeing_alerts = get_wellbeing_alerts(df)
        
        if len(wellbeing_alerts) > 0:
            # Group by status
            high_risk_alerts = wellbeing_alerts[wellbeing_alerts['wellbeing_status'] == 'HIGH WELLBEING RISK']
            medium_risk_alerts = wellbeing_alerts[wellbeing_alerts['wellbeing_status'] == 'MEDIUM WELLBEING RISK']
            
            if len(high_risk_alerts) > 0:
                st.subheader("🔴 HIGH PRIORITY - High Wellbeing Risk")
                st.dataframe(
                    high_risk_alerts[['student_id', 'name', 'attendance', 'assignments_submitted', 'wellbeing_status']],
                    use_container_width=True,
                    hide_index=True
                )
                st.warning(f"⚠️ {len(high_risk_alerts)} students require immediate wellbeing support")
            
            st.divider()
            
            if len(medium_risk_alerts) > 0:
                st.subheader("🟡 MEDIUM PRIORITY - Medium Wellbeing Risk")
                st.dataframe(
                    medium_risk_alerts[['student_id', 'name', 'attendance', 'assignments_submitted', 'wellbeing_status']],
                    use_container_width=True,
                    hide_index=True
                )
                st.info(f"ℹ️ {len(medium_risk_alerts)} students showing concerning patterns")
        else:
            st.success("✅ All students showing normal wellbeing indicators!")
        
        st.divider()
        
        # Wellbeing Support Resources
        st.subheader("🤝 Support Resources")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        
        with col_res1:
            st.markdown("""
            ### 🏥 Counseling Services
            - Mental health support
            - Stress management
            - Crisis intervention
            """)
        
        with col_res2:
            st.markdown("""
            ### 📚 Academic Support
            - Tutoring programs
            - Study groups
            - Time management
            """)
        
        with col_res3:
            st.markdown("""
            ### 💪 Wellness Programs
            - Exercise programs
            - Sleep clinic
            - Peer support
            """)
    
    # ========================================================================
    # PAGE: TREND ANALYSIS
    # ========================================================================
    
    elif page == "📉 Trend Analysis":
        st.header("📉 Historical Trends & Progress")
        
        if historical_df is not None and len(historical_df) > 0:
            # Semester-wise analysis
            st.subheader("📊 Semester-wise Engagement Trends")
            
            # Convert numeric columns to numeric type (in case they were uploaded as strings)
            hist_analysis_df = historical_df.copy()
            numeric_cols = ['attendance', 'lms_logins', 'assignments', 'grade']
            for col in numeric_cols:
                if col in hist_analysis_df.columns:
                    hist_analysis_df[col] = pd.to_numeric(hist_analysis_df[col], errors='coerce')
            
            semester_analysis = hist_analysis_df.groupby('semester').agg({
                'attendance': 'mean',
                'lms_logins': 'mean',
                'assignments': 'mean',
                'grade': 'mean'
            }).reset_index()
            
            # Create multi-line chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=semester_analysis['semester'],
                y=semester_analysis['attendance'],
                mode='lines+markers',
                name='Attendance',
                line=dict(color='#2ecc71', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=semester_analysis['semester'],
                y=semester_analysis['grade'],
                mode='lines+markers',
                name='Average Grade',
                line=dict(color='#3498db', width=2),
                yaxis='y2'
            ))
            
            fig.update_layout(
                xaxis_title="Semester",
                yaxis_title="Attendance (%)",
                yaxis2=dict(
                    title="Average Grade",
                    overlaying='y',
                    side='right'
                ),
                height=400,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            
            # Individual Student Progress
            st.subheader("👤 Individual Student Progress")
            
            student_options = historical_df['student_id'].unique()
            selected_student_id = st.selectbox(
                "Select student to analyze progress",
                student_options,
                key="trend_student_select"
            )
            
            # Get student name
            student_name = df[df['student_id'] == selected_student_id]['name'].values
            if len(student_name) > 0:
                st.markdown(f"### {student_name[0]}")
            
            student_history = historical_df[historical_df['student_id'] == selected_student_id].sort_values('semester')
            
            if len(student_history) > 0:
                col_trend1, col_trend2 = st.columns(2)
                
                with col_trend1:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=student_history['semester'],
                        y=student_history['attendance'],
                        mode='lines+markers',
                        name='Attendance',
                        marker=dict(size=10),
                        line=dict(width=2)
                    ))
                    fig.update_layout(
                        xaxis_title="Semester",
                        yaxis_title="Attendance (%)",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col_trend2:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=student_history['semester'],
                        y=student_history['grade'],
                        mode='lines+markers',
                        name='Grade',
                        marker=dict(size=10, color='#e74c3c'),
                        line=dict(width=2, color='#e74c3c')
                    ))
                    fig.update_layout(
                        xaxis_title="Semester",
                        yaxis_title="Grade",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Progress Summary
                st.subheader("📋 Progress Summary")
                
                col_summary1, col_summary2, col_summary3 = st.columns(3)
                
                with col_summary1:
                    latest = student_history.iloc[-1]
                    latest_attendance = float(latest['attendance'])
                    latest_grade = str(latest['grade']).strip()
                    st.metric("Latest Attendance", f"{latest_attendance:.1f}%")
                    st.metric("Latest Grade", latest_grade)
                
                with col_summary2:
                    first = student_history.iloc[0]
                    first_attendance = float(first['attendance'])
                    first_grade = str(first['grade']).strip()
                    st.metric("Initial Attendance", f"{first_attendance:.1f}%")
                    st.metric("Initial Grade", first_grade)
                
                with col_summary3:
                    att_change = latest_attendance - first_attendance
                    
                    st.metric("Attendance Change", f"{att_change:+.1f}%")
                    st.metric("Grade Trend", f"Latest: {latest_grade} → Initial: {first_grade}")
                
                st.dataframe(student_history, use_container_width=True, hide_index=True)
        else:
            st.info("⚠️ Historical semester data not available. Upload historical_semesters.csv to enable trend analysis.")
    
    # ========================================================================
    # PAGE: AI ASSISTANT
    # ========================================================================
    
    elif page == "🤖 AI Assistant":
        st.header("🤖 Academic Analytics Decision-Support Assistant")
        
        st.info("""
        **For College Administrators**: Dean, HODs, Academic Coordinators, Mentors, Counseling Cell
        
        This AI provides data-driven institutional decision support based ONLY on actual student records.
        No generic advice - only dataset-based rankings, at-risk identification, and institutional procedures.
        
        Example questions:
        - "Show top engaged students" → Get actual students for mentoring roles
        - "Which students are at risk?" → Lists struggling students + intervention procedures
        - "Engagement analysis" → Metrics for Dean/HOD decision-making
        - "Predict performance for struggling students" → Data-based forecasting
        """)
        
        # Import AI components (optional - chromadb removed for deployment stability)
        ai_available = False
        try:
            from ai.ai_assistant import AIAssistant
            from ai.rag_pipeline import perform_rag_retrieval
            ai_available = True
        except Exception as e:
            ai_available = False
            st.warning(f"⚠️ AI Assistant unavailable on this deployment. All other features work normally.")
        
        # Query input
        user_query = st.text_input(
            "Ask a question about student engagement:",
            placeholder="e.g., Which students need the most support?",
            key="ai_query"
        )
        
        if st.button("🔍 Get AI Response", key="ai_submit"):
            if user_query:
                with st.spinner("Analyzing data and generating response..."):
                    try:
                        # Get AI response with student data and Groq API key
                        groq_api_key = os.getenv("GROQ_API_KEY", "YOUR_GROQ_API_KEY_HERE")
                        
                        # Load historical semester data for context
                        hist_df = None
                        try:
                            hist_df = load_historical_data(os.path.join(os.path.dirname(__file__), 'data/historical_semesters.csv'))
                        except Exception as e:
                            st.warning(f"⚠️  Could not load historical data: {str(e)}")
                        
                        assistant = AIAssistant(student_df=df, groq_api_key=groq_api_key, historical_df=hist_df)
                        response = assistant.generate_response(user_query)
                        
                        st.success("✅ Data-Driven Decision Support Response Generated")
                        st.markdown("### Institutional Response:")
                        st.markdown(response)
                    
                    except Exception as e:
                        st.error(f"Error generating response: {str(e)}")
                        st.info("💡 Tip: Make sure Groq API is configured for full AI features")
            else:
                st.warning("Please enter a question first")
        
        st.divider()
        
        # Suggested Questions
        st.subheader("💡 Institutional Decision-Support Questions")
        st.markdown("""
        **For College Administrators (Dean, HOD, Coordinators, Mentors, Counseling Cell):**
        
        - "Show top engaged students" → Returns actual students for peer mentoring roles & merit recognition
        - "Show least engaged students" → Lists critically struggling students requiring immediate intervention
        - "Which students are at risk?" → Lists at-risk students with institutional intervention procedures
        - "Engagement analysis" → Overall metrics & segment distribution with HOD/Dean actions
        - "Predict academic performance based on engagement" → Data-driven performance forecasting
        - "Which students need immediate support?" → Counseling Cell & Dean office referrals
        
        **All responses are based ONLY on actual student records in the system. No generic advice.**
        """)
    
    # ========================================================================
    # PAGE: REPORTS
    # ========================================================================
    
    elif page == "📋 Reports":
        st.header("📋 Comprehensive Reports")
        
        st.subheader("Generate Engagement Analysis Report")
        
        # Report type selection and button in one row
        col_select, col_button = st.columns([2, 1])
        
        with col_select:
            report_type = st.selectbox(
                "Select report type",
                ["Full Report", "Executive Summary", "At-Risk Only", "Wellbeing Only"],
                label_visibility="collapsed"
            )
        
        with col_button:
            st.markdown("")  # Spacing for alignment
            generate_btn = st.button("📄 Generate Report", key="generate_report", use_container_width=True)
        
        if generate_btn:
            with st.spinner("Generating report..."):
                try:
                    # Generate report
                    report_gen = ReportGenerator(df, historical_df)
                    
                    if report_type == "Full Report":
                        report_text = report_gen.generate_full_report()
                    elif report_type == "Executive Summary":
                        report_text = report_gen.generate_header()
                        report_text += report_gen.generate_dataset_summary()
                        report_text += report_gen.generate_engagement_summary()
                    elif report_type == "At-Risk Only":
                        report_text = report_gen.generate_header()
                        report_text += report_gen.generate_at_risk_section()
                    else:  # Wellbeing Only
                        report_text = report_gen.generate_header()
                        report_text += report_gen.generate_wellbeing_alerts()
                    
                    # Display report with proper container
                    st.markdown("### Report Content:")
                    report_container = st.container(border=True)
                    with report_container:
                        st.text(report_text)
                    
                    # Download button
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"engagement_report_{timestamp}.txt"
                    
                    st.download_button(
                        label="📥 Download Report",
                        data=report_text,
                        file_name=filename,
                        mime="text/plain",
                        use_container_width=True
                    )
                
                except Exception as e:
                    st.error(f"Error generating report: {str(e)}")
        
        st.divider()
        
        # Export Options
        st.subheader("📊 Export Data")
        
        col_export1, col_export2, col_export3 = st.columns(3)
        
        with col_export1:
            if st.button("📥 Export Full Data"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Full Data",
                    data=csv,
                    file_name="student_engagement_data.csv",
                    mime="text/csv"
                )
        
        with col_export2:
            if st.button("📥 Export At-Risk Students"):
                at_risk = get_at_risk_students(df)
                csv = at_risk.to_csv(index=False)
                st.download_button(
                    label="Download At-Risk Students",
                    data=csv,
                    file_name="at_risk_students.csv",
                    mime="text/csv"
                )
        
        with col_export3:
            if st.button("📥 Export Wellbeing Alerts"):
                alerts = get_wellbeing_alerts(df)
                csv = alerts.to_csv(index=False)
                st.download_button(
                    label="Download Wellbeing Alerts",
                    data=csv,
                    file_name="wellbeing_alerts.csv",
                    mime="text/csv"
                )
        
        st.divider()
        
        # Data Summary
        st.subheader("📈 Data Summary Statistics")
        
        col_summary1, col_summary2, col_summary3 = st.columns(3)
        
        with col_summary1:
            st.metric("Total Records", len(df))
            st.metric("Unique Students", df['student_id'].nunique())
        
        with col_summary2:
            avg_attendance = round(df['attendance'].mean(), 2)
            st.metric("Avg Attendance", f"{avg_attendance:.2f}%")
            avg_lms = round(df['lms_logins'].mean(), 2)
            st.metric("Avg LMS Logins", f"{avg_lms:.2f}")
        
        with col_summary3:
            avg_engagement = round(df['engagement_score'].mean(), 1)
            st.metric("Avg Engagement", f"{avg_engagement:.1f}/100")
            avg_completion = round((df['assignments_submitted'] / df['total_assignments'] * 100).mean(), 2)
            st.metric("Avg Completion Rate", f"{avg_completion:.2f}%")
        
        st.divider()
        
        # Detailed Statistics
        st.subheader("🔢 Detailed Statistics")
        
        st.dataframe(
            df.describe().round(2),
            use_container_width=True
        )

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown("""
---
**Student Engagement Analysis System v1.0**  
*AI-Powered Analytics for Student Wellbeing & Academic Performance*

For questions or support, contact the analytics team.
""")
