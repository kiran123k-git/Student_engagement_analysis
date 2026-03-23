"""
Visualizations Module

Creates charts and visualizations for engagement analytics dashboard.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import io
import base64

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
}

# Plotly Color Scheme
PLOTLY_COLORS = ['#1e40af', '#0369a1', '#059669', '#d97706', '#dc2626', '#6366f1', '#8b5cf6', '#ec4899']

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['axes.facecolor'] = '#f8fafb'
plt.rcParams['figure.facecolor'] = 'white'


def create_engagement_histogram(df: pd.DataFrame, title: str = "Engagement Score Distribution") -> plt.Figure:
    """
    Create histogram of engagement scores.
    
    Args:
        df: DataFrame with engagement_score column
        title: Chart title
        
    Returns:
        Matplotlib figure
    """
    if 'engagement_score' not in df.columns:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    scores = df['engagement_score']
    ax.hist(scores, bins=20, color=COLOR_PALETTE['primary'], edgecolor='white', alpha=0.8, linewidth=1.5)
    ax.axvline(scores.mean(), color=COLOR_PALETTE['danger'], linestyle='--', linewidth=2.5, label=f'Mean: {scores.mean():.1f}')
    ax.axvline(scores.median(), color=COLOR_PALETTE['success'], linestyle='--', linewidth=2.5, label=f'Median: {scores.median():.1f}')
    
    ax.set_xlabel('Engagement Score', fontsize=12, fontweight='bold', color=COLOR_PALETTE['dark'])
    ax.set_ylabel('Number of Students', fontsize=12, fontweight='bold', color=COLOR_PALETTE['dark'])
    ax.set_title(title, fontsize=14, fontweight='bold', color=COLOR_PALETTE['primary'])
    ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
    ax.grid(axis='y', alpha=0.3, color='gray', linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    return fig



def create_risk_level_pie_chart(df: pd.DataFrame, title: str = "Student Risk Distribution") -> plt.Figure:
    """
    Create pie chart of risk levels.
    
    Args:
        df: DataFrame with risk_level column
        title: Chart title
        
    Returns:
        Matplotlib figure
    """
    if 'risk_level' not in df.columns:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    risk_counts = df['risk_level'].value_counts()
    colors = {'HIGH RISK': COLOR_PALETTE['danger'], 'AT RISK': COLOR_PALETTE['warning'], 'LOW RISK': COLOR_PALETTE['success']}
    color_list = [colors.get(level, COLOR_PALETTE['light']) for level in risk_counts.index]
    
    wedges, texts, autotexts = ax.pie(risk_counts.values, 
                                        labels=risk_counts.index, 
                                        autopct='%1.1f%%',
                                        colors=color_list,
                                        startangle=90,
                                        textprops={'fontsize': 11, 'fontweight': 'bold'},
                                        wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    
    # Make percentage text bold and white
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20, color=COLOR_PALETTE['primary'])
    plt.tight_layout()
    return fig


def create_engagement_level_bar_chart(df: pd.DataFrame, title: str = "Engagement Level Distribution") -> plt.Figure:
    """
    Create bar chart of engagement levels.
    
    Args:
        df: DataFrame with engagement_level column
        title: Chart title
        
    Returns:
        Matplotlib figure
    """
    if 'engagement_level' not in df.columns:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    level_counts = df['engagement_level'].value_counts()
    colors = {'HIGH ENGAGEMENT': '#2ecc71', 'MODERATE ENGAGEMENT': '#f39c12', 'LOW ENGAGEMENT': '#e74c3c'}
    color_list = [colors.get(level, 'gray') for level in level_counts.index]
    
    bars = ax.bar(level_counts.index, level_counts.values, color=color_list, edgecolor='black', alpha=0.8)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_ylabel('Number of Students', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=15, ha='right')
    
    plt.tight_layout()
    return fig


def create_top_students_bar_chart(df: pd.DataFrame, top_n: int = 10, title: str = "Top Engaged Students") -> plt.Figure:
    """
    Create bar chart of top engaged students.
    
    Args:
        df: DataFrame with engagement_score and name columns
        top_n: Number of top students to display
        title: Chart title
        
    Returns:
        Matplotlib figure
    """
    if 'engagement_score' not in df.columns or 'name' not in df.columns:
        return None
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Group by student name and take the maximum engagement score to avoid duplicates
    df_grouped = df.groupby('name', as_index=False).agg({'engagement_score': 'max'})
    top_students = df_grouped.nlargest(top_n, 'engagement_score')
    
    bars = ax.barh(range(len(top_students)), top_students['engagement_score'].values, color=COLOR_PALETTE['primary'], edgecolor='white', alpha=0.85, linewidth=1.5)
    ax.set_yticks(range(len(top_students)))
    ax.set_yticklabels(top_students['name'].values, fontweight='600')
    ax.set_xlabel('Engagement Score', fontsize=12, fontweight='bold', color=COLOR_PALETTE['dark'])
    ax.set_xlim(0, 100)
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}',
                ha='left', va='center', fontsize=10, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor=COLOR_PALETTE['warning'], alpha=0.8))
    
    ax.set_title(title, fontsize=14, fontweight='bold', color=COLOR_PALETTE['primary'])
    ax.grid(axis='x', alpha=0.3, color='gray', linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    return fig


def create_attendance_vs_assignment_scatter(df: pd.DataFrame, title: str = "Attendance vs Assignment Completion") -> plt.Figure:
    """
    Create scatter plot of attendance vs assignments.
    
    Args:
        df: DataFrame with attendance, assignments_submitted, total_assignments columns
        title: Chart title
        
    Returns:
        Matplotlib figure
    """
    if not all(col in df.columns for col in ['attendance', 'assignments_submitted', 'total_assignments']):
        return None
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    assignment_rate = (df['assignments_submitted'] / df['total_assignments'] * 100).clip(0, 100)
    
    # Color by engagement score if available
    if 'engagement_score' in df.columns:
        scatter = ax.scatter(df['attendance'], assignment_rate, 
                            c=df['engagement_score'], cmap='RdYlGn', 
                            s=120, alpha=0.7, edgecolors='white', linewidth=1.5)
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Engagement Score', fontsize=11, fontweight='bold')
    else:
        ax.scatter(df['attendance'], assignment_rate, s=120, alpha=0.7, 
                  color=COLOR_PALETTE['primary'], edgecolors='white', linewidth=1.5)
    
    ax.set_xlabel('Attendance (%)', fontsize=12, fontweight='bold', color=COLOR_PALETTE['dark'])
    ax.set_ylabel('Assignment Completion Rate (%)', fontsize=12, fontweight='bold', color=COLOR_PALETTE['dark'])
    ax.set_title(title, fontsize=14, fontweight='bold', color=COLOR_PALETTE['primary'])
    ax.grid(True, alpha=0.3, color='gray', linestyle='--')
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 105)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    return fig


def create_semester_trend_line_chart(trends: Dict, metric: str = 'attendance') -> plt.Figure:
    """
    Create line chart for semester trends.
    
    Args:
        trends: Dictionary with semesters and metric values
        metric: Metric to plot ('attendance', 'lms_trend', 'grade_trend')
        
    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(11, 6))
    
    semesters = trends.get('semesters', [])
    metric_key = f'{metric}_trend' if metric != 'attendance' else 'attendance_trend'
    values = trends.get(metric_key, [])
    
    if not semesters or not values:
        return None
    
    ax.plot(semesters, values, marker='o', linewidth=3, markersize=10, color=COLOR_PALETTE['primary'], markerfacecolor=COLOR_PALETTE['warning'], markeredgecolor=COLOR_PALETTE['primary'], markeredgewidth=2)
    ax.fill_between(range(len(semesters)), values, alpha=0.25, color=COLOR_PALETTE['primary'])
    
    ax.set_xlabel('Semester', fontsize=12, fontweight='bold', color=COLOR_PALETTE['dark'])
    ax.set_ylabel(f'{metric.capitalize()} Trend', fontsize=12, fontweight='bold', color=COLOR_PALETTE['dark'])
    ax.set_title(f'{metric.capitalize()} Trend Analysis', fontsize=14, fontweight='bold', color=COLOR_PALETTE['primary'])
    ax.grid(True, alpha=0.3, color='gray', linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig


def create_wellbeing_status_pie_chart(df: pd.DataFrame, title: str = "Student Wellbeing Status") -> plt.Figure:
    """
    Create pie chart of wellbeing status.
    
    Args:
        df: DataFrame with wellbeing_status column
        title: Chart title
        
    Returns:
        Matplotlib figure
    """
    if 'wellbeing_status' not in df.columns:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    status_counts = df['wellbeing_status'].value_counts()
    colors = {'HIGH WELLBEING RISK': COLOR_PALETTE['danger'], 'MEDIUM WELLBEING RISK': COLOR_PALETTE['warning'], 'NORMAL': COLOR_PALETTE['success']}
    color_list = [colors.get(status, COLOR_PALETTE['light']) for status in status_counts.index]
    
    wedges, texts, autotexts = ax.pie(status_counts.values,
                                        labels=status_counts.index,
                                        autopct='%1.1f%%',
                                        colors=color_list,
                                        startangle=90,
                                        textprops={'fontsize': 11, 'fontweight': 'bold'},
                                        wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20, color=COLOR_PALETTE['primary'])
    plt.tight_layout()
    return fig


def figure_to_base64(fig: plt.Figure) -> str:
    """
    Convert matplotlib figure to base64 string.
    
    Args:
        fig: Matplotlib figure
        
    Returns:
        Base64 encoded string
    """
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    plt.close(fig)
    return image_base64
