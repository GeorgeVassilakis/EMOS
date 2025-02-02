import numpy as np
import panel as pn
import holoviews as hv
from panel.template import MaterialTemplate

# Initialize Panel and Holoviews extensions
pn.extension(sizing_mode='stretch_width')
hv.extension('bokeh')

# ------------------------------
# Default Values Dictionary
# ------------------------------

DEFAULT_VALUES = {
    'star_radius': 1.0,
    'star_intensity': 1.0,
    'planet_radius': 0.1,
    'planet_distance': 0.5,
    'transit_duration': 4.0,
    'moon_radius': 0.03,
    'moon_distance': 0.2,
    'moon_orbital_period': 24.0,
    'moon_initial_phase': 0.0,
    'moon_orbital_inclination': 0.0,
    'include_moon': True,
    'time': 0.0
}

# ------------------------------
# Simulation Functions
# ------------------------------

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

def transit_area_vectorized(x, y, radius, star_radius):
    """
    Vectorized calculation of the overlap area between the star and a transiting body.
    """
    distance = np.sqrt(x**2 + y**2)
    area = np.zeros_like(distance)
    
    # Case 1: No overlap
    no_overlap = distance >= (star_radius + radius)
    area[no_overlap] = 0
    
    # Case 2: Complete overlap (transiting body entirely within the star)
    complete_overlap = distance <= (star_radius - radius)
    area[complete_overlap] = np.pi * radius**2
    
    # Case 3: Partial overlap
    partial_overlap = ~(no_overlap | complete_overlap)
    d = distance[partial_overlap]
    r, R = radius, star_radius
    argument = (d**2 + r**2 - R**2) / (2*d*r)
    argument_clipped = np.clip(argument, -1, 1)
    phi = 2 * np.arccos(argument_clipped)

    theta = 2 * np.arccos((d**2 + R**2 - r**2) / (2 * d * R))
    area1 = 0.5 * r**2 * (phi - np.sin(phi))
    area2 = 0.5 * R**2 * (theta - np.sin(theta))
    area[partial_overlap] = area1 + area2
    
    return area

def circle_overlap_vectorized(x1, y1, r1, x2, y2, r2):
    """
    Vectorized calculation of the overlap area between two circles.
    """
    distance = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    area = np.zeros_like(distance)
    
    # Case 1: No overlap
    no_overlap = distance >= (r1 + r2)
    area[no_overlap] = 0
    
    # Case 2: Complete overlap (one circle entirely within the other)
    complete_overlap = distance <= np.abs(r1 - r2)
    area[complete_overlap] = np.pi * np.minimum(r1, r2)**2
    
    # Case 3: Partial overlap
    partial_overlap = ~(no_overlap | complete_overlap)
    d = distance[partial_overlap]
    alpha = np.arccos((d**2 + r1**2 - r2**2) / (2 * d * r1))
    beta = np.arccos((d**2 + r2**2 - r1**2) / (2 * d * r2))
    area1 = r1**2 * alpha
    area2 = r2**2 * beta
    area3 = 0.5 * np.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2))
    area[partial_overlap] = area1 + area2 - area3
    
    return area

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
    
    # Calculate moon position with inclination
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
    
    # Create SVG
    svg = f'''
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_size} {view_size}">
        <!-- Background -->
        <rect width="{view_size}" height="{view_size}" fill="#f8f9fa"/>
        
        <!-- Coordinate system -->
        <line x1="{margin}" y1="{cy}" x2="{view_size-margin}" y2="{cy}" 
              stroke="#ccc" stroke-width="1" stroke-dasharray="4"/>
        <line x1="{cx}" y1="{margin}" x2="{cx}" y2="{view_size-margin}" 
              stroke="#ccc" stroke-width="1" stroke-dasharray="4"/>
        
        <!-- Star -->
        <circle cx="{cx}" cy="{cy}" r="{star_radius * scale}" 
                fill="#ffde00" stroke="#ff9900" stroke-width="2"/>
        
        <!-- Planet orbit line -->
        <line x1="{cx - 2*star_radius*scale}" y1="{cy + planet_distance*scale}" 
              x2="{cx + 2*star_radius*scale}" y2="{cy + planet_distance*scale}" 
              stroke="#666" stroke-width="1" stroke-dasharray="4"/>
    '''
    
    # Add moon orbit ellipse if included
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
    
    # Add moon if included
    if include_moon:
        # Adjust moon size based on z-position (perspective effect)
        z_scale = 1.0 - 0.2 * (moon_z / moon_distance)
        moon_apparent_radius = moon_radius * scale * z_scale
        
        svg += f'''
        <!-- Moon -->
        <circle cx="{cx + moon_x*scale}" cy="{cy + moon_y*scale}" 
                r="{moon_apparent_radius}" fill="#999"
                opacity="{1.0 if moon_z >= 0 else 0.5}"/>
        '''
    
    svg += '</svg>'
    return svg

