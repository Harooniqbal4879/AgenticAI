"""
Scoring detail dashboard for the RFP Response Automation application
"""

import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np


def main() -> None:
    """Main scoring detail dashboard."""
    render_scoring_overview()
    render_detailed_breakdown()
    render_improvement_suggestions()


def render_scoring_overview() -> None:
    """Render scoring overview."""
    st.subheader("📊 Scoring Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Score", "87.3/100", "+2.1")
    with col2:
        st.metric("Technical Score", "92.5/100", "+1.8")
    with col3:
        st.metric("Commercial Score", "82.1/100", "+2.4")
    with col4:
        st.metric("Compliance Score", "94.2/100", "+0.5")
    
    categories = ['Technical', 'Commercial', 'Management', 'Experience', 'Innovation']
    our_scores = [92.5, 82.1, 88.7, 91.3, 79.8]
    industry_avg = [78.2, 75.6, 82.1, 84.7, 73.2]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=categories,
        y=our_scores,
        name='Our Score',
        marker_color='darkblue'
    ))
    
    fig.add_trace(go.Bar(
        x=categories,
        y=industry_avg,
        name='Industry Average',
        marker_color='lightblue'
    ))
    
    fig.update_layout(
        title="Score Comparison vs Industry Average",
        xaxis_title="Categories",
        yaxis_title="Score",
        barmode='group',
        template="plotly_white",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_detailed_breakdown() -> None:
    """Render detailed score breakdown."""
    st.subheader("🔍 Detailed Score Breakdown")
    
    scoring_data = [
        {"Category": "Technical Approach", "Weight": "25%", "Raw Score": "9.2/10", "Weighted Score": "23.0/25", "Comments": "Excellent technical solution"},
        {"Category": "Team Qualifications", "Weight": "20%", "Raw Score": "9.1/10", "Weighted Score": "18.2/20", "Comments": "Highly qualified team"},
        {"Category": "Past Performance", "Weight": "15%", "Raw Score": "8.8/10", "Weighted Score": "13.2/15", "Comments": "Strong track record"},
        {"Category": "Price/Cost", "Weight": "15%", "Raw Score": "7.2/10", "Weighted Score": "10.8/15", "Comments": "Competitive but not lowest"},
        {"Category": "Project Management", "Weight": "10%", "Raw Score": "8.9/10", "Weighted Score": "8.9/10", "Comments": "Solid PM approach"},
        {"Category": "Innovation", "Weight": "10%", "Raw Score": "8.0/10", "Weighted Score": "8.0/10", "Comments": "Good innovative elements"},
        {"Category": "Timeline", "Weight": "5%", "Raw Score": "9.1/10", "Weighted Score": "4.6/5", "Comments": "Realistic timeline"}
    ]
    
    df = pd.DataFrame(scoring_data)
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    st.subheader("📈 Score Distribution")
    
    weights = [25, 20, 15, 15, 10, 10, 5]
    categories = ["Technical", "Team", "Performance", "Price", "PM", "Innovation", "Timeline"]
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=categories,
        values=weights,
        hole=0.3,
        textinfo='label+percent'
    )])
    
    fig_pie.update_layout(
        title="Evaluation Weight Distribution",
        height=400
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)


def render_improvement_suggestions() -> None:
    """Render improvement suggestions."""
    st.subheader("💡 Improvement Suggestions")
    
    improvements = [
        {
            "area": "Price/Cost Competitiveness",
            "current_score": 7.2,
            "target_score": 8.5,
            "impact": "High",
            "effort": "Medium",
            "suggestions": [
                "Review cost structure for optimization opportunities",
                "Consider value engineering approaches",
                "Benchmark against competitor pricing"
            ]
        },
        {
            "area": "Innovation",
            "current_score": 8.0,
            "target_score": 9.0,
            "impact": "Medium",
            "effort": "Low",
            "suggestions": [
                "Highlight unique technological approaches",
                "Emphasize proprietary methodologies",
                "Include case studies of innovative solutions"
            ]
        },
        {
            "area": "Technical Approach",
            "current_score": 9.2,
            "target_score": 9.5,
            "impact": "Low",
            "effort": "Low",
            "suggestions": [
                "Add more technical diagrams",
                "Include additional technical specifications",
                "Provide more detailed architecture documentation"
            ]
        }
    ]
    
    for improvement in improvements:
        with st.expander(f"🎯 {improvement['area']} (Current: {improvement['current_score']}/10)"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Current Score", f"{improvement['current_score']}/10")
            with col2:
                st.metric("Target Score", f"{improvement['target_score']}/10")
            with col3:
                potential_gain = improvement['target_score'] - improvement['current_score']
                st.metric("Potential Gain", f"+{potential_gain:.1f}")
            
            st.write(f"**Impact:** {improvement['impact']} | **Effort:** {improvement['effort']}")
            
            st.write("**Suggestions:**")
            for suggestion in improvement['suggestions']:
                st.write(f"• {suggestion}")
    
    st.subheader("📊 Improvement Priority Matrix")
    
    areas = [imp['area'] for imp in improvements]
    impact_scores = {'High': 3, 'Medium': 2, 'Low': 1}
    effort_scores = {'High': 3, 'Medium': 2, 'Low': 1}
    
    impact_values = [impact_scores[imp['impact']] for imp in improvements]
    effort_values = [effort_scores[imp['effort']] for imp in improvements]
    
    fig_matrix = go.Figure()
    
    fig_matrix.add_trace(go.Scatter(
        x=effort_values,
        y=impact_values,
        mode='markers+text',
        text=areas,
        textposition="top center",
        marker=dict(
            size=20,
            color=['red', 'orange', 'green'],
            opacity=0.7
        ),
        showlegend=False
    ))
    
    fig_matrix.update_layout(
        title="Improvement Priority: Impact vs Effort",
        xaxis_title="Effort Required (1=Low, 3=High)",
        yaxis_title="Impact Potential (1=Low, 3=High)",
        template="plotly_white",
        height=400,
        xaxis=dict(range=[0.5, 3.5]),
        yaxis=dict(range=[0.5, 3.5])
    )
    
    fig_matrix.add_annotation(x=1, y=3, text="Quick Wins", showarrow=False, font=dict(size=12, color="green"))
    fig_matrix.add_annotation(x=3, y=3, text="Major Projects", showarrow=False, font=dict(size=12, color="orange"))
    fig_matrix.add_annotation(x=1, y=1, text="Fill-ins", showarrow=False, font=dict(size=12, color="gray"))
    fig_matrix.add_annotation(x=3, y=1, text="Thankless Tasks", showarrow=False, font=dict(size=12, color="red"))
    
    st.plotly_chart(fig_matrix, use_container_width=True)
