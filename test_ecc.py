"""
Comprehensive Test Suite for ECC Mathematical Core
==================================================

Tests all components of the elliptic curve cryptography implementation:
- Modular arithmetic operations
- Elliptic curve point operations
- Cryptographic operations (ECDSA, ECDH)
- Key generation and management
- Edge cases and security validations
"""

import unittest
import hashlib
from elliptic_core import (
    ModularArithmetic, EllipticCurve, EllipticCurvePoint, secp256k1
)
from cryptographic_operations import (
    SecureRandom, KeyPair, ECDSA, ECDH, ECCUtils
)


class TestModularArithmetic(unittest.TestCase):
    """Test modular arithmetic operations."""
    
    def test_mod_inverse(self):
        """Test modular multiplicative inverse."""
        # Test known values
        self.assertEqual(ModularArithmetic.mod_inverse(3, 7), 5)
        self.assertEqual(ModularArithmetic.mod_inverse(2, 7), 4)
        
        # Test that inverse is correct
        a, m = 17, 43
        inv = ModularArithmetic.mod_inverse(a, m)
        self.assertEqual((a * inv) % m, 1)
        
        # Test error for non-coprime numbers
        with self.assertRaises(ValueError):
            ModularArithmetic.mod_inverse(6, 9)
    
    def test_mod_pow(self):
        """Test modular exponentiation."""
        self.assertEqual(ModularArithmetic.mod_pow(2, 10, 1000), 24)
        self.assertEqual(ModularArithmetic.mod_pow(3, 4, 7), 4)
    
    def test_mod_sqrt(self):
        """Test modular square root."""
        # Test known square roots
        p = 7
        for a in [1, 2, 4]:
            sqrt_a = ModularArithmetic.mod_sqrt(a, p)
            self.assertEqual((sqrt_a * sqrt_a) % p, a)
        
        # Test non-quadratic residue
        with self.assertRaises(ValueError):
            ModularArithmetic.mod_sqrt(3, 7)


class TestEllipticCurve(unittest.TestCase):
    """Test elliptic curve implementation."""
    
    def test_curve_creation(self):
        """Test curve creation and validation."""
        # Valid curve
        curve = EllipticCurve(0, 7, 17, 19, 1, 5)
        self.assertIsNotNone(curve)
        
        # Invalid curve (discriminant = 0)
        with self.assertRaises(ValueError):
            EllipticCurve(0, 0, 17, 19, 1, 5)  # y² = x³ has discriminant 0
    
    def test_point_validation(self):
        """Test point validation on curve."""
        curve = secp256k1
        
        # Valid point (generator)
        point = EllipticCurvePoint(curve.G.x, curve.G.y, curve)
        self.assertFalse(point.is_infinity)
        
        # Invalid point
        with self.assertRaises(ValueError):
            EllipticCurvePoint(1, 1, curve)  # (1,1) is not on secp256k1
    
    def test_point_at_infinity(self):
        """Test point at infinity operations."""
        curve = secp256k1
        infinity = EllipticCurvePoint(None, None, curve)
        
        self.assertTrue(infinity.is_infinity)
        
        # Adding infinity should return the other point
        result = curve.G + infinity
        self.assertEqual(result, curve.G)
        
        result = infinity + curve.G
        self.assertEqual(result, curve.G)


class TestEllipticCurvePoint(unittest.TestCase):
    """Test elliptic curve point operations."""
    
    def setUp(self):
        self.curve = secp256k1
        self.G = self.curve.G
    
    def test_point_addition(self):
        """Test point addition operations."""
        # Test doubling (G + G)
        double_G = self.G + self.G
        self.assertIsInstance(double_G, EllipticCurvePoint)
        self.assertFalse(double_G.is_infinity)
        
        # Test that doubling matches scalar multiplication
        double_G_scalar = 2 * self.G
        self.assertEqual(double_G, double_G_scalar)
        
        # Test adding inverse gives infinity
        neg_G = -self.G
        result = self.G + neg_G
        self.assertTrue(result.is_infinity)
    
    def test_scalar_multiplication(self):
        """Test scalar multiplication."""
        # Test known values
        point_2G = 2 * self.G
        point_3G = 3 * self.G
        
        # Test additivity: 2G + G = 3G
        result = point_2G + self.G
        self.assertEqual(result, point_3G)
        
        # Test that n * G = infinity (where n is curve order)
        infinity_point = self.curve.n * self.G
        self.assertTrue(infinity_point.is_infinity)
        
        # Test zero multiplication
        zero_point = 0 * self.G
        self.assertTrue(zero_point.is_infinity)
    
    def test_point_compression(self):
        """Test point compression and decompression."""
        # Test with generator point
        compressed = self.G.compress()
        self.assertEqual(len(compressed), 33)
        
        # Test decompression
        decompressed = EllipticCurvePoint.decompress(compressed, self.curve)
        self.assertEqual(decompressed, self.G)
        
        # Test with other points
        point_2G = 2 * self.G
        compressed_2G = point_2G.compress()
        decompressed_2G = EllipticCurvePoint.decompress(compressed_2G, self.curve)
        self.assertEqual(decompressed_2G, point_2G)
    
    def test_point_negation(self):
        """Test point negation."""
        neg_G = -self.G
        self.assertEqual(neg_G.x, self.G.x)
        self.assertEqual(neg_G.y, (-self.G.y) % self.curve.p)
        
        # Test double negation
        double_neg = -(-self.G)
        self.assertEqual(double_neg, self.G)


