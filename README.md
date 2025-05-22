# Exomoon Transit Simulator

An interactive dashboard for simulating and visualizing exoplanet-exomoon transit light curves. This tool allows users to explore how various parameters affect the appearance of transit light curves when an exoplanet with an exomoon passes in front of its host star.

## Live Web Application

This simulator is deployed as an interactive web application using GitHub Pages. You can access it here:

**[Access the Exomoon Transit Simulator](https://georgevassilakis.github.io/EMOS/)**

---
*The web application is automatically built and deployed using GitHub Actions.*

## Features

- Interactive simulation of exoplanet and exomoon transits
- Real-time light curve visualization
- Dynamic orbital diagram
- Adjustable parameters for star, planet, and moon properties
- Support for inclined moon orbits

## Usage

The primary way to use the Exomoon Transit Simulator is via the live web application linked above.

### Local Development or Offline Use

If you want to run the simulator locally (e.g., for development):

1.  Clone the repository:
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORYNAME.git
    cd YOUR_REPOSITORYNAME
    ```
2.  Install dependencies (preferably in a virtual environment):
    ```bash
    pip install numpy panel holoviews bokeh
    ```
3.  Run the dashboard:
    ```bash
    python exomoon_dashboard.py 
    ```
    (Note: The original entry point `python -m exomoon_simulator.main` should also work if Panel is installed and serving `exomoon_dashboard.py` correctly, but direct execution of the dashboard script is also common for Panel apps.)

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
