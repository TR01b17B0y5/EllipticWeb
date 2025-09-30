#!/usr/bin/env python3
"""
EllipticWeb - Comprehensive Elliptic Curve Web Application
Author: Generated for 256+ bit key support
"""

from flask import Flask, render_template, request, jsonify
import secrets
import hashlib
import json
from dataclasses import dataclass
from typing import Tuple, Optional, Dict, Any

app = Flask(__name__)

@dataclass
class EllipticCurve:
    """Represents an elliptic curve y² = x³ + ax + b (mod p)"""
    name: str
    p: int  # Prime modulus
    a: int  # Coefficient a
    b: int  # Coefficient b
    g_x: int  # Generator point x coordinate
    g_y: int  # Generator point y coordinate
    n: int  # Order of the generator point
    h: int  # Cofactor

class Point:
    """Represents a point on an elliptic curve"""
    def __init__(self, x: Optional[int] = None, y: Optional[int] = None):
        self.x = x
        self.y = y
        self.is_infinity = (x is None and y is None)
    
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y and self.is_infinity == other.is_infinity
        return False
    
    def __str__(self):
        if self.is_infinity:
            return "Point(∞)"
        return f"Point({self.x}, {self.y})"

class EllipticCurveCrypto:
    """Elliptic Curve Cryptography operations"""
    
    # Standard curves with 256+ bit key support
    CURVES = {
        'P-256': EllipticCurve(
            name='P-256',
            p=0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff,
            a=0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc,
            b=0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b,
            g_x=0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
            g_y=0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5,
            n=0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551,
            h=1
        ),
        'P-384': EllipticCurve(
            name='P-384',
            p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffff0000000000000000ffffffff,
            a=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffff0000000000000000fffffffc,
            b=0xb3312fa7e23ee7e4988e056be3f82d19181d9c6efe8141120314088f5013875ac656398d8a2ed19d2a85c8edd3ec2aef,
            g_x=0xaa87ca22be8b05378eb1c71ef320ad746e1d3b628ba79b9859f741e082542a385502f25dbf55296c3a545e3872760ab7,
            g_y=0x3617de4a96262c6f5d9e98bf9292dc29f8f41dbd289a147ce9da3113b5f0b8c00a60b1ce1d7e819d7a431d7c90ea0e5f,
            n=0xffffffffffffffffffffffffffffffffffffffffffffffffc7634d81f4372ddf581a0db248b0a77aecec196accc52973,
            h=1
        ),
        'P-521': EllipticCurve(
            name='P-521',
            p=0x01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff,
            a=0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc,
            b=0x0051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00,
            g_x=0x00c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66,
            g_y=0x011839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650,
            n=0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa51868783bf2f966b7fcc0148f709a5d03bb5c9b8899c47aebb6fb71e91386409,
            h=1
        )
    }
    
    def __init__(self, curve_name: str = 'P-256'):
        if curve_name not in self.CURVES:
            raise ValueError(f"Unsupported curve: {curve_name}")
        self.curve = self.CURVES[curve_name]
    
    def mod_inverse(self, a: int, m: int) -> int:
        """Calculate modular inverse using extended Euclidean algorithm"""
        if a < 0:
            a = (a % m + m) % m
        
        # Extended Euclidean Algorithm
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a % m, m)
        if gcd != 1:
            raise ValueError("Modular inverse does not exist")
        return (x % m + m) % m
    
    def point_add(self, p1: Point, p2: Point) -> Point:
        """Add two points on the elliptic curve"""
        if p1.is_infinity:
            return p2
        if p2.is_infinity:
            return p1
        
        if p1.x == p2.x:
            if p1.y == p2.y:
                return self.point_double(p1)
            else:
                return Point()  # Point at infinity
        
        # Calculate slope
        dx = (p2.x - p1.x) % self.curve.p
        dy = (p2.y - p1.y) % self.curve.p
        slope = (dy * self.mod_inverse(dx, self.curve.p)) % self.curve.p
        
        # Calculate new point
        x3 = (slope * slope - p1.x - p2.x) % self.curve.p
        y3 = (slope * (p1.x - x3) - p1.y) % self.curve.p
        
        return Point(x3, y3)
    
    def point_double(self, p: Point) -> Point:
        """Double a point on the elliptic curve"""
        if p.is_infinity:
            return p
        
        # Calculate slope
        numerator = (3 * p.x * p.x + self.curve.a) % self.curve.p
        denominator = (2 * p.y) % self.curve.p
        slope = (numerator * self.mod_inverse(denominator, self.curve.p)) % self.curve.p
        
        # Calculate new point
        x3 = (slope * slope - 2 * p.x) % self.curve.p
        y3 = (slope * (p.x - x3) - p.y) % self.curve.p
        
        return Point(x3, y3)
    
    def point_multiply(self, k: int, point: Point) -> Point:
        """Multiply a point by a scalar using double-and-add algorithm"""
        if k == 0:
            return Point()  # Point at infinity
        if k == 1:
            return point
        
        result = Point()  # Point at infinity
        addend = point
        
        while k:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_double(addend)
            k >>= 1
        
        return result
    
    def generate_private_key(self) -> int:
        """Generate a random private key"""
        return secrets.randbelow(self.curve.n - 1) + 1
    
    def get_public_key(self, private_key: int) -> Point:
        """Calculate public key from private key"""
        generator = Point(self.curve.g_x, self.curve.g_y)
        return self.point_multiply(private_key, generator)
    
    def sign(self, message: str, private_key: int) -> Tuple[int, int]:
        """Sign a message using ECDSA"""
        # Hash the message
        message_hash = int.from_bytes(hashlib.sha256(message.encode()).digest(), 'big')
        
        while True:
            # Generate random k
            k = secrets.randbelow(self.curve.n - 1) + 1
            
            # Calculate r
            generator = Point(self.curve.g_x, self.curve.g_y)
            point = self.point_multiply(k, generator)
            r = point.x % self.curve.n
            
            if r == 0:
                continue
            
            # Calculate s
            k_inv = self.mod_inverse(k, self.curve.n)
            s = (k_inv * (message_hash + r * private_key)) % self.curve.n
            
            if s == 0:
                continue
            
            return (r, s)
    
    def verify(self, message: str, signature: Tuple[int, int], public_key: Point) -> bool:
        """Verify a signature using ECDSA"""
        r, s = signature
        
        if not (1 <= r < self.curve.n and 1 <= s < self.curve.n):
            return False
        
        # Hash the message
        message_hash = int.from_bytes(hashlib.sha256(message.encode()).digest(), 'big')
        
        # Calculate verification values
        w = self.mod_inverse(s, self.curve.n)
        u1 = (message_hash * w) % self.curve.n
        u2 = (r * w) % self.curve.n
        
        # Calculate point
        generator = Point(self.curve.g_x, self.curve.g_y)
        point1 = self.point_multiply(u1, generator)
        point2 = self.point_multiply(u2, public_key)
        point = self.point_add(point1, point2)
        
        if point.is_infinity:
            return False
        
        return (point.x % self.curve.n) == r

