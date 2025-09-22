"""
Wizard flow for creating new bids in the RFP Response Automation application
"""

import streamlit as st
import db_utils
from ui_components import AGENTS_AVAILABLE


def main() -> None:
    """Main wizard flow for creating new bids."""
    st.markdown("<div class='main-header'><h1>Create New Bid</h1></div>", unsafe_allow_html=True)
    
    if 'wizard_step' not in st.session_state:
        st.session_state.wizard_step = 1
    
    steps = ["Basic Info", "Upload Documents", "Configure Agents", "Review & Submit"]
    current_step = st.session_state.wizard_step
    
    progress = current_step / len(steps)
    st.progress(progress, text=f"Step {current_step} of {len(steps)}: {steps[current_step-1]}")
    
    if current_step == 1:
        render_basic_info_step()
    elif current_step == 2:
        render_upload_step()
    elif current_step == 3:
        render_agents_step()
    elif current_step == 4:
        render_review_step()


def render_basic_info_step() -> None:
    """Render the basic information step."""
    st.subheader("📝 Basic Bid Information")
    
    with st.form("basic_info_form"):
        bid_name = st.text_input("Bid Name*", placeholder="Enter a descriptive name for this bid")
        contact_name = st.text_input("Contact Name", placeholder="Primary contact person")
        contact_email = st.text_input("Contact Email", placeholder="contact@company.com")
        summary = st.text_area("Bid Summary", placeholder="Brief description of the opportunity")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.form_submit_button("Next Step"):
                if bid_name:
                    st.session_state.bid_info = {
                        'bid_name': bid_name,
                        'contact_name': contact_name,
                        'contact_email': contact_email,
                        'summary': summary
                    }
                    st.session_state.wizard_step = 2
                    st.rerun()
                else:
                    st.error("Bid name is required!")


def render_upload_step() -> None:
    """Render the document upload step."""
    st.subheader("📁 Upload RFP Documents")
    
    uploaded_files = st.file_uploader(
        "Upload RFP documents",
        accept_multiple_files=True,
        type=['pdf', 'docx', 'txt'],
        help="Upload all relevant RFP documents for analysis"
    )
    
    if uploaded_files:
        st.success(f"Uploaded {len(uploaded_files)} files")
        for file in uploaded_files:
            st.write(f"📄 {file.name}")
        
        st.session_state.uploaded_files = uploaded_files
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Previous"):
            st.session_state.wizard_step = 1
            st.rerun()
    with col2:
        if st.button("Next Step →"):
            st.session_state.wizard_step = 3
            st.rerun()


def render_agents_step() -> None:
    """Render the AI agents configuration step."""
    st.subheader("🤖 Configure AI Agents")
    
    selected_agents = st.multiselect(
        "Select AI agents for this bid:",
        AGENTS_AVAILABLE,
        default=AGENTS_AVAILABLE[:3],
        help="Choose which AI agents will work on this bid"
    )
    
    if selected_agents:
        st.session_state.selected_agents = selected_agents
        
        st.write("**Selected Agents:**")
        for agent in selected_agents:
            st.write(f"✅ {agent}")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Previous"):
            st.session_state.wizard_step = 2
            st.rerun()
    with col2:
        if st.button("Next Step →"):
            if selected_agents:
                st.session_state.wizard_step = 4
                st.rerun()
            else:
                st.error("Please select at least one agent!")


def render_review_step() -> None:
    """Render the review and submit step."""
    st.subheader("📋 Review & Submit")
    
    if hasattr(st.session_state, 'bid_info'):
        bid_info = st.session_state.bid_info
        
        st.write("**Bid Information:**")
        st.write(f"• **Name:** {bid_info['bid_name']}")
        st.write(f"• **Contact:** {bid_info['contact_name']}")
        st.write(f"• **Email:** {bid_info['contact_email']}")
        st.write(f"• **Summary:** {bid_info['summary']}")
        
        if hasattr(st.session_state, 'uploaded_files'):
            st.write(f"• **Documents:** {len(st.session_state.uploaded_files)} files uploaded")
        
        if hasattr(st.session_state, 'selected_agents'):
            st.write(f"• **Agents:** {', '.join(st.session_state.selected_agents)}")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Previous"):
            st.session_state.wizard_step = 3
            st.rerun()
    with col2:
        if st.button("Create Bid"):
            if hasattr(st.session_state, 'bid_info'):
                bid_info = st.session_state.bid_info
                bid_id = db_utils.create_bid(
                    bid_name=bid_info['bid_name'],
                    contact_name=bid_info['contact_name'],
                    contact_email=bid_info['contact_email'],
                    summary=bid_info['summary']
                )
                
                if bid_id:
                    st.success(f"Bid created successfully! ID: {bid_id}")
                    for key in ['wizard_step', 'bid_info', 'uploaded_files', 'selected_agents']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
                else:
                    st.error("Failed to create bid. Please try again.")
