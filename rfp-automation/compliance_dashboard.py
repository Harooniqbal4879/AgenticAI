"""
Compliance dashboard for the RFP Response Automation application
"""

import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import numpy as np


def main() -> None:
    """Main compliance dashboard."""
    render_compliance_overview()
    render_requirement_tracking()
    render_compliance_checklist()


def render_compliance_overview() -> None:
    """Render compliance overview metrics."""
    st.subheader("✅ Compliance Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Compliance", "94.2%", "+1.8%")
    with col2:
        st.metric("Requirements Met", "47/50", "+3")
    with col3:
        st.metric("Critical Issues", "1", "-2")
    with col4:
        st.metric("Days to Deadline", "12", "-1")
    
    st.subheader("📊 Compliance by Category")
    
    categories = ['Technical', 'Legal', 'Financial', 'Administrative', 'Security']
    compliance_scores = [96, 92, 98, 89, 95]
    
    fig = go.Figure(data=[
        go.Bar(x=categories, y=compliance_scores,
               marker_color=['green' if score >= 95 else 'orange' if score >= 90 else 'red' 
                           for score in compliance_scores])
    ])
    
    fig.update_layout(
        title="Compliance Scores by Category (%)",
        xaxis_title="Category",
        yaxis_title="Compliance Score (%)",
        template="plotly_white",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_requirement_tracking() -> None:
    """Render requirement tracking table."""
    st.subheader("📋 Requirement Tracking")
    
    requirements = [
        {"id": "REQ-001", "category": "Technical", "description": "System Architecture Documentation", "status": "Complete", "priority": "High"},
        {"id": "REQ-002", "category": "Legal", "description": "Insurance Certificate", "status": "Complete", "priority": "High"},
        {"id": "REQ-003", "category": "Financial", "description": "Audited Financial Statements", "status": "Complete", "priority": "Medium"},
        {"id": "REQ-004", "category": "Technical", "description": "Security Compliance Report", "status": "In Progress", "priority": "High"},
        {"id": "REQ-005", "category": "Administrative", "description": "Team Resumes", "status": "Pending", "priority": "Medium"},
        {"id": "REQ-006", "category": "Security", "description": "Background Check Certificates", "status": "Complete", "priority": "High"},
        {"id": "REQ-007", "category": "Technical", "description": "Performance Benchmarks", "status": "Complete", "priority": "Low"},
        {"id": "REQ-008", "category": "Legal", "description": "Contract Terms Acceptance", "status": "Review Required", "priority": "High"},
    ]
    
    df = pd.DataFrame(requirements)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_filter = st.selectbox("Filter by Category", ["All"] + list(df['category'].unique()))
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All"] + list(df['status'].unique()))
    with col3:
        priority_filter = st.selectbox("Filter by Priority", ["All"] + list(df['priority'].unique()))
    
    filtered_df = df.copy()
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df['category'] == category_filter]
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df['status'] == status_filter]
    if priority_filter != "All":
        filtered_df = filtered_df[filtered_df['priority'] == priority_filter]
    
    for _, req in filtered_df.iterrows():
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([1, 2, 4, 2, 1])
            
            with col1:
                st.write(req['id'])
            with col2:
                st.write(req['category'])
            with col3:
                st.write(req['description'])
            with col4:
                status_color = {
                    'Complete': '🟢',
                    'In Progress': '🟡', 
                    'Pending': '🔴',
                    'Review Required': '🟠'
                }
                st.write(f"{status_color.get(req['status'], '⚪')} {req['status']}")
            with col5:
                priority_icon = {
                    'High': '🔴',
                    'Medium': '🟡',
                    'Low': '🟢'
                }
                st.write(f"{priority_icon.get(req['priority'], '⚪')} {req['priority']}")


def render_compliance_checklist() -> None:
    """Render interactive compliance checklist."""
    st.subheader("📝 Compliance Checklist")
    
    checklist_items = [
        "All required documents uploaded",
        "Technical specifications reviewed",
        "Legal terms accepted",
        "Financial documents verified",
        "Security clearances obtained",
        "Team qualifications documented",
        "References provided",
        "Proposal formatting compliant",
        "Submission deadline confirmed",
        "Final review completed"
    ]
    
    if 'checklist_status' not in st.session_state:
        st.session_state.checklist_status = {item: False for item in checklist_items}
    
    completed_count = 0
    
    for item in checklist_items:
        checked = st.checkbox(item, value=st.session_state.checklist_status[item])
        st.session_state.checklist_status[item] = checked
        if checked:
            completed_count += 1
    
    progress = completed_count / len(checklist_items)
    st.progress(progress, text=f"Checklist Progress: {completed_count}/{len(checklist_items)} items completed")
    
    if progress == 1.0:
        st.success("🎉 All compliance items completed! Ready for submission.")
    elif progress >= 0.8:
        st.warning("⚠️ Almost ready! Complete remaining items before submission.")
    else:
        st.info("📋 Continue working through the compliance checklist.")
