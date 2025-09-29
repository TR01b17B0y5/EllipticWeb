/**
 * Main Application Logic for Elliptic Curve Calculator
 */

class EllipticCurveApp {
    constructor() {
        this.curve = null;
        this.initializeEventListeners();
        this.initializeDefaultCurve();
    }

    initializeEventListeners() {
        // Curve generation
        document.getElementById('generate-curve').addEventListener('click', () => {
            this.generateCurve();
        });

        // Point computation
        document.getElementById('compute-point').addEventListener('click', () => {
            this.computePoint();
        });

        // Point addition
        document.getElementById('add-points').addEventListener('click', () => {
            this.addPoints();
        });

        // Point multiplication
        document.getElementById('multiply-point').addEventListener('click', () => {
            this.multiplyPoint();
        });

        // Plot update
        document.getElementById('update-plot').addEventListener('click', () => {
            this.updatePlot();
        });

        // Enter key support
        document.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const activeElement = document.activeElement;
                if (activeElement.tagName === 'INPUT') {
                    // Find the relevant button and click it
                    const section = activeElement.closest('.input-section, .operation-group');
                    if (section) {
                        const button = section.querySelector('button');
                        if (button) button.click();
                    }
                }
            }
        });
    }

    initializeDefaultCurve() {
        // Initialize with a large prime over 256 bits (secp256k1 field)
        this.generateCurve();
    }

    generateCurve() {
        try {
            const a = document.getElementById('coeff-a').value.trim();
            const b = document.getElementById('coeff-b').value.trim();
            const n = document.getElementById('modulus-n').value.trim();

            if (!a || !b || !n) {
                this.showError('Please fill in all curve parameters');
                return;
            }

            // Validate that n is a large number (over 256 bits)
            const nBigInt = BigInt(n);
            const keyLength = nBigInt.toString(2).length;
            
            if (keyLength <= 256) {
                this.showError(`Modulus must have more than 256 bits. Current: ${keyLength} bits`);
                return;
            }

            this.curve = new EllipticCurve(a, b, n);
            
            // Update UI
            document.getElementById('key-length').textContent = `Key length: ${keyLength} bits`;
            document.getElementById('curve-equation').textContent = `Current curve: ${this.curve.getEquation()}`;
            
            this.showSuccess('Curve generated successfully!');
            this.updatePlot();
            
        } catch (error) {
            this.showError(`Error generating curve: ${error.message}`);
        }
    }

    computePoint() {
        if (!this.curve) {
            this.showError('Please generate a curve first');
            return;
        }

        try {
            const x = document.getElementById('x-coord').value.trim();
            
            if (!x) {
                this.showError('Please enter an x coordinate');
                return;
            }

            const yValues = this.curve.computeY(x);
            const resultDiv = document.getElementById('point-result');
            
            if (yValues === null) {
                resultDiv.className = 'error';
                resultDiv.textContent = `No points exist on the curve for x = ${x}`;
            } else {
                resultDiv.className = 'success';
                resultDiv.innerHTML = `
                    <strong>Points on curve for x = ${x}:</strong><br>
                    Point 1: (${x}, ${yValues[0]})<br>
                    Point 2: (${x}, ${yValues[1]})
                `;
            }
            
        } catch (error) {
            this.showError(`Error computing point: ${error.message}`);
        }
    }

    addPoints() {
        if (!this.curve) {
            this.showError('Please generate a curve first');
            return;
        }

        try {
            const px = document.getElementById('px').value.trim();
            const py = document.getElementById('py').value.trim();
            const qx = document.getElementById('qx').value.trim();
            const qy = document.getElementById('qy').value.trim();

            if (!px || !py || !qx || !qy) {
                this.showError('Please enter all point coordinates');
                return;
            }

            const P = { x: px, y: py };
            const Q = { x: qx, y: qy };

            // Validate points are on curve
            if (!this.curve.isOnCurve(P.x, P.y)) {
                this.showError(`Point P(${px}, ${py}) is not on the curve`);
                return;
            }

            if (!this.curve.isOnCurve(Q.x, Q.y)) {
                this.showError(`Point Q(${qx}, ${qy}) is not on the curve`);
                return;
            }

            const result = this.curve.pointAdd(P, Q);
            const resultDiv = document.getElementById('addition-result');
            
            if (result.x === null) {
                resultDiv.className = 'success';
                resultDiv.innerHTML = `
                    <strong>P + Q = Point at infinity (O)</strong><br>
                    The points are additive inverses.
                `;
            } else {
                resultDiv.className = 'success';
                resultDiv.innerHTML = `
                    <strong>P + Q = (${result.x}, ${result.y})</strong><br>
                    Point P: (${px}, ${py})<br>
                    Point Q: (${qx}, ${qy})<br>
                    Result: (${result.x}, ${result.y})
                `;
            }

        } catch (error) {
            this.showError(`Error adding points: ${error.message}`);
        }
    }

    multiplyPoint() {
        if (!this.curve) {
            this.showError('Please generate a curve first');
            return;
        }

        try {
            const px = document.getElementById('mult-px').value.trim();
            const py = document.getElementById('mult-py').value.trim();
            const k = document.getElementById('scalar').value.trim();

            if (!px || !py || !k) {
                this.showError('Please enter point coordinates and scalar');
                return;
            }

            const P = { x: px, y: py };

            // Validate point is on curve
            if (!this.curve.isOnCurve(P.x, P.y)) {
                this.showError(`Point P(${px}, ${py}) is not on the curve`);
                return;
            }

            const result = this.curve.scalarMultiply(k, P);
            const resultDiv = document.getElementById('multiplication-result');
            
            if (result.x === null) {
                resultDiv.className = 'success';
                resultDiv.innerHTML = `
                    <strong>${k} * P = Point at infinity (O)</strong><br>
                    Point P: (${px}, ${py})<br>
                    Scalar k: ${k}
                `;
            } else {
                resultDiv.className = 'success';
                resultDiv.innerHTML = `
                    <strong>${k} * P = (${result.x}, ${result.y})</strong><br>
                    Point P: (${px}, ${py})<br>
                    Scalar k: ${k}<br>
                    Result: (${result.x}, ${result.y})
                `;
            }

        } catch (error) {
            this.showError(`Error multiplying point: ${error.message}`);
        }
    }

    updatePlot() {
        if (!this.curve) {
            // Show empty plot if Plotly is available
            if (typeof Plotly !== 'undefined') {
                Plotly.newPlot('curve-plot', [], {
                    title: 'Generate a curve to see visualization',
                    xaxis: { title: 'x' },
                    yaxis: { title: 'y' }
                });
            } else {
                document.getElementById('curve-plot').innerHTML = '<p style="text-align: center; padding: 50px;">Plotly.js not loaded. Visualization unavailable.</p>';
            }
            return;
        }

        try {
            const range = parseInt(document.getElementById('plot-range').value) || 10;
            
            // For large modulus, we'll show a theoretical curve
            if (this.curve.p > 1000n) {
                this.plotTheoreticalCurve(range);
            } else {
                this.plotActualPoints(range);
            }
            
        } catch (error) {
            this.showError(`Error updating plot: ${error.message}`);
        }
    }

    plotTheoreticalCurve(range) {
        // Check if Plotly is available
        if (typeof Plotly === 'undefined') {
            document.getElementById('curve-plot').innerHTML = '<p style="text-align: center; padding: 50px;">Plotly.js not loaded. Install Plotly.js to see curve visualization.</p>';
            return;
        }

        // Generate theoretical curve points for visualization
        const points = [];
        const step = 0.1;
        
        for (let x = -range; x <= range; x += step) {
            // Calculate y² = x³ + ax + b (without modular arithmetic for visualization)
            const a = Number(this.curve.a);
            const b = Number(this.curve.b);
            const y_squared = x * x * x + a * x + b;
            
            if (y_squared >= 0) {
                const y = Math.sqrt(y_squared);
                points.push({ x: x, y: y });
                if (y !== 0) {
                    points.push({ x: x, y: -y });
                }
            }
        }

        const trace = {
            x: points.map(p => p.x),
            y: points.map(p => p.y),
            mode: 'markers',
            type: 'scatter',
            name: 'Elliptic Curve Points',
            marker: {
                color: 'blue',
                size: 3
            }
        };

        const layout = {
            title: `Elliptic Curve Visualization (Theoretical)<br>y² = x³ + ${this.curve.a}x + ${this.curve.b}`,
            xaxis: { 
                title: 'x',
                range: [-range, range]
            },
            yaxis: { 
                title: 'y',
                range: [-range, range]
            },
            showlegend: false,
            annotations: [{
                text: `Note: This is a theoretical visualization.<br>Actual curve uses modular arithmetic with p = ${this.curve.p}`,
                showarrow: false,
                x: 0.5,
                y: 0.95,
                xref: 'paper',
                yref: 'paper',
                font: { size: 10 },
                bgcolor: 'rgba(255, 255, 255, 0.8)'
            }]
        };

        Plotly.newPlot('curve-plot', [trace], layout);
    }

    plotActualPoints(range) {
        // Check if Plotly is available
        if (typeof Plotly === 'undefined') {
            document.getElementById('curve-plot').innerHTML = '<p style="text-align: center; padding: 50px;">Plotly.js not loaded. Install Plotly.js to see curve visualization.</p>';
            return;
        }

        const points = this.curve.generateSamplePoints(range);
        
        if (points.length === 0) {
            this.plotTheoreticalCurve(range);
            return;
        }

        const trace = {
            x: points.map(p => p.x),
            y: points.map(p => p.y),
            mode: 'markers',
            type: 'scatter',
            name: 'Curve Points',
            marker: {
                color: 'red',
                size: 8
            }
        };

        const layout = {
            title: `Elliptic Curve Points (mod ${this.curve.p})<br>y² = x³ + ${this.curve.a}x + ${this.curve.b}`,
            xaxis: { 
                title: 'x',
                range: [0, range]
            },
            yaxis: { 
                title: 'y',
                range: [0, range]
            },
            showlegend: false
        };

        Plotly.newPlot('curve-plot', [trace], layout);
    }

    showError(message) {
        console.error(message);
        // Could implement a toast notification system here
        alert(`Error: ${message}`);
    }

    showSuccess(message) {
        console.log(message);
        // Could implement a toast notification system here
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EllipticCurveApp();
});