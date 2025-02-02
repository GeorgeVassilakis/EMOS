"""
Template and layout configuration for the exomoon transit simulator.
"""

import panel as pn
from panel.template import MaterialTemplate
from .widgets import create_widgets, create_reset_button, DEFAULT_VALUES, HELP_TEXT
from ..visualization.light_curve import plot_light_curve
from ..visualization.orbital_diagram import create_orbital_diagram

def create_layout():
    """Create the main layout for the simulator interface."""
    # Create template
    template = MaterialTemplate(title='Exomoon Transit Simulator')
    
    # Create widgets
    widgets = create_widgets()
    reset_button = create_reset_button()
    
    # Create plot panes with increased height
    light_curve_pane = pn.pane.HoloViews(sizing_mode='stretch_width', height=500)
    orbital_diagram_pane = pn.pane.SVG(sizing_mode='stretch_width', height=500)
    
    def update_plots(*events):
        """Update both plots when any parameter changes."""
        # Get current parameter values
        params = {name: widget.value for name, widget in widgets.items()}
        
        # Get time value and remove it from params
        time_value = params.pop('time')
        
        # Update light curve plot
        light_curve = plot_light_curve(**params)
        light_curve_pane.object = light_curve
        
        # Filter parameters for orbital diagram
        orbital_params = {
            'star_radius': params['star_radius'],
            'planet_radius': params['planet_radius'],
            'planet_distance': params['planet_distance'],
            'moon_radius': params['moon_radius'],
            'moon_distance': params['moon_distance'],
            'moon_initial_phase': params['moon_initial_phase'],
            'moon_orbital_inclination': params['moon_orbital_inclination'],
            'include_moon': params['include_moon'],
            'time_fraction': time_value
        }
        
        # Update orbital diagram
        orbital_diagram = create_orbital_diagram(**orbital_params)
        orbital_diagram_pane.object = orbital_diagram
    
    # Set up parameter watching
    for widget in widgets.values():
        widget.param.watch(update_plots, 'value')
    
    def reset_parameters(event):
        """Reset all parameters to default values."""
        for name, widget in widgets.items():
            widget.value = DEFAULT_VALUES[name]
    
    reset_button.on_click(reset_parameters)
    
    # Create control tabs with descriptions
    controls = pn.Tabs(
        ('⭐ Star', pn.Column(
            widgets['star_radius'],
            pn.pane.Markdown(f"**Star Radius**: {HELP_TEXT['star_radius']}", sizing_mode='stretch_width'),
            widgets['star_intensity'],
            pn.pane.Markdown(f"**Star Intensity**: {HELP_TEXT['star_intensity']}", sizing_mode='stretch_width'),
            sizing_mode='stretch_width',
            margin=(10, 5)
        )),
        ('🪐 Planet', pn.Column(
            widgets['planet_radius'],
            pn.pane.Markdown(f"**Planet Radius**: {HELP_TEXT['planet_radius']}", sizing_mode='stretch_width'),
            widgets['planet_distance'],
            pn.pane.Markdown(f"**Planet Distance**: {HELP_TEXT['planet_distance']}", sizing_mode='stretch_width'),
            widgets['transit_duration'],
            pn.pane.Markdown(f"**Transit Duration**: {HELP_TEXT['transit_duration']}", sizing_mode='stretch_width'),
            sizing_mode='stretch_width',
            margin=(10, 5)
        )),
        ('🌕 Moon', pn.Column(
            widgets['moon_radius'],
            pn.pane.Markdown(f"**Moon Radius**: {HELP_TEXT['moon_radius']}", sizing_mode='stretch_width'),
            widgets['moon_distance'],
            pn.pane.Markdown(f"**Moon Distance**: {HELP_TEXT['moon_distance']}", sizing_mode='stretch_width'),
            widgets['moon_orbital_period'],
            pn.pane.Markdown(f"**Moon Orbital Period**: {HELP_TEXT['moon_orbital_period']}", sizing_mode='stretch_width'),
            widgets['moon_initial_phase'],
            pn.pane.Markdown(f"**Moon Initial Phase**: {HELP_TEXT['moon_initial_phase']}", sizing_mode='stretch_width'),
            widgets['moon_orbital_inclination'],
            pn.pane.Markdown(f"**Moon Orbital Inclination**: {HELP_TEXT['moon_orbital_inclination']}", sizing_mode='stretch_width'),
            widgets['include_moon'],
            pn.pane.Markdown(f"**Include Moon**: {HELP_TEXT['include_moon']}", sizing_mode='stretch_width'),
            sizing_mode='stretch_width',
            margin=(10, 5)
        )),
        sizing_mode='stretch_width'
    )
    
    # Create visualization tabs
    main_tabs = pn.Tabs(
        ('📈 Light Curve', pn.Column(
            pn.pane.Markdown("### Transit Light Curve", sizing_mode='stretch_width'),
            light_curve_pane,
            sizing_mode='stretch_both'
        )),
        ('🔭 Orbital View', pn.Column(
            pn.pane.Markdown("### System Configuration", sizing_mode='stretch_width'),
            orbital_diagram_pane,
            widgets['time'],
            pn.pane.Markdown(f"**Time**: {HELP_TEXT['time']}", sizing_mode='stretch_width'),
            sizing_mode='stretch_width'
        )),
        sizing_mode='stretch_both'
    )
    
    # Place controls in sidebar with reset button at the bottom
    template.sidebar.append(
        pn.Column(
            pn.pane.Markdown("### Simulation Controls", sizing_mode='stretch_width'),
            controls,
            reset_button,
            sizing_mode='stretch_width'
        )
    )
    
    # Add main visualization tabs to the main area
    template.main.append(main_tabs)
    
    # Initial plot update
    update_plots()
    
    return template 