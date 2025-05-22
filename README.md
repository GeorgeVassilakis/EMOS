# Exomoon Transit Simulator

Interactive web simulator for visualizing exoplanet-exomoon transit light curves.

**[Live Demo](https://georgevassilakis.github.io/EMOS/)**

## Usage

1. Adjust star, planet, and moon parameters using the sliders
2. View real-time light curve updates in the Light Curve tab
3. See the orbital configuration in the Orbital View tab
4. Use the time slider to animate the transit

## Running Locally

Open `index.html` in a browser, or run a local server:

```bash
python -m http.server 8000
```

## Project Structure

```
├── index.html          # Main HTML structure
├── styles.css          # CSS styling
├── js/
│   ├── app.js         # Main application logic
│   ├── config.js      # Configuration and defaults
│   ├── physics.js     # Transit physics calculations
│   ├── lightcurve.js  # Light curve visualization
│   └── orbital.js     # Orbital diagram generation
└── README.md          # This file
```

## License

MIT License - see [LICENSE](LICENSE) file for details.