class TestSecureRandom(unittest.TestCase):
    """Test secure random number generation."""
    
    def test_random_bytes(self):
        """Test random byte generation."""
        bytes1 = SecureRandom.random_bytes(32)
        bytes2 = SecureRandom.random_bytes(32)
        
        self.assertEqual(len(bytes1), 32)
        self.assertEqual(len(bytes2), 32)
        self.assertNotEqual(bytes1, bytes2)  # Very unlikely to be equal
    
    def test_random_int(self):
        """Test random integer generation."""
        # Test range
        for _ in range(100):
            val = SecureRandom.random_int(10, 20)
            self.assertGreaterEqual(val, 10)
            self.assertLess(val, 20)
        
        # Test error for invalid range
        with self.assertRaises(ValueError):
            SecureRandom.random_int(20, 10)
    
    def test_random_scalar(self):
        """Test random scalar generation for curve."""
        curve = secp256k1
        
        for _ in range(10):
            scalar = SecureRandom.random_scalar(curve)
            self.assertGreaterEqual(scalar, 1)
            self.assertLess(scalar, curve.n)


class TestKeyPair(unittest.TestCase):
    """Test key pair generation and management."""
    
    def test_key_generation(self):
        """Test key pair generation."""
        keypair = KeyPair.generate()
        
        self.assertIsInstance(keypair.private_key, int)
        self.assertIsInstance(keypair.public_key, EllipticCurvePoint)
        self.assertGreater(keypair.private_key, 0)
        self.assertLess(keypair.private_key, secp256k1.n)
        
        # Verify public key is correct
        expected_public = keypair.private_key * secp256k1.G
        self.assertEqual(keypair.public_key, expected_public)
    
    def test_from_private_key(self):
        """Test key pair creation from private key."""
        private_key = 12345
        keypair = KeyPair.from_private_key(private_key)
        
        self.assertEqual(keypair.private_key, private_key)
        expected_public = private_key * secp256k1.G
        self.assertEqual(keypair.public_key, expected_public)
        
        # Test invalid private key
        with self.assertRaises(ValueError):
            KeyPair.from_private_key(0)  # Must be >= 1
        
        with self.assertRaises(ValueError):
            KeyPair.from_private_key(secp256k1.n)  # Must be < n
    
    def test_pem_export(self):
        """Test PEM export functionality."""
        keypair = KeyPair.generate()
        private_pem, public_pem = keypair.to_pem()
        
        self.assertIn("BEGIN EC PRIVATE KEY", private_pem)
        self.assertIn("END EC PRIVATE KEY", private_pem)
        self.assertIn("BEGIN PUBLIC KEY", public_pem)
        self.assertIn("END PUBLIC KEY", public_pem)


