"""
Main Streamlit application for RFP Response Automation with AI agents
This file handles initialization, configuration, and routing
"""

import os
import time
import glob
from typing import Optional

import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import numpy as np
from dotenv import load_dotenv

import db_utils
from config import NAV_OPTIONS, LOGO_PATH, BID_COLUMNS, BID_ACTIONS, PAGE_CONFIG, CHART_MONTHS, CHART_TEMPLATE
from styles import MAIN_CSS
from ui_components import AGENTS_AVAILABLE


def initialize_app() -> None:
    """Initialize the Streamlit application with configuration and environment setup."""
    os.environ["LANGCHAIN_TRACING_V2"] = "false"
    load_dotenv()
    
    langsmith_key = os.getenv("LANGSMITH_API_KEY")
    if langsmith_key:
        os.environ["LANGSMITH_API_KEY"] = langsmith_key
        try:
            from langsmith import Client
            langsmith_client = Client()
        except ImportError:
            st.warning("LangSmith client not available")
    
    st.set_page_config(**PAGE_CONFIG)
    
    st.markdown(MAIN_CSS, unsafe_allow_html=True)
    
    db_utils.init_db()


def setup_sidebar() -> str:
    """Setup sidebar with logo, loading animation, and navigation."""
    with st.sidebar:
        progress_bar = st.progress(0, text="Loading...")
        
        try:
            st.image(LOGO_PATH, caption="Company Logo", width=100)
        except Exception:
            st.write("🏢 Company Logo")
        
        for percent_complete in range(1, 101, 20):
            time.sleep(0.05)
            progress_bar.progress(percent_complete/100, text="Loading...")
        progress_bar.empty()
        
        selected_nav = st.radio("Navigation", NAV_OPTIONS, key="main_nav_radio")
        
    return selected_nav


def render_dashboard() -> None:
    """Render the main dashboard page."""
    st.markdown("<div class='main-header'><h1>Agentic AI RFP Response Automation</h1></div>", unsafe_allow_html=True)
    st.info("Welcome to the Agentic AI RFP Response Automation demo dashboard.")

    st.subheader("Performance Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Bids Submitted", "24", "+3")
    col2.metric("Win Rate", "58%", "+4%")
    col3.metric("Avg. Response Time", "2.1 days", "-0.3 days")

    x = np.arange(1, CHART_MONTHS + 1)
    y1 = np.random.randint(10, 30, size=CHART_MONTHS)
    y2 = np.random.randint(5, 20, size=CHART_MONTHS)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y1, mode='lines+markers', name='Bids Submitted'))
    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines+markers', name='Bids Won'))
    fig.update_layout(
        title="Monthly Bid Performance", 
        xaxis_title="Month", 
        yaxis_title="Count", 
        template=CHART_TEMPLATE
    )
    st.plotly_chart(fig, use_container_width=True)


def render_manage_bids() -> None:
    """Render the bid management page."""
    st.markdown("<div class='main-header'><h1>Manage Bids</h1></div>", unsafe_allow_html=True)
    st.info("View and manage all your bids and their statuses.")
    
    try:
        bids = db_utils.get_all_bids()
        if not bids:
            st.warning("No bids found.")
            return
            
        df = pd.DataFrame(bids, columns=BID_COLUMNS)
        selected_bids = []
        
        action = st.selectbox("Take Action", BID_ACTIONS, key="bid_action")
        apply_action = st.button("Apply Action")
        st.write("Select bids and choose an action:")
        
        cols = st.columns(len(df.columns) + 1)
        cols[0].write("Select")
        for i, col_name in enumerate(df.columns):
            cols[i+1].write(col_name)
        
        for idx, row in df.iterrows():
            cols = st.columns(len(df.columns) + 1)
            bid_id = row["ID"]
            checkbox_key = f"select_bid_{bid_id}"
            selected = cols[0].checkbox("", key=checkbox_key)
            if selected:
                selected_bids.append(bid_id)
            for i, col_name in enumerate(df.columns):
                cols[i+1].write(str(row[col_name]))

        if apply_action:
            process_bid_actions(action, selected_bids, bids)
            
    except Exception as e:
        st.error(f"Error loading bids: {str(e)}")


def process_bid_actions(action: str, selected_bids: list, bids: list) -> None:
    """Process the selected action on the selected bids."""
    if not selected_bids:
        st.warning("Please select at least one bid.")
        return
        
    if action == "View":
        for bid_id in selected_bids:
            bid = next((b for b in bids if b[0] == bid_id), None)
            if bid:
                st.info(f"Viewing Bid: {bid[1]}\nContact: {bid[2]}\nEmail: {bid[3]}\nSummary: {bid[4]}\nStatus: {bid[5]}")
                
    elif action == "Edit":
        st.warning("Edit functionality not implemented yet.")
        
    elif action == "Delete":
        for bid_id in selected_bids:
            bid = next((b for b in bids if b[0] == bid_id), None)
            if bid:
                try:
                    db_utils.delete_bid(bid_id)
                    faiss_files = glob.glob(f"faiss_index_*{bid_id}*")
                    for f in faiss_files:
                        try:
                            os.remove(f)
                        except Exception as e:
                            st.warning(f"Could not remove vector DB file {f}: {str(e)}")
                    st.success(f"Bid {bid[1]} and all associated data deleted.")
                except Exception as e:
                    st.error(f"Error deleting bid {bid[1]}: {str(e)}")
        st.rerun()
        
    else:
        st.info("Please select an action.")


def render_other_pages(selected_nav: str) -> None:
    """Render other dashboard pages based on navigation selection."""
    page_configs = {
        "Create New Bid": ("wizard_flow", "Create New Bid"),
        "Competitive Dashboard": ("competitive_dashboard", "Competitive Dashboard"),
        "Win Probability Dashboard": ("win_probability_dashboard", "Win Probability Dashboard"),
        "Compliance Dashboard": ("compliance_dashboard", "Compliance Dashboard"),
        "Evaluator Simulation": ("evaluator_simulation", "Evaluator Simulation"),
        "Scoring Detail": ("scoring_detail", "Scoring Detail"),
        "Settings": (None, "Settings")
    }
    
    if selected_nav in page_configs:
        module_name, page_title = page_configs[selected_nav]
        
        st.markdown(f"<div class='main-header'><h1>{page_title}</h1></div>", unsafe_allow_html=True)
        
        if module_name:
            try:
                module = __import__(module_name)
                module.main()
            except ImportError as e:
                st.error(f"Module {module_name} not found: {str(e)}")
            except Exception as e:
                st.error(f"Error loading {page_title}: {str(e)}")
        else:
            st.info("Update your profile, preferences, and notification settings (demo).")


def main() -> None:
    """Main application entry point."""
    try:
        initialize_app()
        
        selected_nav = setup_sidebar()
        
        if selected_nav == "Dashboard":
            render_dashboard()
        elif selected_nav == "Manage Bids":
            render_manage_bids()
        else:
            render_other_pages(selected_nav)
            
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("Please refresh the page or contact support if the issue persists.")


if __name__ == "__main__":
    main()
