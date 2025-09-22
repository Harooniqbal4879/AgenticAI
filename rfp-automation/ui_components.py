"""
UI components for the RFP Response Automation application
"""

import streamlit as st
from typing import Dict, Any


AGENTS_AVAILABLE = [
    "Research Agent",
    "Writing Agent", 
    "Review Agent",
    "Compliance Agent",
    "Technical Agent"
]


def initialize_session_state() -> None:
    """Initialize Streamlit session state variables."""
    if 'current_phase' not in st.session_state:
        st.session_state.current_phase = 'upload'
    
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False


def render_header() -> None:
    """Render the main application header."""
    st.markdown("""
        <div class='main-header'>
            <h1>🤖 Agentic AI RFP Response Automation</h1>
            <p>Streamline your RFP response process with AI-powered automation</p>
        </div>
    """, unsafe_allow_html=True)


def render_sidebar() -> str:
    """Render the sidebar navigation and return selected option."""
    with st.sidebar:
        st.image("assets/Ether_Logo.png", caption="Company Logo", width=100)
        
        nav_options = [
            "Dashboard",
            "Create New Bid", 
            "Manage Bids",
            "Competitive Dashboard",
            "Win Probability Dashboard",
            "Compliance Dashboard",
            "Evaluator Simulation",
            "Scoring Detail",
            "Settings"
        ]
        
        selected = st.radio("Navigation", nav_options, key="main_nav_radio")
        return selected


def render_upload_phase() -> None:
    """Render the file upload phase."""
    st.markdown("<div class='phase-container'>", unsafe_allow_html=True)
    st.subheader("📁 Upload RFP Documents")
    
    uploaded_files = st.file_uploader(
        "Choose RFP files",
        accept_multiple_files=True,
        type=['pdf', 'docx', 'txt']
    )
    
    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files
        st.success(f"Uploaded {len(uploaded_files)} files successfully!")
        
        for file in uploaded_files:
            st.write(f"📄 {file.name}")
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_processing_phase() -> None:
    """Render the document processing phase."""
    st.markdown("<div class='phase-container'>", unsafe_allow_html=True)
    st.subheader("⚙️ Processing Documents")
    
    if st.session_state.uploaded_files:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        import time
        for i in range(100):
            progress_bar.progress(i + 1)
            status_text.text(f'Processing... {i+1}%')
            time.sleep(0.01)
        
        st.success("Documents processed successfully!")
        st.session_state.processing_complete = True
    else:
        st.warning("Please upload documents first.")
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_qa_phase() -> None:
    """Render the Q&A phase."""
    st.markdown("<div class='phase-container'>", unsafe_allow_html=True)
    st.subheader("❓ Question & Answer")
    
    if st.session_state.processing_complete:
        question = st.text_input("Ask a question about the RFP:")
        
        if question:
            st.markdown("<div class='chat-message user-message'>", unsafe_allow_html=True)
            st.write(f"**You:** {question}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='chat-message ai-message'>", unsafe_allow_html=True)
            st.write("**AI:** This is a demo response to your question.")
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Please process documents first.")
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_gathering_phase() -> None:
    """Render the information gathering phase."""
    st.markdown("<div class='phase-container'>", unsafe_allow_html=True)
    st.subheader("📊 Information Gathering")
    
    st.write("Gathering relevant information from uploaded documents...")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Requirements Found", "15", "+3")
        st.metric("Compliance Items", "8", "+1")
    
    with col2:
        st.metric("Technical Specs", "12", "+2")
        st.metric("Evaluation Criteria", "6", "0")
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_generation_phase() -> None:
    """Render the response generation phase."""
    st.markdown("<div class='phase-container'>", unsafe_allow_html=True)
    st.subheader("✍️ Response Generation")
    
    selected_agents = st.multiselect(
        "Select AI Agents for Response Generation:",
        AGENTS_AVAILABLE,
        default=AGENTS_AVAILABLE[:2]
    )
    
    if st.button("Generate Response"):
        if selected_agents:
            st.success(f"Response generated using {len(selected_agents)} agents!")
            st.text_area("Generated Response Preview:", 
                        "This is a demo response generated by the selected AI agents...",
                        height=200)
        else:
            st.warning("Please select at least one agent.")
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_export_phase() -> None:
    """Render the export phase."""
    st.markdown("<div class='phase-container'>", unsafe_allow_html=True)
    st.subheader("📤 Export Response")
    
    export_format = st.selectbox(
        "Choose export format:",
        ["PDF", "Word Document", "Plain Text"]
    )
    
    if st.button("Export Response"):
        st.success(f"Response exported as {export_format}!")
        st.download_button(
            label="Download Response",
            data="Demo response content...",
            file_name=f"rfp_response.{export_format.lower().replace(' ', '_')}",
            mime="text/plain"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