class TestECDSA(unittest.TestCase):
    """Test ECDSA signature operations."""
    
    def setUp(self):
        self.ecdsa = ECDSA()
        self.keypair = KeyPair.generate()
        self.message = b"Hello, ECDSA!"
    
    def test_sign_and_verify(self):
        """Test basic signing and verification."""
        signature = self.ecdsa.sign(self.message, self.keypair.private_key)
        
        # Verify signature components are valid
        r, s = signature
        self.assertIsInstance(r, int)
        self.assertIsInstance(s, int)
        self.assertGreater(r, 0)
        self.assertGreater(s, 0)
        self.assertLess(r, secp256k1.n)
        self.assertLess(s, secp256k1.n)
        
        # Verify signature
        is_valid = self.ecdsa.verify(self.message, signature, self.keypair.public_key)
        self.assertTrue(is_valid)
    
    def test_signature_validation(self):
        """Test signature validation edge cases."""
        signature = self.ecdsa.sign(self.message, self.keypair.private_key)
        
        # Valid signature
        self.assertTrue(self.ecdsa.verify(self.message, signature, self.keypair.public_key))
        
        # Wrong message
        wrong_message = b"Wrong message"
        self.assertFalse(self.ecdsa.verify(wrong_message, signature, self.keypair.public_key))
        
        # Wrong public key
        wrong_keypair = KeyPair.generate()
        self.assertFalse(self.ecdsa.verify(self.message, signature, wrong_keypair.public_key))
        
        # Invalid signature components
        invalid_sig = (0, signature[1])  # r = 0
        self.assertFalse(self.ecdsa.verify(self.message, invalid_sig, self.keypair.public_key))
        
        invalid_sig = (signature[0], 0)  # s = 0
        self.assertFalse(self.ecdsa.verify(self.message, invalid_sig, self.keypair.public_key))
    
    def test_deterministic_signing(self):
        """Test deterministic signature generation."""
        sig1 = self.ecdsa.sign_deterministic(self.message, self.keypair.private_key)
        sig2 = self.ecdsa.sign_deterministic(self.message, self.keypair.private_key)
        
        # Same message and key should produce same signature
        self.assertEqual(sig1, sig2)
        
        # Verify both signatures
        self.assertTrue(self.ecdsa.verify(self.message, sig1, self.keypair.public_key))
        self.assertTrue(self.ecdsa.verify(self.message, sig2, self.keypair.public_key))


class TestECDH(unittest.TestCase):
    """Test ECDH key exchange."""
    
    def setUp(self):
        self.ecdh = ECDH()
        self.alice_keypair = KeyPair.generate()
        self.bob_keypair = KeyPair.generate()
    
    def test_key_exchange(self):
        """Test basic ECDH key exchange."""
        # Alice generates shared secret with Bob's public key
        alice_shared = self.ecdh.generate_shared_secret(
            self.alice_keypair.private_key,
            self.bob_keypair.public_key
        )
        
        # Bob generates shared secret with Alice's public key
        bob_shared = self.ecdh.generate_shared_secret(
            self.bob_keypair.private_key,
            self.alice_keypair.public_key
        )
        
        # Shared secrets should be identical
        self.assertEqual(alice_shared, bob_shared)
        self.assertEqual(len(alice_shared), 32)  # 256 bits
    
    def test_key_derivation(self):
        """Test key derivation from shared secret."""
        shared_secret = self.ecdh.generate_shared_secret(
            self.alice_keypair.private_key,
            self.bob_keypair.public_key
        )
        
        # Derive keys
        key1 = self.ecdh.derive_key(shared_secret, b"key1", 16)
        key2 = self.ecdh.derive_key(shared_secret, b"key2", 16)
        key3 = self.ecdh.derive_key(shared_secret, b"key1", 16)
        
        self.assertEqual(len(key1), 16)
        self.assertEqual(len(key2), 16)
        self.assertNotEqual(key1, key2)  # Different info should give different keys
        self.assertEqual(key1, key3)  # Same info should give same key
    
    def test_invalid_inputs(self):
        """Test ECDH with invalid inputs."""
        # Invalid private key
        with self.assertRaises(ValueError):
            self.ecdh.generate_shared_secret(0, self.bob_keypair.public_key)
        
        # Point at infinity
        infinity = EllipticCurvePoint(None, None, secp256k1)
        with self.assertRaises(ValueError):
            self.ecdh.generate_shared_secret(self.alice_keypair.private_key, infinity)


