"""
ECC Examples and Demonstrations
===============================

This module provides comprehensive examples of how to use the ECC implementation
for various cryptographic operations including key generation, digital signatures,
key exchange, and address generation.
"""

import hashlib
from elliptic_core import secp256k1, EllipticCurvePoint
from cryptographic_operations import KeyPair, ECDSA, ECDH, ECCUtils, SecureRandom


def example_key_generation():
    """Demonstrate key generation and management."""
    print("=" * 60)
    print("KEY GENERATION EXAMPLE")
    print("=" * 60)
    
    # Generate a new key pair
    print("Generating new key pair...")
    keypair = KeyPair.generate()
    
    print(f"Private Key: {keypair.private_key:064x}")
    print(f"Public Key Point: {keypair.public_key}")
    print(f"Public Key (Compressed): {keypair.public_key.compress().hex()}")
    
    # Generate address from public key
    address = ECCUtils.point_to_address(keypair.public_key)
    print(f"Address: {address}")
    
    # Export to PEM format
    private_pem, public_pem = keypair.to_pem()
    print("\nPEM Format:")
    print("Private Key PEM:")
    print(private_pem)
    print("\nPublic Key PEM:")
    print(public_pem)
    
    # Create keypair from existing private key
    print("\n" + "-" * 40)
    print("Creating keypair from existing private key...")
    existing_private_key = 0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
    keypair_from_existing = KeyPair.from_private_key(existing_private_key)
    print(f"Private Key: {keypair_from_existing.private_key:064x}")
    print(f"Public Key: {keypair_from_existing.public_key}")
    
    return keypair


def example_digital_signatures():
    """Demonstrate ECDSA digital signatures."""
    print("\n" + "=" * 60)
    print("DIGITAL SIGNATURE EXAMPLE")
    print("=" * 60)
    
    # Generate key pair
    alice_keypair = KeyPair.generate()
    ecdsa = ECDSA()
    
    # Message to sign
    message = b"Hello, this is a secure message from Alice!"
    print(f"Message: {message.decode('utf-8')}")
    print(f"Message hash: {hashlib.sha256(message).hexdigest()}")
    
    # Sign the message
    print("\nSigning message...")
    signature = ecdsa.sign(message, alice_keypair.private_key)
    print(f"Signature (r, s): ({signature[0]:064x}, {signature[1]:064x})")
    
    # Convert to DER format
    der_signature = ECCUtils.signature_to_der(signature)
    print(f"DER encoded signature: {der_signature.hex()}")
    
    # Verify the signature
    print("\nVerifying signature...")
    is_valid = ecdsa.verify(message, signature, alice_keypair.public_key)
    print(f"Signature valid: {is_valid}")
    
    # Test with wrong message
    wrong_message = b"This is a different message"
    is_valid_wrong = ecdsa.verify(wrong_message, signature, alice_keypair.public_key)
    print(f"Signature valid for wrong message: {is_valid_wrong}")
    
    # Test deterministic signing
    print("\n" + "-" * 40)
    print("Deterministic signing test...")
    det_sig1 = ecdsa.sign_deterministic(message, alice_keypair.private_key)
    det_sig2 = ecdsa.sign_deterministic(message, alice_keypair.private_key)
    print(f"Deterministic signatures equal: {det_sig1 == det_sig2}")
    
    return alice_keypair, signature


