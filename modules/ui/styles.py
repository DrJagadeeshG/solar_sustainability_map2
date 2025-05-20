# modules/ui/styles.py

"""
Styles module for the Solar Suitability Dashboard.

This module handles all the CSS styling for the application.
Centralizing styles here makes it easier to maintain a consistent
visual appearance across the entire application.
"""

import streamlit as st

def apply_css():
    """
    Apply custom CSS styling to the Streamlit app.
    
    This function defines and applies all the custom CSS needed for the
    application's visual styling, including colors, fonts, spacing,
    and widget appearances.
    
    Returns:
        None
    """
    
    CSS = """
    <style>
        body {
            background-color: white;
        }
        
        .stApp {
            background-color: white;
        }
        
        /* Colorful headers */
        h1, .title-box {
            color: #d81b60 !important; /* Red */
            font-weight: bold;
        }
        
        h2, h3 {
            color: #1976d2 !important; /* Blue */
            font-weight: bold;
        }
        
        h4, h5, h6 {
            color: #388e3c !important; /* Green */
            font-weight: bold;
        }
        
        /* Make all text visible with dark colors */
        p, div, span, label {
            color: #333333 !important;
            font-weight: 500;
        }
        
        /* Metric styling */
        [data-testid="stMetricValue"] {
            color: #d81b60 !important; /* Red */
            font-weight: bold;
            font-size: 1.5rem;
        }
        
        [data-testid="stMetricLabel"] {
            color: #1976d2 !important; /* Blue */
            font-weight: bold;
        }
        
        /* Panel styling with colored borders */
        .panel {
            background-color: white;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            padding: 1rem;
            margin-bottom: 1rem;
            border-left: 4px solid #1976d2; /* Blue border */
        }
        
        .panel h3 {
            margin-top: 0;
        }
        
        .controls-panel {
            border-left: 4px solid #d81b60; /* Red border */
        }
        
        .layer-panel {
            border-left: 4px solid #388e3c; /* Green border */
        }
        
        /* Header styling with logo and title */
        .dashboard-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            background-color: white;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .dashboard-header img {
            height: 50px;
            margin-right: 20px;
        }
        
        .dashboard-title {
            color: #d81b60;
            font-size: 24px;
            font-weight: bold;
        }
        
        /* Fix pie chart background */
        [data-testid="stPlotlyChart"] {
            background-color: white !important;
        }
        
        .js-plotly-plot .plotly .main-svg {
            background-color: white !important;
        }
        
        /* Style select boxes */
        .stSelectbox > div > div {
            background-color: white;
            border-radius: 4px;
            border: 1px solid #ddd;
        }
        
        /* Remove streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Make tooltip & dropdown text BLACK (changed from white) */
        div[role="tooltip"],
        div[aria-live="polite"],
        div[data-testid="stTooltip"],
        button[data-testid="baseButton-secondary"] + div,
        [data-testid="stTooltipIcon"] ~ div,
        div[data-baseweb="tooltip"],
        div[data-baseweb="popover"],
        div[data-baseweb="menu"] {
            color: #333333 !important; /* Changed to dark gray */
        }

        /* Make all text in tooltips BLACK (changed from white) */
        div[role="tooltip"] *,
        div[aria-live="polite"] *,
        div[data-testid="stTooltip"] *,
        button[data-testid="baseButton-secondary"] + div *,
        [data-testid="stTooltipIcon"] ~ div *,
        div[data-baseweb="tooltip"] *,
        div[data-baseweb="popover"] *,
        div[data-baseweb="menu"] * {
            color: #333333 !important; /* Changed to dark gray */
        }

        /* Make dropdown text BLACK (changed from white) */
        div[data-baseweb="select"] ul,
        div[data-baseweb="select"] li,
        div[role="listbox"],
        div[role="option"],
        [data-baseweb="select"] span,
        [data-baseweb="menu"] div,
        div[class*="st-emotion"] [role="listbox"] *,
        div[class*="st-emotion"] [role="option"] * {
            color: #333333 !important; /* Changed to dark gray */
        }

        /* Ensure dropdown options have good contrast */
        div[data-baseweb="select"] ul li:hover,
        div[role="option"]:hover,
        div[role="option"][aria-selected="true"],
        div[data-baseweb="menu"] div:hover {
            background-color: #f0f0f0 !important;
        }

        /* Ensure tooltip info icon remains blue/visible */
        [data-testid="stTooltipIcon"] svg {
            color: #1976d2 !important;
        }
        
        /* Compact panel styling */
        .compact-panel {
            background-color: white;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            padding: 0.5rem;
            margin-bottom: 1rem;
            border-left: 4px solid #d81b60; /* Red border */
        }
        
        /* Control label styling */
        .control-label {
            font-weight: bold;
            color: #1976d2 !important;
            margin-bottom: 0.25rem;
            font-size: 0.9rem;
        }

        /* Ensure selectbox text is visible */
        .stSelectbox label,
        .stSelectbox div[data-baseweb="select"] span {
            color: #333333 !important;
        }

        /* Style tooltips to have a light background with dark text */
        div[data-testid="stTooltip"] div,
        div[data-baseweb="tooltip"] div {
            background-color: white !important;
            border: 1px solid #ddd !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
        }
    </style>
    """
    
    # Apply the CSS
    st.markdown(CSS, unsafe_allow_html=True)