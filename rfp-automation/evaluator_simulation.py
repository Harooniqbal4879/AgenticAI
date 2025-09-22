"""
Evaluator simulation for the RFP Response Automation application
"""

import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import numpy as np


def main() -> None:
    """Main evaluator simulation dashboard."""
    render_simulation_overview()
    render_scoring_simulation()
    render_scenario_analysis()


def render_simulation_overview() -> None:
    """Render simulation overview."""
    st.subheader("🎭 Evaluator Simulation Overview")
    
    st.info("""
    This simulation helps predict how evaluators might score your proposal based on different criteria.
    Adjust the weights and see how your overall score changes.
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Simulated Score", "87.3", "+2.1")
    with col2:
        st.metric("Rank Prediction", "2nd", "↑1")
    with col3:
        st.metric("Win Probability", "78%", "+5%")
    with col4:
        st.metric("Score Confidence", "High", "")


def render_scoring_simulation() -> None:
    """Render interactive scoring simulation."""
    st.subheader("⚖️ Interactive Scoring Simulation")
    
    criteria = [
        "Technical Approach",
        "Team Qualifications", 
        "Past Performance",
        "Price/Cost",
        "Project Management",
        "Innovation",
        "Timeline"
    ]
    
    default_weights = [25, 20, 15, 15, 10, 10, 5]
    
    our_scores = [8.5, 9.0, 8.8, 7.2, 8.3, 7.8, 9.1]
    
    st.write("**Adjust Evaluation Weights:**")
    
    weights = []
    cols = st.columns(len(criteria))
    
    for i, (criterion, default_weight) in enumerate(zip(criteria, default_weights)):
        with cols[i]:
            weight = st.slider(
                criterion,
                min_value=0,
                max_value=50,
                value=default_weight,
                step=5,
                key=f"weight_{i}"
            )
            weights.append(weight)
    
    total_weight = sum(weights)
    if total_weight > 0:
        normalized_weights = [w / total_weight * 100 for w in weights]
    else:
        normalized_weights = default_weights
    
    weighted_score = sum(score * weight / 100 for score, weight in zip(our_scores, normalized_weights))
    
    st.write(f"**Total Weight:** {total_weight}% (normalized to 100%)")
    st.write(f"**Weighted Score:** {weighted_score:.2f}/10 ({weighted_score * 10:.1f}%)")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=criteria,
        y=[score * weight / 100 for score, weight in zip(our_scores, normalized_weights)],
        name='Weighted Scores',
        marker_color='lightblue'
    ))
    
    fig.update_layout(
        title="Weighted Score Breakdown",
        xaxis_title="Evaluation Criteria",
        yaxis_title="Weighted Score",
        template="plotly_white",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_scenario_analysis() -> None:
    """Render scenario analysis."""
    st.subheader("🔮 Scenario Analysis")
    
    evaluator_profiles = {
        "Technical Focused": [35, 15, 20, 10, 10, 10, 0],
        "Cost Conscious": [15, 15, 15, 40, 10, 5, 0],
        "Experience Driven": [20, 25, 30, 15, 5, 5, 0],
        "Innovation Oriented": [20, 15, 10, 15, 10, 25, 5],
        "Balanced": [20, 20, 15, 15, 10, 10, 10]
    }
    
    our_scores = [8.5, 9.0, 8.8, 7.2, 8.3, 7.8, 9.1]
    criteria = ["Technical", "Team", "Performance", "Price", "PM", "Innovation", "Timeline"]
    
    profile_scores = {}
    for profile_name, weights in evaluator_profiles.items():
        score = sum(score * weight / 100 for score, weight in zip(our_scores, weights))
        profile_scores[profile_name] = score * 10  # Convert to percentage
    
    st.write("**Predicted Scores by Evaluator Type:**")
    
    profiles = list(profile_scores.keys())
    scores = list(profile_scores.values())
    
    fig = go.Figure(data=[
        go.Bar(x=profiles, y=scores,
               marker_color=['green' if score >= 80 else 'orange' if score >= 70 else 'red' 
                           for score in scores])
    ])
    
    fig.update_layout(
        title="Score Predictions by Evaluator Profile",
        xaxis_title="Evaluator Profile",
        yaxis_title="Predicted Score (%)",
        template="plotly_white",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("💡 Recommendations")
    
    best_profile = max(profile_scores, key=profile_scores.get)
    worst_profile = min(profile_scores, key=profile_scores.get)
    
    recommendations = [
        f"🎯 **Strongest with:** {best_profile} evaluators ({profile_scores[best_profile]:.1f}%)",
        f"⚠️ **Weakest with:** {worst_profile} evaluators ({profile_scores[worst_profile]:.1f}%)",
        "📈 **Improve price competitiveness** to perform better with cost-conscious evaluators",
        "🚀 **Highlight innovation** to appeal to innovation-oriented evaluators",
        "📊 **Emphasize technical expertise** as it's consistently strong across profiles"
    ]
    
    for rec in recommendations:
        st.markdown(rec)