def example_key_exchange():
    """Demonstrate ECDH key exchange."""
    print("\n" + "=" * 60)
    print("KEY EXCHANGE EXAMPLE")
    print("=" * 60)
    
    # Generate key pairs for Alice and Bob
    alice_keypair = KeyPair.generate()
    bob_keypair = KeyPair.generate()
    
    print("Alice's public key:", alice_keypair.public_key.compress().hex())
    print("Bob's public key:", bob_keypair.public_key.compress().hex())
    
    # Perform ECDH key exchange
    ecdh = ECDH()
    
    print("\nPerforming key exchange...")
    
    # Alice generates shared secret using her private key and Bob's public key
    alice_shared = ecdh.generate_shared_secret(
        alice_keypair.private_key,
        bob_keypair.public_key
    )
    
    # Bob generates shared secret using his private key and Alice's public key
    bob_shared = ecdh.generate_shared_secret(
        bob_keypair.private_key,
        alice_keypair.public_key
    )
    
    print(f"Alice's shared secret: {alice_shared.hex()}")
    print(f"Bob's shared secret: {bob_shared.hex()}")
    print(f"Shared secrets match: {alice_shared == bob_shared}")
    
    # Derive encryption keys
    print("\n" + "-" * 40)
    print("Deriving encryption keys...")
    
    alice_aes_key = ecdh.derive_key(alice_shared, b"AES-256-Encryption", 32)
    bob_aes_key = ecdh.derive_key(bob_shared, b"AES-256-Encryption", 32)
    
    alice_hmac_key = ecdh.derive_key(alice_shared, b"HMAC-SHA256", 32)
    bob_hmac_key = ecdh.derive_key(bob_shared, b"HMAC-SHA256", 32)
    
    print(f"Alice's AES key: {alice_aes_key.hex()}")
    print(f"Bob's AES key: {bob_aes_key.hex()}")
    print(f"AES keys match: {alice_aes_key == bob_aes_key}")
    
    print(f"Alice's HMAC key: {alice_hmac_key.hex()}")
    print(f"Bob's HMAC key: {bob_hmac_key.hex()}")
    print(f"HMAC keys match: {alice_hmac_key == bob_hmac_key}")
    
    return alice_shared


def example_point_operations():
    """Demonstrate elliptic curve point operations."""
    print("\n" + "=" * 60)
    print("POINT OPERATIONS EXAMPLE")
    print("=" * 60)
    
    curve = secp256k1
    G = curve.G
    
    print(f"Generator point G: {G}")
    print(f"Curve order n: {curve.n}")
    
    # Point doubling and addition
    print("\n" + "-" * 40)
    print("Point arithmetic...")
    
    point_2G = G + G
    point_2G_scalar = 2 * G
    print(f"G + G = {point_2G}")
    print(f"2 * G = {point_2G_scalar}")
    print(f"Results equal: {point_2G == point_2G_scalar}")
    
    point_3G = point_2G + G
    point_3G_scalar = 3 * G
    print(f"2G + G = {point_3G}")
    print(f"3 * G = {point_3G_scalar}")
    print(f"Results equal: {point_3G == point_3G_scalar}")
    
    # Point negation
    print("\n" + "-" * 40)
    print("Point negation...")
    
    neg_G = -G
    print(f"-G = {neg_G}")
    
    # Adding a point to its negation should give point at infinity
    infinity = G + neg_G
    print(f"G + (-G) = {infinity}")
    print(f"Is point at infinity: {infinity.is_infinity}")
    
    # Scalar multiplication with curve order should give infinity
    print("\n" + "-" * 40)
    print("Order verification...")
    
    n_times_G = curve.n * G
    print(f"n * G = {n_times_G}")
    print(f"Is point at infinity: {n_times_G.is_infinity}")
    
    # Point compression and decompression
    print("\n" + "-" * 40)
    print("Point compression...")
    
    compressed_G = G.compress()
    print(f"Compressed G: {compressed_G.hex()}")
    
    decompressed_G = EllipticCurvePoint.decompress(compressed_G, curve)
    print(f"Decompressed G: {decompressed_G}")
    print(f"Decompression successful: {G == decompressed_G}")


def example_security_features():
    """Demonstrate security features and edge cases."""
    print("\n" + "=" * 60)
    print("SECURITY FEATURES EXAMPLE")
    print("=" * 60)
    
    # Secure random number generation
    print("Secure random number generation...")
    random_bytes = SecureRandom.random_bytes(32)
    print(f"Random bytes: {random_bytes.hex()}")
    
    random_scalar = SecureRandom.random_scalar(secp256k1)
    print(f"Random scalar: {random_scalar:064x}")
    
    # Signature format validation
    print("\n" + "-" * 40)
    print("Signature validation...")
    
    valid_signature = (12345, 67890)
    invalid_signature_r_zero = (0, 67890)
    invalid_signature_s_too_large = (12345, secp256k1.n)  # s >= n
    
    print(f"Valid signature format: {ECCUtils.validate_signature_format(valid_signature)}")
    print(f"Invalid signature (r=0): {ECCUtils.validate_signature_format(invalid_signature_r_zero)}")
    print(f"Invalid signature (s>=n): {ECCUtils.validate_signature_format(invalid_signature_s_too_large)}")
    
    # Hash to curve point
    print("\n" + "-" * 40)
    print("Hash to curve point...")
    
    data1 = b"hash this data to a point"
    data2 = b"hash different data"
    
    point1 = ECCUtils.hash_to_curve_point(data1)
    point2 = ECCUtils.hash_to_curve_point(data2)
    point1_again = ECCUtils.hash_to_curve_point(data1)
    
    print(f"Point from data1: {point1}")
    print(f"Point from data2: {point2}")
    print(f"Same data gives same point: {point1 == point1_again}")
    print(f"Different data gives different points: {point1 != point2}")


