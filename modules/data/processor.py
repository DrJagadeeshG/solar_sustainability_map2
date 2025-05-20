# modules/data/processor.py

"""
Data processor module for the Solar Suitability Dashboard.

This module handles data filtering, transformation, and specialized
processing functions needed for the dashboard's visualization and
analysis capabilities.
"""

import streamlit as st
import pandas as pd
import geopandas as gpd

def filter_data_with_shapefile(_gdf, selected_state, selected_district):
    """
    Filter the GeoDataFrame based on selected state and district.
    
    This function filters the input GeoDataFrame to return only the rows
    that match the selected state and district. It handles special cases
    like "National Average" and "All Districts" selections.
    
    Args:
        _gdf (GeoDataFrame): Input GeoDataFrame with all data
        selected_state (str): Selected state or "National Average"
        selected_district (str): Selected district or "All Districts"
        
    Returns:
        GeoDataFrame: Filtered data based on selection
    """
    filtered_gdf = _gdf.copy()
    
    if selected_state == "National Average":
        # For national average, get only the national average row
        filtered_gdf = filtered_gdf[filtered_gdf["NAME_1"] == "National Average"]
    else:
        # For state selection
        if selected_district == "All Districts":
            # Get the state average row
            filtered_gdf = filtered_gdf[(filtered_gdf["NAME_1"].astype(str) == selected_state) & 
                                     (filtered_gdf["NAME_2"] == "All Districts")]
        else:
            # Get the specific district
            filtered_gdf = filtered_gdf[(filtered_gdf["NAME_1"].astype(str) == selected_state) & 
                                     (filtered_gdf["NAME_2"].astype(str) == selected_district)]
    
    return filtered_gdf

def get_color_for_value(value):
    """
    Get color based on value for consistent styling.
    
    This function determines the appropriate color for a given value,
    handling both categorical and numeric values with a consistent
    color scheme.
    
    Args:
        value: The value to determine color for (string or number)
        
    Returns:
        str: Hex color code for the value
    """
    if isinstance(value, str):
        if "Very Highly Suitable" in value:
            return "#66CC66"  # Dark green
        elif "Highly Suitable" in value:
            return "#99FF99"  # Light green
        elif "Moderately Suitable" in value:
            return "#FFFF99"  # Yellow
        elif "Less Suitable" in value:
            return "#CC0000"  # Red
    
    # Handle numeric values (like for layers)
    if isinstance(value, (int, float)):
        # Simple threshold-based coloring (adjust thresholds as needed)
        if value > 66:
            return "#66CC66"  # Green for high values
        elif value > 33:
            return "#FFFF99"  # Yellow for medium values
        else:
            return "#CC0000"  # Red for low values
    
    return "#CCCCCC"  # Gray for unknown