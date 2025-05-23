// Orbital diagram SVG generation

function createOrbitalDiagram(params) {
    const {
        starRadius,
        planetRadius,
        planetDistance,
        moonRadius,
        moonDistance,
        moonInitialPhase,
        moonOrbitalInclination,
        includeMoon,
        timeFraction
    } = params;
    
    // SVG viewport and scaling
    const viewSize = 500;
    const margin = 60;
    const scale = (viewSize - 2 * margin) / (4 * starRadius);
    
    // Center of viewport
    const cx = viewSize / 2;
    const cy = viewSize / 2;
    
    // Calculate positions
    const planetX = timeFraction * (2 * starRadius);
    const planetY = planetDistance;
    
    // Convert inclination to radians
    const inclinationRad = moonOrbitalInclination * Math.PI / 180;
    
    // Calculate moon position
    const moonAngle = 2 * Math.PI * moonInitialPhase;
    const moonRelX = moonDistance * Math.cos(moonAngle);
    const moonRelY = moonDistance * Math.sin(moonAngle);
    
    const moonX = planetX + moonRelX;
    const moonY = planetY + moonRelY * Math.cos(inclinationRad);
    const moonZ = moonRelY * Math.sin(inclinationRad);
    
    // Generate moon orbital ellipse points
    const orbitPoints = [];
    const numPoints = 100;
    for (let i = 0; i < numPoints; i++) {
        const angle = (i / (numPoints - 1)) * 2 * Math.PI;
        const orbitRelX = moonDistance * Math.cos(angle);
        const orbitRelY = moonDistance * Math.sin(angle);
        const orbitX = planetX + orbitRelX;
        const orbitY = planetY + orbitRelY * Math.cos(inclinationRad);
        orbitPoints.push({
            x: orbitX * scale + cx,
            y: orbitY * scale + cy
        });
    }
    
    // Create SVG
    let svg = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${viewSize} ${viewSize}">
        <!-- Background -->
        <rect width="${viewSize}" height="${viewSize}" fill="#f8f9fa"/>
        
        <!-- Coordinate system -->
        <line x1="${margin}" y1="${cy}" x2="${viewSize - margin}" y2="${cy}" 
              stroke="#ccc" stroke-width="1" stroke-dasharray="4"/>
        <line x1="${cx}" y1="${margin}" x2="${cx}" y2="${viewSize - margin}" 
              stroke="#ccc" stroke-width="1" stroke-dasharray="4"/>
        
        <!-- Star -->
        <circle cx="${cx}" cy="${cy}" r="${starRadius * scale}" 
                fill="#ffde00" stroke="#ff9900" stroke-width="2"/>
        
        <!-- Planet orbit line -->
        <line x1="${cx - 2*starRadius*scale}" y1="${cy + planetDistance*scale}" 
              x2="${cx + 2*starRadius*scale}" y2="${cy + planetDistance*scale}" 
              stroke="#666" stroke-width="1" stroke-dasharray="4"/>`;
    
    // Add moon orbit if included
    if (includeMoon) {
        let pathD = `M ${orbitPoints[0].x},${orbitPoints[0].y}`;
        for (let i = 1; i < orbitPoints.length; i++) {
            pathD += ` L ${orbitPoints[i].x},${orbitPoints[i].y}`;
        }
        pathD += ' Z';
        
        svg += `
        <!-- Moon orbit -->
        <path d="${pathD}" fill="none" stroke="#999" 
              stroke-width="1" stroke-dasharray="4"/>`;
    }
    
    // Add planet
    svg += `
        <!-- Planet -->
        <circle cx="${cx + planetX*scale}" cy="${cy + planetY*scale}" 
                r="${planetRadius * scale}" fill="#666"/>`;
    
    // Add moon if included
    if (includeMoon) {
        // Adjust moon size based on z-position (perspective)
        const zScale = 1.0 - 0.2 * (moonZ / moonDistance);
        const moonApparentRadius = moonRadius * scale * zScale;
        
        svg += `
        <!-- Moon -->
        <circle cx="${cx + moonX*scale}" cy="${cy + moonY*scale}" 
                r="${moonApparentRadius}" fill="#999" opacity="1.0"/>`;
    }
    
    svg += '</svg>';
    return svg;
}

function updateOrbitalDiagram(params) {
    const diagramContainer = document.getElementById('orbital-diagram');
    diagramContainer.innerHTML = createOrbitalDiagram(params);
}