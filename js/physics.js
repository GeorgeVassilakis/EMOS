// Physics calculations for exomoon transit simulation

function transitAreaVectorized(x, y, radius, starRadius) {
    // Calculate overlap area between star and transiting body
    const area = new Array(x.length);
    
    for (let i = 0; i < x.length; i++) {
        const distance = Math.sqrt(x[i] * x[i] + y[i] * y[i]);
        
        // Case 1: No overlap
        if (distance >= (starRadius + radius)) {
            area[i] = 0;
        }
        // Case 2: Complete overlap (transiting body entirely within star)
        else if (distance <= (starRadius - radius)) {
            area[i] = Math.PI * radius * radius;
        }
        // Case 3: Partial overlap
        else {
            const r = radius;
            const R = starRadius;
            const d = distance;
            
            const argument = (d * d + r * r - R * R) / (2 * d * r);
            const argumentClipped = Math.max(-1, Math.min(1, argument));
            const phi = 2 * Math.acos(argumentClipped);
            
            const theta = 2 * Math.acos((d * d + R * R - r * r) / (2 * d * R));
            const area1 = 0.5 * r * r * (phi - Math.sin(phi));
            const area2 = 0.5 * R * R * (theta - Math.sin(theta));
            area[i] = area1 + area2;
        }
    }
    
    return area;
}

function circleOverlapVectorized(x1, y1, r1, x2, y2, r2) {
    // Calculate overlap area between two circles
    const area = new Array(x1.length);
    
    for (let i = 0; i < x1.length; i++) {
        const dx = x1[i] - x2[i];
        const dy = y1[i] - y2[i];
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        // Case 1: No overlap
        if (distance >= (r1 + r2)) {
            area[i] = 0;
        }
        // Case 2: Complete overlap
        else if (distance <= Math.abs(r1 - r2)) {
            area[i] = Math.PI * Math.min(r1, r2) * Math.min(r1, r2);
        }
        // Case 3: Partial overlap
        else {
            const d = distance;
            const alpha = Math.acos((d * d + r1 * r1 - r2 * r2) / (2 * d * r1));
            const beta = Math.acos((d * d + r2 * r2 - r1 * r1) / (2 * d * r2));
            const area1 = r1 * r1 * alpha;
            const area2 = r2 * r2 * beta;
            const area3 = 0.5 * Math.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2));
            area[i] = area1 + area2 - area3;
        }
    }
    
    return area;
}

function simulateLightCurve(params) {
    const {
        starRadius,
        starIntensity,
        planetRadius,
        planetDistance,
        transitDuration,
        moonRadius,
        moonDistance,
        moonOrbitalPeriod,
        moonInitialPhase,
        moonOrbitalInclination,
        includeMoon,
        numPoints = NUM_POINTS
    } = params;
    
    // Add padding before and after transit
    const totalDuration = transitDuration * (1 + 2 * PADDING_FACTOR);
    const time = [];
    const flux = [];
    
    // Generate time array
    for (let i = 0; i < numPoints; i++) {
        const t = -totalDuration/2 + (i / (numPoints - 1)) * totalDuration;
        time.push(t);
        flux.push(starIntensity);
    }
    
    // Find indices within transit duration
    const transitIndices = [];
    const transitTime = [];
    for (let i = 0; i < time.length; i++) {
        if (time[i] >= -transitDuration/2 && time[i] <= transitDuration/2) {
            transitIndices.push(i);
            transitTime.push(time[i]);
        }
    }
    
    if (transitIndices.length === 0) return { time, flux };
    
    // Convert inclination to radians
    const inclinationRad = moonOrbitalInclination * Math.PI / 180;
    
    // Calculate planet position during transit
    const planetX = transitTime.map(t => t * (2 * starRadius / transitDuration));
    const planetY = transitTime.map(() => planetDistance);
    
    // Calculate moon position with inclination
    const moonX = [];
    const moonY = [];
    const moonZ = [];
    
    for (let i = 0; i < transitTime.length; i++) {
        const angle = 2 * Math.PI * ((transitTime[i] / moonOrbitalPeriod) + moonInitialPhase);
        const moonRelX = moonDistance * Math.cos(angle);
        const moonRelY = moonDistance * Math.sin(angle);
        
        moonX.push(planetX[i] + moonRelX);
        moonY.push(planetY[i] + moonRelY * Math.cos(inclinationRad));
        moonZ.push(moonRelY * Math.sin(inclinationRad));
    }
    
    // Calculate overlap areas
    const starPlanetOverlap = transitAreaVectorized(planetX, planetY, planetRadius, starRadius);
    
    let starMoonOverlap = new Array(transitTime.length).fill(0);
    let planetMoonOverlap = new Array(transitTime.length).fill(0);
    
    if (includeMoon) {
        // Only consider moon when it's in front of star (z >= 0)
        for (let i = 0; i < transitTime.length; i++) {
            if (moonZ[i] >= 0) {
                const moonOverlap = transitAreaVectorized([moonX[i]], [moonY[i]], moonRadius, starRadius);
                starMoonOverlap[i] = moonOverlap[0];
                
                const pmOverlap = circleOverlapVectorized(
                    [planetX[i]], [planetY[i]], planetRadius,
                    [moonX[i]], [moonY[i]], moonRadius
                );
                planetMoonOverlap[i] = pmOverlap[0];
            }
        }
    }
    
    // Apply transit effects
    for (let i = 0; i < transitIndices.length; i++) {
        const idx = transitIndices[i];
        const totalOverlap = starPlanetOverlap[i] + starMoonOverlap[i] - planetMoonOverlap[i];
        flux[idx] -= (totalOverlap / (Math.PI * starRadius * starRadius)) * starIntensity;
    }
    
    return { time, flux };
}