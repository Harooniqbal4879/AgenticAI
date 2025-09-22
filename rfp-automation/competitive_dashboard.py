"""
Competitive dashboard for the RFP Response Automation application
"""

import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np


def main() -> None:
    """Main competitive dashboard."""
    render_competitive_metrics()
    render_competitor_analysis()
    render_market_positioning()


def render_competitive_metrics() -> None:
    """Render competitive performance metrics."""
    st.subheader("🏆 Competitive Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Market Share", "23.5%", "+2.1%")
    with col2:
        st.metric("Win Rate vs Competitors", "67%", "+5%")
    with col3:
        st.metric("Avg. Bid Value", "$2.3M", "+$0.4M")
    with col4:
        st.metric("Response Time Advantage", "-1.2 days", "-0.3 days")


def render_competitor_analysis() -> None:
    """Render competitor analysis charts."""
    st.subheader("📊 Competitor Analysis")
    
    competitors = ['Company A', 'Company B', 'Company C', 'Company D', 'Our Company']
    win_rates = [45, 38, 52, 41, 67]
    avg_bid_values = [1.8, 2.1, 1.9, 2.0, 2.3]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_win = go.Figure(data=[
            go.Bar(x=competitors, y=win_rates, 
                  marker_color=['lightblue' if x != 'Our Company' else 'darkblue' for x in competitors])
        ])
        fig_win.update_layout(
            title="Win Rate Comparison (%)",
            xaxis_title="Companies",
            yaxis_title="Win Rate (%)",
            template="plotly_white"
        )
        st.plotly_chart(fig_win, use_container_width=True)
    
    with col2:
        fig_value = go.Figure(data=[
            go.Bar(x=competitors, y=avg_bid_values,
                  marker_color=['lightgreen' if x != 'Our Company' else 'darkgreen' for x in competitors])
        ])
        fig_value.update_layout(
            title="Average Bid Value ($M)",
            xaxis_title="Companies", 
            yaxis_title="Bid Value ($M)",
            template="plotly_white"
        )
        st.plotly_chart(fig_value, use_container_width=True)


def render_market_positioning() -> None:
    """Render market positioning analysis."""
    st.subheader("🎯 Market Positioning")
    
    companies = ['Company A', 'Company B', 'Company C', 'Company D', 'Our Company']
    quality_scores = [7.2, 6.8, 8.1, 7.5, 8.7]
    price_competitiveness = [6.5, 8.2, 6.9, 7.8, 8.5]
    
    fig_scatter = go.Figure()
    
    for i, company in enumerate(companies):
        color = 'red' if company == 'Our Company' else 'blue'
        size = 15 if company == 'Our Company' else 10
        
        fig_scatter.add_trace(go.Scatter(
            x=[quality_scores[i]],
            y=[price_competitiveness[i]],
            mode='markers+text',
            name=company,
            text=[company],
            textposition="top center",
            marker=dict(size=size, color=color),
            showlegend=False
        ))
    
    fig_scatter.update_layout(
        title="Market Positioning: Quality vs Price Competitiveness",
        xaxis_title="Quality Score (1-10)",
        yaxis_title="Price Competitiveness (1-10)",
        template="plotly_white",
        height=500
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.subheader("💡 Competitive Insights")
    
    insights = [
        "🔥 **Strength**: Highest quality score among competitors",
        "📈 **Opportunity**: Price competitiveness is strong but can be improved",
        "⚠️ **Watch**: Company C has similar quality but lower price competitiveness",
        "🎯 **Strategy**: Focus on value proposition to maintain quality leadership"
    ]
    
    for insight in insights:
        st.markdown(insight)
