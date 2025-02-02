"""
Widget definitions and help text for the exomoon transit simulator.
"""

import panel as pn

# Default parameter values
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

# Help text for each parameter
HELP_TEXT = {
    'star_radius': 'Radius of the star (arbitrary units)',
    'star_intensity': 'Base intensity of the star (arbitrary units)',
    'planet_radius': 'Radius of the planet relative to star radius',
    'planet_distance': 'Distance of planet from star center in transit plane',
    'transit_duration': 'Duration of the transit in hours',
    'moon_radius': 'Radius of the moon relative to star radius',
    'moon_distance': 'Distance of moon from planet center',
    'moon_orbital_period': 'Orbital period of moon around planet in hours',
    'moon_initial_phase': 'Initial orbital phase of moon (0-1)',
    'moon_orbital_inclination': 'Inclination of moon orbit relative to transit plane (degrees)',
    'include_moon': 'Whether to include the moon in the simulation',
    'time': 'Current time in the simulation'
}

def create_slider(name, start, end, step, value, help_text):
    """Create a labeled slider with help text."""
    return pn.widgets.FloatSlider(
        name=name.replace('_', ' ').title(),
        start=start,
        end=end,
        step=step,
        value=value
    )

def create_widgets():
    """Create all widgets for the simulator interface."""
    widgets = {
        'star_radius': create_slider('star_radius', 0.5, 2.0, 0.1, DEFAULT_VALUES['star_radius'], 
                                   HELP_TEXT['star_radius']),
        'star_intensity': create_slider('star_intensity', 0.5, 2.0, 0.1, DEFAULT_VALUES['star_intensity'],
                                      HELP_TEXT['star_intensity']),
        'planet_radius': create_slider('planet_radius', 0.01, 0.3, 0.01, DEFAULT_VALUES['planet_radius'],
                                     HELP_TEXT['planet_radius']),
        'planet_distance': create_slider('planet_distance', 0.0, 2.0, 0.1, DEFAULT_VALUES['planet_distance'],
                                       HELP_TEXT['planet_distance']),
        'transit_duration': create_slider('transit_duration', 1.0, 10.0, 0.5, DEFAULT_VALUES['transit_duration'],
                                        HELP_TEXT['transit_duration']),
        'moon_radius': create_slider('moon_radius', 0.005, 0.1, 0.005, DEFAULT_VALUES['moon_radius'],
                                   HELP_TEXT['moon_radius']),
        'moon_distance': create_slider('moon_distance', 0.05, 0.5, 0.05, DEFAULT_VALUES['moon_distance'],
                                     HELP_TEXT['moon_distance']),
        'moon_orbital_period': create_slider('moon_orbital_period', 1.0, 48.0, 1.0, 
                                           DEFAULT_VALUES['moon_orbital_period'],
                                           HELP_TEXT['moon_orbital_period']),
        'moon_initial_phase': create_slider('moon_initial_phase', 0.0, 1.0, 0.05, 
                                          DEFAULT_VALUES['moon_initial_phase'],
                                          HELP_TEXT['moon_initial_phase']),
        'moon_orbital_inclination': create_slider('moon_orbital_inclination', -90.0, 90.0, 5.0,
                                                DEFAULT_VALUES['moon_orbital_inclination'],
                                                HELP_TEXT['moon_orbital_inclination']),
        'include_moon': pn.widgets.Checkbox(name='Include Moon', value=DEFAULT_VALUES['include_moon']),
        'time': create_slider('time', -2.0, 2.0, 0.1, DEFAULT_VALUES['time'],
                            HELP_TEXT['time'])
    }
    
    return widgets

def create_reset_button():
    """Create a button to reset all parameters to default values."""
    return pn.widgets.Button(name='Reset Parameters', button_type='primary') 