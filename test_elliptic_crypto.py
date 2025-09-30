#!/usr/bin/env python3
"""
Unit tests for EllipticWeb cryptographic functions
"""

import unittest
from app import EllipticCurveCrypto, Point

class TestEllipticCurveCrypto(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.crypto_p256 = EllipticCurveCrypto('P-256')
        self.crypto_p384 = EllipticCurveCrypto('P-384')
        self.crypto_p521 = EllipticCurveCrypto('P-521')
    
    def test_curve_initialization(self):
        """Test that curves are initialized correctly"""
        # Test P-256
        self.assertEqual(self.crypto_p256.curve.name, 'P-256')
        self.assertEqual(self.crypto_p256.curve.n.bit_length(), 256)
        
        # Test P-384
        self.assertEqual(self.crypto_p384.curve.name, 'P-384')
        self.assertEqual(self.crypto_p384.curve.n.bit_length(), 384)
        
        # Test P-521
        self.assertEqual(self.crypto_p521.curve.name, 'P-521')
        self.assertEqual(self.crypto_p521.curve.n.bit_length(), 521)
    
    def test_invalid_curve(self):
        """Test that invalid curve names raise exceptions"""
        with self.assertRaises(ValueError):
            EllipticCurveCrypto('INVALID-CURVE')
    
    def test_private_key_generation(self):
        """Test private key generation"""
        for crypto in [self.crypto_p256, self.crypto_p384, self.crypto_p521]:
            private_key = crypto.generate_private_key()
            
            # Private key should be in valid range
            self.assertGreater(private_key, 0)
            self.assertLess(private_key, crypto.curve.n)
    
    def test_public_key_generation(self):
        """Test public key generation from private key"""
        for crypto in [self.crypto_p256, self.crypto_p384, self.crypto_p521]:
            private_key = crypto.generate_private_key()
            public_key = crypto.get_public_key(private_key)
            
            # Public key should be a valid point
            self.assertIsInstance(public_key, Point)
            self.assertIsNotNone(public_key.x)
            self.assertIsNotNone(public_key.y)
            self.assertFalse(public_key.is_infinity)
    
    def test_point_operations(self):
        """Test elliptic curve point operations"""
        crypto = self.crypto_p256
        
        # Test point at infinity
        infinity = Point()
        self.assertTrue(infinity.is_infinity)
        
        # Test generator point
        generator = Point(crypto.curve.g_x, crypto.curve.g_y)
        self.assertFalse(generator.is_infinity)
        
        # Test point doubling
        doubled = crypto.point_double(generator)
        self.assertFalse(doubled.is_infinity)
        
        # Test point addition
        added = crypto.point_add(generator, generator)
        self.assertEqual(added.x, doubled.x)
        self.assertEqual(added.y, doubled.y)
        
        # Test adding point at infinity
        result = crypto.point_add(generator, infinity)
        self.assertEqual(result.x, generator.x)
        self.assertEqual(result.y, generator.y)
    
    def test_point_multiplication(self):
        """Test scalar point multiplication"""
        crypto = self.crypto_p256
        generator = Point(crypto.curve.g_x, crypto.curve.g_y)
        
        # Test multiplication by 0
        result = crypto.point_multiply(0, generator)
        self.assertTrue(result.is_infinity)
        
        # Test multiplication by 1
        result = crypto.point_multiply(1, generator)
        self.assertEqual(result.x, generator.x)
        self.assertEqual(result.y, generator.y)
        
        # Test multiplication by 2 equals doubling
        doubled = crypto.point_double(generator)
        multiplied = crypto.point_multiply(2, generator)
        self.assertEqual(doubled.x, multiplied.x)
        self.assertEqual(doubled.y, multiplied.y)
    
    def test_signature_generation_verification(self):
        """Test ECDSA signature generation and verification"""
        message = "Hello EllipticWeb Test!"
        
        for crypto in [self.crypto_p256, self.crypto_p384, self.crypto_p521]:
            # Generate key pair
            private_key = crypto.generate_private_key()
            public_key = crypto.get_public_key(private_key)
            
            # Sign message
            signature = crypto.sign(message, private_key)
            self.assertEqual(len(signature), 2)  # Should return (r, s)
            r, s = signature
            
            # Verify signature should pass
            is_valid = crypto.verify(message, signature, public_key)
            self.assertTrue(is_valid)
            
            # Verify with wrong message should fail
            wrong_message = "Wrong message"
            is_valid = crypto.verify(wrong_message, signature, public_key)
            self.assertFalse(is_valid)
            
            # Verify with wrong signature should fail
            wrong_signature = (r + 1, s)
            is_valid = crypto.verify(message, wrong_signature, public_key)
            self.assertFalse(is_valid)
    
    def test_modular_inverse(self):
        """Test modular inverse calculation"""
        crypto = self.crypto_p256
        
        # Test known values
        a = 3
        p = 7
        inv = crypto.mod_inverse(a, p)
        self.assertEqual((a * inv) % p, 1)
        
        # Test with curve prime
        a = 12345
        p = crypto.curve.p
        inv = crypto.mod_inverse(a, p)
        self.assertEqual((a * inv) % p, 1)
    
    def test_cross_curve_compatibility(self):
        """Test that different curves don't interfere with each other"""
        message = "Cross-curve test"
        
        # Generate keys for different curves
        private_256 = self.crypto_p256.generate_private_key()
        public_256 = self.crypto_p256.get_public_key(private_256)
        
        private_521 = self.crypto_p521.generate_private_key()
        public_521 = self.crypto_p521.get_public_key(private_521)
        
        # Sign with P-256
        signature_256 = self.crypto_p256.sign(message, private_256)
        
        # Sign with P-521
        signature_521 = self.crypto_p521.sign(message, private_521)
        
        # Verify correct combinations
        self.assertTrue(self.crypto_p256.verify(message, signature_256, public_256))
        self.assertTrue(self.crypto_p521.verify(message, signature_521, public_521))
        
        # Cross-verification should fail (different curves)
        # Note: This would actually cause errors due to different field sizes,
        # but in a real implementation you'd want to handle this gracefully

if __name__ == '__main__':
    unittest.main()