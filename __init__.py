"""
EllipticWeb - Comprehensive Elliptic Curve Cryptography Library
===============================================================

A complete implementation of elliptic curve cryptography with 256-bit security,
featuring the secp256k1 curve used by Bitcoin and other cryptocurrencies.

Key Features:
- Complete ECC mathematical foundation
- ECDSA digital signatures
- ECDH key exchange
- Secure key generation
- Point compression/decompression
- Web interface for easy interaction
- Comprehensive test suite

Usage:
    from elliptic_core import secp256k1, EllipticCurvePoint
    from cryptographic_operations import KeyPair, ECDSA, ECDH
    
    # Generate key pair
    keypair = KeyPair.generate()
    
    # Sign message
    ecdsa = ECDSA()
    signature = ecdsa.sign(b"message", keypair.private_key)
    
    # Verify signature
    is_valid = ecdsa.verify(b"message", signature, keypair.public_key)
"""

from .elliptic_core import (
    ModularArithmetic,
    EllipticCurve,
    EllipticCurvePoint,
    secp256k1
)

from .cryptographic_operations import (
    SecureRandom,
    KeyPair,
    ECDSA,
    ECDH,
    ECCUtils
)

__version__ = "1.0.0"
__author__ = "EllipticWeb Team"
__description__ = "Comprehensive Elliptic Curve Cryptography Library"

__all__ = [
    # Core components
    'ModularArithmetic',
    'EllipticCurve', 
    'EllipticCurvePoint',
    'secp256k1',
    
    # Cryptographic operations
    'SecureRandom',
    'KeyPair',
    'ECDSA',
    'ECDH',
    'ECCUtils',
    
    # Version info
    '__version__',
    '__author__',
    '__description__'
]