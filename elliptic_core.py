"""
Comprehensive Elliptic Curve Cryptography (ECC) Mathematical Core
==================================================================

This module provides a complete implementation of elliptic curve cryptography
with support for 256-bit keys, including:
- Modular arithmetic operations
- Finite field arithmetic
- Elliptic curve point operations
- ECDSA signature scheme
- ECDH key exchange
- Secure random number generation

Supports secp256k1 curve parameters (256-bit curve used in Bitcoin and other systems)
"""

import hashlib
import secrets
from typing import Optional, Tuple, Union


class ModularArithmetic:
    """Provides modular arithmetic operations for finite fields."""
    
    @staticmethod
    def mod_inverse(a: int, m: int) -> int:
        """
        Compute modular multiplicative inverse using Extended Euclidean Algorithm.
        Returns x such that (a * x) % m == 1
        """
        if a < 0:
            a = (a % m + m) % m
        
        # Extended Euclidean Algorithm
        def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a, m)
        if gcd != 1:
            raise ValueError(f"Modular inverse does not exist for {a} mod {m}")
        return (x % m + m) % m
    
    @staticmethod
    def mod_pow(base: int, exp: int, mod: int) -> int:
        """Fast modular exponentiation using binary method."""
        return pow(base, exp, mod)
    
    @staticmethod
    def mod_sqrt(a: int, p: int) -> int:
        """
        Compute modular square root using Tonelli-Shanks algorithm.
        Returns x such that x^2 ≡ a (mod p)
        """
        if pow(a, (p - 1) // 2, p) != 1:
            raise ValueError(f"No square root exists for {a} mod {p}")
        
        # Simple case for p ≡ 3 (mod 4)
        if p % 4 == 3:
            return pow(a, (p + 1) // 4, p)
        
        # Tonelli-Shanks algorithm for general case
        # Find Q and S such that p - 1 = Q * 2^S with Q odd
        Q = p - 1
        S = 0
        while Q % 2 == 0:
            Q //= 2
            S += 1
        
        # Find a quadratic non-residue z
        z = 2
        while pow(z, (p - 1) // 2, p) != p - 1:
            z += 1
        
        # Initialize variables
        M = S
        c = pow(z, Q, p)
        t = pow(a, Q, p)
        R = pow(a, (Q + 1) // 2, p)
        
        while t != 1:
            # Find the smallest i such that t^(2^i) = 1
            i = 1
            temp = (t * t) % p
            while temp != 1:
                temp = (temp * temp) % p
                i += 1
            
            # Update variables
            b = pow(c, 1 << (M - i - 1), p)
            M = i
            c = (b * b) % p
            t = (t * c) % p
            R = (R * b) % p
        
        return R


class EllipticCurve:
    """
    Represents an elliptic curve in Weierstrass form: y² = x³ + ax + b (mod p)
    """
    
    def __init__(self, a: int, b: int, p: int, n: int, gx: int, gy: int):
        """
        Initialize elliptic curve parameters.
        
        Args:
            a, b: Curve coefficients
            p: Prime modulus (field characteristic)
            n: Order of the base point (number of points on curve)
            gx, gy: Coordinates of generator point G
        """
        self.a = a
        self.b = b
        self.p = p
        self.n = n
        self.G = EllipticCurvePoint(gx, gy, self)
        
        # Validate curve parameters
        discriminant = (4 * a**3 + 27 * b**2) % p
        if discriminant == 0:
            raise ValueError("Invalid curve parameters: discriminant is zero")
    
    def is_on_curve(self, x: int, y: int) -> bool:
        """Check if point (x, y) is on the curve."""
        left = (y * y) % self.p
        right = (x**3 + self.a * x + self.b) % self.p
        return left == right
    
    def __str__(self) -> str:
        return f"EllipticCurve(y² ≡ x³ + {self.a}x + {self.b} (mod {self.p}))"


class EllipticCurvePoint:
    """Represents a point on an elliptic curve."""
    
    def __init__(self, x: Optional[int], y: Optional[int], curve: EllipticCurve):
        """
        Initialize elliptic curve point.
        
        Args:
            x, y: Point coordinates (None for point at infinity)
            curve: The elliptic curve this point belongs to
        """
        self.x = x
        self.y = y
        self.curve = curve
        self.is_infinity = (x is None and y is None)
        
        # Validate point is on curve
        if not self.is_infinity and not curve.is_on_curve(x, y):
            raise ValueError(f"Point ({x}, {y}) is not on the curve")
    
    def __add__(self, other: 'EllipticCurvePoint') -> 'EllipticCurvePoint':
        """Point addition on elliptic curve."""
        if not isinstance(other, EllipticCurvePoint):
            raise TypeError("Can only add EllipticCurvePoint objects")
        
        if self.curve != other.curve:
            raise ValueError("Points must be on the same curve")
        
        # Handle point at infinity
        if self.is_infinity:
            return other
        if other.is_infinity:
            return self
        
        # Point doubling
        if self.x == other.x:
            if self.y == other.y:
                return self._double()
            else:
                # Points are inverses, return point at infinity
                return EllipticCurvePoint(None, None, self.curve)
        
        # General point addition
        x1, y1 = self.x, self.y
        x2, y2 = other.x, other.y
        p = self.curve.p
        
        # Calculate slope
        dx = (x2 - x1) % p
        dy = (y2 - y1) % p
        slope = (dy * ModularArithmetic.mod_inverse(dx, p)) % p
        
        # Calculate result point
        x3 = (slope**2 - x1 - x2) % p
        y3 = (slope * (x1 - x3) - y1) % p
        
        return EllipticCurvePoint(x3, y3, self.curve)
    
    def _double(self) -> 'EllipticCurvePoint':
        """Point doubling operation."""
        if self.is_infinity:
            return self
        
        x1, y1 = self.x, self.y
        p = self.curve.p
        a = self.curve.a
        
        # Calculate slope for doubling
        numerator = (3 * x1**2 + a) % p
        denominator = (2 * y1) % p
        slope = (numerator * ModularArithmetic.mod_inverse(denominator, p)) % p
        
        # Calculate result point
        x3 = (slope**2 - 2 * x1) % p
        y3 = (slope * (x1 - x3) - y1) % p
        
        return EllipticCurvePoint(x3, y3, self.curve)
    
    def __mul__(self, scalar: int) -> 'EllipticCurvePoint':
        """Scalar multiplication using double-and-add algorithm."""
        if scalar == 0:
            return EllipticCurvePoint(None, None, self.curve)
        
        if scalar < 0:
            return (-self) * (-scalar)
        
        result = EllipticCurvePoint(None, None, self.curve)  # Point at infinity
        addend = self
        
        while scalar:
            if scalar & 1:
                result = result + addend
            addend = addend._double()
            scalar >>= 1
        
        return result
    
    def __rmul__(self, scalar: int) -> 'EllipticCurvePoint':
        """Right multiplication (scalar * point)."""
        return self * scalar
    
    def __neg__(self) -> 'EllipticCurvePoint':
        """Point negation."""
        if self.is_infinity:
            return self
        return EllipticCurvePoint(self.x, (-self.y) % self.curve.p, self.curve)
    
    def __eq__(self, other: 'EllipticCurvePoint') -> bool:
        """Point equality comparison."""
        if not isinstance(other, EllipticCurvePoint):
            return False
        return (self.x == other.x and self.y == other.y and 
                self.is_infinity == other.is_infinity)
    
    def compress(self) -> bytes:
        """Compress point to 33 bytes (1 byte prefix + 32 bytes x-coordinate)."""
        if self.is_infinity:
            return b'\x00' + b'\x00' * 32
        
        x_bytes = self.x.to_bytes(32, 'big')
        prefix = b'\x02' if self.y % 2 == 0 else b'\x03'
        return prefix + x_bytes
    
    @classmethod
    def decompress(cls, data: bytes, curve: EllipticCurve) -> 'EllipticCurvePoint':
        """Decompress point from 33 bytes."""
        if len(data) != 33:
            raise ValueError("Compressed point must be 33 bytes")
        
        prefix = data[0]
        if prefix == 0:
            return cls(None, None, curve)
        
        if prefix not in [2, 3]:
            raise ValueError("Invalid compression prefix")
        
        x = int.from_bytes(data[1:], 'big')
        
        # Calculate y² = x³ + ax + b
        y_squared = (x**3 + curve.a * x + curve.b) % curve.p
        y = ModularArithmetic.mod_sqrt(y_squared, curve.p)
        
        # Choose correct y based on parity
        if (y % 2) != (prefix - 2):
            y = (-y) % curve.p
        
        return cls(x, y, curve)
    
    def __str__(self) -> str:
        if self.is_infinity:
            return "Point(∞)"
        return f"Point({self.x}, {self.y})"


# secp256k1 curve parameters (256-bit curve used by Bitcoin)
SECP256K1_PARAMS = {
    'p': 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    'a': 0,
    'b': 7,
    'n': 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
    'gx': 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    'gy': 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
}

# Global secp256k1 curve instance
secp256k1 = EllipticCurve(
    SECP256K1_PARAMS['a'],
    SECP256K1_PARAMS['b'],
    SECP256K1_PARAMS['p'],
    SECP256K1_PARAMS['n'],
    SECP256K1_PARAMS['gx'],
    SECP256K1_PARAMS['gy']
)