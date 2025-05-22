// Light curve plotting using Chart.js

let lightCurveChart = null;

function initializeLightCurve() {
    const ctx = document.getElementById('light-curve-chart').getContext('2d');
    
    lightCurveChart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Normalized Flux',
                data: [],
                borderColor: '#1f77b4',
                backgroundColor: 'rgba(31, 119, 180, 0.1)',
                borderWidth: 2,
                pointRadius: 0,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Exomoon Transit Light Curve',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        title: function(context) {
                            return `Time: ${context[0].parsed.x.toFixed(2)} hours`;
                        },
                        label: function(context) {
                            return `Flux: ${context.parsed.y.toFixed(6)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: 'Time (hours)',
                        font: {
                            size: 14
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Normalized Flux',
                        font: {
                            size: 14
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                }
            }
        }
    });
}

function updateLightCurve(params) {
    if (!lightCurveChart) {
        initializeLightCurve();
    }
    
    // Simulate light curve
    const { time, flux } = simulateLightCurve(params);
    
    // Prepare data for Chart.js
    const data = time.map((t, i) => ({ x: t, y: flux[i] }));
    
    // Update chart data
    lightCurveChart.data.datasets[0].data = data;
    
    // Update title based on moon inclusion
    lightCurveChart.options.plugins.title.text = params.includeMoon ? 
        'Exomoon Transit Light Curve' : 'Planet Transit Light Curve';
    
    // Calculate y-axis range
    const minFlux = Math.min(...flux);
    const maxFlux = Math.max(...flux);
    const fluxRange = maxFlux - minFlux;
    const yPadding = fluxRange * 0.1;
    
    lightCurveChart.options.scales.y.min = minFlux - yPadding;
    lightCurveChart.options.scales.y.max = maxFlux + yPadding;
    
    lightCurveChart.update();
}