"""
Cryptographic Operations for ECC
=================================

This module implements high-level cryptographic operations using elliptic curves:
- Key generation
- ECDSA (Elliptic Curve Digital Signature Algorithm)
- ECDH (Elliptic Curve Diffie-Hellman) key exchange
- Secure random number generation
- Hash integration
"""

import hashlib
import secrets
import time
from typing import Tuple, Optional, Union
from elliptic_core import EllipticCurve, EllipticCurvePoint, secp256k1, ModularArithmetic


class SecureRandom:
    """Cryptographically secure random number generator."""
    
    @staticmethod
    def random_bytes(n: int) -> bytes:
        """Generate n cryptographically secure random bytes."""
        return secrets.token_bytes(n)
    
    @staticmethod
    def random_int(min_val: int, max_val: int) -> int:
        """Generate cryptographically secure random integer in range [min_val, max_val)."""
        if min_val >= max_val:
            raise ValueError("min_val must be less than max_val")
        
        range_size = max_val - min_val
        num_bytes = (range_size.bit_length() + 7) // 8
        
        while True:
            random_bytes = secrets.token_bytes(num_bytes)
            random_int = int.from_bytes(random_bytes, 'big')
            if random_int < range_size:
                return min_val + random_int
    
    @staticmethod
    def random_scalar(curve: EllipticCurve) -> int:
        """Generate a random scalar in the range [1, n-1] where n is the curve order."""
        return SecureRandom.random_int(1, curve.n)


class KeyPair:
    """Represents an ECC key pair (private key, public key)."""
    
    def __init__(self, private_key: int, public_key: EllipticCurvePoint):
        """
        Initialize key pair.
        
        Args:
            private_key: Private key (scalar)
            public_key: Public key (point on curve)
        """
        self.private_key = private_key
        self.public_key = public_key
        self.curve = public_key.curve
    
    @classmethod
    def generate(cls, curve: EllipticCurve = secp256k1) -> 'KeyPair':
        """Generate a new random key pair."""
        private_key = SecureRandom.random_scalar(curve)
        public_key = private_key * curve.G
        return cls(private_key, public_key)
    
    @classmethod
    def from_private_key(cls, private_key: int, curve: EllipticCurve = secp256k1) -> 'KeyPair':
        """Create key pair from existing private key."""
        if not (1 <= private_key < curve.n):
            raise ValueError("Private key must be in range [1, n-1]")
        
        public_key = private_key * curve.G
        return cls(private_key, public_key)
    
    def to_pem(self) -> Tuple[str, str]:
        """Export key pair to PEM format (simplified)."""
        private_pem = f"-----BEGIN EC PRIVATE KEY-----\n{self.private_key:064x}\n-----END EC PRIVATE KEY-----"
        
        # Compress public key for PEM
        pub_compressed = self.public_key.compress()
        pub_hex = pub_compressed.hex()
        public_pem = f"-----BEGIN PUBLIC KEY-----\n{pub_hex}\n-----END PUBLIC KEY-----"
        
        return private_pem, public_pem
    
    def __str__(self) -> str:
        return f"KeyPair(private={self.private_key:064x}, public={self.public_key})"


