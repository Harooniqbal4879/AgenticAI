"""
Win probability dashboard for the RFP Response Automation application
"""

import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np


def main() -> None:
    """Main win probability dashboard."""
    render_probability_overview()
    render_factor_analysis()
    render_historical_trends()


def render_probability_overview() -> None:
    """Render win probability overview."""
    st.subheader("🎯 Win Probability Overview")
    
    current_bids = [
        {"name": "Healthcare System RFP", "probability": 85, "value": "$3.2M", "status": "High"},
        {"name": "Government Contract", "probability": 62, "value": "$1.8M", "status": "Medium"},
        {"name": "Tech Modernization", "probability": 45, "value": "$2.1M", "status": "Medium"},
        {"name": "Infrastructure Upgrade", "probability": 78, "value": "$4.5M", "status": "High"},
        {"name": "Security Assessment", "probability": 33, "value": "$0.9M", "status": "Low"}
    ]
    
    col1, col2, col3, col4 = st.columns(4)
    
    avg_probability = np.mean([bid["probability"] for bid in current_bids])
    total_value = sum([float(bid["value"].replace("$", "").replace("M", "")) for bid in current_bids])
    weighted_value = sum([float(bid["value"].replace("$", "").replace("M", "")) * bid["probability"] / 100 for bid in current_bids])
    
    with col1:
        st.metric("Average Win Probability", f"{avg_probability:.1f}%", "+3.2%")
    with col2:
        st.metric("Total Pipeline Value", f"${total_value:.1f}M", "+$1.2M")
    with col3:
        st.metric("Expected Value", f"${weighted_value:.1f}M", "+$0.8M")
    with col4:
        st.metric("High Probability Bids", "2", "+1")
    
    st.subheader("📋 Current Bid Probabilities")
    
    df = pd.DataFrame(current_bids)
    
    def get_probability_color(prob):
        if prob >= 70:
            return "🟢"
        elif prob >= 50:
            return "🟡"
        else:
            return "🔴"
    
    for _, bid in df.iterrows():
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.write(f"**{bid['name']}**")
        with col2:
            st.write(f"{get_probability_color(bid['probability'])} {bid['probability']}%")
        with col3:
            st.write(bid['value'])
        with col4:
            st.write(bid['status'])


def render_factor_analysis() -> None:
    """Render win probability factor analysis."""
    st.subheader("📊 Probability Factors Analysis")
    
    factors = [
        "Technical Expertise",
        "Price Competitiveness", 
        "Past Performance",
        "Team Experience",
        "Solution Innovation",
        "Client Relationship",
        "Compliance Score"
    ]
    
    our_scores = [8.5, 7.2, 9.1, 8.8, 7.9, 8.3, 9.5]
    competitor_avg = [7.1, 8.0, 7.5, 7.8, 6.9, 7.2, 8.1]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=our_scores,
        theta=factors,
        fill='toself',
        name='Our Company',
        line_color='blue'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=competitor_avg,
        theta=factors,
        fill='toself',
        name='Competitor Average',
        line_color='red',
        opacity=0.6
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=True,
        title="Win Probability Factors Comparison",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_historical_trends() -> None:
    """Render historical win probability trends."""
    st.subheader("📈 Historical Win Probability Trends")
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    win_probabilities = [65, 68, 72, 69, 74, 78, 75, 80, 77, 82, 79, 85]
    actual_wins = [60, 70, 75, 65, 80, 75, 70, 85, 80, 85, 75, 90]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months,
        y=win_probabilities,
        mode='lines+markers',
        name='Predicted Win Probability',
        line=dict(color='blue', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=months,
        y=actual_wins,
        mode='lines+markers',
        name='Actual Win Rate',
        line=dict(color='green', width=3)
    ))
    
    fig.update_layout(
        title="Win Probability vs Actual Results",
        xaxis_title="Month",
        yaxis_title="Percentage (%)",
        template="plotly_white",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        accuracy = 100 - np.mean(np.abs(np.array(win_probabilities) - np.array(actual_wins)))
        st.metric("Prediction Accuracy", f"{accuracy:.1f}%", "+2.3%")
    
    with col2:
        correlation = np.corrcoef(win_probabilities, actual_wins)[0, 1]
        st.metric("Prediction Correlation", f"{correlation:.3f}", "+0.05")
    
    with col3:
        improvement = (win_probabilities[-1] - win_probabilities[0])
        st.metric("YTD Improvement", f"+{improvement:.1f}%", "+5.2%")
