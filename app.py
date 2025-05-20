# app.py

"""
Solar Suitability Dashboard Main Application.

This is the main entry point for the Solar Suitability Dashboard application.
It sets up the page, loads data, and orchestrates the different components
of the application.
"""

import streamlit as st
from modules.ui.styles import apply_css
from modules.ui.layout import create_header, create_footer, create_controls
from modules.data.loader import load_shapefile_data
from modules.data.processor import filter_data_with_shapefile
from modules.visualization.maps import create_simple_map
from modules.visualization.charts import display_statistics
from modules.utils.constants import layer_column_mapping

# Set page configuration
st.set_page_config(
    page_title="Solar Suitability Dashboard",
    page_icon="☀️",
    layout="wide"
)

# Apply CSS styles
apply_css()

def main():
    """
    Main application function to run the dashboard.
    
    This function orchestrates the different components of the application,
    loading data, creating the user interface, and handling user interactions.
    """
    # Create the header
    create_header()
    
    # Load the data directly from shapefile - with caching, this is only done once
    df = load_shapefile_data()
    
    # Initialize session state for storing selected layer
    if 'selected_layer' not in st.session_state:
        st.session_state.selected_layer = "GW Development Stage"  # Default selection
    
    # Create the control panel (state, district, category, layer selection)
    selected_state, selected_district, selected_category = create_controls(df)
    
    # Create 2-column layout for map and statistics
    map_stats_cols = st.columns([2, 1])
    
    # Middle column - Map
    with map_stats_cols[0]:
        # Filter data based on selection
        filtered_df = filter_data_with_shapefile(df, selected_state, selected_district)
        
        # Create the map panel
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        
        # Get the column to visualize
        vis_column = selected_category
        if st.session_state.selected_layer and layer_column_mapping[st.session_state.selected_layer] in filtered_df.columns:
            vis_column = layer_column_mapping[st.session_state.selected_layer]
        
        # Use the simple matplotlib approach for map rendering
        with st.spinner("Creating map..."):
            fig = create_simple_map(df, selected_state, selected_district, vis_column, selected_category)
            st.pyplot(fig)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Right column - Statistics
    with map_stats_cols[1]:
        display_statistics(df, filtered_df, selected_state, selected_district, selected_category)
    
    # Create footer
    create_footer()

# Run the app
if __name__ == "__main__":
    main()