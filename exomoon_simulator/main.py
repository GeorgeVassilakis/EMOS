"""
Main entry point for the exomoon transit simulator dashboard.
"""

import panel as pn
import holoviews as hv
from .ui.layout import create_layout

def main():
    """Launch the exomoon transit simulator dashboard."""
    # Initialize Panel and Holoviews extensions
    pn.extension('bokeh', sizing_mode='stretch_width')
    hv.extension('bokeh')
    
    # Create and serve the dashboard
    dashboard = create_layout()
    pn.serve(dashboard, show=True, port=5007)

if __name__ == '__main__':
    main() 