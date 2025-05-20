# modules/visualization/maps.py

"""
Maps visualization module for the Solar Suitability Dashboard.

This module contains functions for creating and styling maps
based on the geodata and user selections.
"""

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import streamlit as st

def create_simple_map(_gdf, selected_state, selected_district, vis_column, selected_category=None):
    """
    Create a simplified map using matplotlib with custom legend based on category.
    
    This function creates a map visualization of the selected data using matplotlib.
    It handles different types of data (categorical and numeric) and creates
    appropriate legends and styling.
    
    Args:
        _gdf (GeoDataFrame): The geodataframe containing all data
        selected_state (str): The selected state or "National Average"
        selected_district (str): The selected district or "All Districts" 
        vis_column (str): The column to visualize
        selected_category (str, optional): The selected category (Adaptation, Mitigation, etc.)
        
    Returns:
        matplotlib.figure.Figure: The created map figure
    """
    try:
        # If selected_category is not provided, try to determine it from vis_column
        if selected_category is None:
            if vis_column in ["Adaptation", "Mitigation", "Replacment"]:
                selected_category = vis_column
            else:
                selected_category = "Mitigation"  # Default if we can't determine
        
        # Filter data
        if selected_state == "National Average":
            map_data = _gdf[(_gdf["NAME_2"] != "All Districts") & (_gdf["NAME_1"] != "National Average")]
        elif selected_district == "All Districts":
            map_data = _gdf[(_gdf["NAME_1"].astype(str) == selected_state) & (_gdf["NAME_2"] != "All Districts")]
        else:
            map_data = _gdf[(_gdf["NAME_1"].astype(str) == selected_state) & (_gdf["NAME_2"].astype(str) == selected_district)]
        
        # Create plot
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        
        # Check if we're dealing with a categorical column
        is_categorical = (vis_column in ["Adaptation", "Mitigation", "Replacment", "General_SI"])
        
        if is_categorical:
            # For categorical data, we use the predefined categories
            category_mapping = {
                "Very Highly Suitable": 4,
                "Highly Suitable": 3,
                "Moderately Suitable": 2,
                "Less Suitable": 1,
                "Mixed": 0
            }
            
            # Custom colors based on your legend image
            custom_colors = {
                "Very Highly Suitable": '#66CC66',  # Dark green
                "Highly Suitable": '#99FF99',       # Light green
                "Moderately Suitable": '#FFFF99',   # Yellow
                "Less Suitable": '#CC0000',         # Red
                "Mixed": '#CCCCCC'                  # Gray
            }
            
            # Create a numeric column based on the categorical values
            if vis_column in map_data.columns:
                map_data['value_numeric'] = map_data[vis_column].map(category_mapping).fillna(0)
                
                # Create a custom colormap
                cmap = ListedColormap([
                    custom_colors["Less Suitable"],
                    custom_colors["Moderately Suitable"], 
                    custom_colors["Highly Suitable"],
                    custom_colors["Very Highly Suitable"]
                ])
                
                # Plot with custom colormap - ADD BLACK BOUNDARIES
                map_data.plot(column='value_numeric', cmap=cmap, ax=ax, legend=False, 
                              edgecolor='black', linewidth=0.5)  # Add black boundaries
                
                # Add a custom legend
                legend_elements = [
                    Patch(facecolor=custom_colors["Very Highly Suitable"], label='Very Highly Suitable'),
                    Patch(facecolor=custom_colors["Highly Suitable"], label='Highly Suitable'),
                    Patch(facecolor=custom_colors["Moderately Suitable"], label='Moderately Suitable'),
                    Patch(facecolor=custom_colors["Less Suitable"], label='Less Suitable')
                ]
                
                ax.legend(handles=legend_elements, loc='lower right')
            else:
                # If column doesn't exist, show outline only
                map_data.plot(ax=ax, color='lightgrey', edgecolor='black', linewidth=0.5)
                ax.set_title(f"Column '{vis_column}' not found in data")
        else:
            # For numeric data like GW Development Stage, use custom color mapping based on category
            if vis_column in map_data.columns:
                # First, create a new column with the classification
                map_data = map_data.copy()  # Create a copy to avoid SettingWithCopyWarning
                map_data['classification'] = 'Unknown'
                
                # CRITICAL FIX: Use fixed value boundaries instead of relative data ranges
                # This ensures consistent coloring regardless of the selected view
                
                if selected_category == "Adaptation":
                    # Inverted scale for adaptation
                    # Very Highly Suitable: <50%
                    # Highly Suitable: 50-70%
                    # Moderately Suitable: 70-100%
                    # Less Suitable: >100%
                    map_data.loc[map_data[vis_column] > 100, 'classification'] = 'Less Suitable'
                    map_data.loc[(map_data[vis_column] <= 100) & (map_data[vis_column] > 70), 'classification'] = 'Moderately Suitable'
                    map_data.loc[(map_data[vis_column] <= 70) & (map_data[vis_column] > 50), 'classification'] = 'Highly Suitable'
                    map_data.loc[map_data[vis_column] <= 50, 'classification'] = 'Very Highly Suitable'
                else:
                    # Standard scale for mitigation and replacement
                    # Very Highly Suitable: >100%
                    # Highly Suitable: 70-100%
                    # Moderately Suitable: 50-70%
                    # Less Suitable: <50%
                    map_data.loc[map_data[vis_column] < 50, 'classification'] = 'Less Suitable'
                    map_data.loc[(map_data[vis_column] >= 50) & (map_data[vis_column] < 70), 'classification'] = 'Moderately Suitable'
                    map_data.loc[(map_data[vis_column] >= 70) & (map_data[vis_column] <= 100), 'classification'] = 'Highly Suitable'
                    map_data.loc[map_data[vis_column] > 100, 'classification'] = 'Very Highly Suitable'
                
                # Map classification to numeric values for plotting
                category_mapping = {
                    "Very Highly Suitable": 4,
                    "Highly Suitable": 3,
                    "Moderately Suitable": 2,
                    "Less Suitable": 1,
                    "Unknown": 0
                }
                
                # Create numeric values for colors
                map_data['value_numeric'] = map_data['classification'].map(category_mapping)
                
                # Custom colors based on your legend image
                colors = {
                    "Very Highly Suitable": '#66CC66',  # Dark green
                    "Highly Suitable": '#99FF99',       # Light green
                    "Moderately Suitable": '#FFFF99',   # Yellow
                    "Less Suitable": '#CC0000',         # Red
                    "Unknown": '#CCCCCC'                # Gray
                }
                
                # Create a custom colormap
                cmap = ListedColormap([
                    colors["Less Suitable"],
                    colors["Moderately Suitable"], 
                    colors["Highly Suitable"],
                    colors["Very Highly Suitable"]
                ])
                
                # Plot with the custom colormap - ADD BLACK BOUNDARIES
                # Use vmin=1 and vmax=4 to ensure consistent coloring
                map_data.plot(column='value_numeric', cmap=cmap, ax=ax, legend=False,
                              edgecolor='black', linewidth=0.5, vmin=1, vmax=4)
                
                # Add a custom legend with percentage ranges
                if selected_category == "Adaptation":
                    # Inverted legend for adaptation
                    legend_elements = [
                        Patch(facecolor=colors["Very Highly Suitable"], label='Very Highly Suitable (<50%)'),
                        Patch(facecolor=colors["Highly Suitable"], label='Highly Suitable (50-70%)'),
                        Patch(facecolor=colors["Moderately Suitable"], label='Moderately Suitable (70-100%)'),
                        Patch(facecolor=colors["Less Suitable"], label='Less Suitable (>100%)')
                    ]
                else:
                    # Standard legend for mitigation and replacement
                    legend_elements = [
                        Patch(facecolor=colors["Very Highly Suitable"], label='Very Highly Suitable (>100%)'),
                        Patch(facecolor=colors["Highly Suitable"], label='Highly Suitable (70-100%)'),
                        Patch(facecolor=colors["Moderately Suitable"], label='Moderately Suitable (50-70%)'),
                        Patch(facecolor=colors["Less Suitable"], label='Less Suitable (<50%)')
                    ]
                
                ax.legend(handles=legend_elements, loc='lower right')
            else:
                # If column doesn't exist, show outline only
                map_data.plot(ax=ax, color='lightgrey', edgecolor='black', linewidth=0.5)
                ax.set_title(f"Column '{vis_column}' not found in data")
        
        # Set title
        if selected_district == "All Districts":
            ax.set_title(f"{selected_state} - {vis_column}")
        else:
            ax.set_title(f"{selected_state} - {selected_district} - {vis_column}")
            
        # Remove axes
        ax.set_axis_off()
        
        # Add district labels for state view
        if selected_state != "National Average" and selected_district == "All Districts":
            for idx, row in map_data.iterrows():
                if 'geometry' in row and row['geometry'] and hasattr(row['geometry'], 'centroid'):
                    x, y = row['geometry'].centroid.x, row['geometry'].centroid.y
                    if 'NAME_2' in row and row['NAME_2'] != "All Districts":
                        ax.text(x, y, row['NAME_2'], fontsize=8, ha='center', va='center')
        
        return fig
    except Exception as e:
        st.error(f"Error creating simple map: {str(e)}")
        # Create empty figure with error message
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        ax.text(0.5, 0.5, f"Error creating map: {str(e)}", 
                horizontalalignment='center', verticalalignment='center')
        ax.set_axis_off()
        return fig