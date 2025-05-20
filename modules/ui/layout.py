# modules/ui/layout.py

"""
UI layout module for the Solar Suitability Dashboard.

This module contains functions for creating the layout components
of the dashboard, including the header, footer, and control panels.
"""

import streamlit as st
from modules.utils.constants import layer_explanations, layer_column_mapping

def create_header():
    """
    Create the dashboard header with title and branding.
    
    Returns:
        None
    """
    st.markdown("""
    <div class="dashboard-header">
        <div class="dashboard-title">Solar Suitability Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

def create_footer():
    """
    Create the dashboard footer with contact information.
    
    Returns:
        None
    """
    st.markdown("""
    <div style="background-color: white; padding: 15px; border-radius: 5px; margin-top: 20px; border-top: 2px solid #1976d2;">
        <p style="color: #d81b60 !important; font-weight: bold; margin-bottom: 5px;">Contact</p>
        <p style="color: #333333 !important; margin: 0;">Mohammad Faiz Alam, Regional Researcher<br>
        International Water Management Institute (IWMI)<br>
        Email: m.alam@cgiar.org</p>
    </div>
    """, unsafe_allow_html=True)

def create_controls(df):
    """
    Create the control panel with state, district, and category selection.
    
    This function creates a row of controls for selecting the state,
    district, category, and layer to display in the dashboard.
    
    Args:
        df (GeoDataFrame): The data to populate the selection options
        
    Returns:
        tuple: (selected_state, selected_district, selected_category)
    """
    # COMPACT CONTROLS - All in one row
    st.markdown('<div class="compact-panel">', unsafe_allow_html=True)
    
    # Create 5 columns in one row for all controls
    all_controls = st.columns([1, 1, 1, 1.5, 0.5])
    
    # State selection
    with all_controls[0]:
        st.markdown('<p class="control-label">State</p>', unsafe_allow_html=True)
        states = df["NAME_1"].unique()
        states_list = ["National Average"] + sorted([str(s) for s in states if str(s) != "National Average"])
        selected_state = st.selectbox("State", states_list, label_visibility="collapsed", key="state_select")
    
    # District selection
    with all_controls[1]:
        st.markdown('<p class="control-label">District</p>', unsafe_allow_html=True)
        if selected_state == "National Average":
            districts_list = ["All Districts"]
        else:
            district_df = df[df["NAME_1"].astype(str) == selected_state]
            districts = district_df["NAME_2"].unique()
            districts_list = ["All Districts"] + sorted([str(d) for d in districts if str(d) != "All Districts"])
        selected_district = st.selectbox("District", districts_list, label_visibility="collapsed", key="district_select")
    
    # Category selection
    with all_controls[2]:
        st.markdown('<p class="control-label">Category</p>', unsafe_allow_html=True)
        categories = ["Adaptation", "Mitigation", "Replacment", "General_SI"]
        selected_category = st.selectbox("Category", categories, label_visibility="collapsed", key="category_select")
    
    # Layer selection
    with all_controls[3]:
        st.markdown('<p class="control-label">Layer Selection</p>', unsafe_allow_html=True)
        layers_list = list(layer_explanations.keys())
        selected_layer_dropdown = st.selectbox(
            "Layer",
            layers_list,
            index=layers_list.index("GW Development Stage") if "GW Development Stage" in layers_list else 0,
            label_visibility="collapsed",
            key="layer_select"
        )
        # Update session state based on dropdown selection
        if selected_layer_dropdown:
            st.session_state.selected_layer = selected_layer_dropdown
    
    # Layer info button (optional)
    with all_controls[4]:
        st.markdown('<p class="control-label">&nbsp;</p>', unsafe_allow_html=True)
        if st.button("ℹ️", help=layer_explanations.get(st.session_state.selected_layer, ""), key="info_button"):
            st.info(layer_explanations.get(st.session_state.selected_layer, "No description available"))
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return selected_state, selected_district, selected_category