# ------------------------------
# Create Widgets with Help Texts
# ------------------------------

def create_slider(name, start, end, step, value, help_text):
    slider = pn.widgets.FloatSlider(
        name=name,
        start=start,
        end=end,
        step=step,
        value=value,
        sizing_mode='stretch_width',
        tooltips=True
    )
    help_pane = pn.pane.Markdown(f"**{name}**: {help_text}", sizing_mode='stretch_width')
    return pn.Column(slider, help_pane)

# Star parameters
star_radius_slider = create_slider(
    name='Star Radius (R☉)',
    start=0.5,
    end=2.0,
    step=0.1,
    value=DEFAULT_VALUES['star_radius'],
    help_text='Radius of the star in solar radii (R☉).'
)
star_intensity_slider = create_slider(
    name='Star Intensity',
    start=0.5,
    end=1.5,
    step=0.1,
    value=DEFAULT_VALUES['star_intensity'],
    help_text='Normalized intensity of the star.'
)

# Planet parameters
planet_radius_slider = create_slider(
    name='Planet Radius (R*)',
    start=0.05,
    end=0.2,
    step=0.005,
    value=DEFAULT_VALUES['planet_radius'],
    help_text='Radius of the planet in stellar radii (R*).'
)
planet_distance_slider = create_slider(
    name='Planet Impact Parameter (R*)',
    start=0.0,
    end=1.0,
    step=0.01,
    value=DEFAULT_VALUES['planet_distance'],
    help_text='Impact parameter of the planet in stellar radii (R*).'
)
transit_duration_slider = create_slider(
    name='Transit Duration (hours)',
    start=1.0,
    end=10.0,
    step=0.5,
    value=DEFAULT_VALUES['transit_duration'],
    help_text='Duration of the transit in hours.'
)

# Moon parameters
moon_radius_slider = create_slider(
    name='Moon Radius (R*)',
    start=0.01,
    end=0.05,
    step=0.001,
    value=DEFAULT_VALUES['moon_radius'],
    help_text='Radius of the moon in stellar radii (R*).'
)
moon_distance_slider = create_slider(
    name='Moon Distance from Planet (R*)',
    start=0.1,
    end=0.5,
    step=0.01,
    value=DEFAULT_VALUES['moon_distance'],
    help_text='Distance of the moon from the planet in stellar radii (R*).'
)
moon_orbital_period_slider = create_slider(
    name='Moon Orbital Period (hours)',
    start=1.0,
    end=48.0,
    step=1.0,
    value=DEFAULT_VALUES['moon_orbital_period'],
    help_text='Orbital period of the moon around the planet in hours.'
)
moon_initial_phase_slider = create_slider(
    name='Moon Initial Phase',
    start=0.0,
    end=1.0,
    step=0.05,
    value=DEFAULT_VALUES['moon_initial_phase'],
    help_text='Initial phase of the moon\'s orbit (0 to 1).'
)
moon_inclination_slider = create_slider(
    name='Moon Orbital Inclination (°)',
    start=0.0,
    end=90.0,
    step=1.0,
    value=DEFAULT_VALUES['moon_orbital_inclination'],
    help_text='Inclination of moon\'s orbit relative to transit plane (0° = edge-on, 90° = face-on).'
)

# Include Moon Toggle
include_moon_toggle = pn.widgets.Checkbox(
    name='Include Moon',
    value=DEFAULT_VALUES['include_moon'],
    sizing_mode='stretch_width'
)
include_moon_help = pn.pane.Markdown(
    "**Include Moon**: Toggle to include or exclude the moon from the simulation.",
    sizing_mode='stretch_width'
)

# Create a time slider for the orbital diagram
time_slider = pn.widgets.FloatSlider(
    name='Transit Time',
    start=-1,
    end=1,
    step=0.1,
    value=DEFAULT_VALUES['time'],
    sizing_mode='stretch_width'
)

# Create the orbital diagram pane
orbital_diagram = pn.pane.SVG(sizing_mode='stretch_width', height=500)

# ------------------------------
# Reset Button Function
# ------------------------------

