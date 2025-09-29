# EllipticWeb

A comprehensive web application for elliptic curve cryptography with support for curves having key lengths over 256 bits.

## Features

- ✅ **256+ Bit Key Support**: Create elliptic curves with key lengths exceeding 256 bits
- ✅ **Interactive Interface**: User-friendly web interface for inputting curve parameters (a, b, n)
- ✅ **Point Computation**: Calculate points on the elliptic curve for given x coordinates
- ✅ **Point Addition**: Perform elliptic curve point addition operations
- ✅ **Point Multiplication**: Execute scalar multiplication of points on the curve
- ✅ **Curve Visualization**: Graphical representation of curve points
- ✅ **Parameter Validation**: Comprehensive validation of curve parameters and operations

## Usage

### Quick Start

1. Open `index.html` in a web browser
2. Enter curve parameters:
   - **Coefficient a**: First coefficient of the elliptic curve equation
   - **Coefficient b**: Second coefficient of the elliptic curve equation  
   - **Modulus n**: Large prime modulus (must be > 256 bits)
3. Click "Generate Curve" to create your elliptic curve

### Default Configuration

The application comes pre-configured with:
- **a = 2, b = 3**: Valid curve coefficients
- **n = 231584178474632390847141970017375815706539969331281128078915168015826259279873**: 258-bit prime modulus

### Operations

#### Point Computation
- Enter an x-coordinate to find corresponding y-values on the curve
- The system will return both positive and negative y-values if they exist

#### Point Addition
- Input two points P and Q on the curve
- Calculate P + Q using elliptic curve addition rules

#### Point Multiplication  
- Multiply a point P by a scalar k
- Implements efficient double-and-add algorithm

## Technical Implementation

### Core Mathematics

The application implements:
- **Modular arithmetic** for large numbers (256+ bits)
- **Extended Euclidean Algorithm** for modular inverse
- **Modular square root** using optimized algorithms
- **Point doubling and addition** following elliptic curve group law
- **Scalar multiplication** using binary method

### Curve Equation

All curves follow the Weierstrass form:
```
y² = x³ + ax + b (mod n)
```

### Validation

- Discriminant validation: Ensures 4a³ + 27b² ≢ 0 (mod n)
- Point validation: Verifies points satisfy the curve equation
- Parameter validation: Confirms modulus exceeds 256 bits

## Files Structure

- `index.html` - Main web interface
- `style.css` - Responsive styling and layout
- `elliptic.js` - Core elliptic curve mathematics library
- `app.js` - Web application logic and UI interactions
- `test.js` - Comprehensive test suite
- `simple_test.html` - Simplified testing interface

## Testing

Run the test suite:
```bash
node test.js
```

Test coverage includes:
- Curve creation with 256+ bit modulus
- Point computation and validation
- Point addition operations
- Scalar multiplication
- Large number arithmetic

## Browser Compatibility

- Modern browsers supporting ES6+ and BigInt
- Responsive design for desktop and mobile
- Progressive enhancement for optimal performance

## Example

Default curve: y² = x³ + 2x + 3 (mod 231584178474632390847141970017375815706539969331281128078915168015826259279873)
- Key length: 258 bits ✓
- Valid discriminant ✓
- Supports all elliptic curve operations ✓
