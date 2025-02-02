"""
SVG orbital diagram generation for exomoon transit simulations.

Includes projection of inclined moon orbit and dashed lines for orbital paths.
"""

import numpy as np


def create_orbital_diagram(star_radius, planet_radius, planet_distance, moon_radius, 
                           moon_distance, moon_initial_phase, moon_orbital_inclination,
                           include_moon, time_fraction=0):
    """
    Create an SVG orbital diagram showing the current configuration of the system.
    Includes projection of inclined moon orbit.
    """
    # SVG viewport and scaling parameters
    view_size = 500
    margin = 60
    scale = (view_size - 2 * margin) / (4 * star_radius)
    
    # Center of the viewport
    cx = view_size / 2
    cy = view_size / 2
    
    # Calculate positions
    planet_x = time_fraction * (2 * star_radius)
    planet_y = planet_distance
    
    # Convert inclination to radians
    inclination_rad = np.radians(moon_orbital_inclination)
    
    # Calculate moon position with inclination effects
    moon_angle = 2 * np.pi * moon_initial_phase
    moon_rel_x = moon_distance * np.cos(moon_angle)
    moon_rel_y = moon_distance * np.sin(moon_angle)
    
    moon_x = planet_x + moon_rel_x
    moon_y = planet_y + moon_rel_y * np.cos(inclination_rad)
    moon_z = moon_rel_y * np.sin(inclination_rad)
    
    # Generate points for moon's orbital ellipse
    orbit_points = []
    num_points = 100
    for angle in np.linspace(0, 2*np.pi, num_points):
        orbit_rel_x = moon_distance * np.cos(angle)
        orbit_rel_y = moon_distance * np.sin(angle)
        orbit_x = planet_x + orbit_rel_x
        orbit_y = planet_y + orbit_rel_y * np.cos(inclination_rad)
        orbit_points.append((orbit_x * scale + cx, orbit_y * scale + cy))
    
    # Create SVG using an f-string with viewBox attribute
    svg = f'''
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_size} {view_size}">
        <!-- Background -->
        <rect width="{view_size}" height="{view_size}" fill="#f8f9fa"/>
        
        <!-- Coordinate system -->
        <line x1="{margin}" y1="{cy}" x2="{view_size - margin}" y2="{cy}" 
              stroke="#ccc" stroke-width="1" stroke-dasharray="4"/>
        <line x1="{cx}" y1="{margin}" x2="{cx}" y2="{view_size - margin}" 
              stroke="#ccc" stroke-width="1" stroke-dasharray="4"/>
        
        <!-- Star -->
        <circle cx="{cx}" cy="{cy}" r="{star_radius * scale}" 
                fill="#ffde00" stroke="#ff9900" stroke-width="2"/>
        
        <!-- Planet orbit line -->
        <line x1="{cx - 2*star_radius*scale}" y1="{cy + planet_distance*scale}" 
              x2="{cx + 2*star_radius*scale}" y2="{cy + planet_distance*scale}" 
              stroke="#666" stroke-width="1" stroke-dasharray="4"/>
    '''
    
    # Add moon orbit if included
    if include_moon:
        path_d = f"M {orbit_points[0][0]},{orbit_points[0][1]}"
        for x, y in orbit_points[1:]:
            path_d += f" L {x},{y}"
        path_d += " Z"
        svg += f'''
        <!-- Moon orbit -->
        <path d="{path_d}" fill="none" stroke="#999" 
              stroke-width="1" stroke-dasharray="4"/>
        '''
    
    # Add planet
    svg += f'''
        <!-- Planet -->
        <circle cx="{cx + planet_x*scale}" cy="{cy + planet_y*scale}" 
                r="{planet_radius * scale}" fill="#666"/>
    '''
    
    # Add moon if included (always draw with full opacity)
    if include_moon:
        # Adjust moon size based on z-position (perspective effect)
        z_scale = 1.0 - 0.2 * (moon_z / moon_distance) if moon_distance != 0 else 1.0
        moon_apparent_radius = moon_radius * scale * z_scale
        
        svg += f'''
        <!-- Moon -->
        <circle cx="{cx + moon_x*scale}" cy="{cy + moon_y*scale}" 
                r="{moon_apparent_radius}" fill="#999" opacity="1.0"/>
        '''
    
    svg += '</svg>'
    return svg