def reset_parameters(event):
    """Reset all parameters to their default values"""
    star_radius_slider[0].value = DEFAULT_VALUES['star_radius']
    star_intensity_slider[0].value = DEFAULT_VALUES['star_intensity']
    planet_radius_slider[0].value = DEFAULT_VALUES['planet_radius']
    planet_distance_slider[0].value = DEFAULT_VALUES['planet_distance']
    transit_duration_slider[0].value = DEFAULT_VALUES['transit_duration']
    moon_radius_slider[0].value = DEFAULT_VALUES['moon_radius']
    moon_distance_slider[0].value = DEFAULT_VALUES['moon_distance']
    moon_orbital_period_slider[0].value = DEFAULT_VALUES['moon_orbital_period']
    moon_initial_phase_slider[0].value = DEFAULT_VALUES['moon_initial_phase']
    moon_inclination_slider[0].value = DEFAULT_VALUES['moon_orbital_inclination']
    include_moon_toggle.value = DEFAULT_VALUES['include_moon']
    time_slider.value = DEFAULT_VALUES['time']

reset_button = pn.widgets.Button(
    name='Reset Parameters',
    button_type='primary',
    sizing_mode='stretch_width'
)
reset_button.on_click(reset_parameters)

def update_orbital_diagram(*args, **kwargs):
    """Update the orbital diagram based on current parameter values"""
    svg = create_orbital_diagram(
        star_radius=star_radius_slider[0].value,
        planet_radius=planet_radius_slider[0].value,
        planet_distance=planet_distance_slider[0].value,
        moon_radius=moon_radius_slider[0].value,
        moon_distance=moon_distance_slider[0].value,
        moon_initial_phase=moon_initial_phase_slider[0].value,
        moon_orbital_inclination=moon_inclination_slider[0].value,
        include_moon=include_moon_toggle.value,
        time_fraction=time_slider.value
    )
    orbital_diagram.object = svg

# Bind all parameters to update the orbital diagram
for param in [star_radius_slider[0], planet_radius_slider[0], planet_distance_slider[0],
              moon_radius_slider[0], moon_distance_slider[0], moon_initial_phase_slider[0],
              moon_inclination_slider[0], include_moon_toggle, time_slider]:
    param.param.watch(update_orbital_diagram, 'value')

# ------------------------------
# Organize Controls into Tabs
# ------------------------------

controls = pn.Tabs(
    ('⭐ Star', pn.Column(
        star_radius_slider,
        star_intensity_slider,
        sizing_mode='stretch_width',
        margin=(10, 5)
    )),
    ('🪐 Planet', pn.Column(
        planet_radius_slider,
        planet_distance_slider,
        transit_duration_slider,
        sizing_mode='stretch_width',
        margin=(10, 5)
    )),
    ('🌕 Moon', pn.Column(
        moon_radius_slider,
        moon_distance_slider,
        moon_orbital_period_slider,
        moon_initial_phase_slider,
        moon_inclination_slider,
        include_moon_toggle,
        include_moon_help,
        sizing_mode='stretch_width',
        margin=(10, 5)
    )),
    sizing_mode='stretch_width'
)

# ------------------------------
# Create the Interactive Plot
# ------------------------------

interactive_plot = pn.bind(
    plot_light_curve,
    star_radius=star_radius_slider[0],
    star_intensity=star_intensity_slider[0],
    planet_radius=planet_radius_slider[0],
    planet_distance=planet_distance_slider[0],
    transit_duration=transit_duration_slider[0],
    moon_radius=moon_radius_slider[0],
    moon_distance=moon_distance_slider[0],
    moon_orbital_period=moon_orbital_period_slider[0],
    moon_initial_phase=moon_initial_phase_slider[0],
    moon_orbital_inclination=moon_inclination_slider[0],
    include_moon=include_moon_toggle
)

# ------------------------------
# Create the Template and Layout
# ------------------------------

template = MaterialTemplate(title='Exomoon Transit Simulator')

# Place controls first, then the reset button at the bottom
template.sidebar.append(
    pn.Column(
        pn.pane.Markdown("### Simulation Controls", sizing_mode='stretch_width'),
        controls,
        reset_button,  # Moved the reset button below the controls
        sizing_mode='stretch_width'
    )
)

main_tabs = pn.Tabs(
    ('📈 Light Curve', pn.Column(
        pn.pane.HoloViews(interactive_plot, sizing_mode='stretch_both')
    )),
    ('🔭 Orbital View', pn.Column(
        pn.pane.Markdown("### System Configuration", sizing_mode='stretch_width'),
        orbital_diagram,
        time_slider,
        sizing_mode='stretch_width'
    )),
    sizing_mode='stretch_both'
)

template.main.append(main_tabs)

# Initialize the orbital diagram
update_orbital_diagram()

# Make the dashboard servable
template.servable()