class TestECCUtils(unittest.TestCase):
    """Test ECC utility functions."""
    
    def test_signature_format_validation(self):
        """Test signature format validation."""
        # Valid signature
        valid_sig = (12345, 67890)
        self.assertTrue(ECCUtils.validate_signature_format(valid_sig))
        
        # Invalid signatures
        invalid_sig1 = (0, 67890)  # r = 0
        self.assertFalse(ECCUtils.validate_signature_format(invalid_sig1))
        
        invalid_sig2 = (12345, secp256k1.n)  # s >= n
        self.assertFalse(ECCUtils.validate_signature_format(invalid_sig2))
    
    def test_der_encoding(self):
        """Test DER signature encoding/decoding."""
        signature = (12345, 67890)
        
        # Encode to DER
        der_bytes = ECCUtils.signature_to_der(signature)
        self.assertIsInstance(der_bytes, bytes)
        self.assertGreater(len(der_bytes), 6)
        
        # Decode from DER
        decoded_sig = ECCUtils.signature_from_der(der_bytes)
        self.assertEqual(decoded_sig, signature)
    
    def test_point_to_address(self):
        """Test address generation from public key."""
        keypair = KeyPair.generate()
        address = ECCUtils.point_to_address(keypair.public_key)
        
        self.assertIsInstance(address, str)
        self.assertEqual(len(address), 40)  # 20 bytes = 40 hex chars
        
        # Same point should give same address
        address2 = ECCUtils.point_to_address(keypair.public_key)
        self.assertEqual(address, address2)
    
    def test_hash_to_curve_point(self):
        """Test hashing data to curve point."""
        data = b"test data"
        point = ECCUtils.hash_to_curve_point(data)
        
        self.assertIsInstance(point, EllipticCurvePoint)
        self.assertFalse(point.is_infinity)
        
        # Same data should give same point
        point2 = ECCUtils.hash_to_curve_point(data)
        self.assertEqual(point, point2)
        
        # Different data should give different points
        point3 = ECCUtils.hash_to_curve_point(b"different data")
        self.assertNotEqual(point, point3)


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple components."""
    
    def test_full_ecdsa_workflow(self):
        """Test complete ECDSA workflow."""
        # Generate key pairs
        alice = KeyPair.generate()
        bob = KeyPair.generate()
        
        # Alice signs a message
        message = b"Contract: Alice pays Bob 100 coins"
        ecdsa = ECDSA()
        signature = ecdsa.sign(message, alice.private_key)
        
        # Bob verifies Alice's signature
        is_valid = ecdsa.verify(message, signature, alice.public_key)
        self.assertTrue(is_valid)
        
        # Carol (using different key) cannot forge Alice's signature
        carol = KeyPair.generate()
        carol_signature = ecdsa.sign(message, carol.private_key)
        
        # Carol's signature won't verify as Alice's
        is_carol_valid = ecdsa.verify(message, carol_signature, alice.public_key)
        self.assertFalse(is_carol_valid)
    
    def test_full_ecdh_workflow(self):
        """Test complete ECDH workflow."""
        # Alice and Bob generate key pairs
        alice = KeyPair.generate()
        bob = KeyPair.generate()
        
        # Perform ECDH key exchange
        ecdh = ECDH()
        alice_shared = ecdh.generate_shared_secret(alice.private_key, bob.public_key)
        bob_shared = ecdh.generate_shared_secret(bob.private_key, alice.public_key)
        
        # Verify shared secrets match
        self.assertEqual(alice_shared, bob_shared)
        
        # Derive encryption keys
        alice_key = ecdh.derive_key(alice_shared, b"encryption", 32)
        bob_key = ecdh.derive_key(bob_shared, b"encryption", 32)
        
        # Keys should be identical
        self.assertEqual(alice_key, bob_key)
    
    def test_cross_component_compatibility(self):
        """Test compatibility between different components."""
        # Generate keypair and test with all components
        keypair = KeyPair.generate()
        
        # Test point compression/decompression
        compressed = keypair.public_key.compress()
        decompressed = EllipticCurvePoint.decompress(compressed, secp256k1)
        self.assertEqual(decompressed, keypair.public_key)
        
        # Test address generation
        address = ECCUtils.point_to_address(keypair.public_key)
        self.assertIsInstance(address, str)
        
        # Test signature operations
        ecdsa = ECDSA()
        message = b"test message"
        signature = ecdsa.sign(message, keypair.private_key)
        is_valid = ecdsa.verify(message, signature, keypair.public_key)
        self.assertTrue(is_valid)
        
        # Test ECDH
        other_keypair = KeyPair.generate()
        ecdh = ECDH()
        shared_secret = ecdh.generate_shared_secret(
            keypair.private_key,
            other_keypair.public_key
        )
        self.assertEqual(len(shared_secret), 32)


def run_all_tests():
    """Run all test suites."""
    test_classes = [
        TestModularArithmetic,
        TestEllipticCurve,
        TestEllipticCurvePoint,
        TestSecureRandom,
        TestKeyPair,
        TestECDSA,
        TestECDH,
        TestECCUtils,
        TestIntegration
    ]
    
    suite = unittest.TestSuite()
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)