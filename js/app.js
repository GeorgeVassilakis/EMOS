// Main application logic

// Get current parameters from UI
function getCurrentParameters() {
    return {
        starRadius: parseFloat(document.getElementById('star-radius').value),
        starIntensity: parseFloat(document.getElementById('star-intensity').value),
        planetRadius: parseFloat(document.getElementById('planet-radius').value),
        planetDistance: parseFloat(document.getElementById('planet-distance').value),
        transitDuration: parseFloat(document.getElementById('transit-duration').value),
        moonRadius: parseFloat(document.getElementById('moon-radius').value),
        moonDistance: parseFloat(document.getElementById('moon-distance').value),
        moonOrbitalPeriod: parseFloat(document.getElementById('moon-orbital-period').value),
        moonInitialPhase: parseFloat(document.getElementById('moon-initial-phase').value),
        moonOrbitalInclination: parseFloat(document.getElementById('moon-orbital-inclination').value),
        includeMoon: document.getElementById('include-moon').checked,
        timeFraction: parseFloat(document.getElementById('time-slider').value)
    };
}

// Update all visualizations
function updateVisualizations() {
    const params = getCurrentParameters();
    updateLightCurve(params);
    updateOrbitalDiagram(params);
}

// Switch parameter tabs
function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    event.target.classList.add('active');
}

// Switch main tabs
function switchMainTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.main-tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.main-tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    event.target.classList.add('active');
}

// Toggle sidebar (mobile)
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('open');
}

// Reset all parameters
function resetParameters() {
    // Star parameters
    document.getElementById('star-radius').value = DEFAULT_VALUES.starRadius;
    document.getElementById('star-intensity').value = DEFAULT_VALUES.starIntensity;
    
    // Planet parameters
    document.getElementById('planet-radius').value = DEFAULT_VALUES.planetRadius;
    document.getElementById('planet-distance').value = DEFAULT_VALUES.planetDistance;
    document.getElementById('transit-duration').value = DEFAULT_VALUES.transitDuration;
    
    // Moon parameters
    document.getElementById('moon-radius').value = DEFAULT_VALUES.moonRadius;
    document.getElementById('moon-distance').value = DEFAULT_VALUES.moonDistance;
    document.getElementById('moon-orbital-period').value = DEFAULT_VALUES.moonOrbitalPeriod;
    document.getElementById('moon-initial-phase').value = DEFAULT_VALUES.moonInitialPhase;
    document.getElementById('moon-orbital-inclination').value = DEFAULT_VALUES.moonOrbitalInclination;
    document.getElementById('include-moon').checked = DEFAULT_VALUES.includeMoon;
    
    // Time slider
    document.getElementById('time-slider').value = DEFAULT_VALUES.time;
    
    // Update all value displays
    updateAllValueDisplays();
    
    // Update visualizations
    updateVisualizations();
}

// Update value display for a slider
function updateValueDisplay(sliderId, valueId, decimals = 2, suffix = '') {
    const slider = document.getElementById(sliderId);
    const valueDisplay = document.getElementById(valueId);
    if (valueDisplay) {
        valueDisplay.textContent = parseFloat(slider.value).toFixed(decimals) + suffix;
    }
}

// Update all value displays
function updateAllValueDisplays() {
    updateValueDisplay('star-radius', 'star-radius-value', 1);
    updateValueDisplay('star-intensity', 'star-intensity-value', 1);
    updateValueDisplay('planet-radius', 'planet-radius-value', 2);
    updateValueDisplay('planet-distance', 'planet-distance-value', 2);
    updateValueDisplay('transit-duration', 'transit-duration-value', 0);
    updateValueDisplay('moon-radius', 'moon-radius-value', 2);
    updateValueDisplay('moon-distance', 'moon-distance-value', 2);
    updateValueDisplay('moon-orbital-period', 'moon-orbital-period-value', 0);
    updateValueDisplay('moon-initial-phase', 'moon-initial-phase-value', 2);
    updateValueDisplay('moon-orbital-inclination', 'moon-orbital-inclination-value', 0, '');
    updateValueDisplay('time-slider', 'time-value', 1);
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Set up slider event listeners
    const sliders = [
        'star-radius', 'star-intensity', 'planet-radius', 'planet-distance',
        'transit-duration', 'moon-radius', 'moon-distance', 'moon-orbital-period',
        'moon-initial-phase', 'moon-orbital-inclination'
    ];
    
    sliders.forEach(sliderId => {
        const slider = document.getElementById(sliderId);
        slider.addEventListener('input', function() {
            // Determine decimals and suffix based on slider
            let decimals = 2;
            let suffix = '';
            
            if (sliderId === 'transit-duration' || sliderId === 'moon-orbital-period') {
                decimals = 0;
            } else if (sliderId === 'moon-orbital-inclination') {
                decimals = 0;
            } else if (sliderId === 'star-radius' || sliderId === 'star-intensity') {
                decimals = 1;
            }
            
            updateValueDisplay(sliderId, sliderId + '-value', decimals, suffix);
            updateVisualizations();
        });
    });
    
    // Special handling for time slider
    const timeSlider = document.getElementById('time-slider');
    timeSlider.addEventListener('input', function() {
        updateValueDisplay('time-slider', 'time-value', 1);
        // Only update orbital diagram for time changes (more efficient)
        const params = getCurrentParameters();
        updateOrbitalDiagram(params);
    });
    
    // Set up checkbox listener
    document.getElementById('include-moon').addEventListener('change', updateVisualizations);
    
    // Initialize value displays
    updateAllValueDisplays();
    
    // Initialize visualizations
    initializeLightCurve();
    updateVisualizations();
    
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(event) {
        const sidebar = document.getElementById('sidebar');
        const menuToggle = document.querySelector('.menu-toggle');
        
        if (window.innerWidth <= 768 && 
            sidebar.classList.contains('open') &&
            !sidebar.contains(event.target) &&
            !menuToggle.contains(event.target)) {
            sidebar.classList.remove('open');
        }
    });
});