# Global crypto instance
crypto = EllipticCurveCrypto()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/curves')
def get_curves():
    """Get available elliptic curves"""
    curves_info = {}
    for name, curve in EllipticCurveCrypto.CURVES.items():
        curves_info[name] = {
            'name': curve.name,
            'key_size': curve.n.bit_length(),
            'description': f"{curve.name} - {curve.n.bit_length()}-bit security"
        }
    return jsonify(curves_info)

@app.route('/api/generate_keys', methods=['POST'])
def generate_keys():
    """Generate a new key pair"""
    data = request.get_json() or {}
    curve_name = data.get('curve', 'P-256')
    
    try:
        global crypto
        crypto = EllipticCurveCrypto(curve_name)
        
        private_key = crypto.generate_private_key()
        public_key = crypto.get_public_key(private_key)
        
        return jsonify({
            'success': True,
            'curve': curve_name,
            'private_key': hex(private_key),
            'public_key': {
                'x': hex(public_key.x),
                'y': hex(public_key.y)
            },
            'key_size': crypto.curve.n.bit_length()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/sign', methods=['POST'])
def sign_message():
    """Sign a message"""
    data = request.get_json()
    if not data or 'message' not in data or 'private_key' not in data:
        return jsonify({'success': False, 'error': 'Missing message or private_key'}), 400
    
    try:
        message = data['message']
        private_key = int(data['private_key'], 16) if data['private_key'].startswith('0x') else int(data['private_key'])
        curve_name = data.get('curve', 'P-256')
        
        global crypto
        crypto = EllipticCurveCrypto(curve_name)
        
        r, s = crypto.sign(message, private_key)
        
        return jsonify({
            'success': True,
            'signature': {
                'r': hex(r),
                's': hex(s)
            },
            'message': message,
            'curve': curve_name
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/verify', methods=['POST'])
def verify_signature():
    """Verify a signature"""
    data = request.get_json()
    required_fields = ['message', 'signature', 'public_key']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'success': False, 'error': f'Missing required fields: {required_fields}'}), 400
    
    try:
        message = data['message']
        signature_data = data['signature']
        public_key_data = data['public_key']
        curve_name = data.get('curve', 'P-256')
        
        global crypto
        crypto = EllipticCurveCrypto(curve_name)
        
        r = int(signature_data['r'], 16) if signature_data['r'].startswith('0x') else int(signature_data['r'])
        s = int(signature_data['s'], 16) if signature_data['s'].startswith('0x') else int(signature_data['s'])
        
        pub_x = int(public_key_data['x'], 16) if public_key_data['x'].startswith('0x') else int(public_key_data['x'])
        pub_y = int(public_key_data['y'], 16) if public_key_data['y'].startswith('0x') else int(public_key_data['y'])
        
        public_key = Point(pub_x, pub_y)
        signature = (r, s)
        
        is_valid = crypto.verify(message, signature, public_key)
        
        return jsonify({
            'success': True,
            'valid': is_valid,
            'message': message,
            'curve': curve_name
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/curve_info/<curve_name>')
def get_curve_info(curve_name):
    """Get detailed information about a specific curve"""
    if curve_name not in EllipticCurveCrypto.CURVES:
        return jsonify({'success': False, 'error': 'Curve not found'}), 404
    
    curve = EllipticCurveCrypto.CURVES[curve_name]
    return jsonify({
        'success': True,
        'curve': {
            'name': curve.name,
            'prime_modulus': hex(curve.p),
            'coefficient_a': hex(curve.a),
            'coefficient_b': hex(curve.b),
            'generator_point': {
                'x': hex(curve.g_x),
                'y': hex(curve.g_y)
            },
            'order': hex(curve.n),
            'cofactor': curve.h,
            'key_size_bits': curve.n.bit_length()
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)