def example_complete_workflow():
    """Demonstrate a complete cryptographic workflow."""
    print("\n" + "=" * 60)
    print("COMPLETE WORKFLOW EXAMPLE")
    print("=" * 60)
    
    print("Scenario: Secure message exchange between Alice and Bob")
    print("-" * 60)
    
    # Step 1: Key generation
    print("Step 1: Generate key pairs...")
    alice_keypair = KeyPair.generate()
    bob_keypair = KeyPair.generate()
    
    alice_address = ECCUtils.point_to_address(alice_keypair.public_key)
    bob_address = ECCUtils.point_to_address(bob_keypair.public_key)
    
    print(f"Alice's address: {alice_address}")
    print(f"Bob's address: {bob_address}")
    
    # Step 2: Key exchange for secure communication
    print("\nStep 2: Perform key exchange...")
    ecdh = ECDH()
    
    shared_secret = ecdh.generate_shared_secret(
        alice_keypair.private_key,
        bob_keypair.public_key
    )
    
    # Derive symmetric keys
    aes_key = ecdh.derive_key(shared_secret, b"AES-256", 32)
    hmac_key = ecdh.derive_key(shared_secret, b"HMAC-SHA256", 32)
    
    print(f"Shared secret established: {shared_secret[:8].hex()}...")
    print(f"AES key derived: {aes_key[:8].hex()}...")
    print(f"HMAC key derived: {hmac_key[:8].hex()}...")
    
    # Step 3: Alice signs a message
    print("\nStep 3: Alice signs a message...")
    message = b"Transfer 100 BTC from Alice to Bob"
    
    ecdsa = ECDSA()
    signature = ecdsa.sign(message, alice_keypair.private_key)
    
    print(f"Message: {message.decode('utf-8')}")
    print(f"Signature: {signature[0]:016x}...{signature[1]:016x}")
    
    # Step 4: Bob verifies Alice's signature
    print("\nStep 4: Bob verifies the signature...")
    is_valid = ecdsa.verify(message, signature, alice_keypair.public_key)
    
    print(f"Signature verification: {'VALID ✅' if is_valid else 'INVALID ❌'}")
    
    # Step 5: Create transaction record
    print("\nStep 5: Create transaction record...")
    
    transaction = {
        'from_address': alice_address,
        'to_address': bob_address,
        'amount': '100 BTC',
        'message': message.decode('utf-8'),
        'signature': {
            'r': f"{signature[0]:064x}",
            's': f"{signature[1]:064x}",
            'der': ECCUtils.signature_to_der(signature).hex()
        },
        'public_key': alice_keypair.public_key.compress().hex()
    }
    
    print("Transaction record created:")
    for key, value in transaction.items():
        if key == 'signature':
            print(f"  {key}:")
            for sig_key, sig_value in value.items():
                display_value = sig_value[:32] + "..." if len(sig_value) > 32 else sig_value
                print(f"    {sig_key}: {display_value}")
        else:
            display_value = value[:32] + "..." if len(str(value)) > 32 else value
            print(f"  {key}: {display_value}")
    
    return transaction


def run_all_examples():
    """Run all examples."""
    print("🔐 EllipticWeb - Comprehensive ECC Examples")
    print("=" * 80)
    
    try:
        # Run individual examples
        keypair = example_key_generation()
        alice_keypair, signature = example_digital_signatures()
        shared_secret = example_key_exchange()
        example_point_operations()
        example_security_features()
        transaction = example_complete_workflow()
        
        print("\n" + "=" * 80)
        print("✅ ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR IN EXAMPLES: {e}")
        print("=" * 80)
        return False


if __name__ == "__main__":
    success = run_all_examples()
    exit(0 if success else 1)