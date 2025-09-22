"""
Configuration constants for the RFP Response Automation application
"""

NAV_OPTIONS = [
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

LOGO_PATH = "assets/Ether_Logo.png"

BID_COLUMNS = [
    "ID", 
    "Bid Name", 
    "Contact Name", 
    "Contact Email", 
    "Summary", 
    "Status", 
    "Created At", 
    "Updated At"
]

BID_ACTIONS = [
    "Select Action", 
    "View", 
    "Edit", 
    "Delete"
]

PAGE_CONFIG = {
    "page_title": "Agentic AI RFP Response Automation",
    "page_icon": "🤖",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

CHART_MONTHS = 12
CHART_TEMPLATE = "plotly_dark"
