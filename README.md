# 🔐 EllipticWeb - Comprehensive Elliptic Curve Cryptography

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](#testing)

A complete, production-ready implementation of **Elliptic Curve Cryptography (ECC)** with **256-bit security**, featuring the **secp256k1** curve used by Bitcoin and other major cryptocurrencies.

## 🌟 Features

### 🔢 Mathematical Foundation
- **Complete modular arithmetic** operations (addition, multiplication, inversion)
- **Finite field arithmetic** for prime fields  
- **Elliptic curve point operations** (addition, doubling, scalar multiplication)
- **Optimized algorithms** including fast modular exponentiation and square root

### 🔐 Cryptographic Operations
- **ECDSA** (Elliptic Curve Digital Signature Algorithm) with deterministic signing
- **ECDH** (Elliptic Curve Diffie-Hellman) key exchange
- **Secure key generation** with cryptographically secure random numbers
- **Key derivation functions** for generating symmetric keys

### 🛡️ Security Features
- **secp256k1 curve parameters** (same as Bitcoin)
- **Point compression/decompression** for efficient storage
- **Input validation** and comprehensive error handling
- **Constant-time operations** where applicable
- **Address generation** (Bitcoin-style)

### 🌐 Web Interface
- **Modern web UI** for interactive ECC operations
- **REST API** for programmatic access
- **Real-time demonstrations** of all cryptographic functions
- **Mobile-responsive design**

### 🧪 Quality Assurance
- **Comprehensive test suite** with 100+ test cases
- **Integration tests** for real-world scenarios
- **Performance benchmarks**
- **Security validation**

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/TR01b17B0y5/EllipticWeb.git
cd EllipticWeb
```

### Run Examples

```bash
python main.py examples
```

### Start Web Interface

```bash
python main.py web
```

Then open your browser to `http://localhost:8080`

### Run Tests

```bash
python main.py test
```

## 📋 Usage Examples

### Key Generation

```python
from elliptic_core import secp256k1
from cryptographic_operations import KeyPair

# Generate a new key pair
keypair = KeyPair.generate()
print(f"Private Key: {keypair.private_key:064x}")
print(f"Public Key: {keypair.public_key.compress().hex()}")

# Generate address
from cryptographic_operations import ECCUtils
address = ECCUtils.point_to_address(keypair.public_key)
print(f"Address: {address}")
```

### Digital Signatures (ECDSA)

```python
from cryptographic_operations import ECDSA

# Sign a message
ecdsa = ECDSA()
message = b"Hello, ECC!"
signature = ecdsa.sign(message, keypair.private_key)

# Verify signature
is_valid = ecdsa.verify(message, signature, keypair.public_key)
print(f"Signature valid: {is_valid}")
```

### Key Exchange (ECDH)

```python
from cryptographic_operations import ECDH

# Generate key pairs for Alice and Bob
alice_keypair = KeyPair.generate()
bob_keypair = KeyPair.generate()

# Perform key exchange
ecdh = ECDH()
alice_shared = ecdh.generate_shared_secret(
    alice_keypair.private_key, 
    bob_keypair.public_key
)
bob_shared = ecdh.generate_shared_secret(
    bob_keypair.private_key, 
    alice_keypair.public_key
)

# Shared secrets match!
assert alice_shared == bob_shared

# Derive encryption keys
aes_key = ecdh.derive_key(alice_shared, b"AES-256", 32)
```

### Point Operations

```python
from elliptic_core import secp256k1

G = secp256k1.G  # Generator point

# Point arithmetic
point_2G = G + G        # Point addition
point_3G = 3 * G        # Scalar multiplication
point_neg = -G          # Point negation

# Point compression
compressed = G.compress()
decompressed = EllipticCurvePoint.decompress(compressed, secp256k1)
```

## 🖥️ Command Line Interface

```bash
# Show implementation information
python main.py info

# Run comprehensive examples
python main.py examples

# Run all tests
python main.py test

# Start web interface
python main.py web

# Start web interface on custom port
python main.py web --port 9000

# Start interactive Python shell with ECC modules loaded
python main.py interactive
```

## 🌐 Web Interface

The web interface provides an intuitive way to interact with all ECC functionality:

- **🔑 Key Generation**: Generate secure key pairs
- **✍️ Digital Signatures**: Sign and verify messages
- **🤝 Key Exchange**: Perform ECDH key exchange
- **🏠 Address Generation**: Generate Bitcoin-style addresses
- **📊 Real-time Results**: See cryptographic operations in action

### API Endpoints

- `GET /api/generate_keys` - Generate new key pair
- `POST /api/sign` - Sign a message
- `POST /api/verify` - Verify a signature  
- `POST /api/ecdh` - Perform key exchange
- `POST /api/address` - Generate address from public key
- `GET /api/health` - Health check

## 🏗️ Architecture

### Core Modules

```
elliptic_core.py          # Mathematical foundation
├── ModularArithmetic     # Modular arithmetic operations
├── EllipticCurve        # Curve definition and validation
└── EllipticCurvePoint   # Point operations and arithmetic

cryptographic_operations.py  # High-level crypto operations
├── SecureRandom         # Cryptographically secure RNG
├── KeyPair             # Key generation and management
├── ECDSA               # Digital signature algorithm
├── ECDH                # Key exchange protocol
└── ECCUtils            # Utility functions

ecc_web_interface.py     # Web interface and REST API
test_ecc.py             # Comprehensive test suite
examples.py             # Usage examples and demos
main.py                 # Command-line interface
```

### Mathematical Foundation

The implementation uses the **secp256k1** elliptic curve:

```
y² = x³ + 7 (mod p)

Where:
p = FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
n = FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
```

## 🧪 Testing

The test suite includes:

- **Unit tests** for all mathematical operations
- **Cryptographic tests** for ECDSA and ECDH
- **Integration tests** for complete workflows
- **Edge case testing** for security validation
- **Performance benchmarks**

```bash
# Run all tests
python main.py test

# Run specific test class
python -m unittest test_ecc.TestECDSA

# Run with verbose output
python -m unittest test_ecc -v
```

## 🔒 Security Considerations

### ✅ Security Features
- Uses industry-standard **secp256k1** curve parameters
- **Cryptographically secure** random number generation
- **Input validation** for all operations
- **Deterministic signatures** (RFC 6979) available
- **Point validation** on curve operations
- **Constant-time operations** where possible

### ⚠️ Important Notes
- This is a **demonstration implementation** for educational purposes
- For **production use**, consider established libraries like `cryptography` or `ecdsa`
- **Never reuse nonces** in ECDSA signatures
- **Always validate** public keys and signatures
- **Use secure channels** for key exchange

## 🤝 Contributing

Contributions are welcome! Please ensure:

1. **Tests pass**: `python main.py test`
2. **Code quality**: Follow existing style conventions
3. **Documentation**: Update README and docstrings
4. **Security**: Consider security implications of changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Satoshi Nakamoto** for Bitcoin and popularizing secp256k1
- **NIST** for elliptic curve cryptography standards
- **RFC 6979** for deterministic ECDSA signatures
- **Bitcoin Core** developers for reference implementations

## 📚 Further Reading

- [SEC 2: Recommended Elliptic Curve Domain Parameters](https://www.secg.org/sec2-v2.pdf)
- [RFC 6979: Deterministic Usage of DSA and ECDSA](https://tools.ietf.org/html/rfc6979)
- [Guide to Elliptic Curve Cryptography](https://link.springer.com/book/10.1007/b97644)
- [Bitcoin Developer Guide](https://bitcoin.org/en/developer-guide)

---

**🔐 Built with security, performance, and education in mind.**
