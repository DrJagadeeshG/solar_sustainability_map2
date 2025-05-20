# modules/utils/constants.py

"""
Constants module for the Solar Suitability Dashboard.

This module contains all the constant values, mappings, and configuration settings
used throughout the application. Centralizing these values makes the application
more maintainable and ensures consistency across different components.
"""

# Layer explanations for tooltips
layer_explanations = {
    "Solar radiance": "Gives solar radiance",
    "Cropping Intensity (%)": "Gives how intensively an area is cultivated (Gross cultivated area/Net cultivated area)",
    "Irrigation Coverage (%)": "Gives the extent of irrigation coverage and contribution of GW in a district.",
    "Irrigation Water Requirement": "Gives irrigation requirement (as part of consumptive needs) which provide information on crop water needs relative to rainfall in a district.",
    "Cultivated land": "Gives indication of how intensively a district is cultivated.",
    "Pump energy": "Gives source of power for groundwater pumping, here electric with most of the rest being diesel.",
    "Energy Subsidy": "Indicators how subsidises electricity for pumping is in a district.",
    "GW Development Stage": "How much groundwater has been used in a district relative to recharge.",
    "Aquifer(Shallow) (mbgl)": "How deep are the groundwater tables, this dictates energy needed for pumping.",
    "Surface Water Body (ha)": "Extent of surface water body area (ha) in a district, gives the suitability of using solar with surface water sources",
    "Small & marginal holdings (%)": "Percent of small and marginal farmers in a district.",
    "Farmers average area (ha)": "Average holding of farmer",
    "Land fragmentation (number)": "Number of parcels per holding indicating how fragmented the land holdings are.",
    "Aridity Index": "Measure of dryness of the climate, higher values indicate more arid conditions."
}

# Layer to column mapping
layer_column_mapping = {
    "Solar radiance": "Rainfall__",
    "Cropping Intensity (%)": "CI_yield",
    "Irrigation Coverage (%)": "Irrig_cov_",
    "Irrigation Water Requirement": "C_Irr_Ex_G",
    "Cultivated land": "C_Land_Rc",
    "Pump energy": "C_PHS",
    "Energy Subsidy": "C_E_FC",
    "GW Development Stage": "GW_dev_sta",
    "Aquifer(Shallow) (mbgl)": "Aquifer_ty",
    "Surface Water Body (ha)": "Sw____",
    "Small & marginal holdings (%)": "C_S_H",
    "Farmers average area (ha)": "C_F_L",
    "Land fragmentation (number)": "C_L_R",
    "Aridity Index": "aridity",
    "Others": "Himalayan"
}

# Color definitions for consistent use throughout the application
colors = {
    """
    Color palette for consistent styling throughout the application.
    Using these predefined colors ensures visual consistency.
    """
    # Main theme colors
    "primary": "#1976d2",    # Blue
    "secondary": "#d81b60",  # Red
    "success": "#388e3c",    # Green
    "warning": "#fbc02d",    # Yellow
    
    # Suitability colors
    "very_highly_suitable": "#66CC66",  # Dark green
    "highly_suitable": "#99FF99",       # Light green
    "moderately_suitable": "#FFFF99",   # Yellow
    "less_suitable": "#CC0000",         # Red
    "mixed": "#CCCCCC",                 # Gray
    
    # UI colors
    "background": "#ffffff",            # White
    "panel_background": "#f5f5f5",      # Light gray
    "text": "#333333",                  # Dark gray
    "light_text": "#757575",            # Medium gray
}

# Suitability category mapping (for consistent numeric values)
suitability_category_mapping = {
    """
    Maps suitability categories to numeric values for visualization.
    Higher values represent more suitable categories.
    """
    "Very Highly Suitable": 4,
    "Highly Suitable": 3,
    "Moderately Suitable": 2,
    "Less Suitable": 1,
    "Mixed": 0
}