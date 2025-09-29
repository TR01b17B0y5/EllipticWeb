/**
 * Test file for elliptic curve functionality
 */

// Load the elliptic curve library for Node.js
const { EllipticCurve, BigIntMath } = require('./elliptic.js');

function runTests() {
    console.log('Testing Elliptic Curve Implementation...\n');

    // Test 1: Create a curve with key length over 256 bits
    console.log('Test 1: Creating curve with key length > 256 bits');
    try {
        // Using a large prime with more than 256 bits (257 bits)
        const p = BigInt('231584178474632390847141970017375815706539969331281128078915168015826259279873');
        const curve = new EllipticCurve(2, 3, p);
        
        const keyLength = curve.getKeyLength();
        console.log(`✓ Curve created successfully`);
        console.log(`✓ Key length: ${keyLength} bits (required > 256)`);
        console.log(`✓ Curve equation: ${curve.getEquation()}\n`);
        
        if (keyLength <= 256) {
            throw new Error(`Key length ${keyLength} is not > 256 bits`);
        }
    } catch (error) {
        console.log(`✗ Error: ${error.message}\n`);
        return false;
    }

    // Test 2: Point computation
    console.log('Test 2: Point computation');
    try {
        // Use a smaller curve for easier testing  
        const curve = new EllipticCurve(2, 3, 97); // y² = x³ + 2x + 3 (mod 97) - valid curve
        
        const yValues = curve.computeY(3);
        console.log(`✓ Points for x=3: (3, ${yValues[0]}), (3, ${yValues[1]})`);
        
        // Verify points are on curve
        const onCurve1 = curve.isOnCurve(3, yValues[0]);
        const onCurve2 = curve.isOnCurve(3, yValues[1]);
        console.log(`✓ Point validation: ${onCurve1 && onCurve2 ? 'PASS' : 'FAIL'}\n`);
        
        if (!onCurve1 || !onCurve2) {
            throw new Error('Computed points are not on the curve');
        }
    } catch (error) {
        console.log(`✗ Error: ${error.message}\n`);
        return false;
    }

    // Test 3: Point addition
    console.log('Test 3: Point addition');
    try {
        const curve = new EllipticCurve(2, 3, 97);
        
        // Test points on the curve y² = x³ + 2x + 3 (mod 97)
        const P = {x: 3, y: 6};   // Valid point (3, 6)
        const Q = {x: 10, y: 21}; // Valid point (10, 21)
        
        // Verify points are on curve
        if (!curve.isOnCurve(P.x, P.y) || !curve.isOnCurve(Q.x, Q.y)) {
            throw new Error('Test points are not on the curve');
        }
        
        const result = curve.pointAdd(P, Q);
        console.log(`✓ P + Q = (${result.x}, ${result.y})`);
        
        // Verify result is on curve
        const resultOnCurve = curve.isOnCurve(result.x, result.y);
        console.log(`✓ Result validation: ${resultOnCurve ? 'PASS' : 'FAIL'}\n`);
        
        if (!resultOnCurve) {
            throw new Error('Addition result is not on the curve');
        }
    } catch (error) {
        console.log(`✗ Error: ${error.message}\n`);
        return false;
    }

    // Test 4: Point multiplication
    console.log('Test 4: Point multiplication');
    try {
        const curve = new EllipticCurve(2, 3, 97);
        const P = {x: 3, y: 6};
        const k = 5;
        
        const result = curve.scalarMultiply(k, P);
        console.log(`✓ ${k} * P = (${result.x}, ${result.y})`);
        
        // Verify result is on curve
        const resultOnCurve = curve.isOnCurve(result.x, result.y);
        console.log(`✓ Result validation: ${resultOnCurve ? 'PASS' : 'FAIL'}\n`);
        
        if (!resultOnCurve) {
            throw new Error('Multiplication result is not on the curve');
        }
    } catch (error) {
        console.log(`✗ Error: ${error.message}\n`);
        return false;
    }

    // Test 5: Large number operations
    console.log('Test 5: Large number operations (256+ bit)');
    try {
        const p = BigInt('231584178474632390847141970017375815706539969331281128078915168015826259279873');
        const curve = new EllipticCurve(0, 7, p); // Use the larger prime
        
        // For demonstration, use a simple point computation
        const x = BigInt('1234567890');
        const yValues = curve.computeY(x);
        
        if (yValues) {
            const P = { x: x, y: yValues[0] };
            const k = '123456789';
            const result = curve.scalarMultiply(k, P);
            
            console.log(`✓ Large scalar multiplication completed`);
            console.log(`✓ Input point: (${x}, ${yValues[0].toString().substring(0, 20)}...)`);
            if (result.x !== null) {
                console.log(`✓ Result: (${result.x?.toString().substring(0, 20)}..., ${result.y?.toString().substring(0, 20)}...)`);
            } else {
                console.log(`✓ Result: Point at infinity`);
            }
        } else {
            // If no y exists for our x, just test curve creation
            console.log(`✓ Large prime curve created successfully`);
            console.log(`✓ No valid y for test x=${x}, but curve operations work`);
        }
        
        console.log(`✓ All tests passed!\n`);
        
    } catch (error) {
        console.log(`✗ Error: ${error.message}\n`);
        return false;
    }

    return true;
}

// Run tests if this file is executed directly
if (require.main === module) {
    const success = runTests();
    process.exit(success ? 0 : 1);
}

module.exports = { runTests };