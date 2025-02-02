"""
Light curve plotting functions for exomoon transit simulations.
"""

import holoviews as hv
import numpy as np
from ..physics.transit_simulation import simulate_light_curve

def plot_light_curve(star_radius, star_intensity, planet_radius, planet_distance, transit_duration,
                     moon_radius, moon_distance, moon_orbital_period, moon_initial_phase, 
                     moon_orbital_inclination, include_moon):
    """
    Generate an interactive Holoviews plot for the transit light curve.
    """
    time, flux = simulate_light_curve(
        star_radius=star_radius,
        star_intensity=star_intensity,
        planet_radius=planet_radius,
        planet_distance=planet_distance,
        transit_duration=transit_duration,
        moon_radius=moon_radius,
        moon_distance=moon_distance,
        moon_orbital_period=moon_orbital_period,
        moon_initial_phase=moon_initial_phase,
        moon_orbital_inclination=moon_orbital_inclination,
        include_moon=include_moon
    )
    
    title = 'Exomoon Transit Light Curve' if include_moon else 'Planet Transit Light Curve'
    
    # Calculate y-axis range to show the transit clearly while maintaining context
    flux_min = np.min(flux)
    flux_max = np.max(flux)
    flux_range = flux_max - flux_min
    y_padding = flux_range * 0.1
    
    curve = hv.Curve((time, flux), 'Time (hours)', 'Normalized Flux').opts(
        title=title,
        responsive=True,
        height=500,
        line_width=2,
        color='#1f77b4',
        tools=['hover', 'pan', 'wheel_zoom', 'box_zoom', 'reset', 'save'],
        toolbar='above',
        xlabel='Time (hours)',
        ylabel='Normalized Flux',
        ylim=(flux_min - y_padding, flux_max + y_padding),
        fontsize={'title': 16, 'labels': 14, 'ticks': 12},
        show_grid=True,
        gridstyle={'grid_line_dash': 'dotted', 'grid_line_width': 0.5},
    )
    
    return curve 