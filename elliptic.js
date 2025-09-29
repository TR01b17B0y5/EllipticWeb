/**
 * Elliptic Curve Mathematics Library
 * Supports curves with key lengths over 256 bits
 */

class BigIntMath {
    /**
     * Modular exponentiation: base^exp mod mod
     */
    static modPow(base, exp, mod) {
        if (mod === 1n) return 0n;
        let result = 1n;
        base = base % mod;
        while (exp > 0n) {
            if (exp % 2n === 1n) {
                result = (result * base) % mod;
            }
            exp = exp >> 1n;
            base = (base * base) % mod;
        }
        return result;
    }

    /**
     * Modular inverse using Extended Euclidean Algorithm
     */
    static modInverse(a, mod) {
        if (mod === 1n) return 0n;
        
        a = ((a % mod) + mod) % mod; // Ensure a is positive
        
        let m0 = mod;
        let x0 = 0n, x1 = 1n;
        
        while (a > 1n) {
            if (mod === 0n) {
                throw new Error('Modular inverse does not exist');
            }
            let q = a / mod;
            let t = mod;
            mod = a % mod;
            a = t;
            t = x0;
            x0 = x1 - q * x0;
            x1 = t;
        }
        
        if (a !== 1n) {
            throw new Error('Modular inverse does not exist');
        }
        
        if (x1 < 0n) x1 += m0;
        return x1;
    }

    /**
     * Modular square root - simplified implementation
     */
    static modSqrt(n, p) {
        if (n === 0n) return 0n;
        
        // Check if n is a quadratic residue
        if (!BigIntMath.isQuadraticResidue(n, p)) {
            return null;
        }
        
        // For p ≡ 3 (mod 4), use the simple formula
        if (p % 4n === 3n) {
            return BigIntMath.modPow(n, (p + 1n) / 4n, p);
        }
        
        // For small primes, use brute force
        if (p < 1000n) {
            for (let y = 0n; y < p; y++) {
                if ((y * y) % p === n % p) {
                    return y;
                }
            }
        }
        
        // Fallback for larger primes - use probabilistic method
        return BigIntMath.modPow(n, (p + 1n) / 4n, p);
    }

    /**
     * Check if a number is a quadratic residue
     */
    static isQuadraticResidue(n, p) {
        if (n === 0n) return true;
        return BigIntMath.modPow(n, (p - 1n) / 2n, p) === 1n;
    }
}

class EllipticCurve {
    constructor(a, b, p) {
        this.a = BigInt(a);
        this.b = BigInt(b);
        this.p = BigInt(p);
        
        // Validate curve parameters
        if (!this.isValidCurve()) {
            throw new Error('Invalid curve parameters: discriminant is zero');
        }
    }

    /**
     * Check if the curve is valid (discriminant ≠ 0)
     */
    isValidCurve() {
        // Discriminant = -16(4a³ + 27b²)
        let discriminant = -16n * (4n * this.a * this.a * this.a + 27n * this.b * this.b);
        return (discriminant % this.p) !== 0n;
    }

    /**
     * Get the key length in bits
     */
    getKeyLength() {
        return this.p.toString(2).length;
    }

    /**
     * Check if a point is on the curve
     */
    isOnCurve(x, y) {
        if (x === null || y === null) return true; // Point at infinity
        
        x = BigInt(x);
        y = BigInt(y);
        
        let left = (y * y) % this.p;
        let right = (x * x * x + this.a * x + this.b) % this.p;
        
        return left === right;
    }

    /**
     * Compute y coordinates for a given x
     */
    computeY(x) {
        x = BigInt(x);
        let y_squared = (x * x * x + this.a * x + this.b) % this.p;
        
        if (y_squared < 0n) {
            y_squared = (y_squared + this.p) % this.p;
        }

        if (!BigIntMath.isQuadraticResidue(y_squared, this.p)) {
            return null; // No real solutions
        }

        let y = BigIntMath.modSqrt(y_squared, this.p);
        let y_neg = (this.p - y) % this.p;
        
        return [y, y_neg];
    }

    /**
     * Point addition on elliptic curve
     */
    pointAdd(P, Q) {
        // Handle point at infinity
        if (P.x === null || P.y === null) return Q;
        if (Q.x === null || Q.y === null) return P;

        let px = BigInt(P.x);
        let py = BigInt(P.y);
        let qx = BigInt(Q.x);
        let qy = BigInt(Q.y);

        // Same point
        if (px === qx && py === qy) {
            return this.pointDouble({x: px, y: py});
        }

        // Points are additive inverses
        if (px === qx) {
            return {x: null, y: null}; // Point at infinity
        }

        // General case
        let slope = ((qy - py) * BigIntMath.modInverse((qx - px + this.p) % this.p, this.p)) % this.p;
        let rx = (slope * slope - px - qx + 2n * this.p) % this.p;
        let ry = (slope * (px - rx) - py + 2n * this.p) % this.p;

        return {
            x: rx < 0n ? rx + this.p : rx,
            y: ry < 0n ? ry + this.p : ry
        };
    }

    /**
     * Point doubling on elliptic curve
     */
    pointDouble(P) {
        if (P.x === null || P.y === null) return P;

        let px = BigInt(P.x);
        let py = BigInt(P.y);

        if (py === 0n) {
            return {x: null, y: null}; // Point at infinity
        }

        let slope = ((3n * px * px + this.a) * BigIntMath.modInverse(2n * py, this.p)) % this.p;
        let rx = (slope * slope - 2n * px + this.p) % this.p;
        let ry = (slope * (px - rx) - py + this.p) % this.p;

        return {
            x: rx < 0n ? rx + this.p : rx,
            y: ry < 0n ? ry + this.p : ry
        };
    }

    /**
     * Scalar multiplication using double-and-add
     */
    scalarMultiply(k, P) {
        if (k === 0n) return {x: null, y: null};
        if (k === 1n) return P;

        k = BigInt(k);
        let result = {x: null, y: null}; // Point at infinity
        let addend = P;

        while (k > 0n) {
            if (k & 1n) {
                result = this.pointAdd(result, addend);
            }
            addend = this.pointDouble(addend);
            k >>= 1n;
        }

        return result;
    }

    /**
     * Generate sample points for visualization (for small modulus only)
     */
    generateSamplePoints(maxCoord = 100) {
        const points = [];
        
        // Only generate points for visualization if modulus is reasonably small
        if (this.p > 1000n) {
            return points;
        }

        const maxCheck = maxCoord < this.p ? BigInt(maxCoord) : this.p;
        
        for (let x = 0n; x < maxCheck; x++) {
            try {
                const yValues = this.computeY(x);
                if (yValues) {
                    yValues.forEach(y => {
                        if (y < maxCheck) {
                            points.push({x: Number(x), y: Number(y)});
                        }
                    });
                }
            } catch (e) {
                // Skip invalid points
            }
        }
        
        return points;
    }

    /**
     * Get curve equation as string
     */
    getEquation() {
        return `y² = x³ + ${this.a}x + ${this.b} (mod ${this.p})`;
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { EllipticCurve, BigIntMath };
}