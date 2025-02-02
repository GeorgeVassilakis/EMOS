# Exomoon Transit Simulator

An interactive dashboard for simulating and visualizing exoplanet-exomoon transit light curves. This tool allows users to explore how various parameters affect the appearance of transit light curves when an exoplanet with an exomoon passes in front of its host star.

## Features

- Interactive simulation of exoplanet and exomoon transits
- Real-time light curve visualization
- Dynamic orbital diagram
- Adjustable parameters for star, planet, and moon properties
- Support for inclined moon orbits

## Usage

To run the simulator dashboard:

```bash
python -m exomoon_simulator.main
```

The dashboard will open in your default web browser. Use the sliders and controls to adjust the simulation parameters:

- Star Parameters: Adjust the star's radius and intensity
- Planet Parameters: Modify the planet's size, distance, and transit duration
- Moon Parameters: Configure the moon's properties and orbital characteristics
- Time Control: Navigate through the transit event

## Project Structure

```
exomoon_simulator/
├── __init__.py
├── physics/
│   ├── __init__.py
│   ├── transit_simulation.py    # Core simulation functions
│   └── geometry.py             # Geometric calculations
├── visualization/
│   ├── __init__.py
│   ├── light_curve.py          # Light curve plotting
│   └── orbital_diagram.py      # SVG orbital diagram
├── ui/
│   ├── __init__.py
│   ├── widgets.py              # Widget definitions
│   └── layout.py              # Dashboard layout
└── main.py                     # Main entry point
```

## Dependencies

- numpy: Scientific computing and numerical operations
- panel: Dashboard framework
- holoviews: Data visualization library
- bokeh: Interactive visualization backend

## License

This project is licensed under the MIT License - see the LICENSE file for details.
