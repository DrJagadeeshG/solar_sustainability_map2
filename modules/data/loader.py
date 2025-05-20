# modules/data/loader.py

"""
Data loader module for the Solar Suitability Dashboard.

This module handles loading and caching data from various sources,
particularly the shapefile data that forms the foundation of the
dashboard's visualizations and analysis.
"""

import streamlit as st
import pandas as pd
import geopandas as gpd
import os
from shapely.geometry import Point
from modules.data.calculator import calculate_averages

# Define the path to your shapefile
SHAPEFILE_PATH = r"F:\GitHub\IWMI_dashboard_2.0\data\shapefiles\Solar_Suitability_layer_optimized.shp"
ORIGINAL_SHAPEFILE_PATH = r"F:\GitHub\IWMI_dashboard_2.0\data\shapefiles\Solar_Suitability_layer.shp"

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_shapefile_data():
    """
    Load the shapefile data with caching to improve performance.
    
    This function attempts to load either an optimized version of the shapefile
    (if available) or the original shapefile. It handles data type conversion,
    calculates aggregated statistics, and provides a fallback to dummy data
    if loading fails.
    
    Returns:
        GeoDataFrame: The processed geodataframe with calculated averages
    """
    try:
        # Try to load the optimized version if it exists
        if os.path.exists(SHAPEFILE_PATH):
            st.info(f"Loading optimized shapefile from: {SHAPEFILE_PATH}")
            gdf = gpd.read_file(SHAPEFILE_PATH)
        elif os.path.exists(ORIGINAL_SHAPEFILE_PATH):
            st.info(f"Loading original shapefile from: {ORIGINAL_SHAPEFILE_PATH}")
            gdf = gpd.read_file(ORIGINAL_SHAPEFILE_PATH)
        else:
            st.warning(f"Neither optimized nor original shapefile found at the specified paths.")
            raise FileNotFoundError(f"Could not find shapefile at {SHAPEFILE_PATH} or {ORIGINAL_SHAPEFILE_PATH}")
        
        # Make sure GW_dev_sta is numeric
        if "GW_dev_sta" in gdf.columns:
            gdf["GW_dev_sta"] = pd.to_numeric(gdf["GW_dev_sta"], errors='coerce')
        
        # Add district and state averages
        calculated_data = calculate_averages(gdf)
        
        return calculated_data
    except Exception as e:
        st.error(f"Error loading shapefile: {e}")
        # Return a simplified dummy dataset
        return get_dummy_data()

def get_dummy_data():
    """
    Generate dummy data for testing with geometry.
    
    This function creates a simple GeoDataFrame with dummy data
    that can be used for testing the application when the actual
    data is unavailable or cannot be loaded.
    
    Returns:
        GeoDataFrame: A simple geodataframe with dummy data
    """
    # Create a blank geodataframe with basic columns
    gdf = gpd.GeoDataFrame({
        "NAME_1": ["Dummy State"],
        "NAME_2": ["Dummy District"],
        "GW_dev_sta": [50.0],
        "Adaptation": ["Highly Suitable"],
        "Mitigation": ["Moderately Suitable"],
        "Replacment": ["Less Suitable"],
        "General_SI": ["Highly Suitable"]
    }, geometry=[None])
    
    # Add a dummy point geometry
    from shapely.geometry import Point
    gdf.geometry = [Point(78.5, 20.5)]
    
    # Set CRS
    gdf.crs = "EPSG:4326"
    
    return gdf

def optimize_shapefile(input_path=ORIGINAL_SHAPEFILE_PATH, output_path=SHAPEFILE_PATH, simplify_tolerance=0.01):
    """
    Create a simplified version of the shapefile with optimized geometries.
    
    This function should be run once before deploying the app to create
    an optimized version of the shapefile with simplified geometries,
    which improves loading time and performance.
    
    Args:
        input_path (str): Path to the original shapefile
        output_path (str): Path to save the optimized shapefile
        simplify_tolerance (float): Tolerance for simplification (higher = more simplification)
        
    Returns:
        str: Success message or error message
    """
    try:
        # Load the shapefile
        gdf = gpd.read_file(input_path)
        
        st.info(f"Original shapefile loaded: {len(gdf)} features")
        
        # Simplify geometries to reduce file size and improve performance
        gdf['geometry'] = gdf['geometry'].simplify(tolerance=simplify_tolerance, preserve_topology=True)
        
        st.info("Geometries simplified")
        
        # Ensure numeric columns are properly typed
        for col in gdf.columns:
            if col not in ['geometry', 'NAME_1', 'NAME_2']:
                try:
                    gdf[col] = pd.to_numeric(gdf[col], errors='coerce')
                except:
                    pass  # Skip columns that can't be converted
        
        st.info("Column types optimized")
        
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save optimized shapefile
        gdf.to_file(output_path)
        
        st.success(f"Optimized shapefile saved to {output_path}")
        return f"Successfully created optimized shapefile at {output_path}"
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return f"Error: {str(e)}"