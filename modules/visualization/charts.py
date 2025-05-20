# modules/visualization/charts.py

"""
Charts visualization module for the Solar Suitability Dashboard.

This module contains functions for creating charts, statistics displays,
and other non-map visualizations for the dashboard.
"""

import streamlit as st
import plotly.express as px
from modules.utils.constants import layer_column_mapping

def display_statistics(df, filtered_df, selected_state, selected_district, selected_category):
    """
    Display statistics panel based on selected data.
    
    This function creates a panel showing statistics and charts based on
    the selected state, district, and category. It displays metrics and
    a pie chart showing distribution of suitability levels when appropriate.
    
    Args:
        df (GeoDataFrame): The complete geodataframe
        filtered_df (GeoDataFrame): The filtered data based on selection
        selected_state (str): The selected state or "National Average"
        selected_district (str): The selected district or "All Districts"
        selected_category (str): The selected category (Adaptation, Mitigation, etc.)
        
    Returns:
        None
    """
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("<h3>Statistics</h3>", unsafe_allow_html=True)
    
    # Display statistics based on selection
    if not filtered_df.empty:
        district_data = filtered_df.iloc[0]
        
        # Display appropriate title based on selection
        if selected_state == "National Average":
            st.metric("Selected Level", "National Average")
        elif selected_district == "All Districts":
            st.metric("Selected Level", f"{selected_state} State Average")
        else:
            st.metric("Selected District", selected_district)
        
        if selected_category in district_data:
            st.metric(f"{selected_category} Suitability", district_data[selected_category])
        
        # Show additional metrics if a layer is selected
        if 'selected_layer' in st.session_state and layer_column_mapping[st.session_state.selected_layer] in district_data:
            layer_col = layer_column_mapping[st.session_state.selected_layer]
            layer_value = district_data[layer_col]
            
            # Format the numeric value to display nicely
            if isinstance(layer_value, (int, float)):
                formatted_value = f"{layer_value:.2f}"  # Format to 2 decimal places
            else:
                formatted_value = layer_value
                
            st.metric(st.session_state.selected_layer, formatted_value)
        
        # For All Districts, add distribution pie chart
        if selected_state != "National Average" and selected_district == "All Districts" and "NAME_2" in df.columns:
            create_suitability_chart(df, selected_state, selected_category, "state")
        
        # For National Average, show distribution across states
        elif selected_state == "National Average" and "NAME_1" in df.columns:
            create_suitability_chart(df, selected_state, selected_category, "national")
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_suitability_chart(df, selected_state, selected_category, level="state"):
    """
    Create a pie chart showing distribution of suitability levels.
    
    This function creates a pie chart showing the distribution of suitability
    levels for the selected state or at the national level. It also displays
    summary metrics.
    
    Args:
        df (GeoDataFrame): The complete geodataframe
        selected_state (str): The selected state or "National Average"
        selected_category (str): The selected category (Adaptation, Mitigation, etc.)
        level (str): The level of aggregation ("state" or "national")
        
    Returns:
        None
    """
    if level == "state":
        # Get all districts in the state (excluding the average row)
        filtered_data = df[(df["NAME_1"].astype(str) == selected_state) & 
                          (df["NAME_2"] != "All Districts")]
        title = f'Distribution of {selected_category} in {selected_state}'
    else:  # national level
        # Get all state averages (excluding the national average)
        filtered_data = df[(df["NAME_2"] == "All Districts") & 
                          (df["NAME_1"] != "National Average")]
        title = f'Distribution of {selected_category} Across States'
    
    if not filtered_data.empty and selected_category in filtered_data.columns:
        # Count occurrences of each suitability level
        suitability_counts = filtered_data[selected_category].value_counts().reset_index()
        suitability_counts.columns = ['Suitability Level', 'Count']
        
        # Calculate percentage
        total = suitability_counts['Count'].sum()
        suitability_counts['Percentage'] = (suitability_counts['Count'] / total * 100).round(2)
        
        # Create custom colors for the chart - using red, blue, green theme
        color_map = {
            'Very Highly Suitable': '#66CC66',  # Dark green
            'Highly Suitable': '#99FF99',       # Light green
            'Moderately Suitable': '#FFFF99',   # Yellow
            'Less Suitable': '#CC0000'          # Red
        }
        
        colors = [color_map.get(level, '#333333') for level in suitability_counts['Suitability Level']]
        
        # Create pie chart with optimized settings
        fig = px.pie(
            suitability_counts, 
            values='Count', 
            names='Suitability Level',
            title=title,
            color_discrete_sequence=colors
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont=dict(size=14, color="white", family="Arial, sans-serif")
        )
        
        fig.update_layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(l=10, r=10, t=40, b=10),
            title_font=dict(size=16, color='#1976d2', family="Arial, sans-serif")
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display summary metrics
        st.metric("Total " + ("Districts" if level == "state" else "States"), len(filtered_data))
        
        # Calculate the percentage of highly suitable areas
        highly_suitable = filtered_data[filtered_data[selected_category] == "Highly Suitable"]
        highly_suitable_pct = len(highly_suitable) / len(filtered_data) * 100 if len(filtered_data) > 0 else 0
        st.metric("Highly Suitable " + ("Districts" if level == "state" else "States"), f"{highly_suitable_pct:.1f}%")