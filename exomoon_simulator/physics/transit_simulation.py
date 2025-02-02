"""
Core simulation functions for exomoon transit light curves.
"""

import numpy as np
from .geometry import transit_area_vectorized, circle_overlap_vectorized

def simulate_light_curve(
    star_radius=1.0,
    star_intensity=1.0,
    planet_radius=0.1,
    planet_distance=1.0,
    transit_duration=2.0,
    moon_radius=0.03,
    moon_distance=0.3,
    moon_orbital_period=24.0,
    moon_initial_phase=0.0,
    moon_orbital_inclination=0.0,
    include_moon=True,
    num_points=1000
):
    """
    Simulate a transit light curve for a star with a planet and its moon.
    Moon orbit can be inclined relative to the transit plane.
    """
    # Add padding before and after transit for better visualization
    padding_factor = 1.5  # Amount of extra time to show on each side
    total_duration = transit_duration * (1 + 2 * padding_factor)
    time = np.linspace(-total_duration/2, total_duration/2, num_points)
    flux = np.ones_like(time) * star_intensity
    
    # Only calculate transit effects within the actual transit duration
    transit_mask = (time >= -transit_duration/2) & (time <= transit_duration/2)
    transit_time = time[transit_mask]
    
    # Convert inclination to radians
    inclination_rad = np.radians(moon_orbital_inclination)
    
    # Planet position (in transit plane)
    planet_x = transit_time * (2 * star_radius / transit_duration)
    planet_y = np.full_like(transit_time, planet_distance)
    
    # Calculate moon position with inclination effects
    angles = 2 * np.pi * ((transit_time / moon_orbital_period) + moon_initial_phase)
    
    # Moon position relative to planet before projection
    moon_rel_x = moon_distance * np.cos(angles)
    moon_rel_y = moon_distance * np.sin(angles)
    
    # Project moon position considering orbital inclination
    moon_x = planet_x + moon_rel_x  # x-coordinate unchanged
    moon_y = planet_y + moon_rel_y * np.cos(inclination_rad)
    moon_z = moon_rel_y * np.sin(inclination_rad)

    # Calculate overlap areas during transit
    star_planet_overlap = transit_area_vectorized(planet_x, planet_y, planet_radius, star_radius)
    
    if include_moon:
        # Only consider moon transit when it's in front of the star (z >= 0)
        moon_in_front = moon_z >= 0
        star_moon_overlap = np.zeros_like(transit_time)
        star_moon_overlap[moon_in_front] = transit_area_vectorized(
            moon_x[moon_in_front], 
            moon_y[moon_in_front], 
            moon_radius, 
            star_radius
        )
        
        # Calculate planet-moon overlap only when moon is in front
        planet_moon_overlap = np.zeros_like(transit_time)
        planet_moon_overlap[moon_in_front] = circle_overlap_vectorized(
            planet_x[moon_in_front], 
            planet_y[moon_in_front], 
            planet_radius,
            moon_x[moon_in_front], 
            moon_y[moon_in_front], 
            moon_radius
        )
    else:
        star_moon_overlap = 0
        planet_moon_overlap = 0
    
    # Total overlap area considering overlaps
    total_overlap = star_planet_overlap + star_moon_overlap - planet_moon_overlap
    
    # Apply transit effects only during transit
    flux[transit_mask] -= (total_overlap / (np.pi * star_radius**2)) * star_intensity
    
    return time, flux 