# Solar Suitability Dashboard

![Dashboard Preview](https://i.imgur.com/RqXBMXl.png)

## Overview

The Solar Suitability Dashboard is an interactive web application that visualizes solar suitability across various regions. It provides stakeholders with a powerful tool to analyze multiple factors affecting solar potential and make data-driven decisions for solar implementation strategies.

This dashboard was developed for the International Water Management Institute (IWMI) to support sustainable energy and water management initiatives.

## Key Features

- **Interactive Geographic Visualization**: Explore solar suitability across different states and districts
- **Multi-layered Analysis**: Examine various factors affecting solar potential
- **Statistical Insights**: View distribution of suitability levels with interactive charts
- **Comparative Analysis**: Compare different regions at national, state, and district levels
- **Intuitive Filtering**: Easily filter by state, district, category, and data layer

## Technical Architecture

The dashboard is built with a modular architecture to ensure maintainability, reusability, and performance optimization. The codebase is organized into the following structure:

```
IWMI_dashboard_2.0/
│
├── app.py                      # Main application entry point
│
├── .streamlit/                 # Streamlit configuration
│   └── config.toml             # Theme and settings
│
├── requirements.txt            # Project dependencies
│
├── README.md                   # Project documentation
│
├── data/                       # Data files
│   └── shapefiles/             # GIS shapefiles
│       ├── Solar_Suitability_layer.shp
│       ├── Solar_Suitability_layer.shx
│       ├── Solar_Suitability_layer.dbf
│       └── Solar_Suitability_layer.prj
│
├── static/                     # Static assets
│   └── images/                 # Images and logos
│       └── logo.png
│
├── modules/                    # Application modules
│   │
│   ├── __init__.py             # Makes modules directory a package
│   │
│   ├── data/                   # Data handling modules
│   │   ├── __init__.py
│   │   ├── loader.py           # Data loading and caching
│   │   ├── processor.py        # Data filtering and processing
│   │   └── calculator.py       # Statistical calculations
│   │
│   ├── visualization/          # Visualization modules
│   │   ├── __init__.py
│   │   ├── maps.py             # Map creation functions
│   │   └── charts.py           # Charts and plots
│   │
│   ├── ui/                     # UI components
│   │   ├── __init__.py
│   │   ├── layout.py           # Page layout components
│   │   └── styles.py           # CSS and styling
│   │
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       └── constants.py        # Application constants
│
└── run.bat                     # Startup script for Windows
```

### Module Descriptions

#### Data Modules

- **loader.py**: Handles loading and caching of shapefile data
- **processor.py**: Processes and filters data based on user selections
- **calculator.py**: Performs statistical calculations and aggregations

#### Visualization Modules

- **maps.py**: Creates and styles interactive maps
- **charts.py**: Generates statistical charts and visualizations

#### UI Modules

- **layout.py**: Defines page layout components (header, footer, controls)
- **styles.py**: Manages CSS styling for consistent appearance

#### Utility Modules

- **constants.py**: Stores application-wide constants and mappings

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**

```bash
git clone https://github.com/IWMI/Solar-Suitability-Dashboard.git
cd IWMI_dashboard_2.0
```

2. **Create and activate a virtual environment**

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure shapefile path**

Ensure your shapefiles are placed in the correct location:

```
IWMI_dashboard_2.0/data/shapefiles/Solar_Suitability_layer.shp
```

Or update the path in `modules/data/loader.py` to point to your shapefile location.

5. **Run the application**

```bash
streamlit run app.py
```

Or use the provided `run.bat` script on Windows.

## Usage Guide

### Basic Navigation

1. **Select State and District**:
   - Use the dropdown menus to choose your area of interest.
   - Select "National Average" for a country-wide view.
   - Select a specific state and "All Districts" for a state-level view.
   - Select a specific state and district for detailed district-level analysis.

2. **Choose Analysis Category**:
   - Select one of the following categories:
     - **Adaptation**: Suitability for adaptation strategies
     - **Mitigation**: Suitability for mitigation approaches
     - **Replacement**: Suitability for replacing existing energy sources
     - **General_SI**: General Suitability Index

3. **Select Data Layer**:
   - Choose the specific data layer to visualize, including:
     - Solar radiance
     - Groundwater Development Stage
     - Irrigation Coverage
     - Cropping Intensity
     - And many more parameters

### Interpreting the Map

- **Color Coding**:
  - **Dark Green**: Very Highly Suitable
  - **Light Green**: Highly Suitable
  - **Yellow**: Moderately Suitable
  - **Red**: Less Suitable
  - **Gray**: Mixed or Insufficient Data

- **Map Features**:
  - District boundaries are shown with black outlines.
  - District names are displayed when viewing state-level data.
  - The legend shows the suitability classification.

### Statistics Panel

The statistics panel on the right displays:
- Selected state and district
- Suitability category value
- Selected layer value
- Distribution charts (for state and national views)
- Summary metrics

## Technical Details

### Data Processing

The application uses GeoPandas to handle geospatial data and implements several optimization techniques:

1. **Data Caching**: Utilizes Streamlit's caching mechanism to avoid reloading data unnecessarily.
2. **Shapefile Optimization**: Offers an option to create optimized versions of shapefiles for better performance.
3. **Efficient Filtering**: Implements efficient data filtering techniques to quickly respond to user selections.

### Visualization

The dashboard uses a combination of visualization libraries:

1. **Matplotlib**: For creating the geographic maps
2. **Plotly**: For interactive charts and statistical visualizations

### UI Components

The user interface is built with Streamlit and enhanced with custom CSS for a polished appearance:

1. **Custom Styling**: Implements a consistent color scheme and styling
2. **Responsive Layout**: Adapts to different screen sizes
3. **Modular Components**: Encapsulates UI elements in reusable functions

## Performance Considerations

- **Large Shapefiles**: When working with large shapefiles, consider using the optimization function:
  ```python
  from modules.data.loader import optimize_shapefile
  optimize_shapefile()
  ```

- **Memory Usage**: The application caches data to improve performance but may require significant memory for large datasets. Recommended minimum RAM is 4GB.

## Future Enhancements

Planned improvements include:

- **Temporal Data**: Integration of time-series data for trend analysis
- **Export Functionality**: Ability to export maps and data as reports
- **Mobile Responsiveness**: Improved interface for mobile devices
- **API Integration**: Expose dashboard data through an API for external applications
- **Advanced Analytics**: Integration of predictive modeling and more sophisticated analysis tools

## Troubleshooting

### Common Issues

1. **Shapefile Not Found Error**:
   - Ensure shapefiles are placed in the correct directory
   - Check the path in `modules/data/loader.py`
   - Verify the shapefile has all necessary components (.shp, .shx, .dbf, .prj)

2. **Rendering Issues**:
   - Update your browser to the latest version
   - Try a different browser if problems persist
   - Ensure you have sufficient memory available

3. **Package Dependencies**:
   - If you encounter package errors, try installing dependencies individually:
     ```bash
     pip install streamlit pandas geopandas matplotlib plotly
     ```

## Contributing

We welcome contributions to improve the Solar Suitability Dashboard! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests to ensure functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions, issues, or collaboration opportunities, please contact:

**Mohammad Faiz Alam**  
Regional Researcher  
International Water Management Institute (IWMI)  
Email: m.alam@cgiar.org

## Acknowledgments

- International Water Management Institute (IWMI) for supporting this project
- Contributors to the open-source libraries used in this dashboard
- All stakeholders who provided feedback during the development process