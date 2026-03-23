"""
Report Generator Module

Generates comprehensive analytical reports from student engagement data.
"""

import pandas as pd
from datetime import datetime
from typing import Dict, List


class ReportGenerator:
    """Generates structured engagement analysis reports."""
    
    def __init__(self, current_df: pd.DataFrame, historical_df: pd.DataFrame = None):
        """
        Initialize report generator.
        
        Args:
            current_df: Current semester student data
            historical_df: Optional historical semester data
        """
        self.current_df = current_df
        self.historical_df = historical_df if historical_df is not None else pd.DataFrame()
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_header(self) -> str:
        """Generate report header."""
        header = f"""
{'='*80}
STUDENT ENGAGEMENT ANALYSIS REPORT
{'='*80}
Report Generated: {self.timestamp}
{'='*80}
"""
        return header
    
    def generate_dataset_summary(self) -> str:
        """Generate dataset summary section."""
        total_students = len(self.current_df)
        avg_attendance = self.current_df['attendance'].mean() if 'attendance' in self.current_df.columns else 0
        avg_lms = self.current_df['lms_logins'].mean() if 'lms_logins' in self.current_df.columns else 0
        
        section = f"""
{'-'*80}
DATASET SUMMARY
{'-'*80}
Total Students: {total_students}
Average Attendance: {avg_attendance:.2f}%
Average LMS Logins: {avg_lms:.2f}
Report Period: Current Semester
{'-'*80}
"""
        return section
    
    def generate_engagement_summary(self) -> str:
        """Generate engagement metrics summary."""
        if 'engagement_score' not in self.current_df.columns:
            from modules.engagement_calculator import add_engagement_scores
            df = add_engagement_scores(self.current_df)
        else:
            df = self.current_df
        
        avg_engagement = df['engagement_score'].mean()
        high_engagement = len(df[df['engagement_score'] >= 80])
        moderate_engagement = len(df[(df['engagement_score'] >= 60) & (df['engagement_score'] < 80)])
        low_engagement = len(df[df['engagement_score'] < 60])
        
        section = f"""
{'-'*80}
ENGAGEMENT METRICS
{'-'*80}
Average Engagement Score: {avg_engagement:.2f}/100
Highly Engaged Students: {high_engagement} ({high_engagement/len(df)*100:.1f}%)
Moderately Engaged Students: {moderate_engagement} ({moderate_engagement/len(df)*100:.1f}%)
Low Engagement Students: {low_engagement} ({low_engagement/len(df)*100:.1f}%)
{'-'*80}
"""
        return section
    
    def generate_top_students(self, top_n: int = 5) -> str:
        """Generate top engaged students section."""
        if 'engagement_score' not in self.current_df.columns:
            from modules.engagement_calculator import add_engagement_scores
            df = add_engagement_scores(self.current_df)
        else:
            df = self.current_df
        
        top_students = df.nlargest(top_n, 'engagement_score')[['student_id', 'name', 'engagement_score', 'attendance']]
        
        section = f"""
{'-'*80}
TOP {top_n} ENGAGED STUDENTS
{'-'*80}
"""
        for idx, (_, row) in enumerate(top_students.iterrows(), 1):
            section += f"{idx}. {row['name']} ({row['student_id']}) - Score: {row['engagement_score']:.2f}, Attendance: {row['attendance']:.1f}%\n"
        
        section += f"{'-'*80}\n"
        return section
    
    def generate_at_risk_section(self) -> str:
        """Generate at-risk students section."""
        if 'risk_level' not in self.current_df.columns:
            from modules.risk_detector import add_risk_levels
            df = add_risk_levels(self.current_df)
        else:
            df = self.current_df
        
        at_risk = df[df['risk_level'].isin(['AT RISK', 'HIGH RISK'])].sort_values('engagement_score')
        
        section = f"""
{'-'*80}
AT-RISK STUDENTS
{'-'*80}
Total At-Risk Students: {len(at_risk)}

"""
        if len(at_risk) > 0:
            section += "ID\tName\tEngagement\tAttendance\tAssignments\tRisk Level\n"
            section += "-" * 80 + "\n"
            for _, row in at_risk.iterrows():
                assignments = f"{row['assignments_submitted']}/{row['total_assignments']}" if 'assignments_submitted' in row else "N/A"
                section += f"{row['student_id']}\t{row['name']}\t{row['engagement_score']:.1f}\t{row['attendance']:.1f}%\t{assignments}\t{row['risk_level']}\n"
        
        section += f"{'-'*80}\n"
        return section
    
    def generate_wellbeing_alerts(self) -> str:
        """Generate wellbeing alerts section."""
        if 'wellbeing_status' not in self.current_df.columns:
            from modules.wellbeing_detector import add_wellbeing_status
            df = add_wellbeing_status(self.current_df)
        else:
            df = self.current_df
        
        high_risk = df[df['wellbeing_status'] == 'HIGH WELLBEING RISK']
        medium_risk = df[df['wellbeing_status'] == 'MEDIUM WELLBEING RISK']
        
        section = f"""
{'-'*80}
WELLBEING INDICATORS
{'-'*80}
High Wellbeing Risk: {len(high_risk)} students
Medium Wellbeing Risk: {len(medium_risk)} students
Normal Wellbeing: {len(df[df['wellbeing_status'] == 'NORMAL'])} students

"""
        if len(high_risk) > 0:
            section += "HIGH PRIORITY WELLBEING ALERTS:\n"
            for _, row in high_risk.head(10).iterrows():
                section += f"  - {row['name']} ({row['student_id']}): Attendance {row['attendance']:.1f}%, Assignments {row['assignments_submitted']}/{row['total_assignments']}\n"
        
        section += f"{'-'*80}\n"
        return section
    
    def generate_recommendations(self) -> str:
        """Generate recommendations section."""
        if 'risk_level' not in self.current_df.columns:
            from modules.risk_detector import add_risk_levels
            df = add_risk_levels(self.current_df)
        else:
            df = self.current_df
        
        at_risk_count = len(df[df['risk_level'].isin(['AT RISK', 'HIGH RISK'])])
        high_engagement = len(df[df['engagement_score'] >= 80]) if 'engagement_score' in df.columns else 0
        
        section = f"""
{'-'*80}
RECOMMENDATIONS
{'-'*80}

1. IMMEDIATE ACTIONS:
   - Reach out to {at_risk_count} at-risk students with personalized support
   - Schedule one-on-one meetings to understand barriers to engagement
   - Provide tutoring and academic resources

2. ENGAGEMENT IMPROVEMENT:
   - Implement weekly engagement check-ins
   - Encourage LMS platform usage through interactive content
   - Create peer mentoring program with {high_engagement} highly engaged students

3. WELLBEING SUPPORT:
   - Offer counseling and mental health services
   - Create support groups for struggling students
   - Establish early warning system for behavioral changes

4. MONITORING:
   - Track engagement trends biweekly
   - Update prediction models monthly
   - Generate quarterly trend reports

{'-'*80}
"""
        return section
    
    def generate_full_report(self) -> str:
        """Generate complete report."""
        report = self.generate_header()
        report += self.generate_dataset_summary()
        report += self.generate_engagement_summary()
        report += self.generate_top_students()
        report += self.generate_at_risk_section()
        report += self.generate_wellbeing_alerts()
        report += self.generate_recommendations()
        report += f"\n{'='*80}\nEND OF REPORT\n{'='*80}\n"
        
        return report
    
    def save_report(self, file_path: str) -> bool:
        """
        Save report to file.
        
        Args:
            file_path: Path to save report
            
        Returns:
            True if successful
        """
        try:
            with open(file_path, 'w') as f:
                f.write(self.generate_full_report())
            return True
        except Exception as e:
            print(f"Error saving report: {str(e)}")
            return False
