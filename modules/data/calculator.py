# modules/data/calculator.py

"""
Calculator module for the Solar Suitability Dashboard.

This module handles statistical calculations and data transformations
needed for the dashboard, such as calculating averages at different
geographical levels.
"""

import geopandas as gpd
import pandas as pd

def calculate_averages(_gdf):
    """
    Calculate state and national averages for the GeoDataFrame.
    
    This function takes a GeoDataFrame with district-level data and
    calculates average values for each state and for the entire country.
    It adds these as new rows to the GeoDataFrame, with special handling
    for geographic features and categorical values.
    
    Args:
        _gdf (GeoDataFrame): Original GeoDataFrame with district-level data
        
    Returns:
        GeoDataFrame: Original data with added state and national average rows
    """
    # Make a copy to avoid changing the original
    avg_df = _gdf.copy()
    
    # Identify numeric columns for averaging
    numeric_columns = avg_df.select_dtypes(include=['number']).columns.tolist()
    
    # Calculate national averages (all districts)
    national_avg = {}
    for col in numeric_columns:
        try:
            national_avg[col] = avg_df[col].mean()
        except:
            # Skip columns that can't be averaged
            national_avg[col] = None
    
    # Add string columns as None or 'Average'
    for col in avg_df.columns:
        if col not in numeric_columns and col != 'geometry':
            national_avg[col] = "National Average"
    
    national_avg["NAME_1"] = "National Average"
    national_avg["NAME_2"] = "All Districts"
    
    # Create a geometry for the national average (centroid of all geometries)
    if 'geometry' in avg_df.columns:
        try:
            # Use the union of all geometries to create a representative geometry
            # Using union_all() instead of unary_union
            if hasattr(avg_df.geometry, 'union_all'):
                national_avg["geometry"] = avg_df.geometry.union_all().centroid
            else:
                # Fallback for older versions of geopandas
                national_avg["geometry"] = avg_df.geometry.unary_union.centroid
        except:
            # If that fails, use the first geometry
            national_avg["geometry"] = avg_df.geometry.iloc[0]
    
    # Calculate state averages
    state_avgs = []
    # Get unique states once for better performance
    unique_states = list(avg_df["NAME_1"].unique())
    
    for state in unique_states:
        # Skip the national average row if it exists
        if state == "National Average":
            continue
            
        state_df = avg_df[avg_df["NAME_1"] == state]
        state_avg = {}
        
        for col in numeric_columns:
            try:
                state_avg[col] = state_df[col].mean()
            except:
                # Skip columns that can't be averaged
                state_avg[col] = None
        
        # Add string columns
        for col in avg_df.columns:
            if col not in numeric_columns and col != "NAME_1" and col != "NAME_2" and col != 'geometry':
                state_avg[col] = "State Average"
        
        state_avg["NAME_1"] = state
        state_avg["NAME_2"] = "All Districts"
        
        # Create a geometry for the state average (centroid of state geometries)
        if 'geometry' in state_df.columns:
            try:
                # Using union_all() instead of unary_union
                if hasattr(state_df.geometry, 'union_all'):
                    state_avg["geometry"] = state_df.geometry.union_all().centroid
                else:
                    # Fallback for older versions of geopandas
                    state_avg["geometry"] = state_df.geometry.unary_union.centroid
            except:
                # If that fails, use the first geometry
                state_avg["geometry"] = state_df.geometry.iloc[0]
        
        state_avgs.append(state_avg)
    
    # Special case for categorical columns like suitability levels
    categorical_columns = ["Adaptation", "Mitigation", "Replacment", "General_SI"]
    for category in categorical_columns:
        if category in avg_df.columns:
            # For national average, use the most common value
            if len(avg_df) > 0:
                try:
                    national_avg[category] = avg_df[category].mode().iloc[0] if not avg_df[category].mode().empty else "Mixed"
                except:
                    national_avg[category] = "Mixed"
            
            # For state averages, use the most common value per state
            for state_avg in state_avgs:
                state_name = state_avg["NAME_1"]
                state_df = avg_df[avg_df["NAME_1"] == state_name]
                if len(state_df) > 0:
                    try:
                        state_avg[category] = state_df[category].mode().iloc[0] if not state_df[category].mode().empty else "Mixed"
                    except:
                        state_avg[category] = "Mixed"
    
    # Create GeoDataFrames from the dictionaries
    national_gdf = gpd.GeoDataFrame([national_avg], geometry='geometry')
    state_gdf = gpd.GeoDataFrame(state_avgs, geometry='geometry')
    
    # Set CRS for the GeoDataFrames to match the original
    if hasattr(_gdf, 'crs') and _gdf.crs is not None:
        national_gdf.crs = _gdf.crs
        state_gdf.crs = _gdf.crs
    
    # Combine the original GeoDataFrame with the averages
    result_gdf = pd.concat([national_gdf, state_gdf, _gdf])
    
    # Ensure the result has the correct CRS
    if hasattr(_gdf, 'crs') and _gdf.crs is not None:
        result_gdf.crs = _gdf.crs
    
    return result_gdf