class ECDSA:
    """Elliptic Curve Digital Signature Algorithm implementation."""
    
    def __init__(self, curve: EllipticCurve = secp256k1):
        self.curve = curve
    
    def sign(self, message: bytes, private_key: int, k: Optional[int] = None) -> Tuple[int, int]:
        """
        Sign a message using ECDSA.
        
        Args:
            message: Message to sign
            private_key: Signer's private key
            k: Nonce (if None, generated randomly)
        
        Returns:
            Signature tuple (r, s)
        """
        if not (1 <= private_key < self.curve.n):
            raise ValueError("Invalid private key")
        
        # Hash the message
        message_hash = hashlib.sha256(message).digest()
        z = int.from_bytes(message_hash, 'big')
        
        # Truncate hash if longer than curve order
        if z.bit_length() > self.curve.n.bit_length():
            z = z >> (z.bit_length() - self.curve.n.bit_length())
        
        while True:
            # Generate or use provided nonce
            if k is None:
                k_val = SecureRandom.random_scalar(self.curve)
            else:
                k_val = k
            
            if not (1 <= k_val < self.curve.n):
                if k is not None:
                    raise ValueError("Invalid nonce k")
                continue
            
            # Calculate signature components
            point = k_val * self.curve.G
            r = point.x % self.curve.n
            
            if r == 0:
                if k is not None:
                    raise ValueError("Invalid nonce k (r = 0)")
                continue
            
            k_inv = ModularArithmetic.mod_inverse(k_val, self.curve.n)
            s = (k_inv * (z + r * private_key)) % self.curve.n
            
            if s == 0:
                if k is not None:
                    raise ValueError("Invalid nonce k (s = 0)")
                continue
            
            # Use low-S value (canonical signature)
            if s > self.curve.n // 2:
                s = self.curve.n - s
            
            return (r, s)
    
    def verify(self, message: bytes, signature: Tuple[int, int], public_key: EllipticCurvePoint) -> bool:
        """
        Verify ECDSA signature.
        
        Args:
            message: Original message
            signature: Signature tuple (r, s)
            public_key: Signer's public key
        
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            r, s = signature
            
            # Validate signature components
            if not (1 <= r < self.curve.n) or not (1 <= s < self.curve.n):
                return False
            
            # Hash the message
            message_hash = hashlib.sha256(message).digest()
            z = int.from_bytes(message_hash, 'big')
            
            # Truncate hash if longer than curve order
            if z.bit_length() > self.curve.n.bit_length():
                z = z >> (z.bit_length() - self.curve.n.bit_length())
            
            # Calculate verification values
            s_inv = ModularArithmetic.mod_inverse(s, self.curve.n)
            u1 = (z * s_inv) % self.curve.n
            u2 = (r * s_inv) % self.curve.n
            
            # Calculate verification point
            point = u1 * self.curve.G + u2 * public_key
            
            if point.is_infinity:
                return False
            
            # Verify signature
            return point.x % self.curve.n == r
            
        except Exception:
            return False
    
    def sign_deterministic(self, message: bytes, private_key: int) -> Tuple[int, int]:
        """
        Sign using deterministic nonce generation (RFC 6979).
        This ensures the same message and private key always produce the same signature.
        """
        # Simplified deterministic nonce generation
        # In production, use full RFC 6979 implementation
        h1 = hashlib.sha256(message).digest()
        private_bytes = private_key.to_bytes(32, 'big')
        
        # Generate deterministic k
        k_bytes = hashlib.sha256(private_bytes + h1).digest()
        k = int.from_bytes(k_bytes, 'big') % (self.curve.n - 1) + 1
        
        return self.sign(message, private_key, k)


class ECDH:
    """Elliptic Curve Diffie-Hellman key exchange."""
    
    def __init__(self, curve: EllipticCurve = secp256k1):
        self.curve = curve
    
    def generate_shared_secret(self, private_key: int, public_key: EllipticCurvePoint) -> bytes:
        """
        Generate shared secret using ECDH.
        
        Args:
            private_key: Own private key
            public_key: Other party's public key
        
        Returns:
            Shared secret as bytes
        """
        if not (1 <= private_key < self.curve.n):
            raise ValueError("Invalid private key")
        
        if public_key.is_infinity:
            raise ValueError("Invalid public key (point at infinity)")
        
        # Calculate shared point
        shared_point = private_key * public_key
        
        if shared_point.is_infinity:
            raise ValueError("Shared secret calculation resulted in point at infinity")
        
        # Use x-coordinate as shared secret
        return shared_point.x.to_bytes(32, 'big')
    
    def derive_key(self, shared_secret: bytes, info: bytes = b"", length: int = 32) -> bytes:
        """
        Derive key from shared secret using HKDF-like approach.
        
        Args:
            shared_secret: Shared secret from ECDH
            info: Additional info for key derivation
            length: Desired key length
        
        Returns:
            Derived key
        """
        # Simplified key derivation (use proper HKDF in production)
        salt = b"ECC-HKDF-Salt"
        prk = hashlib.sha256(salt + shared_secret).digest()
        
        output = b""
        counter = 1
        
        while len(output) < length:
            data = prk + info + counter.to_bytes(1, 'big')
            output += hashlib.sha256(data).digest()
            counter += 1
        
        return output[:length]


class ECCUtils:
    """Utility functions for ECC operations."""
    
    @staticmethod
    def hash_to_curve_point(data: bytes, curve: EllipticCurve = secp256k1) -> EllipticCurvePoint:
        """
        Hash arbitrary data to a point on the curve (simplified implementation).
        """
        # This is a simplified approach - use proper hash-to-curve methods in production
        counter = 0
        while counter < 1000:  # Prevent infinite loop
            hash_input = data + counter.to_bytes(4, 'big')
            hash_output = hashlib.sha256(hash_input).digest()
            x = int.from_bytes(hash_output, 'big') % curve.p
            
            # Try to find corresponding y
            try:
                y_squared = (x**3 + curve.a * x + curve.b) % curve.p
                y = ModularArithmetic.mod_sqrt(y_squared, curve.p)
                return EllipticCurvePoint(x, y, curve)
            except ValueError:
                counter += 1
                continue
        
        raise ValueError("Could not hash to curve point")
    
    @staticmethod
    def point_to_address(public_key: EllipticCurvePoint, prefix: bytes = b'\x04') -> str:
        """
        Convert public key point to address (Bitcoin-style).
        """
        if public_key.is_infinity:
            raise ValueError("Cannot create address from point at infinity")
        
        # Create uncompressed public key
        pub_bytes = prefix + public_key.x.to_bytes(32, 'big') + public_key.y.to_bytes(32, 'big')
        
        # Hash with SHA-256 then RIPEMD-160 (simplified - just use SHA-256)
        hash1 = hashlib.sha256(pub_bytes).digest()
        hash2 = hashlib.sha256(hash1).digest()
        
        # Take first 20 bytes and encode as hex
        address_bytes = hash2[:20]
        return address_bytes.hex()
    
    @staticmethod
    def validate_signature_format(signature: Tuple[int, int], curve: EllipticCurve = secp256k1) -> bool:
        """Validate that signature components are in valid ranges."""
        r, s = signature
        return (1 <= r < curve.n) and (1 <= s < curve.n)
    
    @staticmethod
    def signature_to_der(signature: Tuple[int, int]) -> bytes:
        """Convert signature to DER encoding format."""
        r, s = signature
        
        def encode_integer(value: int) -> bytes:
            bytes_val = value.to_bytes((value.bit_length() + 7) // 8, 'big')
            # Add padding if high bit is set
            if bytes_val[0] & 0x80:
                bytes_val = b'\x00' + bytes_val
            return b'\x02' + len(bytes_val).to_bytes(1, 'big') + bytes_val
        
        r_encoded = encode_integer(r)
        s_encoded = encode_integer(s)
        
        sequence = r_encoded + s_encoded
        return b'\x30' + len(sequence).to_bytes(1, 'big') + sequence
    
    @staticmethod
    def signature_from_der(der_bytes: bytes) -> Tuple[int, int]:
        """Parse signature from DER encoding format."""
        if len(der_bytes) < 6 or der_bytes[0] != 0x30:
            raise ValueError("Invalid DER signature format")
        
        length = der_bytes[1]
        if length != len(der_bytes) - 2:
            raise ValueError("Invalid DER signature length")
        
        pos = 2
        
        # Parse r
        if der_bytes[pos] != 0x02:
            raise ValueError("Invalid DER signature: expected INTEGER")
        pos += 1
        
        r_length = der_bytes[pos]
        pos += 1
        
        r = int.from_bytes(der_bytes[pos:pos + r_length], 'big')
        pos += r_length
        
        # Parse s
        if der_bytes[pos] != 0x02:
            raise ValueError("Invalid DER signature: expected INTEGER")
        pos += 1
        
        s_length = der_bytes[pos]
        pos += 1
        
        s = int.from_bytes(der_bytes[pos:pos + s_length], 'big')
        
        return (r, s)


# Export main classes and utilities
__all__ = [
    'SecureRandom',
    'KeyPair', 
    'ECDSA',
    'ECDH',
    'ECCUtils'
]